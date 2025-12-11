from etl.api_client import APIClient
from etl.extract import extract_all_pokemons, extract_attributes, extract_all_combats
import pandas as pd

def main():
    client = APIClient()

    df_pok = extract_all_pokemons(client)
    df_att = extract_attributes(client, df_pok)
    df_comb = extract_all_combats(client)

    print("\n🎉 EXTRAÇÃO COMPLETA!")
    print(df_pok.head())
    print(df_att.head())
    print(df_comb.head())


if __name__ == "__main__":
    main()
