from binance import Client
import pandas as pd
import awswrangler as wr
import os

api = os.environ.get("apikey")
secret = os.environ.get("secret")
coin = 'ETHBTC'

client = Client(api, secret)

tickers = client.get_all_tickers()

df = pd.DataFrame(tickers)

wr.s3.to_parquet(
    df=df,
    path="s3://how-eng-dados-biss/btc/",
    dataset=True)