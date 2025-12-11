import os
import pandas as pd

PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)


# ---------------------------------------
# Função auxiliar: padronizar colunas
# ---------------------------------------
def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        c.strip().lower().replace(" ", "_")
        for c in df.columns
    ]
    return df


# ---------------------------------------
# 1) DIM_POKEMON  (pokemons + atributos)
# ---------------------------------------
def build_dim_pokemon(df_pok: pd.DataFrame, df_attrs: pd.DataFrame) -> pd.DataFrame:
    """
    Une os dados básicos de pokémon com os atributos completos.
    Também normaliza tipos e converte colunas numéricas.
    """
    df_pok = _normalize_columns(df_pok)
    df_attrs = _normalize_columns(df_attrs)

    # junta pelos ids
    df = df_pok.merge(
        df_attrs,
        on="id",
        suffixes=("", "_attr")
    )

    # resolve possíveis colunas duplicadas de "name"
    if "name_attr" in df.columns:
        df["name"] = df["name_attr"]
        df = df.drop(columns=["name_attr"])

    # atributos numéricos
    numeric_cols = [
        "hp", "attack", "defense", "sp_attack",
        "sp_defense", "speed", "generation"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # legendary para bool
    if "legendary" in df.columns:
        df["legendary"] = df["legendary"].astype(str).str.lower().map(
            {"true": True, "false": False}
        )

    # separa tipos: "Grass/Poison" → primary_type, secondary_type
    if "types" in df.columns:
        types_split = df["types"].astype(str).str.split("/", n=1, expand=True)
        df["primary_type"] = types_split[0]
        df["secondary_type"] = types_split[1]

    # salva
    path = os.path.join(PROCESSED_DIR, "dim_pokemon.csv")
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"💾 dim_pokemon salvo em {path} ({df.shape[0]} linhas)")

    return df


# ---------------------------------------
# 2) FACT_COMBAT  (normalizar combates)
# ---------------------------------------
def build_fact_combat(df_comb: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa a tabela de combates.

    No seu CSV, os campos são:
      first_pokemon, second_pokemon, winner
    (todos IDs)
    Vamos:
      - normalizar nomes
      - criar um battle_id
    """
    df_comb = _normalize_columns(df_comb)

    # garante nomes esperados
    rename_map = {
        "first_pokemon": "first_pokemon_id",
        "second_pokemon": "second_pokemon_id",
        "winner": "winner_pokemon_id",
    }
    df_comb = df_comb.rename(columns=rename_map)

    # cria um ID de batalha sequencial (1, 2, 3...)
    df_comb = df_comb.reset_index(drop=True)
    df_comb["battle_id"] = df_comb.index + 1

    # organiza colunas
    cols = ["battle_id", "first_pokemon_id", "second_pokemon_id", "winner_pokemon_id"]
    other_cols = [c for c in df_comb.columns if c not in cols]
    df_comb = df_comb[cols + other_cols]

    path = os.path.join(PROCESSED_DIR, "fact_combat.csv")
    df_comb.to_csv(path, index=False, encoding="utf-8")
    print(f"💾 fact_combat salvo em {path} ({df_comb.shape[0]} linhas)")

    return df_comb


# ---------------------------------------
# 3) POKEMON_BATTLE_STATS
#    (estatísticas de batalha por pokémon)
# ---------------------------------------
def build_pokemon_battle_stats(dim_pokemon: pd.DataFrame, fact_combat: pd.DataFrame) -> pd.DataFrame:
    """
    Gera uma tabela analítica por pokémon:
      - battles
      - wins
      - losses
      - win_rate
    Junta com os atributos de dim_pokemon
    """

    pok = _normalize_columns(dim_pokemon)
    comb = _normalize_columns(fact_combat)

    # Garantir tipos numéricos
    pok["id"] = pd.to_numeric(pok["id"], errors="coerce").astype("Int64")

    comb["first_pokemon_id"] = pd.to_numeric(comb["first_pokemon_id"], errors="coerce").astype("Int64")
    comb["second_pokemon_id"] = pd.to_numeric(comb["second_pokemon_id"], errors="coerce").astype("Int64")
    comb["winner_pokemon_id"] = pd.to_numeric(comb["winner_pokemon_id"], errors="coerce").astype("Int64")

    registros = []

    for _, row in comb.iterrows():
        battle_id = row["battle_id"]
        first_id = row["first_pokemon_id"]
        second_id = row["second_pokemon_id"]
        winner_id = row["winner_pokemon_id"]

        registros.append({
            "pokemon_id": first_id,
            "battle_id": battle_id,
            "is_winner": 1 if first_id == winner_id else 0,
        })

        registros.append({
            "pokemon_id": second_id,
            "battle_id": battle_id,
            "is_winner": 1 if second_id == winner_id else 0,
        })

    df_stats = pd.DataFrame(registros)
    df_stats["pokemon_id"] = pd.to_numeric(df_stats["pokemon_id"], errors="coerce").astype("Int64")

    # Agregação
    agg = (
        df_stats
        .groupby("pokemon_id")
        .agg(
            battles=("battle_id", "nunique"),
            wins=("is_winner", "sum"),
        )
        .reset_index()
    )

    agg["losses"] = agg["battles"] - agg["wins"]
    agg["win_rate"] = agg["wins"] / agg["battles"]

    # Antes do merge, garantir tipos idênticos
    agg["pokemon_id"] = agg["pokemon_id"].astype("Int64")
    pok["id"] = pok["id"].astype("Int64")

    final = pok.merge(
        agg,
        left_on="id",
        right_on="pokemon_id",
        how="left"
    )

    # Preenchimento de pokemons sem batalhas
    for col in ["battles", "wins", "losses"]:
        final[col] = final[col].fillna(0).astype(int)

    final["win_rate"] = final["win_rate"].fillna(0.0)

    path = os.path.join(PROCESSED_DIR, "pokemon_battle_stats.csv")
    final.to_csv(path, index=False, encoding="utf-8")
    print(f"💾 pokemon_battle_stats salvo em {path} ({final.shape[0]} linhas)")

    return final
