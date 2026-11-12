
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def interpretar_loja(analise):
    """Solicita ao Gemini uma interpretação dos dados de uma loja."""

    chave_api = os.getenv("GEMINI_API_KEY")

    if not chave_api:
        raise ValueError("Chave GEMINI_API_KEY não encontrada no .env")

    cliente = genai.Client(api_key=chave_api)

    prompt = f"""
    Você é um analista de operações de uma plataforma de delivery.

    Dados da loja:
    {analise}

    Produza um relatório objetivo em português brasileiro
    com as seguintes seções:

    1. RESUMO OPERACIONAL
    Apresente os indicadores fornecidos e explique
    por que a loja foi priorizada.

    2. FATOS COMPROVADOS
    Utilize exclusivamente os números e informações recebidos.
    Não invente indicadores ou comparações.

    3. HIPÓTESES PARA INVESTIGAÇÃO
    Apresente possíveis linhas de investigação,
    deixando explícito que não são causas confirmadas.

    4. PRÓXIMA AÇÃO RECOMENDADA
    Sugira uma ação concreta para o gestor investigar
    os cancelamentos.

    Regras obrigatórias:
    - Não invente causas, resultados ou impactos financeiros.
    - Não afirme que houve falhas logísticas sem evidências.
    - Não atribua responsabilidades a clientes ou restaurantes.
    - Não apresente hipóteses como fatos.
    - Não altere os números fornecidos.
    - Seja claro, objetivo e profissional.
    """

    resposta = cliente.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return resposta.text
