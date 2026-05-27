import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('../data/processed/final_included.csv')
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 1. 年度发文趋势图
    plt.figure(figsize=(10, 6))
    annual_counts = df['PY'].value_counts().sort_index()
    plt.plot(annual_counts.index, annual_counts.values, marker='o', linewidth=2, color='#1f77b4')
    plt.title('AIGC在人文社科领域的年度发文趋势 (2020-2025)', fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('发文量', fontsize=12)
    plt.grid(alpha=0.3)
    plt.savefig('../outputs/figures/annual_publications.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ 年度发文趋势图已生成")
    
    # 2. Top10作者表
    top_authors = df['AU'].str.split('; ').explode().value_counts().head(10)
    top_authors.to_csv('../outputs/tables/top_authors.csv', header=['发文量'])
    print("✅ Top10作者表已生成")
    
    # 3. Top10期刊表
    top_journals = df['SO'].value_counts().head(10)
    top_journals.to_csv('../outputs/tables/top_journals.csv', header=['发文量'])
    print("✅ Top10期刊表已生成")
    
    print("\n🎉 所有统计图表生成完成！")
