import pandas as pd
import os

if __name__ == '__main__':
    # 读取最终纳入文献
    df = pd.read_csv('../data/processed/final_included.csv')
    
    # 重命名列为CiteSpace标准列名
    df_cite = df.rename(columns={
        'UT': 'UT',
        'TI': 'TI',
        'AU': 'AU',
        'PY': 'PY',
        'SO': 'SO',
        'DE': 'DE',
        'AB': 'AB',
        'DI': 'DI'
    })
    
    # 只保留CiteSpace需要的列
    cols = ['UT', 'TI', 'AU', 'PY', 'SO', 'DE', 'AB', 'DI']
    df_cite = df_cite[cols]
    
    # 用UTF-8编码保存
    output = '../data/processed/citespace_import.csv'
    df_cite.to_csv(output, index=False, encoding='utf-8')
    
    print(f"✅ CiteSpace专用文件已生成：{output}")
    print(f"📄 包含 {len(df_cite)} 篇文献")
    print("👉 现在下载这个文件导入CiteSpace即可")