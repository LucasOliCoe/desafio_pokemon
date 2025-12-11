import os
import math
import time
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

# ----------------------------
# Carrega variáveis do .env
# ----------------------------
load_dotenv()

BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://ec2-52-67-119-247.sa-east-1.compute.amazonaws.com:8000"
)
USERNAME = os.getenv("API_USERNAME", "kaizen-poke")
PASSWORD = os.getenv("API_PASSWORD", "4w9f@D39fkkO")


# =====================================================
#                 API CLIENT
# =====================================================
class APIClient:
    """
    Cliente da API Pokémon com:
      ✔ Autenticação via JWT
      ✔ GET simples com retry para erro 429
      ✔ GET paginado universal (para /pokemon e /combats)
    """

    def __init__(
        self,
        username: str = USERNAME,
        password: str = PASSWORD,
        base_url: str = BASE_URL,
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.token: Optional[str] = None

    # -----------------------
    # LOGIN
    # -----------------------
    def login(self) -> None:
        """
        POST /login → retorna o token JWT.
        """
        url = f"{self.base_url}/login"
        payload = {"username": self.username, "password": self.password}

        resp = requests.post(url, json=payload)
        resp.raise_for_status()

        data = resp.json()
        self.token = data.get("access_token") or data.get("token")

        if not self.token:
            raise ValueError(f"Token não encontrado na resposta: {data}")

    def _headers(self) -> Dict[str, str]:
        if not self.token:
            self.login()
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    # -----------------------
    # GET COM RETRY (TRATA 429)
    # -----------------------
    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}{path}"

        max_attempts = 6
        backoff = 1

        for attempt in range(max_attempts):
            resp = requests.get(url, headers=self._headers(), params=params)

            # sucesso
            if resp.status_code == 200:
                return resp.json()

            # RATE LIMIT
            if resp.status_code == 429:
                print(f"⚠️ 429 Too Many Requests — aguardando {backoff}s antes de tentar novamente...")
                time.sleep(backoff)
                backoff *= 2
                continue

            # outros erros → quebrar
            resp.raise_for_status()

        raise Exception("❌ Falha após múltiplas tentativas devido ao rate limit (429).")

    # -----------------------
    # GET PAGINADO
    # -----------------------
    def get_all_paginated(
        self,
        path: str,
        list_key: str,
        per_page: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Para endpoints com estrutura:
        {
            "<list_key>": [...],
            "page": 1,
            "per_page": 20,
            "total": 799
        }
        """
        all_items: List[Dict[str, Any]] = []
        page = 1

        while True:
            params = {"page": page, "per_page": per_page}
            data = self.get(path, params=params)

            items = data.get(list_key, [])
            total = data.get("total", 0)
            per_page_resp = data.get("per_page", per_page)

            all_items.extend(items)

            # Se a API devolveu nada → fim
            if not items:
                break

            # calcula total de páginas
            total_pages = math.ceil(total / per_page_resp)

            if page >= total_pages:
                break

            page += 1

        return all_items
