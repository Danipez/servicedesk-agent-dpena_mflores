import json
from langchain_core.messages import HumanMessage, ToolMessage
from agent.gemini import GeminiChatModel

class Respuesta:
    def __init__(self,data):
        self.data=json.dumps(data).encode()
    def __enter__(self):
        return self
    def __exit__(self,*args):
        pass
    def read(self):
        return self.data

def test_conserva_firma_y_respuesta_de_herramienta(monkeypatch):
    from agent import gemini
    recibidos=[]
    def responder(req,timeout):
        recibidos.append(json.loads(req.data))
        parts=([{'functionCall':{'name':'consultar_ticket','args':{'ticket_id':'INC-022'}},
                 'thoughtSignature':'firma-prueba'}] if len(recibidos)==1 else [{'text':'Requiere aprobación'}])
        return Respuesta({'candidates':[{'content':{'parts':parts}}]})
    monkeypatch.setattr(gemini.urllib.request,'urlopen',responder)
    llm=GeminiChatModel(model='modelo-prueba',api_key='secreto-de-prueba')
    primera=llm.invoke([HumanMessage(content='Consulta INC-022')])
    llamada=primera.tool_calls[0]
    segunda=llm.invoke([HumanMessage(content='Consulta INC-022'),primera,
        ToolMessage(content='{"costo":250000}',tool_call_id=llamada['id'])])
    assert recibidos[1]['contents'][1]['parts'][0]['thoughtSignature']=='firma-prueba'
    respuesta=recibidos[1]['contents'][2]['parts'][0]['functionResponse']
    assert respuesta['name']=='consultar_ticket' and respuesta['response']['result']['costo']==250000
    assert segunda.content=='Requiere aprobación'
    assert 'secreto-de-prueba' not in repr(llm)

def test_sin_candidatos_informa_error(monkeypatch):
    import pytest
    from agent import gemini
    monkeypatch.setattr(gemini.urllib.request,'urlopen',lambda *args,**kw:Respuesta({}))
    with pytest.raises(RuntimeError,match='respuesta utilizable'):
        GeminiChatModel(model='prueba',api_key='secreto').invoke('Hola')
