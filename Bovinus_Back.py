from datetime import datetime, timezone
from typing import Literal, Optional

import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =====================================================================
# 1. CONFIGURAÇÃO DA API E DO BANCO MYSQL
# =====================================================================
app = FastAPI(title="Bobinus Augusta - Controle de Tempo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "bobinus_augusta",
}


class BipRequest(BaseModel):
    codigo: str
    etapa: Literal["ENTRADA", "PESAGEM", "SAIDA"]
    timestamp: Optional[datetime] = None


def get_conn():
    return mysql.connector.connect(**DB_CONFIG)


# =====================================================================
# 2. CAPTURA DO HORÁRIO E CÁLCULO DE TEMPO EM SEGUNDOS
# =====================================================================
def normalizar_dt(dt: Optional[datetime]) -> datetime:
    """Usa o timestamp enviado ou o horário atual do servidor e padroniza para o MySQL."""
    alvo = dt or datetime.now(timezone.utc)
    if alvo.tzinfo is not None:
        alvo = alvo.astimezone(timezone.utc).replace(tzinfo=None)
    return alvo.replace(microsecond=0)


def calc_segundos(inicio: Optional[datetime], fim: Optional[datetime]) -> Optional[int]:
    """Calcula a diferença entre dois horários em segundos (nunca menor que 0)."""
    if not inicio or not fim:
        return None
    return max(int((fim - inicio).total_seconds()), 0)


# =====================================================================
# 3. ROTA PRINCIPAL: REGISTRO DOS 3 BIPS E CÁLCULO DOS TEMPOS
# =====================================================================
@app.post("/api/bip")
def registrar_bip(payload: BipRequest):
    codigo = payload.codigo.strip().upper()
    agora = normalizar_dt(payload.timestamp)

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        # --- ETAPA 1: ENTRADA (Abre a comanda e grava entrada_em) ---
        if payload.etapa == "ENTRADA":
            cursor.execute(
                """
                SELECT * FROM sessoes_comanda
                WHERE codigo_comanda = %s AND status != 'FINALIZADA'
                ORDER BY id DESC LIMIT 1
                """,
                (codigo,),
            )
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Comanda já está ativa.")

            cursor.execute(
                """
                INSERT INTO sessoes_comanda (codigo_comanda, status, entrada_em)
                VALUES (%s, 'ABERTA', %s)
                """,
                (codigo, agora),
            )
            conn.commit()

            cursor.execute("SELECT * FROM sessoes_comanda WHERE id = %s", (cursor.lastrowid,))
            return {"sessao": cursor.fetchone()}

        # --- ETAPA 2: PESAGEM (Grava pesagem_em e calcula tempo_ate_pesagem_seg) ---
        if payload.etapa == "PESAGEM":
            cursor.execute(
                """
                SELECT * FROM sessoes_comanda
                WHERE codigo_comanda = %s AND status = 'ABERTA'
                ORDER BY id DESC LIMIT 1
                """,
                (codigo,),
            )
            sessao = cursor.fetchone()
            if not sessao:
                raise HTTPException(status_code=404, detail="Comanda ABERTA não encontrada.")

            tempo_ate_pesagem = calc_segundos(sessao["entrada_em"], agora)
            cursor.execute(
                """
                UPDATE sessoes_comanda
                SET status = 'PESADA',
                    pesagem_em = %s,
                    tempo_ate_pesagem_seg = %s
                WHERE id = %s
                """,
                (agora, tempo_ate_pesagem, sessao["id"]),
            )
            conn.commit()

            cursor.execute("SELECT * FROM sessoes_comanda WHERE id = %s", (sessao["id"],))
            return {"sessao": cursor.fetchone()}

        # --- ETAPA 3: SAÍDA (Grava saida_em e calcula tempo_apos_pesagem_seg e tempo_total_seg) ---
        if payload.etapa == "SAIDA":
            cursor.execute(
                """
                SELECT * FROM sessoes_comanda
                WHERE codigo_comanda = %s AND status IN ('ABERTA', 'PESADA')
                ORDER BY id DESC LIMIT 1
                """,
                (codigo,),
            )
            sessao = cursor.fetchone()
            if not sessao:
                raise HTTPException(status_code=404, detail="Comanda ativa não encontrada.")

            tempo_apos_pesagem = calc_segundos(sessao["pesagem_em"], agora)
            tempo_total = calc_segundos(sessao["entrada_em"], agora)

            cursor.execute(
                """
                UPDATE sessoes_comanda
                SET status = 'FINALIZADA',
                    saida_em = %s,
                    tempo_apos_pesagem_seg = %s,
                    tempo_total_seg = %s
                WHERE id = %s
                """,
                (agora, tempo_apos_pesagem, tempo_total, sessao["id"]),
            )
            conn.commit()

            cursor.execute("SELECT * FROM sessoes_comanda WHERE id = %s", (sessao["id"],))
            return {"sessao": cursor.fetchone()}

    finally:
        cursor.close()
        conn.close()


# =====================================================================
# 4. ROTAS DE CONSULTA PARA MONITORAMENTO E DASHBOARD
# =====================================================================
@app.get("/api/comandas/ativas")
def listar_ativas():
    """Lista comandas ainda no restaurante e quanto tempo já passou desde a entrada."""
    agora = normalizar_dt(None)
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT * FROM sessoes_comanda
            WHERE status IN ('ABERTA', 'PESADA')
            ORDER BY entrada_em ASC
            """
        )
        comandas = cursor.fetchall()
        for c in comandas:
            c["tempo_decorrido_seg"] = calc_segundos(c["entrada_em"], agora)
        return {"total_ativas": len(comandas), "comandas": comandas}
    finally:
        cursor.close()
        conn.close()


@app.get("/api/metricas/resumo")
def metricas_resumo():
    """Retorna médias e máximos dos tempos calculados no banco."""
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_sessoes,
                SUM(CASE WHEN status = 'FINALIZADA' THEN 1 ELSE 0 END) AS total_finalizadas,
                ROUND(AVG(tempo_ate_pesagem_seg), 0) AS media_ate_pesagem_seg,
                ROUND(AVG(tempo_apos_pesagem_seg), 0) AS media_apos_pesagem_seg,
                ROUND(AVG(tempo_total_seg), 0) AS media_total_seg,
                MAX(tempo_ate_pesagem_seg) AS max_ate_pesagem_seg,
                MAX(tempo_total_seg) AS max_total_seg
            FROM sessoes_comanda
            """
        )
        return {"metricas": cursor.fetchone()}
    finally:
        cursor.close()
        conn.close()