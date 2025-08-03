from binance import Client
import pandas as pd
import awswrangler as wr
import os

api = os.environ.get("apikey")
secret = os.environ.get("secret")
coin = 'ETHBTC'

client = Client(api, secret)

historical = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, '1 Jan 2022')

hist_df = pd.DataFrame(historical)
hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                    'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']
                    
wr.s3.to_parquet(
    df=hist_df,
    path="s3://how-eng-dados-biss/btc/historical",
    dataset=True)

