import streamlit as st
from dashboard.utils import load_table

def main():
    # Título principal
    st.markdown(
        """
        <h1 style="color:#FFD92F; font-size: 38px; margin-bottom: 0;">
            🔍 Análise de Batalha Pokédex
        </h1>
        <p style="font-size:18px; margin-top: 5px;">
            Painel analítico construído a partir de uma API protegida por JWT, 
            pipeline ETL em Python e banco SQLite local.  
            Use o menu à esquerda para explorar as seções da Pokédex analítica.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- KPIs PRINCIPAIS ----------------
    try:
        dim_pok = load_table("dim_pokemon")
        fact_comb = load_table("fact_combat")
        battle_stats = load_table("pokemon_battle_stats")
    except Exception:
        dim_pok = fact_comb = battle_stats = None

    st.markdown("---")

    st.markdown(
        "<h3 style='color:#FFD92F;'>📊 Visão rápida do dataset</h3>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        total_pokemons = len(dim_pok) if dim_pok is not None else 0
        st.metric("Pokémons cadastrados", f"{total_pokemons}")

    with col2:
        tipos_primarios = (
            dim_pok["primary_type"].nunique() if dim_pok is not None else 0
        )
        st.metric("Tipos primários", f"{tipos_primarios}")

    with col3:
        total_battles = len(fact_comb) if fact_comb is not None else 0
        st.metric("Combates simulados", f"{total_battles:,}".replace(",", "."))

    # ---------------- COMO NAVEGAR ----------------
    st.markdown("---")
    st.markdown(
        """
        <h3 style="color:#FFD92F;">🧭 Como navegar pelo painel</h3>
        <ul style="font-size:16px; line-height: 1.7;">
            <li><b>Visão Geral</b> – distribuição de Pokémons por tipo e contagem de cadastros.</li>
            <li><b>Taxa de Vitória</b> – win rate médio por tipo primário nas batalhas.</li>
            <li><b>Correlação</b> – relação entre atributos (HP, ataque, defesa, etc.) e taxa de vitória.</li>
            <li><b>Modelo Preditivo</b> – escolha dois Pokémons e veja quem tem maior probabilidade de vencer.</li>
            <li><b>Tempo Ideal</b> – sugestões de equipe com base nas estatísticas agregadas.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- CARTÃO DE STATUS DO ETL ----------------
    st.markdown("---")

    st.markdown(
        """
        <div style="
            background-color:#111319;
            border-radius: 12px;
            border: 2px solid #FFD92F;
            padding: 18px 22px;
            margin-top: 10px;
        ">
            <h3 style="color:#FFD92F; margin-top: 0;">⚙️ Status do ETL</h3>
            <ul style="font-size:15px; line-height:1.6;">
                <li>✅ Dados extraídos de uma API protegida por <b>JWT</b>.</li>
                <li>✅ Processamento em múltiplas etapas (<b>extract → transform → load</b>).</li>
                <li>✅ Arquivos intermediários salvos em <code>data/raw/</code> e <code>data/processed/</code>.</li>
                <li>✅ Banco analítico em <code>data/db/pokemon.db</code> (SQLite).</li>
                <li>✅ Tabelas principais: <code>dim_pokemon</code>, <code>fact_combat</code>, <code>pokemon_battle_stats</code>.</li>
            </ul>
            <p style="font-size:14px; opacity:0.85;">
                Esta página funciona como um resumo executivo do projeto, 
                destacando o domínio de ETL, modelagem de dados e visualização interativa 
                em um contexto lúdico com a temática Pokémon.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
