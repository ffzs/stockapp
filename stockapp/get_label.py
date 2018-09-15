from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from sqlalchemy.types import NVARCHAR, Float, Integer

engine = create_engine('mysql+pymysql://ffzs:666@localhost:3306/stock')

BaseModel = declarative_base()

# 获取database 的 所有table
BaseModel.metadata.reflect(engine)
tables = BaseModel.metadata.tables
# 获取所有table名称
tables_names = list(tables.keys())

df = pd.DataFrame()
# 写入名称列
df['名称'] = tables_names
# 写入代码列
df['代码'] = list(map(lambda x: x.split('(')[1].split(')')[0], tables_names))
con = engine.connect()

def map_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: Integer()})
    return dtypedict

df.to_sql(name='股票代码', con=con, if_exists='replace', index=False, dtype=map_types(df))

con.close()
