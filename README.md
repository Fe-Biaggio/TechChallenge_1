# Tech Challenge Fase 1 — NPS Preditivo

**Pós-Tech FIAP | 1IAST | Fase 1**

## Objetivo do Projeto

Transformar dados operacionais de um e-commerce em insights acionáveis sobre a satisfação dos clientes, medida pelo Net Promoter Score (NPS). O projeto busca dar visibilidade dos problemas encontrados no quesito dados e negócio, além de buscar responder com aquilo que foi fornecido: **quais fatores operacionais realmente influenciam o NPS e como a empresa pode agir de forma proativa antes da aplicação da pesquisa?**

---

## Estrutura do Repositório

```
TechChallenge_1/
├── data/                               # Pasta de dados (referência)
├── notebooks/
│   ├── 01_entendimento_negocio.ipynb       # Análise conceitual e definição da target
│   ├── 02_eda_analise_exploratoria.ipynb   # Análise exploratória dos dados
│   └── 03_modelo_preditivo.ipynb           # Pipeline de modelo preditivo (opcional)
├── models/                             # Modelos treinados salvos
├── reports/
│   └── figures/                        # Visualizações geradas pelos notebooks
├── desafio_nps_fase_1.csv              # Base de dados original
├── requirements.txt                    # Dependências Python
└── README.md
```

---

## Descrição da Base de Dados

**Arquivo:** `desafio_nps_fase_1.csv`
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

1. **Entendimento do Negócio** (`01_entendimento_negocio.ipynb`)
   - Análise conceitual do problema
   - Reflexão sobre impacto do NPS no negócio
   - Definição e justificativa da variável alvo

2. **Análise Exploratória dos Dados — EDA** (`02_eda_analise_exploratoria.ipynb`)
   - Visão geral e qualidade dos dados
   - Distribuição do NPS e classificação em Promotores / Neutros / Detratores
   - Análise de fatores logísticos, de atendimento e perfil do cliente
   - Identificação de pontos críticos e insights de negócio

3. **Modelo Preditivo** (`03_modelo_preditivo.ipynb`) — *Desafio opcional*
   - Classificação binária: Promotor vs Não-Promotor
   - Pipeline completo: feature engineering, split, treino, avaliação
   - Modelos: Regressão Logística (baseline) e Random Forest
   - Feature importance e interpretação de negócio

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
1. `notebooks/01_entendimento_negocio.ipynb`
2. `notebooks/02_eda_analise_exploratoria.ipynb`
3. `notebooks/03_modelo_preditivo.ipynb`

### 3. Dados

O arquivo `desafio_nps_fase_1.csv` está na raiz do repositório. Os notebooks o referenciam como `'../desafio_nps_fase_1.csv'` — nenhuma configuração adicional é necessária.

---

## Principais Insights

- **Atraso na entrega** é o fator que mais derruba o NPS — clientes com 5+ dias de atraso têm NPS médio próximo de zero
- **Contatos com atendimento** deterioram a satisfação — cada contato adicional reduz a nota média significativamente
- **Reclamações** têm impacto direto e proporcional na nota NPS
- **Clientes com mais tempo de relacionamento** tendem a ser mais tolerantes, porém com expectativas maiores
- **Região Nordeste** apresenta menores NPS médios, sinalizando possíveis gargalos logísticos regionais

---

## Tecnologias Utilizadas

- Python 3.10+
- pandas, numpy
- matplotlib, seaborn
- scikit-learn
- joblib
