# =============================================================================
# Tech Challenge Fase 1 | Case NPS Preditivo | Pós-Tech FIAP
# Notebook 04 — Simulação de Predição em Novos Pedidos
#
# Entrada : ../data/simulacao_predicao.csv  (500 pedidos sem NPS)
# Saídas  : ../data/simulacao_predicao.xlsx (registros + predição)
#            ../reports/figures/N04_01_distribuicao_probabilidade.png
#            ../reports/figures/N04_02_pizza_promotor_detrator.png
# =============================================================================

# ── 0. Imports e Configurações ────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

os.makedirs('../reports/figures', exist_ok=True)

plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['font.size'] = 12

print('Ambiente configurado.')

# ── 1. Carregar Artefatos do Modelo ──────────────────────────────────────────
modelo   = joblib.load('../models/random_forest_nps.pkl')
colunas  = joblib.load('../models/feature_columns.pkl')

print(f'Modelo carregado. Features esperadas: {len(colunas)}')

# ── 2. Carregar Dados de Simulação ───────────────────────────────────────────
df_sim = pd.read_csv('../data/simulacao_predicao.csv')

print(f'Registros carregados: {len(df_sim)}')
print(f'Colunas: {df_sim.columns.tolist()}')

# ── 3. Preparar Features (mesma pipeline do treino) ──────────────────────────
X_sim = df_sim.copy()

# One-Hot Encoding da região (sem drop_first — igual ao treino)
X_sim = pd.get_dummies(X_sim, columns=['customer_region'], dtype=int)

# Garantir que todas as colunas do modelo estejam presentes na ordem correta
for col in colunas:
    if col not in X_sim.columns:
        X_sim[col] = 0

X_sim = X_sim[colunas]

print(f'Features preparadas: {X_sim.shape[1]} colunas')

# ── 4. Executar Predição ──────────────────────────────────────────────────────
prob_promotor = modelo.predict_proba(X_sim)[:, 1]

df_resultado = df_sim.copy()
df_resultado['prob_promotor']  = prob_promotor.round(4)
df_resultado['classificacao']  = np.where(prob_promotor >= 0.5, 'PROMOTOR', 'NAO-PROMOTOR')
df_resultado['risco_detrator'] = pd.cut(
    prob_promotor,
    bins=[-0.001, 0.4, 0.7, 1.001],
    labels=['ALTO', 'MEDIO', 'BAIXO']
)

# Faixa de probabilidade para o gráfico de colunas (0-10%, 10-20%, ...)
df_resultado['faixa_prob'] = pd.cut(
    prob_promotor,
    bins=[i/10 for i in range(11)],
    labels=[f'{i*10}-{i*10+10}%' for i in range(10)],
    include_lowest=True
)

print('\n=== RESUMO DA PREDIÇÃO ===')
n_total     = len(df_resultado)
n_promotor  = (df_resultado['classificacao'] == 'PROMOTOR').sum()
n_detrator  = n_total - n_promotor
print(f'  Total de pedidos analisados : {n_total}')
print(f'  Classificados como PROMOTOR : {n_promotor} ({n_promotor/n_total:.1%})')
print(f'  Classificados como NAO-PROM.: {n_detrator} ({n_detrator/n_total:.1%})')
print(f'  Prob. média de ser promotor : {prob_promotor.mean():.2%}')
print()
print('Distribuição de risco:')
print(df_resultado['risco_detrator'].value_counts().to_string())

# ── 5. Salvar Excel ──────────────────────────────────────────────────────────
caminho_xlsx = '../data/simulacao_predicao.xlsx'
df_resultado.to_excel(caminho_xlsx, index=False)
print(f'\nArquivo salvo: {caminho_xlsx}')

# ── 6. Gráfico 1 — Distribuição por Faixa de Probabilidade (Colunas) ─────────
contagem_faixa = df_resultado['faixa_prob'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(13, 5))

cores_barra = [
    '#e74c3c' if i < 4 else ('#f39c12' if i < 7 else '#27ae60')
    for i in range(len(contagem_faixa))
]

bars = ax.bar(contagem_faixa.index, contagem_faixa.values,
              color=cores_barra, edgecolor='white', linewidth=1.5, width=0.7)

for bar, val in zip(bars, contagem_faixa.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            str(val), ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_title('Distribuição de Pedidos por Faixa de Probabilidade de Ser Promotor',
             fontweight='bold', fontsize=14)
ax.set_xlabel('Faixa de Probabilidade')
ax.set_ylabel('Quantidade de Pedidos')
ax.set_ylim(0, contagem_faixa.max() * 1.18)

# Legenda de cores
from matplotlib.patches import Patch
legenda = [
    Patch(facecolor='#e74c3c', label='Risco ALTO (0–40%)'),
    Patch(facecolor='#f39c12', label='Risco MÉDIO (40–70%)'),
    Patch(facecolor='#27ae60', label='Risco BAIXO (70–100%)'),
]
ax.legend(handles=legenda, loc='upper right')

plt.tight_layout()
caminho_g1 = '../reports/figures/N04_01_distribuicao_probabilidade.png'
plt.savefig(caminho_g1, dpi=150, bbox_inches='tight')
plt.show()
print(f'Gráfico salvo: {caminho_g1}')

# ── 7. Gráfico 2 — Pizza: % Promotor vs % Não-Promotor ───────────────────────
fig, ax = plt.subplots(figsize=(8, 6))

labels  = ['NAO-PROMOTOR', 'PROMOTOR']
valores = [n_detrator, n_promotor]
cores   = ['#e74c3c', '#27ae60']
explode = [0.03, 0.03]

wedges, texts, autotexts = ax.pie(
    valores,
    labels=labels,
    autopct='%1.1f%%',
    colors=cores,
    explode=explode,
    startangle=90,
    pctdistance=0.78,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2.5}
)

for at in autotexts:
    at.set_fontsize(13)
    at.set_fontweight('bold')

ax.set_title(
    f'Simulação de Predição NPS — {n_total} Pedidos\n'
    f'Promotores: {n_promotor} | Não-Promotores: {n_detrator}',
    fontweight='bold', fontsize=13
)

plt.tight_layout()
caminho_g2 = '../reports/figures/N04_02_pizza_promotor_detrator.png'
plt.savefig(caminho_g2, dpi=150, bbox_inches='tight')
plt.show()
print(f'Gráfico salvo: {caminho_g2}')

print('\nConcluído. Todos os artefatos foram gerados.')
