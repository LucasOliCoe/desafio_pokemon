import os
import pandas as pd
from .api_client import APIClient

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)


def extract_all_pokemons(client: APIClient):
    """
    1. Busca todos os pokémons paginados em /pokemon
    2. Salva em data/raw/pokemons_raw.csv
    3. Retorna DataFrame
    """
    print("📥 Extraindo lista completa de pokémons...")

    pokemons = client.get_all_paginated("/pokemon", list_key="pokemons", per_page=50)
    df = pd.DataFrame(pokemons)

    path = os.path.join(RAW_DIR, "pokemons_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"  ✔ {df.shape[0]} pokémons salvos em {path}")

    return df


def extract_attributes(client: APIClient, df_pokemons: pd.DataFrame):
    """
    Para cada Pokémon obtém seus atributos detalhados chamando:
    GET /pokemon/{id}
    """
    print("\n📥 Extraindo atributos de cada pokémon...")

    attributes = []

    for i, row in df_pokemons.iterrows():
        pokemon_id = row["id"]

        data = client.get(f"/pokemon/{pokemon_id}")
        attributes.append(data)

        if (i + 1) % 50 == 0:
            print(f"  → {i + 1} pokémons processados...")

    df = pd.DataFrame(attributes)

    path = os.path.join(RAW_DIR, "pokemon_attributes_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"  ✔ {df.shape[0]} atributos salvos em {path}")

    return df


def extract_all_combats(client: APIClient):
    """
    Extração completa dos combates via /combats
    (assumindo que o schema CombatPage tem chave 'combats')
    """
    print("\n📥 Extraindo lista completa de combates...")

    combats = client.get_all_paginated("/combats", list_key="combats", per_page=50)
    df = pd.DataFrame(combats)

    path = os.path.join(RAW_DIR, "combats_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"  ✔ {df.shape[0]} combates salvos em {path}")

    return df
