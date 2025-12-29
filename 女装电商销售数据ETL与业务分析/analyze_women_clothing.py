import pandas as pd
import numpy as np

# 加载数据
df = pd.read_csv('women_clothing_ecommerce_sales.csv')

# 基本概况查看
print("数据基本信息:")
print(df.info())
print("\n数据描述统计:")
print(df.describe())

# 查看size列的缺失情况
print("\nSize列缺失值统计:")
print(f"Size列总缺失值数量: {df['size'].isnull().sum()}")
print(f"Size列缺失值占比: {df['size'].isnull().mean():.2%}")

# 查看包含缺失值的样本
print("\n包含缺失size的样本示例:")
print(df[df['size'].isnull()].head(10))

# 缺失值填充为均码
df['size_filled'] = df['size'].fillna('One Size')

# 检查填充结果
print("\n填充后size分布:")
print(df['size_filled'].value_counts())

# 对比填充前后的差异
print("\n对比填充前后的样本:")
print(df[df['size'].isnull()][['sku','color','size','size_filled']].head())

