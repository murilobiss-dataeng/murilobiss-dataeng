from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db')

sql = '''
    select * from public.artist;
'''

df = pd.read_sql_query(sql, engine)