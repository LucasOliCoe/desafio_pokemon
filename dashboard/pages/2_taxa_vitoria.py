import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.utils import load_table

st.set_page_config(layout="wide")

st.markdown("<h1 style='color: #f7d21e;'>🔥 TAXA DE VITÓRIA POR TIPO</h1>", unsafe_allow_html=True)
st.write("Análise de desempenho dos tipos de Pokémon nas batalhas.")

# ----------------------------------------------------------------------
# 1) Carregar a tabela correta: pokemon_battle_stats
# ----------------------------------------------------------------------
df = load_table("pokemon_battle_stats")

# Verificar colunas disponíveis (útil para debug)
# st.write("Colunas do DF:", df.columns)

# ----------------------------------------------------------------------
# 2) Garantir que a coluna primary_type existe
# ----------------------------------------------------------------------
if "primary_type" not in df.columns:
    st.error("❌ A coluna 'primary_type' não foi encontrada no dataframe carregado.")
    st.stop()

# ----------------------------------------------------------------------
# 3) Criar o ranking por win rate
# ----------------------------------------------------------------------
df_type = (
    df.groupby("primary_type")
      .agg(
          avg_win_rate=("win_rate", "mean"),
          total_battles=("battles", "sum"),
          total_wins=("wins", "sum")
      )
      .reset_index()
      .sort_values(by="avg_win_rate", ascending=False)
)

# ----------------------------------------------------------------------
# 4) Gráfico
# ----------------------------------------------------------------------
fig = px.bar(
    df_type,
    x="primary_type",
    y="avg_win_rate",
    color="primary_type",
    title="Ranking de Tipos por Taxa Média de Vitória",
    labels={"primary_type": "Tipo", "avg_win_rate": "Taxa Média de Vitória"},
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# 5) Mostrar tabela
# ----------------------------------------------------------------------
st.dataframe(df_type, use_container_width=True)
