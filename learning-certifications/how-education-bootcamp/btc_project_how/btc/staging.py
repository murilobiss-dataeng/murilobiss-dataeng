import pandas as pd
import awswrangler as wr

hist_df = wr.s3.read_parquet("s3://how-eng-dados-biss/btc/historical/", dataset=True)

hist_df['Open Time'] = pd.to_datetime(hist_df['Open_Time']/1000, unit='s')
hist_df['Close Time'] = pd.to_datetime(hist_df['Close_Time']/1000, unit='s')

numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote_Asset_Volume', 'TB_Base_Volume', 'TB_Quote_Volume']
hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)

wr.s3.to_parquet(
    df=hist_df,
    path="s3://how-eng-dados-biss/btc/historical/staging/",
    dataset=True)
