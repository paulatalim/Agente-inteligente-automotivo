from PyPDF2 import PdfReader
import speech_recognition as sr
import os
from google import genai
from google.genai import types
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = "TAOS_25_MANUAL_INSTRUCOES.pdf"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#-------- Funções auxiliares -----------

# Carrega um arquivo
def upload_file (file_path):
    file = ""
    # Abrir o arquivo PDF em modo de leitura binária
    with open(file_path, "rb") as arquivo_pdf:
        # Crie um objeto leitor
        leitor_pdf = PdfReader(arquivo_pdf)

        # Obtenha o número de páginas
        num_paginas = len(leitor_pdf.pages)

        # Itere sobre cada página e extraia o texto
        for numero_pagina in range(num_paginas):
            if(numero_pagina < 9): continue
            pagina = leitor_pdf.pages[numero_pagina]
            texto = pagina.extract_text()
            file += texto

    fileText = file.replace('...', "").replace("  ", "")[1:300000]
    
    return fileText

# Converte voz em texto
def listen():
    # Inicializa o reconhecedor
    r = sr.Recognizer()

    # Usa o microfone como fonte de áudio
    with sr.Microphone() as source:
        print("🎙️ Fale algo...")
        r.adjust_for_ambient_noise(source)  # Ajusta para ruídos do ambiente
        audio = r.listen(source)

    try:
        print("🧠 Reconhecendo o que você disse...")
        texto = r.recognize_google(audio, language="pt-BR")
        speak(f"Você disse: {texto}")
        return texto

    except sr.UnknownValueError:
        speak("Não entendi o que você disse. Tente novamente")
        return listen()
    except sr.RequestError:
        speak("Erro ao se conectar com o serviço de reconhecimento de voz. Tentando se conectar novamente")
        return listen()

# Converte texto em voz
def speak(text):
    audio_path = os.path.join(os.getcwd(), "file_audio.mp3")
    print(text)
    try:
        tts = gTTS(text=text, lang="pt")
        tts.save(audio_path)
        playsound(audio_path)
        os.remove(audio_path)

    except Exception as e:
        print("⚠️ Erro:", e)

# Consulta a API do Gemini
def requestGemini(context, question):
    speak("Procurando resposta...")

    client = genai.Client(api_key=GOOGLE_API_KEY)

    mensage = "Responda a pergunta de forma resumida: " + question + "Com base no manual a seguir: " + context
    answer = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=mensage,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    return answer.text.replace('*', '')

# Verifica se ha intencao de interrupção do programa
def verifyAnswerTokens(answer):
    words = answer.split()
    for word in words:
        if "finalizar" in word.lower():
            speak("Adeus!")
            return True
        
    return False

#------------- Código principal --------------

while __name__ != "__main__": continue

print("Carregando manual...")
pdfContent = upload_file(FILE_PATH)

print("Inicializando microfone...")
recognizer = sr.Recognizer()
stop_program = False
os.system('cls')

speak("Olá! Eu sou sua assistente virtual automotiva. Me diga Finalizar para interromper a execução dessa conversa. Como posso ajudar?")

while not stop_program:
    answer = ""
    text = listen()

    stop_program = verifyAnswerTokens(text)
    
    if(stop_program): continue

    answer = requestGemini(text, pdfContent)
    speak(answer)
    speak("\nMe diga, no que posso ajudar?")