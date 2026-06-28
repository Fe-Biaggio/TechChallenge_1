# Tech Challenge Fase 1 — NPS Preditivo

**Pós-Tech FIAP | 1IAST | Fase 1**

## Apresentação em Vídeo

Os vídeos abaixo estão disponíveis na pasta `reports/presentation/` e devem ser assistidos nessa ordem:

| # | Arquivo | Descrição |
|---|---------|-----------|
| 1 | [00_NPS_Pontos_de_Atencao.mp4](reports/presentation/00_NPS_Pontos_de_Atencao.mp4) | Pontos de atenção que impactam os números e dados apresentados — Se possível, assista antes da apresentação principal |
| 2 | [01_NPS_Apresentacao.mp4](reports/presentation/01_NPS_Apresentacao.mp4) | Apresentação do projeto para gestão e stakeholders - Limite 5 minutos |

---

## Objetivo do Projeto

Transformar dados operacionais de um e-commerce em insights acionáveis sobre a satisfação dos clientes, medida pelo Net Promoter Score (NPS). O projeto busca dar visibilidade dos problemas encontrados no quesito dados e negócio, além de buscar responder com aquilo que foi fornecido: **quais fatores operacionais realmente influenciam o NPS e como a empresa pode agir de forma proativa antes da aplicação da pesquisa?**

---

## Estrutura do Repositório

```
TechChallenge_1/
├── data/
│   ├── desafio_nps_fase_1.csv              # Base de dados original
│   ├── simulacao_predicao.csv              # 500 pedidos sintéticos sem NPS (entrada do notebook 04)
│   └── simulacao_predicao.xlsx             # Resultado da predição: registros + prob_promotor + classificação
├── notebooks/
│   ├── 01_entendimento_negocio.ipynb       # Análise conceitual e definição da target
│   ├── 02_eda_analise_exploratoria.ipynb   # Análise exploratória dos dados
│   ├── 03_modelo_preditivo.ipynb           # Pipeline de modelo preditivo
│   └── 04_simulacao_predicao.py            # Simulação de predição em lote com novos pedidos
├── models/                                 # Artefatos do modelo treinado (pkl)
├── reports/
│   └── figures/                            # Visualizações geradas pelos notebooks
├── requirements.txt                        # Dependências Python
└── README.md
```

---

## Descrição da Base de Dados

**Arquivo:** [`data/desafio_nps_fase_1.csv`](data/desafio_nps_fase_1.csv)
**Registros:** 2.500 pedidos
**Fonte:** Dados históricos de pedidos, entregas e atendimento de e-commerce nacional, sem visibilidade se a amostra atinge o tamanho mínimo necessário para nível de confiança e cálculo da margem de erro.

| Coluna | Descrição |
|--------|-----------|
| `customer_id` | Identificador único do cliente |
| `order_id` | Identificador único do pedido |
| `customer_age` | Idade do cliente |
| `customer_region` | Região geográfica (Norte, Nordeste, Sudeste, Sul, Centro-Oeste) |
| `customer_tenure_months` | Tempo de relacionamento com a empresa (meses) |
| `order_value` | Valor total do pedido (R$) |
| `items_quantity` | Quantidade de itens no pedido |
| `discount_value` | Valor de desconto aplicado (R$) |
| `payment_installments` | Número de parcelas do pagamento |
| `delivery_time_days` | Tempo total de entrega (dias) |
| `delivery_delay_days` | Dias de atraso na entrega |
| `freight_value` | Valor do frete (R$) |
| `delivery_attempts` | Número de tentativas de entrega |
| `customer_service_contacts` | Quantidade de contatos com o atendimento ao cliente |
| `resolution_time_days` | Tempo para resolução de problemas (dias) |
| `complaints_count` | Número de reclamações registradas |
| `repeat_purchase_30d` | Recompra em 30 dias (0=não, 1=sim) |
| `csat_internal_score` | Score interno de satisfação |
| **`nps_score`** | **Variável alvo — Nota NPS (0 a 10)** |

---

## Metodologia

O projeto segue a estrutura CRISP-DM adaptada:

1. **Entendimento do Negócio** ([`01_entendimento_negocio.ipynb`](notebooks/01_entendimento_negocio.ipynb))
   - Pontos de atenção para todo o projeto
   - Análise conceitual do problema
   - Reflexão sobre impacto do NPS no negócio
   - Definição e justificativa da variável alvo

2. **Análise Exploratória dos Dados — EDA** ([`02_eda_analise_exploratoria.ipynb`](notebooks/02_eda_analise_exploratoria.ipynb))
   - Visão geral e qualidade dos dados
   - Distribuição do NPS e classificação em Promotores / Neutros / Detratores
   - Análise de fatores logísticos, de atendimento e perfil do cliente
   - Identificação de pontos críticos e insights de negócio

3. **Modelo Preditivo** ([`03_modelo_preditivo.ipynb`](notebooks/03_modelo_preditivo.ipynb)) — *Desafio opcional*
   - Classificação binária: Promotor vs Não-Promotor
   - Pipeline completo: feature engineering, split, treino, avaliação
   - Modelos: Regressão Logística (baseline) e Random Forest (18 features, todas as 5 regiões)
   - Feature importance e interpretação de negócio
   - Seção de uso em produção com função `prever_nps` e 3 cenários de exemplo

4. **Simulação de Predição em Lote** ([`04_simulacao_predicao.py`](notebooks/04_simulacao_predicao.py))
   - Aplica o modelo treinado sobre 500 novos pedidos ([`simulacao_predicao.csv`](data/simulacao_predicao.csv))
   - Gera [`simulacao_predicao.xlsx`](data/simulacao_predicao.xlsx) com colunas `prob_promotor`, `classificacao` e `risco_detrator`
   - Produz dois gráficos: distribuição de pedidos por faixa de probabilidade e pizza Promotor vs Não-Promotor

---

## Como Reproduzir os Resultados

### 1. Pré-requisitos

```bash
pip install -r requirements.txt
```

### 2. Executar os Notebooks (ordem recomendada)

```bash
jupyter lab
```

Execute os notebooks na ordem:
1. [`notebooks/01_entendimento_negocio.ipynb`](notebooks/01_entendimento_negocio.ipynb)
2. [`notebooks/02_eda_analise_exploratoria.ipynb`](notebooks/02_eda_analise_exploratoria.ipynb)
3. [`notebooks/03_modelo_preditivo.ipynb`](notebooks/03_modelo_preditivo.ipynb)
4. [`notebooks/04_simulacao_predicao.py`](notebooks/04_simulacao_predicao.py) (requer que o notebook 03 tenha sido executado para gerar os artefatos em `models/`)

```bash
python notebooks/04_simulacao_predicao.py
```

### 3. Dados

O arquivo [`desafio_nps_fase_1.csv`](data/desafio_nps_fase_1.csv) está na pasta `data/`. Os notebooks o referenciam como `'../data/desafio_nps_fase_1.csv'` — nenhuma configuração adicional é necessária.

O arquivo [`simulacao_predicao.csv`](data/simulacao_predicao.csv) contém 500 pedidos sintéticos sem NPS, gerado para demonstrar a predição em lote com o modelo treinado.

---

## Principais Insights

- **Atraso na entrega** - é o fator que mais derruba o NPS, clientes com 5+ dias de atraso têm NPS médio próximo de zero
- **Contatos com atendimento** - deterioram a satisfação, cada contato adicional reduz a nota média significativamente
- **Reclamações** - têm impacto direto e proporcional na nota NPS
- **Clientes com mais tempo de relacionamento** - tendem a ser mais tolerantes, porém com expectativas maiores
- **Diferenças regionais no NPS são mínimas** - o problema é sistêmico e afeta todas as regiões igualmente

---

## Artefatos do Modelo (`models/`)

O notebook 03 gera três arquivos na pasta `models/` que são reutilizados nas predições:

| Arquivo | Descrição | Usado em |
|---------|-----------|----------|
| [`random_forest_nps.pkl`](models/random_forest_nps.pkl) | Modelo Random Forest treinado — recebe as 18 features e retorna a probabilidade de o cliente ser Promotor | nb03 seção 11, nb04 |
| [`feature_columns.pkl`](models/feature_columns.pkl) | Lista ordenada das 18 colunas de entrada — garante que novos dados sejam alinhados à mesma estrutura usada no treino, preenchendo dummies ausentes com `0` e reordenando as colunas | nb03 seção 11, nb04 |
| [`scaler_lr.pkl`](models/scaler_lr.pkl) | StandardScaler ajustado para a Regressão Logística (baseline) — necessário apenas se a LR for utilizada em produção, pois ela exige normalização das features | nb03 seção 10 (salvo como artefato complementar) |

O `feature_columns.pkl` é essencial para qualquer predição: sem ele, o modelo pode receber as colunas em ordem errada e gerar resultados incorretos.

---

## Tecnologias Utilizadas

- Python 3.10+
- pandas, numpy
- matplotlib, seaborn
- scikit-learn
- joblib
