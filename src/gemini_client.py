
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

    Analise exclusivamente os indicadores fornecidos abaixo.

    DADOS DO RESTAURANTE:
    {analise}

    REFERÊNCIA DA PLATAFORMA:
    Taxa geral de cancelamento: 4,60%.

    CRITÉRIOS DE ANÁLISE:

    - Compare a taxa de cancelamento da loja com a
      referência geral de 4,60%.

    - Considere também o volume absoluto de pedidos
      e cancelamentos.

    - Lojas com menos de 100 pedidos possuem uma
      amostra operacional limitada. Evite conclusões
      definitivas sobre seu desempenho.

    - Uma taxa elevada de cancelamento não significa
      automaticamente que a loja é prioritária.

    - Não classifique uma loja como prioritária
      sem considerar seu volume de pedidos.

    - Valores None representam dados indisponíveis,
      não valores iguais a zero.

    - Se houver indicadores de tempo de ciclo,
      utilize-os com cautela e não presuma suas causas.

    ESTRUTURA DO RELATÓRIO:

    1. RESUMO OPERACIONAL
    Apresente o desempenho da loja considerando
    a taxa de cancelamento e o volume de pedidos.

    2. FATOS COMPROVADOS
    Liste somente os indicadores disponíveis
    e as comparações matematicamente verificáveis.

    3. PONTOS DE ATENÇÃO
    Identifique indicadores que merecem investigação.
    Diferencie fatos de possíveis hipóteses.

    4. PRÓXIMA AÇÃO RECOMENDADA
    Sugira uma ação concreta e proporcional
    aos indicadores observados.

    REGRAS OBRIGATÓRIAS:

    - Não invente causas para os cancelamentos.
    - Não invente resultados ou impactos financeiros.
    - Não atribua responsabilidades sem evidências.
    - Não apresente hipóteses como fatos.
    - Não altere os números fornecidos.
    - Não invente períodos de análise.
    - Não presuma a existência de logs ou campos adicionais.
    - Não classifique automaticamente todas as lojas
      como críticas.
    - Seja objetivo, profissional e use português brasileiro.
    """

    resposta = cliente.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return resposta.text
