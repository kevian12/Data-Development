import pandas as pd
from sqlalchemy import create_engine
import pymysql
from datetime import datetime

df = pd.read_csv('women_clothing_ecommerce_sales.csv')

# 确保处理了缺失值和日期格式
df['order_date'] = pd.to_datetime(df['order_date'])
df['size'] = df['size'].fillna('One Size')  # 填充缺失值


# 2. 创建数据库连接
def create_db_connection():
    try:
        # 格式：mysql+pymysql://user:password@host:port/database
        engine = create_engine(
            'mysql+pymysql://zyx:123456@localhost:3306/ecommerce_db',
            echo=False  # 设置为True可查看SQL日志
        )
        print("✓ 数据库连接成功")
        return engine
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return None


# 3. 导入数据函数
def df_to_mysql(df, table_name, engine):
    try:
        # 将NaN转换为None（MySQL兼容）
        df = df.where(pd.notnull(df), None)

        # 导入到MySQL
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',  # 选项: 'fail', 'replace', 'append'
            index=False,  # 不导入DataFrame索引
            chunksize=1000,  # 分批导入，大文件时重要
            method='multi'  # 批量插入，提升性能
        )
        print(f"✓ 数据导入成功！共导入 {len(df)} 条记录")

        # 验证导入结果
        with engine.connect() as conn:
            result = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = result.fetchone()[0]
            print(f"✓ 表中总记录数: {count}")

    except Exception as e:
        print(f"✗ 导入失败: {e}")


# 4. 执行导入
if __name__ == "__main__":
    # 创建连接
    engine = create_db_connection()

    if engine:
        # 执行导入
        df_to_mysql(df, 'women_clothing_sales', engine)

        # 关闭连接
        engine.dispose()



