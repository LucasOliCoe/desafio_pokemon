import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils import load_table


def main():
    st.markdown(
        "<h1 style='color:#FFD92F;'>📊 Visão Geral da Pokédex</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "Um resumo completo dos Pokémon e suas características essenciais, "
        "alimentado pelos dados de batalha."
    )

    # ================= CARREGA DADOS =================
    df = load_table("pokemon_battle_stats").copy()

    # Garantias básicas
    df["generation"] = pd.to_numeric(df["generation"], errors="coerce")
    df["primary_type"] = df["primary_type"].fillna("Unknown")

    # ================= MÉTRICAS PRINCIPAIS =================
    total_pokemon = len(df)
    total_tipos = df["primary_type"].nunique()
    total_geracoes = df["generation"].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pokémons cadastrados", f"{total_pokemon}")
    with col2:
        st.metric("Tipos Primários", f"{total_tipos}")
    with col3:
        st.metric("Gerações", f"{int(total_geracoes)}")

    st.markdown("---")

    # ================= DISTRIBUIÇÃO POR TIPO (ORDENADO) =================
    st.markdown("### 📊 Distribuição por Tipo")

    # Agrupa por tipo e conta, já ordenando do maior para o menor
    dist_tipo = (
        df.groupby("primary_type")["id"]
        .count()
        .reset_index(name="quantidade")
        .sort_values("quantidade", ascending=False)
    )

    fig = px.bar(
        dist_tipo,
        x="primary_type",
        y="quantidade",
        labels={"primary_type": "Tipo primário", "quantidade": "Quantidade"},
    )

    # Deixa mais compacto e bonito
    fig.update_layout(
        xaxis_title="Tipo primário",
        yaxis_title="Quantidade de Pokémon",
        margin=dict(l=0, r=0, t=40, b=80),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ================= TABELA: ATRIBUTOS MÉDIOS POR TIPO =================
    st.markdown("### 🧬 Atributos médios por tipo")

    stats_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]

    atributos_medios = (
        df.groupby("primary_type")[stats_cols]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("primary_type")
    )

    st.dataframe(
        atributos_medios,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # ================= TABELA: TOP 10 POR ATAQUE =================
    st.markdown("### 🔥 Top 10 Pokémon por ataque")

    top_attack = (
        df[["id", "name", "primary_type", "attack"]]
        .sort_values("attack", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    st.dataframe(
        top_attack,
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()
