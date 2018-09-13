from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import plotly.offline as po
import plotly.graph_objs as go


def get_graph(search):
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

        trace = go.Candlestick(x=df['日期'],
                               open=df['开盘价'],
                               high=df['最高价'],
                               low=df['最低价'],
                               close=df['收盘价'])
        data = [trace]
        layout = {
            'title': stock_name}
        fig = dict(data=data, layout=layout)
        po.plot(fig, filename='templates/stock.html', auto_open=False)
        con.close()
        return True
    except:
        return False
