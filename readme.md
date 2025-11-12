# Agente Inteligente

1ª avaliação da disciplica de Sistema Inteligentes de Hardware e Software

## Como executar

### 1. Instalando dependências

Execute o seguinte comando em seu terminl=al

```
pip install pypdf2 load_dotenv os playsound gTTS speech_recognition PyPDF2 google-genai
```
### 2. Configurando a API do Gemini

Crie um arquivo `.env` e adicione o seguinte código:

```
GOOGLE_API_KEY = "sua_key"
```
Substitua `sua_key` pela sua chave na API do google

### 3. Execute o código do arquivo `main.py`