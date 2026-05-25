import pandas as pd

if __name__ == '__main__':
    # 读取筛选结果
    df = pd.read_csv('../data/processed/screening_results.csv')
    
    # 只保留纳入的文献
    final = df[df['include'] == True]
    
    # 选择CiteSpace需要的核心列
    cols = ['UT', 'TI', 'AU', 'PY', 'SO', 'DE', 'AB', 'DI', 'TC']
    final_list = final[cols]
    
    # 保存
    output = '../data/processed/final_included.csv'
    final_list.to_csv(output, index=False, encoding='utf-8-sig')
    
    print(f'✅ Final included: {len(final_list)} papers')
    print(f'📄 Saved to: {output}')