
# AI Customer Intelligence

Plataforma de inteligência operacional para restaurantes e serviços de delivery, desenvolvida com Python, SQL, Streamlit e Inteligência Artificial Generativa.

O projeto transforma dados históricos de pedidos em indicadores operacionais, visualizações interativas e análises contextualizadas para apoiar a tomada de decisões.

## Sobre o projeto

O AI Customer Intelligence foi desenvolvido como projeto de portfólio, com foco na aplicação prática de análise de dados, bancos de dados relacionais, desenvolvimento Python e integração com modelos de linguagem.

A proposta é demonstrar como dados operacionais de uma plataforma de delivery podem ser utilizados para identificar restaurantes que merecem atenção, comparar indicadores e apoiar investigações de problemas operacionais.

A aplicação combina:

- Processamento e análise de dados com Python e Pandas.
- Consultas SQL em banco SQLite.
- Dashboard interativo desenvolvido com Streamlit.
- Visualizações de dados com Altair.
- Classificação operacional baseada em critérios definidos.
- Integração com Google Gemini para geração de relatórios.
- Testes automatizados com pytest.

## Objetivos

- Analisar o desempenho operacional de restaurantes.
- Identificar estabelecimentos com indicadores de cancelamento elevados.
- Comparar restaurantes com a referência geral da plataforma.
- Investigar indicadores de tempo de ciclo dos pedidos.
- Diferenciar estabelecimentos com volume relevante daqueles com amostras limitadas.
- Gerar relatórios operacionais com apoio de IA generativa.
- Demonstrar um fluxo reproduzível de processamento e análise de dados.

## Base de dados

O projeto utiliza o dataset público **Brazilian Delivery Center**, disponível no Kaggle.

**Fonte:** https://www.kaggle.com/datasets/nosbielcs/brazilian-delivery-center

O conjunto original contém sete tabelas relacionadas a pedidos, pagamentos, entregas, estabelecimentos, canais de venda, entregadores e centros operacionais.

A análise operacional implementada neste projeto utiliza principalmente os arquivos `orders.csv` e `stores.csv`.

Os dados originais e os bancos SQLite gerados são mantidos localmente e não são incluídos no repositório.

### Indicadores gerais

| Indicador | Resultado |
|---|---:|
| Restaurantes analisados | 951 |
| Pedidos registrados | 368.999 |
| Pedidos cancelados | 16.979 |
| Taxa geral de cancelamento | 4,60% |

A taxa geral de cancelamento é utilizada como referência para a classificação operacional dos restaurantes.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Processamento, consultas e lógica de negócio |
| Pandas | Exploração, tratamento e agregação de dados |
| SQL | Consultas aos indicadores operacionais |
| SQLite | Armazenamento dos dados consolidados |
| Streamlit | Interface e dashboard interativo |
| Altair | Gráficos e visualizações |
| Google Gemini API | Interpretação dos indicadores com IA |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| pytest | Testes automatizados |
| Git e GitHub | Versionamento e documentação |
| Jupyter Notebook | Exploração e validação dos dados |

## Funcionalidades

### 1. Dashboard operacional

O dashboard apresenta uma visão geral da plataforma, incluindo:

- Quantidade de restaurantes analisados.
- Volume total de pedidos.
- Quantidade de cancelamentos.
- Taxa geral de cancelamento.
- Ranking de restaurantes com maior volume de cancelamentos entre os elegíveis.
- Gráficos para comparação de indicadores.

### 2. Pesquisa de restaurantes

A aplicação permite pesquisar restaurantes por nome ou identificador.

Ao selecionar um estabelecimento, são apresentados:

- Total de pedidos.
- Pedidos cancelados.
- Taxa de cancelamento.
- Tempo mediano de ciclo, quando disponível.
- Comparação com a referência geral da plataforma.
- Classificação operacional.

### 3. Classificação operacional

Os restaurantes são classificados conforme critérios definidos na aplicação.

| Classificação | Critério |
|---|---|
| Amostra limitada | Menos de 100 pedidos |
| Atenção | Pelo menos 100 pedidos e taxa de cancelamento acima da referência |
| Dentro da referência | Pelo menos 100 pedidos e taxa igual ou inferior à referência |

A classificação considera tanto o percentual de cancelamentos quanto o volume de pedidos.

Um restaurante com poucos pedidos não é automaticamente considerado prioritário apenas por apresentar uma taxa elevada de cancelamento.

Esses critérios são exploratórios e não representam diagnósticos definitivos.

### 4. Comparação de indicadores

O dashboard apresenta gráficos comparativos entre a taxa de cancelamento do restaurante selecionado e a taxa geral da plataforma.

Também sinaliza tempos medianos de ciclo elevados para apoiar investigações operacionais.

Os indicadores de tempo são utilizados com cautela devido à presença de valores extremos e possíveis inconsistências na base original.

### 5. Relatórios com inteligência artificial

A aplicação integra o modelo `gemini-3.1-flash-lite`, por meio da API do Google Gemini.

O usuário pode solicitar um relatório operacional para o restaurante selecionado.

O modelo recebe os indicadores disponíveis e instruções para produzir uma análise estruturada.

O relatório contempla:

1. Resumo operacional.
2. Fatos comprovados pelos dados.
3. Pontos de atenção.
4. Próxima ação recomendada.

#### Regras de interpretação

A integração foi desenvolvida para orientar o modelo a:

- Utilizar exclusivamente os indicadores fornecidos.
- Comparar os resultados com a referência geral.
- Considerar o volume de pedidos.
- Reconhecer amostras operacionais limitadas.
- Não inventar causas de cancelamentos.
- Não atribuir responsabilidades sem evidências.
- Não apresentar hipóteses como fatos comprovados.
- Não inventar impactos financeiros.
- Reconhecer indicadores indisponíveis.

A geração dos relatórios ocorre sob demanda, mediante ação do usuário.

## Processamento dos dados

O processamento original foi desenvolvido em Jupyter Notebook e posteriormente organizado em um script Python para reconstrução dos indicadores.

### Etapas do processamento

1. Leitura dos arquivos originais de pedidos e restaurantes.
2. Relacionamento dos registros pelo identificador `store_id`.
3. Identificação dos pedidos com status `CANCELED`.
4. Agrupamento dos pedidos por restaurante.
5. Cálculo do volume de pedidos e cancelamentos.
6. Cálculo da taxa percentual de cancelamento.
7. Seleção dos pedidos com status `FINISHED`.
8. Cálculo do tempo mediano de ciclo por restaurante.
9. Consolidação dos indicadores operacionais.
10. Armazenamento dos resultados em SQLite.

### Tabela consolidada

A tabela `store_performance` contém os campos:

| Campo | Descrição |
|---|---|
| `store_id` | Identificador do restaurante |
| `store_name` | Nome do restaurante |
| `total_pedidos` | Quantidade de pedidos |
| `pedidos_cancelados` | Quantidade de cancelamentos |
| `taxa_cancelamento` | Percentual de cancelamentos |
| `tempo_mediano_ciclo` | Mediana do tempo de ciclo dos pedidos finalizados |
| `pedidos_com_tempo` | Quantidade de pedidos finalizados com indicador de tempo disponível |

## Instalação e execução

### Pré-requisitos

- Python 3.14
- Git
- Acesso ao dataset Brazilian Delivery Center
- Chave de API do Google Gemini para utilizar os relatórios de IA

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

A chave pode ser obtida por meio do Google AI Studio, conforme as condições de acesso ao serviço.

O arquivo `.env` deve permanecer fora do controle de versão.

**Nunca publique chaves de API no GitHub.**

### 5. Preparar os dados

Baixe o dataset original:

https://www.kaggle.com/datasets/nosbielcs/brazilian-delivery-center

Crie a estrutura de diretórios:

```text
data/
├── raw/
│   ├── orders.csv
│   └── stores.csv
└── processed/
```

Coloque os arquivos `orders.csv` e `stores.csv` na pasta `data/raw/`.

### 6. Reconstruir o banco SQLite

Na raiz do projeto, execute:

```bash
python scripts/rebuild_database.py
```

O script processa os arquivos originais e gera:

```text
data/processed/customer_intelligence_rebuild.db
```

A reconstrução foi validada com os seguintes resultados:

| Indicador | Resultado |
|---|---:|
| Restaurantes | 951 |
| Pedidos | 368.999 |
| Cancelamentos | 16.979 |

Os registros dos 951 restaurantes foram comparados com o banco original, incluindo seus indicadores operacionais.

**Resultado da comparação: indicadores idênticos.**

#### Segurança da reconstrução

O script não modifica o banco principal `customer_intelligence.db`.

Caso o arquivo `customer_intelligence_rebuild.db` já exista, a execução é interrompida para evitar sobrescrita acidental.

Para repetir o processamento, remova somente o banco reconstruído e execute novamente o script.

O processo foi testado após a remoção do banco temporário e reproduziu os mesmos totais.

#### Preparar o banco para o dashboard

O dashboard utiliza o arquivo:

```text
data/processed/customer_intelligence.db
```

Após reconstruir e validar o banco, em uma instalação nova, copie o arquivo gerado para o nome esperado pela aplicação.

No PowerShell:

```powershell
Copy-Item "data/processed/customer_intelligence_rebuild.db" "data/processed/customer_intelligence.db"
```

Esse comando deve ser utilizado em uma instalação nova, sem um banco principal preexistente.

Não substitua um banco existente sem realizar uma cópia de segurança.

### 7. Executar o dashboard

Na raiz do projeto, execute:

```bash
python -m streamlit run app.py
```

O Streamlit exibirá no terminal o endereço local para acessar a aplicação.

### 8. Executar os testes

```bash
python -m pytest tests/ -v
```

## Testes automatizados

O projeto possui 11 testes automatizados implementados e validados individualmente durante o desenvolvimento.

Os testes abrangem:

### Classificação operacional

- Restaurantes com amostra limitada.
- Restaurantes classificados como Atenção.
- Restaurantes dentro da referência.
- Limite mínimo de 100 pedidos.
- Taxa de cancelamento igual à referência.

### Integração com SQLite

- Retorno de restaurantes cadastrados.
- Quantidade esperada de 951 restaurantes.
- Presença dos campos operacionais.
- Integridade dos indicadores de pedidos e cancelamentos.

### Relatórios de IA

- Geração simulada de relatório para restaurante existente.
- Tratamento de restaurante inexistente.
- Verificação de chamadas simuladas ao módulo de interpretação.

Os testes de relatório utilizam `unittest.mock` para evitar chamadas reais ao Gemini.

A execução completa da suíte pode ser realizada com:

```bash
python -m pytest tests/ -v
```

## Estrutura do projeto

```text
ai-customer-intelligence/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_data_exploration.ipynb
├── scripts/
│   └── rebuild_database.py
├── sql/
│   └── store_analysis.sql
├── src/
│   ├── analysis.py
│   ├── database.py
│   ├── gemini_client.py
│   └── report.py
└── tests/
    ├── test_analysis.py
    ├── test_classificacao.py
    ├── test_consultas_sqlite.py
    ├── test_database.py
    ├── test_gemini.py
    ├── test_gemini_analysis.py
    └── test_relatorio_ia.py
```

Os arquivos de dados locais, bancos SQLite, ambientes virtuais e credenciais não são publicados no repositório.

## Limitações

- O projeto utiliza dados históricos de um conjunto público.
- Os indicadores operacionais não representam dados em tempo real.
- A análise atual concentra-se principalmente em pedidos, cancelamentos e tempos de ciclo.
- Os dados de tempo apresentam valores extremos e possíveis inconsistências.
- A classificação operacional utiliza critérios exploratórios.
- Não há informações suficientes para determinar automaticamente as causas dos cancelamentos.
- As análises geradas pela IA dependem dos indicadores fornecidos.
- A IA pode produzir interpretações incorretas e suas recomendações devem ser revisadas.
- A geração de relatórios depende da disponibilidade da API do Gemini.
- A utilização da API pode estar sujeita a limites e custos conforme as condições do serviço.

## Próximas melhorias

Possíveis evoluções do projeto incluem:

- Análise de tendências temporais.
- Indicadores adicionais de desempenho logístico.
- Comparação entre segmentos de restaurantes.
- Exportação de relatórios.
- Ampliação dos testes automatizados.
- Publicação de uma demonstração acessível pela internet.

## Status do projeto

**Funcionalidades principais implementadas.**

O projeto possui:

- Processamento de dados desenvolvido.
- Banco SQLite consolidado.
- Script de reconstrução validado.
- Dashboard interativo implementado.
- Classificação operacional automatizada.
- Integração com Google Gemini.
- Testes automatizados.
- Documentação de instalação e execução.

A validação final da aplicação e a preparação da demonstração fazem parte das últimas etapas do desenvolvimento.

## Autor

**Daniel Gonçalves Santana**

Estudante de Análise e Desenvolvimento de Sistemas, com foco em análise de dados, inteligência de negócios, Python e inteligência artificial.

**GitHub:** https://github.com/DanielDevCC26

**Portfólio:** https://DanielDevCC26.github.io
