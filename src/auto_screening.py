import pandas as pd
import os
from datetime import date

def screen_papers(df):
    # 定义排除规则
    exclude = {
        'E1': {
            'terms': ['cancer', 'tumor', 'diagnosis', 'treatment', 'medical', 'hospital', 'patient', 'disease', 'biology', 'gene', 'cell', 'neural', 'brain', 'heart', 'liver', 'kidney', 'skin', 'pharmacy', 'vaccine', 'virus', 'bacteria'],
            'except': ['humanities', 'education']
        },
        'E2': {
            'terms': ['chip', 'semiconductor', 'circuit', 'robot', 'autonomous', 'industry', 'manufacturing', 'code', 'programming', 'algorithm', 'optimization', 'training', 'inference', 'cloud', 'server', 'network', 'communication', '5g', '6g', 'iot', 'blockchain', 'encryption', 'security'],
            'except': ['design', 'art']
        },
        'E3': {
            'terms': ['economy', 'finance', 'stock', 'market', 'marketing', 'advertising', 'business', 'enterprise', 'management', 'hr', 'supply chain', 'logistics', 'investment', 'bank', 'insurance', 'accounting', 'audit'],
            'except': ['journalism', 'writing']
        },
        'E4': {
            'terms': ['philosophy', 'ethics', 'morality', 'law', 'politics', 'society', 'psychology', 'sociology', 'anthropology', 'history', 'literature', 'art', 'music', 'film', 'game'],
            'except': ['aigc', 'generative ai', 'large language model', 'chatgpt', 'gpt']
        }
    }

    # 添加筛选列
    df['include'] = True
    df['reason_code'] = ''
    df['reason_detail'] = ''
    df['screener'] = '董恒清' 
    df['screen_date'] = date.today().strftime('%Y-%m-%d')
    df['stage'] = 'initial'

    # 逐篇筛选
    for i, row in df.iterrows():
        title = str(row['TI']).lower() if pd.notna(row['TI']) else ''
        
        # 检查排除规则
        for code, rule in exclude.items():
            has_term = any(t in title for t in rule['terms'])
            has_exception = any(e in title for e in rule['except'])
            
            if has_term and not has_exception:
                df.at[i, 'include'] = False
                df.at[i, 'reason_code'] = code
                df.at[i, 'reason_detail'] = f'Excluded by {code} rule'
                break

    return df

if __name__ == '__main__':
    # 读取数据
    input_path = '../data/processed/raw_records.csv'
    df = pd.read_csv(input_path)
    
    # 执行筛选
    print('Screening papers...')
    result = screen_papers(df)
    
    # 统计结果
    total = len(result)
    included = len(result[result['include'] == True])
    excluded = total - included
    
    # 保存结果
    output_path = '../data/processed/screening_results.csv'
    result.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    # 输出统计
    print(f'Total: {total}')
    print(f'Included: {included}')
    print(f'Excluded: {excluded}')
    print(f'Saved to {output_path}')
    
    # 按原因统计
    print('\nExclusion reasons:')
    counts = result[result['include'] == False]['reason_code'].value_counts()
    for code, cnt in counts.items():
        print(f'{code}: {cnt}')