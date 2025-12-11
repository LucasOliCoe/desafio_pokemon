import sqlite3
import pandas as pd
import streamlit as st
import unicodedata

DB_PATH = "data/db/pokemon.db"


# ================================
# FUNÇÃO PARA CARREGAR TABELA
# ================================
def load_table(table_name: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


# ================================
# SLUGIFY — converter nome → formato de sprite
# ================================
def slugify_pokemon_name(name: str) -> str:
    """
    Converte nomes de Pokémon para o formato usado em sprites do Pokemondb.
    Exemplo:
      Farfetch'd → farfetchd
      Mr. Mime → mr-mime
      Nidoran♀ → nidoran-f
      Type: Null → type-null
    """

    name = name.strip()

    # Casos realmente especiais
    special_cases = {
        "Farfetch'd": "farfetchd",
        "Sirfetch'd": "sirfetchd",
        "Mr. Mime": "mr-mime",
        "Mr. Rime": "mr-rime",
        "Nidoran♀": "nidoran-f",
        "Nidoran♂": "nidoran-m",
        "Type: Null": "type-null",
        "Ho-Oh": "ho-oh",
    }

    if name in special_cases:
        return special_cases[name]

    # Remover acentos
    s = unicodedata.normalize("NFKD", name)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))

    # Padronização geral
    s = s.lower()
    s = s.replace(" ", "-")
    s = s.replace(".", "")
    s = s.replace("'", "")
    s = s.replace(":", "")
    s = s.replace("é", "e")
    s = s.replace("’", "")

    return s


# ================================
# GERAR SPRITE VIA NOME
# ================================
def get_sprite_url_by_name(name: str) -> str:
    slug = slugify_pokemon_name(name)
    return f"https://img.pokemondb.net/sprites/home/normal/{slug}.png"


# ================================
# CARD ESTILO GBA PARA O STREAMLIT
# ================================
def render_pokemon_card_gba(stats: pd.Series, subtitle: str = "Pokémon"):
    """Renderiza card estilo GBA"""

    name = stats["name"]
    sprite = get_sprite_url_by_name(name)

    html = f"""
<div style="
    background:#111827;
    border-radius:18px;
    padding:16px;
    border:2px solid #FACC15;
    max-width:320px;
    margin:0 auto;
    box-shadow:0 0 20px rgba(0,0,0,0.6);
">

    <div style="display:flex; justify-content:space-between; color:#FACC15; font-size:13px;">
        <span>BATTLE·DEX</span>
        <span style="color:#9CA3AF;">{subtitle}</span>
    </div>

    <div style="text-align:center; margin-top:6px;">
        <img src="{sprite}" style="width:96px; image-rendering:pixelated;" />
    </div>

    <h3 style="text-align:center; margin:8px 0 0 0; color:#FACC15; font-size:22px;">
        {name}
    </h3>

</div>
"""
    st.markdown(html, unsafe_allow_html=True)
