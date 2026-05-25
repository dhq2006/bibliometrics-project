import pandas as pd
import os

def calculate_missing_rate(df):
    """计算各字段缺失率"""
    missing = df.isnull().sum()
    total = len(df)
    missing_rate = (missing / total * 100).round(2)
    
    result = pd.DataFrame({
        '字段名': missing.index,
        '缺失数量': missing.values,
        '缺失率(%)': missing_rate.values
    })
    return result.sort_values('缺失率(%)', ascending=False)

def check_duplicates(df):
    """检查重复文献（基于DOI和UT）"""
    duplicate_doi = df[df.duplicated('DI', keep=False)] if 'DI' in df.columns else pd.DataFrame()
    duplicate_ut = df[df.duplicated('UT', keep=False)] if 'UT' in df.columns else pd.DataFrame()
    
    # 修复：过滤掉NaN值并转换为字符串
    duplicate_doi_list = []
    if len(duplicate_doi) > 0:
        duplicate_doi_list = [str(doi) for doi in duplicate_doi['DI'].dropna().unique()]
    
    return {
        'doi_duplicates': len(duplicate_doi),
        'ut_duplicates': len(duplicate_ut),
        'duplicate_doi_list': duplicate_doi_list
    }

if __name__ == '__main__':
    # 读取解析后的数据
    input_file = '../data/processed/raw_records.csv'
    df = pd.read_csv(input_file)
    
    # 创建输出目录
    os.makedirs('../data/processed', exist_ok=True)
    os.makedirs('../reports', exist_ok=True)
    
    # 计算缺失率
    missing_report = calculate_missing_rate(df)
    missing_report.to_csv('../data/processed/missing_rate_report.csv', index=False)
    
    # 检查重复
    duplicate_report = check_duplicates(df)
    
    # 生成Markdown报告
    with open('../reports/data_quality.md', 'w', encoding='utf-8') as f:
        f.write("# 数据质量报告\n\n")
        f.write(f"**总文献数**：{len(df)} 篇\n\n")
        
        f.write("## 1. 字段缺失率统计\n\n")
        f.write(missing_report.to_markdown(index=False))
        f.write("\n\n")
        
        f.write("## 2. 重复文献检查\n\n")
        f.write(f"- UT重复数：{duplicate_report['ut_duplicates']}\n")
        f.write(f"- DOI重复数：{duplicate_report['doi_duplicates']}\n")
        if duplicate_report['doi_duplicates'] > 0:
            f.write(f"- 重复DOI列表：{', '.join(duplicate_report['duplicate_doi_list'])}\n")
        f.write("\n")
        
        f.write("## 3. 异常值说明\n\n")
        if 'PY' in df.columns:
            f.write(f"- 年份范围：{df['PY'].min()} - {df['PY'].max()}\n")
        if 'TC' in df.columns:
            f.write(f"- 最高被引：{df['TC'].max()}\n")
            f.write(f"- 平均被引：{df['TC'].mean():.2f}\n")
        f.write("\n")
    
    print("✅ 数据质量报告已生成：reports/data_quality.md")
    print(f"📄 缺失率报告：data/processed/missing_rate_report.csv")