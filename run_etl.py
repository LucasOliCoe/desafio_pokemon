import pandas as pd

from etl.api_client import APIClient
from etl.extract import extract_all_pokemons, extract_attributes, extract_all_combats
from etl.transform import build_dim_pokemon, build_fact_combat, build_pokemon_battle_stats
from etl.load import load_all_tables


def main():

    print("=" * 60)
    print("🚀 INICIANDO PIPELINE ETL – POKEMON BATTLE ANALYTICS")
    print("=" * 60)

    # --------------------------
    # 1) EXTRAÇÃO
    # --------------------------
    print("\n📥 ETAPA 1 – EXTRAÇÃO")

    client = APIClient()

    df_pok = extract_all_pokemons(client)
    df_attrs = extract_attributes(client, df_pok)
    df_comb = extract_all_combats(client)

    # --------------------------
    # 2) TRANSFORMAÇÃO
    # --------------------------
    print("\n🔧 ETAPA 2 – TRANSFORMAÇÃO")

    dim_pok = build_dim_pokemon(df_pok, df_attrs)
    fact_comb = build_fact_combat(df_comb)
    stats = build_pokemon_battle_stats(dim_pok, fact_comb)

    # --------------------------
    # 3) LOAD
    # --------------------------
    print("\n💾 ETAPA 3 – LOAD")

    load_all_tables(dim_pok, fact_comb, stats)

    print("\n🎉 PIPELINE COMPLETA!")
    print("-" * 60)


if __name__ == "__main__":
    main()
