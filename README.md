
# AI Customer Intelligence

Plataforma de inteligência operacional para restaurantes e serviços de delivery, desenvolvida com Python, SQL, Streamlit e inteligência artificial generativa.

O projeto transforma dados de pedidos em indicadores, visualizações e recomendações para apoiar a tomada de decisões operacionais.

## Objetivo

Desenvolver uma aplicação capaz de analisar o desempenho de restaurantes, identificar padrões de cancelamento, comparar indicadores operacionais e oferecer análises contextualizadas com apoio de inteligência artificial.

## Base de dados

O projeto utiliza o conjunto de dados público **Brazilian Delivery Center**, disponível no Kaggle.

**Fonte:** https://www.kaggle.com/datasets/nosbielcs/brazilian-delivery-center

A base original contém sete tabelas relacionadas a pedidos, pagamentos, entregas, estabelecimentos, canais de venda, entregadores e centros operacionais.

Os arquivos originais são mantidos localmente e não são incluídos no repositório.

### Indicadores da base processada

| Indicador | Resultado |
|---|---:|
| Restaurantes analisados | 951 |
| Pedidos registrados | 368.999 |
| Pedidos cancelados | 16.979 |
| Taxa geral de cancelamento | 4,60% |

## Tecnologias utilizadas

- **Python:** processamento de dados e lógica de análise.
- **SQL e SQLite:** armazenamento e consultas dos indicadores.
- **Pandas:** exploração e tratamento dos dados.
- **Streamlit:** desenvolvimento do dashboard interativo.
- **Altair:** visualizações e gráficos comparativos.
- **Google Gemini API:** geração de análises operacionais em linguagem natural.
- **pytest:** testes automatizados.
- **Git e GitHub:** versionamento do projeto.

## Funcionalidades implementadas

### Dashboard operacional

- Visão geral dos indicadores da plataforma.
- Ranking de restaurantes com maior volume de cancelamentos entre os elegíveis.
- Gráficos de cancelamentos.
- Pesquisa de restaurantes por nome ou ID.
- Visualização individual de indicadores operacionais.
- Comparação da taxa de cancelamento com a média da plataforma.
- Alertas exploratórios para tempos medianos elevados.

### Classificação operacional

Os restaurantes são classificados por critérios transparentes:

| Classificação | Critério |
|---|---|
| Amostra limitada | Menos de 100 pedidos |
| Atenção | Pelo menos 100 pedidos e cancelamento acima da média |
| Dentro da referência | Pelo menos 100 pedidos e cancelamento igual ou inferior à média |

Essas classificações são exploratórias e não representam diagnósticos definitivos.

### Inteligência artificial

A aplicação permite solicitar análises operacionais utilizando o modelo Gemini.

As instruções de análise orientam o modelo a:

- Considerar o volume de pedidos e cancelamentos.
- Comparar os indicadores com a referência geral.
- Diferenciar fatos observados de hipóteses.
- Reconhecer dados indisponíveis.
- Evitar atribuir causas sem evidências.
- Sugerir ações proporcionais aos indicadores apresentados.

A geração de relatórios ocorre sob demanda.

## Testes automatizados

O projeto possui 11 testes automatizados implementados, distribuídos entre:

- Classificação operacional e valores-limite.
- Consultas e integridade dos indicadores no SQLite.
- Geração simulada de relatórios de IA.
- Tratamento de restaurantes inexistentes.

Para executar os testes:

```bash
python -m pytest tests/ -v
```

Os testes de relatórios utilizam simulações para evitar chamadas reais à API.


## Instalação e execução

### Pré-requisitos

- Python 3.14
- Git
- Chave de API do Google Gemini
- Banco SQLite processado do projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/DanielDevCC26/ai-customer-intelligence.git
cd ai-customer-intelligence
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

No Windows, utilizando PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar a API do Gemini

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

**Importante:** nunca publique sua chave de API no GitHub.

### 5. Preparar o banco de dados

A aplicação utiliza o arquivo:

```text
data/processed/customer_intelligence.db
```

O banco processado precisa estar disponível nesse caminho para que o dashboard funcione.

### 6. Executar o dashboard

```bash
python -m streamlit run app.py
```

O Streamlit exibirá no terminal o endereço local para acessar a aplicação.

### 7. Executar os testes

```bash
python -m pytest tests/ -v
```

Os testes automatizados de relatórios de IA utilizam simulações e não consomem chamadas da API do Gemini.

**Observação:** o projeto ainda está em desenvolvimento. O processo de preparação do banco de dados será documentado para permitir a reprodução completa a partir dos arquivos públicos.


## Limitações

- A análise utiliza dados históricos de um conjunto público.
- Os indicadores de tempo podem apresentar valores extremos e inconsistências que exigem investigação.
- A classificação operacional utiliza critérios exploratórios.
- As recomendações da IA não substituem a avaliação de especialistas.
- A disponibilidade da geração de relatórios depende do serviço externo de IA.

## Status

**Em desenvolvimento — fase de validação e documentação.**

O dashboard, as consultas SQLite, a classificação operacional e a integração com inteligência artificial já foram implementados.

As próximas atividades incluem validação final, revisão da documentação e preparação da demonstração do projeto.
