from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd


def get_stock_data(search):
    try:
        # 创建基础类
        engine = create_engine('mysql+pymysql://ffzs:666@localhost:3306/stock')
        BaseModel = declarative_base()
        # 初始话数据库记过，与数据库连接
        BaseModel.metadata.create_all(engine)
        # 实例化一个会话，之后通过session进行操作
        con = engine.connect()
        df_stock_name = pd.read_sql("select 名称 from `股票代码` where 代码={}".format(search), con=con)
        stock_name = df_stock_name.values[0][0]
        df = pd.read_sql('select *  from `{}`'.format(stock_name), con=con)
        # 不需要成交量 删除掉
        df.drop(columns=['成交量'], inplace=True)
        df['日期'] = df['日期'].astype('str')
        header = [["<b>{}</b>".format(i)] for i in df.columns.tolist()]
        data = df.T.values.tolist()
        con.close()
        return data, stock_name, header
    except:
        return False, False


# data = get_stock_data('000555')
#