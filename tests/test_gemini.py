import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Carrega as variáveis do arquivo .env na raiz do projeto
raiz_projeto = Path(__file__).resolve().parent.parent
load_dotenv(raiz_projeto / ".env")

# Recupera a chave sem exibir seu conteúdo
chave_api = os.getenv("GEMINI_API_KEY")

if not chave_api:
    raise RuntimeError("Chave do Gemini não encontrada.")

# Configura o cliente do Gemini
cliente = genai.Client(api_key=chave_api)

# Envia uma mensagem simples para testar a conexão
resposta = cliente.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Responda apenas: Conexão funcionando!"
)

print(resposta.text)