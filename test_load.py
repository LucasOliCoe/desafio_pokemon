import pandas as pd
from etl.load import load_all_tables

def main():
    print("📥 Lendo arquivos processados...")

    dim = pd.read_csv("data/processed/dim_pokemon.csv")
    fact = pd.read_csv("data/processed/fact_combat.csv")
    stats = pd.read_csv("data/processed/pokemon_battle_stats.csv")

    print("💾 Carregando para o banco SQLite...")
    load_all_tables(dim, fact, stats)

    print("\n🎉 LOAD FINALIZADO!")

if __name__ == "__main__":
    main()
