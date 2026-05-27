import re
import pandas as pd

def parse_wos_file(file_path):
    """解析WoS纯文本全记录文件，支持所有字段"""
    records = []
    current_record = {}
    current_field = None
    current_value = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.rstrip('\n')
            
            # 跳过文件头
            if line.startswith('FN ') or line.startswith('VR '):
                continue
            
            # 记录结束
            if line == 'ER':
                if current_record:
                    records.append(current_record)
                current_record = {}
                current_field = None
                current_value = []
                continue
            
            # 新字段开始
            if re.match(r'^[A-Z0-9]{2} ', line):
                if current_field:
                    current_record[current_field] = ' '.join(current_value).strip()
                current_field = line[:2]
                current_value = [line[3:].strip()]
            else:
                # 多行字段继续
                current_value.append(line.strip())
        
        # 处理最后一条记录
        if current_record:
            records.append(current_record)
    
    return pd.DataFrame(records)

if __name__ == '__main__':
    input_file = '../data/raw/savedrecs_full.txt'
    print(f"🔍 正在解析原始WoS数据: {input_file}")
    
    df = parse_wos_file(input_file)
    print(f"✅ 解析完成，总记录数: {len(df)}")
    
    # 筛选2020-2025年的期刊文章
    df['PY'] = pd.to_numeric(df['PY'], errors='coerce')
    df_filtered = df[
        (df['PT'] == 'J') & 
        (df['PY'] >= 2020) & 
        (df['PY'] <= 2025)
    ].copy()
    
    print(f"✅ 筛选完成，保留2020-2025年期刊文章: {len(df_filtered)} 篇")
    
    # 保存筛选后的数据
    output_file = '../data/processed/final_included.csv'
    df_filtered.to_csv(output_file, index=False, encoding='utf-8')
    print(f"💾 筛选后的数据已保存到: {output_file}")
    
    # 打印基本统计
    print("\n📊 基本统计信息:")
    print(f"  时间范围: {int(df_filtered['PY'].min())} - {int(df_filtered['PY'].max())}")
    print(f"  期刊数量: {df_filtered['SO'].nunique()}")
    print(f"  作者数量: {df_filtered['AU'].str.split('; ').explode().nunique()}")
