import streamlit as st
import pandas as pd
from dashboard.utils import load_table

st.set_page_config(layout="wide")

st.markdown("""
<h1 style='color:#ffcb05; text-shadow: 2px 2px 2px #2a75bb;'>
⚔️ TIME IDEAL — EQUIPE ÓTIMA
</h1>
""", unsafe_allow_html=True)

df = load_table("pokemon_battle_stats")

# Ranking por win rate
df_best = df.sort_values(by="win_rate", ascending=False).head(6)

st.markdown("### 🏆 Sugestão automática baseada no win rate")

st.dataframe(df_best[["name", "primary_type", "win_rate"]].style.format({"win_rate": "{:.2%}"}))

