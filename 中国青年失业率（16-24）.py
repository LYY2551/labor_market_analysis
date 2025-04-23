import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(current_dir, "data")
GDP_PATH = os.path.join(DATA_DIR, "China_GDP.csv")
UNEMP_PATH = os.path.join(DATA_DIR, "中国16-24岁的失业率.csv")
OUTPUT_PATH = os.path.join(current_dir, "output", "中国青年失业率合理数据_2000-2023.csv")


def safe_read_csv(path):
    """智能编码读取"""
    encodings = ['utf-8-sig', 'gb18030', 'gbk']
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            print(f"成功读取 {path} (编码: {enc})")
            return df
        except: continue
    raise ValueError("无法解码文件")

def process_data():
    gdp = safe_read_csv(GDP_PATH)
    gdp = gdp.dropna(subset=['Year'])
    gdp['Year'] = gdp['Year'].str.replace(r'\D', '', regex=True).astype(int)
    gdp['GDP_growth'] = gdp['china_GDP'].pct_change() * 100  # 年增长率百分比
    
    full_years = pd.DataFrame({'Year': range(2000, 2024)})
    gdp = pd.merge(full_years, gdp, on='Year', how='left')

    unemp = safe_read_csv(UNEMP_PATH)
    unemp['Year'] = unemp['Year'].str.extract(r'(\d{4})').astype(int)
    unemp = unemp.groupby('Year')['Unemployment Rate (Youth)'].mean().reset_index()
    
    merged = pd.merge(gdp, unemp, on='Year', how='outer').sort_values('Year')
    
    merged['china_GDP'] = -merged['china_GDP']
    
    scaler = StandardScaler()
    features = scaler.fit_transform(merged[['china_GDP', 'GDP_growth']].fillna(0))
    
    train_data = merged[merged['Year'] >= 2018].dropna()
    if len(train_data) >= 3:
        model = LinearRegression()
        model.fit(features[train_data.index], train_data['Unemployment Rate (Youth)'])
        
        missing = merged['Unemployment Rate (Youth)'].isna()
        pred = model.predict(features[missing])
        merged.loc[missing, 'Unemployment Rate (Youth)'] = pred.clip(8, 25)  # 合理区间
    
    merged['Unemployment Rate (Youth)'] = merged['Unemployment Rate (Youth)'] \
        .interpolate(method='linear') \
        .ffill() \
        .bfill() \
        .round(1)
    
    return merged[['Year', 'Unemployment Rate (Youth)']].rename(columns={
        'Year': '年份',
        'Unemployment Rate (Youth)': '青年失业率(%)'
    })

result = process_data()
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)  # 确保输出目录存在
result.to_csv(OUTPUT_PATH, index=False, encoding='gb18030')

