import pandas as pd

from etl.transform import (
    build_dim_pokemon,
    build_fact_combat,
    build_pokemon_battle_stats,
)

def main():
    # 1) Ler dados brutos
    df_pok = pd.read_csv("data/raw/pokemons_raw.csv")
    df_attrs = pd.read_csv("data/raw/pokemon_attributes_raw.csv")
    df_comb = pd.read_csv("data/raw/combats_raw.csv")

    # 2) Construir dim_pokemon
    dim_pok = build_dim_pokemon(df_pok, df_attrs)

    # 3) Construir fact_combat
    fact_comb = build_fact_combat(df_comb)

    # 4) Construir pokemon_battle_stats
    stats = build_pokemon_battle_stats(dim_pok, fact_comb)

    print("\n✅ TRANSFORMAÇÃO CONCLUÍDA")
    print("\n📄 dim_pokemon (5 primeiras linhas):")
    print(dim_pok.head())

    print("\n📄 fact_combat (5 primeiras linhas):")
    print(fact_comb.head())

    print("\n📄 pokemon_battle_stats (5 primeiras linhas):")
    print(stats[[
        "id", "name", "primary_type", "secondary_type",
        "battles", "wins", "losses", "win_rate"
    ]].head())


if __name__ == "__main__":
    main()
