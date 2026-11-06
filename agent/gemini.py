"""Adaptador LangChain para Gemini con preservación de firmas de herramientas."""
import json
import urllib.error
import urllib.request
from typing import Any
from pydantic import SecretStr
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool

class GeminiChatModel(BaseChatModel):
    model: str
    api_key: SecretStr
    temperature: float = 0.2
    timeout: float = 45

    @property
    def _llm_type(self):
        return 'gemini-rest-with-tool-signatures'

    def bind_tools(self, tools, **kwargs):
        declarations=[]
        for tool in tools:
            f=convert_to_openai_tool(tool)['function']
            declarations.append({'name':f['name'],'description':f.get('description',''),
                                 'parametersJsonSchema':f['parameters']})
        return self.bind(tools=[{'functionDeclarations':declarations}],**kwargs)

    def _generate(self,messages,stop=None,run_manager=None,**kwargs: Any):
        system=[]
        contents=[]
        names={}
        for message in messages:
            if isinstance(message,SystemMessage):
                system.append({'text':str(message.content)})
                continue
            if isinstance(message,AIMessage):
                for call in message.tool_calls:
                    names[call['id']]=call['name']
                parts=message.additional_kwargs.get('gemini_parts')
                if parts is None:
                    parts=[{'text':str(message.content)}] if message.content else []
                    parts += [{'functionCall':{'name':t['name'],'args':t['args']}} for t in message.tool_calls]
                if parts:
                    contents.append({'role':'model','parts':parts})
            elif isinstance(message,ToolMessage):
                try:
                    value=json.loads(message.content)
                except (ValueError,TypeError):
                    value=message.content
                name=message.name or names.get(message.tool_call_id)
                if not name:
                    raise ValueError('Respuesta de herramienta sin nombre asociado')
                contents.append({'role':'user','parts':[{'functionResponse':{'name':name,'response':{'result':value}}}]})
            else:
                contents.append({'role':'user','parts':[{'text':str(message.content)}]})
        body={'contents':contents,'generationConfig':{'temperature':self.temperature}}
        if system:
            body['systemInstruction']={'parts':system}
        if kwargs.get('tools'):
            body['tools']=kwargs['tools']
        if stop:
            body['generationConfig']['stopSequences']=stop
        request=urllib.request.Request(
            f'https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent',
            data=json.dumps(body).encode('utf-8'),
            headers={'Content-Type':'application/json','x-goog-api-key':self.api_key.get_secret_value()})
        try:
            with urllib.request.urlopen(request,timeout=self.timeout) as response:
                result=json.load(response)
        except urllib.error.HTTPError as error:
            raise RuntimeError(f'Gemini respondió HTTP {error.code}; revisa modelo, cuota y permisos.') from None
        candidates=result.get('candidates',[])
        if not candidates:
            raise RuntimeError('Gemini no devolvió una respuesta utilizable')
        parts=candidates[0].get('content',{}).get('parts',[])
        calls=[]
        for i,part in enumerate(parts):
            if 'functionCall' in part:
                f=part['functionCall']
                calls.append({'name':f['name'],'args':f.get('args',{}),'id':f.get('id',f'call_{len(messages)}_{i}')})
        text='\n'.join(p['text'] for p in parts if 'text' in p and not p.get('thought'))
        message=AIMessage(content=text,tool_calls=calls,additional_kwargs={'gemini_parts':parts})
        return ChatResult(generations=[ChatGeneration(message=message)])
