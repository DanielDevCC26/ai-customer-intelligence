
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def interpretar_loja(analise):
    """Solicita ao Gemini uma interpretação dos dados de uma loja."""

    cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Você é um analista de operações de uma plataforma de delivery.

    Analise os dados abaixo:
    {analise}

    Explique por que essa loja merece atenção e sugira
    uma próxima ação para o gestor.

    Regras:
    - Utilize somente os dados fornecidos.
    - Não invente causas para os cancelamentos.
    - Diferencie fatos de hipóteses.
    - Seja objetivo e use português brasileiro.
    """

    resposta = cliente.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return resposta.text
