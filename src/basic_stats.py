import pandas as pd
import matplotlib.pyplot as plt
import os

if __name__ == '__main__':
    # 读取最终纳入文献
    df = pd.read_csv('../data/processed/final_included.csv')
    
    # 创建输出目录
    os.makedirs('../outputs/tables', exist_ok=True)
    os.makedirs('../outputs/figures', exist_ok=True)
    
    # 1. 年度发文趋势
    yearly = df['PY'].value_counts().sort_index()
    yearly.to_csv('../outputs/tables/yearly_trend.csv')
    
    # 绘制趋势图
    plt.figure(figsize=(10, 6))
    yearly.plot(kind='bar', color='#1f77b4')
    plt.title('Annual Publication Trend (2020-2025)')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('../outputs/figures/yearly_trend.png', dpi=300)
    plt.close()
    
    # 2. Top 10作者
    authors = []
    for _, row in df.iterrows():
        if pd.notna(row['AU']):
            for a in row['AU'].split(';'):
                authors.append(a.strip())
    top_authors = pd.Series(authors).value_counts().head(10)
    top_authors.to_csv('../outputs/tables/top_authors.csv')
    
    # 3. Top 10期刊
    top_journals = df['SO'].value_counts().head(10)
    top_journals.to_csv('../outputs/tables/top_journals.csv')
    
    # 4. 被引统计
    print(f"✅ 总文献数：{len(df)}")
    print(f"📅 年份范围：{df['PY'].min()} - {df['PY'].max()}")
    print(f"📊 最高被引：{df['TC'].max()}")
    print(f"📈 平均被引：{df['TC'].mean():.2f}")
    print(f"📄 年度趋势图已保存：outputs/figures/yearly_trend.png")
    print(f"📋 Top作者和期刊已保存：outputs/tables/")