import streamlit as st

# --- Corrige caminho para permitir imports do pacote dashboard ---
import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Configuração básica da página
st.set_page_config(
    page_title="Pokédex Battle Analytics",
    page_icon="🧿",
    layout="wide"
)

# ==============================
# CSS para estilo de Pokédex
# ==============================
POKEDEX_CSS = """
<style>
/* Fundo geral */
.stApp {
    background: radial-gradient(circle at top left, #ff5252 0, #b71c1c 40%, #000 100%);
    color: #f5f5f5;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Caixa principal tipo visor da Pokédex */
.pokedex-container {
    background: #111827;
    border-radius: 24px;
    padding: 24px 28px;
    border: 3px solid #facc15;
    box-shadow: 0 0 0 4px #1f2937, 0 18px 40px rgba(0,0,0,0.6);
}

/* Título com estilo */
.pokedex-title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #facc15;
    text-shadow: 0 0 6px rgba(0,0,0,0.8);
}

/* Subtítulo */
.pokedex-subtitle {
    font-size: 16px;
    color: #e5e7eb;
}

/* Barrinha de status tipo “LED” */
.status-bar {
    display: flex;
    gap: 8px;
    margin-top: 16px;
    margin-bottom: 16px;
}

.status-dot {
    width: 14px;
    height: 14px;
    border-radius: 999px;
    box-shadow: 0 0 10px rgba(0,0,0,0.7);
}

.status-dot.red    { background: #ef4444; }
.status-dot.yellow { background: #facc15; }
.status-dot.green  { background: #22c55e; }

/* Caixa de descrição à direita */
.info-box {
    background: #020617;
    border-radius: 16px;
    border: 1px solid #4b5563;
    padding: 16px 18px;
}

/* Sidebar com pegada de Pokédex */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0, #020617 100%);
    border-right: 2px solid #374151;
}

section[data-testid="stSidebar"] .css-1d391kg, 
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

</style>
"""

st.markdown(POKEDEX_CSS, unsafe_allow_html=True)

# ==============================
# Layout principal
# ==============================
col_left, col_right = st.columns([2.3, 1.2])

with col_left:
    st.markdown(
        """
        <div class="pokedex-container">
            <div class="pokedex-title">
                Pokédex Battle Analytics
            </div>
            <div class="pokedex-subtitle">
                Análises avançadas de batalhas Pokémon · Powered by ETL + Streamlit
            </div>

            <div class="status-bar">
                <div class="status-dot red"></div>
                <div class="status-dot yellow"></div>
                <div class="status-dot green"></div>
            </div>

            <div style="margin-top: 12px; font-size: 15px; line-height: 1.6;">
                Use o menu lateral para navegar entre as seções da Pokédex analítica:
                <ul>
                    <li><b>Visão Geral</b> – catálogo de Pokémons e atributos médios por tipo.</li>
                    <li><b>Taxa de Vitória</b> – rankings por win rate e desempenho por tipo.</li>
                    <li><b>Correlação</b> – como os atributos influenciam as vitórias.</li>
                    <li><b>Modelo Preditivo</b> – estime a chance de vitória a partir dos atributos.</li>
                    <li><b>Time Ideal</b> – sugestão de equipe otimizada com base nas estatísticas.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    st.markdown(
        """
        <div class="info-box">
            <b>STATUS DO ETL</b><br/>
            <span style="font-size: 13px;">
                • Dados extraídos da API protegida por JWT<br/>
                • Transformações salvas em <code>data/processed/</code><br/>
                • Banco SQLite em <code>data/db/pokemon.db</code><br/>
                • Tabelas principais: <code>dim_pokemon</code>, 
                  <code>fact_combat</code>, <code>pokemon_battle_stats</code>
            </span>
            <hr style="border: none; border-top: 1px solid #374151; margin: 10px 0;" />
            <span style="font-size: 13px;">
                Este painel foi construído para demonstrar raciocínio analítico, 
                domínio de ETL e visualização interativa de dados usando a temática Pokémon.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
