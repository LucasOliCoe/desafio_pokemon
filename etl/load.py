import os
import sqlite3
import pandas as pd

DB_PATH = "data/db/pokemon.db"


def init_db():
    """
    Cria o banco SQLite caso não exista.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.close()
    print(f"🗄️ Banco criado/aberto em {DB_PATH}")


def load_table(df: pd.DataFrame, table_name: str):
    """
    Carrega um DataFrame em uma tabela SQLite (substituindo se já existir).
    """
    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()
    print(f"💾 Tabela '{table_name}' carregada com {df.shape[0]} linhas")


def load_all_tables(dim_pok, fact_comb, stats):
    """
    Carrega todas as tabelas transformadas para dentro do banco.
    """
    init_db()

    load_table(dim_pok, "dim_pokemon")
    load_table(fact_comb, "fact_combat")
    load_table(stats, "pokemon_battle_stats")

    print("🎉 Todas as tabelas foram carregadas com sucesso!")
