import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.utils import load_table

st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='color:#f7d21e;'>📊 Relação entre atributos e taxa de vitória</h1>",
    unsafe_allow_html=True
)

st.write("Analise como cada atributo influencia a taxa de vitória dos Pokémon.")

# ----------------------------------------------------------------------
# 1) Carregar dados
# ----------------------------------------------------------------------
df = load_table("pokemon_battle_stats")

# ----------------------------------------------------------------------
# 2) Seleção de atributo numérico para correlação
# ----------------------------------------------------------------------
atributos_numericos = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]

atributo = st.selectbox("Selecione um atributo:", atributos_numericos)

# ----------------------------------------------------------------------
# 3) Cálculo da correlação
# ----------------------------------------------------------------------
correlacao = df[atributo].corr(df["win_rate"])

st.metric(
    label=f"Correlação entre {atributo} e taxa de vitória",
    value=f"{correlacao:.3f}"
)

# ----------------------------------------------------------------------
# 4) Gráfico de dispersão com linha de regressão
# ----------------------------------------------------------------------
fig = px.scatter(
    df,
    x=atributo,
    y="win_rate",
    trendline="ols",
    title=f"Relação entre {atributo} e taxa de vitória",
    opacity=0.7
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# 5) Explicação abaixo do gráfico
# ----------------------------------------------------------------------
st.info(
    f"""
    **Interpretação da correlação ({correlacao:.3f}):**
    
    - Valores próximos de **1.0** → forte relação positiva  
    - Valores próximos de **-1.0** → forte relação negativa  
    - Valores próximos de **0** → relação fraca ou inexistente  
    """
)
