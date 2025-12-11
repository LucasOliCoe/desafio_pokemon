import streamlit as st
import pandas as pd

# --------------------------------------------------------------
#  CONFIGURACAO DA PAGINA
# --------------------------------------------------------------
st.set_page_config(
    page_title="Arquitetura ETL",
    layout="wide",
    page_icon="⚙️"
)

st.title("⚙️ Arquitetura do Pipeline ETL")
st.markdown(
    """
Esta pagina apresenta a arquitetura completa do pipeline ETL que alimenta a Pokedex Analitica.  
Aqui estao descritas as etapas de Extracao, Transformacao e Carga, bem como metricas importantes
e a estrutura de diretorios utilizada no projeto.
"""
)

st.divider()

# --------------------------------------------------------------
#  SECAO 1 - DIAGRAMA DO PIPELINE (MERMAID)
# --------------------------------------------------------------
st.subheader("📡 Fluxo Geral do Pipeline")

st.markdown(
    """
```mermaid
flowchart LR
    A[API Pokemon com JWT] --> B[Extract - Coleta de Dados]
    B --> C[Raw Layer - CSV bruto]
    C --> D[Transform - Limpeza e Engenharia]
    D --> E[Processed Layer - Dados tratados]
    E --> F[(SQLite DB)]
    F --> G[Dashboard Streamlit]
```
"""
)

st.divider()

# --------------------------------------------------------------
#  SECAO 2 - ETAPAS EXPLICADAS
# --------------------------------------------------------------
st.subheader("Etapas do ETL")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        ### Extract
        - Autenticacao via JWT  
        - Extracao de:
            - Lista de Pokemons  
            - Atributos detalhados  
            - Combates  
        - Salvamento em **data/raw**
        """
    )

with col2:
    st.markdown(
        """
        ### Transform
        - Limpeza e padronizacao  
        - Conversao de tipos  
        - Juncoes  
        - Criacao de features:
            - win_rate  
            - numero de batalhas  
        - Salvamento em **data/processed**
        """
    )

with col3:
    st.markdown(
        """
        ### Load
        - Criacao do banco SQLite  
        - Tabelas:
            - dim_pokemon  
            - fact_combat  
            - pokemon_battle_stats  
        - Processo seguro e idempotente
        """
    )

st.divider()

# --------------------------------------------------------------
#  SECAO 3 - METRICAS DO PIPELINE
# --------------------------------------------------------------
st.subheader("Metricas do Pipeline")

try:
    df_stats = pd.read_csv("data/processed/pokemon_battle_stats.csv")
    df_dim = pd.read_csv("data/processed/dim_pokemon.csv")
    df_combat = pd.read_csv("data/processed/fact_combat.csv")

    colA, colB, colC, colD = st.columns(4)

    with colA:
        st.metric("Pokemons carregados", len(df_stats))

    with colB:
        st.metric("Batalhas registradas", f"{len(df_combat):,}".replace(",", "."))

    with colC:
        st.metric("Tipos primarios", df_dim["primary_type"].nunique())

    with colD:
        st.metric("Geracoes", df_dim["generation"].nunique())

except Exception as e:
    st.error(f"Erro ao carregar metricas: {e}")

st.divider()

# --------------------------------------------------------------
#  SECAO 4 - ESTRUTURA DE PASTAS
# --------------------------------------------------------------
st.subheader("Estrutura de Pastas do Projeto")

st.code(
    """
desafio_pokemon_kaizen/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│
├── dashboard/
│   ├── app.py
│   └── pages/
│       ├── 0_arquitetura_etl.py
│       ├── 1_home.py
│       ├── 2_visao_geral.py
│       ├── 3_taxa_vitoria.py
│       ├── 4_correlacao.py
│       ├── 5_modelo_preditivo.py
│       └── 6_tempo_ideal.py
│
├── etl/
│   ├── api_client.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── run_etl.py
└── README.md
"""
)

st.divider()

# --------------------------------------------------------------
#  SECAO 5 - DESTAQUES TECNICOS
# --------------------------------------------------------------
st.subheader("Destaques tecnicos do pipeline")

st.markdown(
    """
- ETL completo com autenticacao JWT  
- Camadas bem definidas: raw, processed e banco de dados  
- Banco SQLite leve e facil de distribuir para avaliacao  
- Engenharia de atributos para analise de batalhas (win_rate, numero de batalhas etc.)  
- Dashboard Streamlit tematico inspirado em Pokedex  
"""
)

st.success("Pagina de Arquitetura ETL carregada com sucesso!")
