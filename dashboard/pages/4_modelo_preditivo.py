import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils import load_table, get_sprite_url_by_name


# ==========================================
# CÁLCULO DE PROBABILIDADE
# ==========================================
def calcular_probabilidades(p1_row: pd.Series, p2_row: pd.Series):
    """Calcula probabilidade de vitória baseada no win_rate."""
    w1 = float(p1_row.get("win_rate", 0) or 0)
    w2 = float(p2_row.get("win_rate", 0) or 0)

    if (w1 + w2) == 0:
        return 0.5, 0.5

    p1 = w1 / (w1 + w2)
    p2 = w2 / (w1 + w2)
    return p1, p2


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================
def main():
    st.markdown(
        "<h1 style='color:#FFD92F;'>✨ Modelo Preditivo de Batalha</h1>",
        unsafe_allow_html=True,
    )

    st.write(
        "Escolha dois Pokémon para estimar quem tem maior "
        "**probabilidade de vitória** com base nas estatísticas históricas."
    )

    # ================= LOAD DATA =================
    df = load_table("pokemon_battle_stats").copy()
    df["win_rate"] = pd.to_numeric(df["win_rate"], errors="coerce")

    nomes = sorted(df["name"].unique().tolist())

    # ================= SELECT BOXES =================
    col_sel1, col_sel2 = st.columns(2)

    with col_sel1:
        pokemon1 = st.selectbox("Selecione o Pokémon 1:", nomes, index=0)

    with col_sel2:
        default_idx = 1 if len(nomes) > 1 else 0
        pokemon2 = st.selectbox("Selecione o Pokémon 2:", nomes, index=default_idx)

    if pokemon1 == pokemon2:
        st.warning("Selecione **Pokémons diferentes**!")
        return

    # PEGAR STATS
    p1_stats = df[df["name"] == pokemon1].iloc[0]
    p2_stats = df[df["name"] == pokemon2].iloc[0]

    # ================= PROBABILIDADES =================
    prob1, prob2 = calcular_probabilidades(p1_stats, p2_stats)

    col_prob1, col_prob2 = st.columns(2)

    with col_prob1:
        st.markdown(
            f"<h2 style='color:#FFD92F;'>{pokemon1}</h2>",
            unsafe_allow_html=True,
        )
        st.metric("Probabilidade de Vitória", f"{prob1 * 100:.1f}%")

    with col_prob2:
        st.markdown(
            f"<h2 style='color:#7FB3FF;'>{pokemon2}</h2>",
            unsafe_allow_html=True,
        )
        st.metric("Probabilidade de Vitória", f"{prob2 * 100:.1f}%")

    st.markdown("---")

    # ================= SPRITES VS =================
    col_s1, col_mid, col_s2 = st.columns([2, 1, 2])

    with col_s1:
        st.image(
            get_sprite_url_by_name(pokemon1),
            width=120,
            caption=pokemon1,
        )

    with col_mid:
        st.markdown(
            "<h2 style='text-align:center; margin-top:40px;'>⚔️ VS ⚔️</h2>",
            unsafe_allow_html=True,
        )

    with col_s2:
        st.image(
            get_sprite_url_by_name(pokemon2),
            width=120,
            caption=pokemon2,
        )

    # ================= RADAR =================
    st.markdown("### ⚔️ Comparação dos Atributos (Radar Style)")

    stats_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]

    radar_df = pd.DataFrame(
        {
            "atributo": stats_cols * 2,
            "valor": [p1_stats[c] for c in stats_cols]
            + [p2_stats[c] for c in stats_cols],
            "pokemon": [pokemon1] * len(stats_cols)
            + [pokemon2] * len(stats_cols),
        }
    )

    fig_radar = px.line_polar(
        radar_df,
        r="valor",
        theta="atributo",
        color="pokemon",
        line_close=True,
        template="plotly_dark",
    )
    fig_radar.update_traces(fill="toself")
    fig_radar.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", y=-0.15),
    )

    st.plotly_chart(fig_radar, use_container_width=True)


if __name__ == "__main__":
    main()
