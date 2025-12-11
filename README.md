
# 📘 Pokédex Analytics — ETL + Machine Learning + Streamlit Dashboard

Bem-vindo ao **Pokédex Analytics**, um projeto completo que integra:

- **Coleta de dados Pokémon**
- **Processamento e Transformação (ETL)**
- **Criação de tabelas dimensionais e fato**
- **Cálculo de estatísticas de batalha**
- **Banco SQLite otimizado**
- **Dashboard interativo no Streamlit**
- **Modelo preditivo simples para batalhas Pokémon**

Este repositório demonstra domínio prático de análise de dados, engenharia, visualização e machine learning aplicado a um tema divertido: **Pokémon!**

---

## 🧱 Arquitetura do Projeto

```
Pokémon API / CSV Raw
          │
          ▼
Extração (E)
CSV brutos + API PokéAPI
          │
          ▼
Transformação (T)
Limpeza, padronização e enriquecimento
          │
          ├── Dim_Pokemon
          ├── Fact_Combate
          └── Pokemon_Battle_Stats (winrate)
          │
          ▼
Carga (L)
Banco SQLite → pokemon.db
          │
          ▼
Dashboard Streamlit
```

---

## 📂 Estrutura de Diretórios

```
desafio_pokemon_kaizen/
│
├── etl/
│   ├── api_client.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/pokemon.db
│
├── dashboard/
│   ├── app.py
│   ├── utils.py
│   ├── pages/
│   │   ├── 1_visao_geral.py
│   │   ├── 2_taxa_vitoria.py
│   │   ├── 3_correlacao.py
│   │   ├── 4_modelo_preditivo.py
│   │   └── 5_tempo_ideal.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Tecnologias Utilizadas

| Tipo | Ferramenta |
|------|------------|
| Linguagem | **Python 3.11** |
| Dashboard | **Streamlit** |
| Banco | **SQLite + Pandas** |
| Visualização | **Plotly Express** |
| ETL | Python + Requests + Pandas |
| API | PokeAPI |

---

## 🚀 Como Executar o Projeto

### 1️⃣ Criar ambiente virtual
```bash
python -m venv .venv
```

Ativar:

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

---

### 2️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

---

### 3️⃣ Rodar o ETL (opcional)
```bash
python etl/extract.py
python etl/transform.py
python etl/load.py
```

---

### 4️⃣ Executar o dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📊 Funcionalidades do Dashboard

### 🟡 1. Visão Geral
- Contagem total de Pokémon
- Distribuição por tipos (gráfico ordenado)
- Principais atributos médios

### 🔵 2. Taxa de Vitória
- Ranking por winrate
- Filtros por tipo e geração

### 🟣 3. Correlação
- Heatmap das correlações entre atributos

### ⚔️ 4. Modelo Preditivo
- Seleção de Pokémon
- Probabilidade de vitória
- Radar Chart

### 🟢 5. Time Ideal
- Sugestão de time ideal

---

## 👤 Autor
**Lucas de Oliveira Coelho**

---

## 📄 Licença
MIT — Livre para uso.

