import pandas as pd
import sqlite3


# Extração (Extract)
df = pd.read_csv("vendas_novembro.csv")


# Transformação (Transform)
analise_vendas = df.groupby("id_cliente").agg(
    qtde_vendas=("id_venda", "count"),
    total_gasto=("valor_da_venda", "sum"),
    ticket_medio=("valor_da_venda", "mean")
).reset_index()

def classificar_cliente(total):
    if total >= 600:
        return "Ouro"
    elif total >= 300:
        return "Prata"
    else:
        return "Bronze"

analise_vendas["classificacao"] = analise_vendas["total_gasto"].apply(classificar_cliente)
analise_vendas["total_gasto"] = analise_vendas["total_gasto"].round(2)
analise_vendas["ticket_medio"] = analise_vendas["ticket_medio"].round(2)


# Carregamento (Load)
conn = sqlite3.connect("vendas.db")

analise_vendas.to_sql(
    "vendas_cliente",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Dados salvos com sucesso!")
