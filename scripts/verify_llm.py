"""Verifica una respuesta real sin imprimir credenciales."""
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GOOGLE_API_KEY, LLM_MODEL

def verificar():
    if not GOOGLE_API_KEY:
        raise SystemExit('Configura GOOGLE_API_KEY en .env')
    try:
        llm=ChatGoogleGenerativeAI(model=LLM_MODEL,google_api_key=GOOGLE_API_KEY,
            temperature=0,timeout=30,max_retries=0,transport='rest')
        print(llm.invoke('Responde solo: Hola desde Gemini').content)
    except Exception as error:
        print(f'Gemini no disponible ({type(error).__name__}). Revisa conexión, clave, modelo y cuota.')
        raise SystemExit(1)

if __name__=='__main__':
    verificar()
