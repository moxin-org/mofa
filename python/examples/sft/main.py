import pandas as pd

# 读取 Parquet 文件
df = pd.read_parquet('0000.parquet')
head_data = df.head(10).to_dict(orient='records')
# 显示前几行数据
print(df.head())
