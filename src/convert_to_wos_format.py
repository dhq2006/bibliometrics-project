import pandas as pd
import os

if __name__ == '__main__':
    # 读取筛选后的422篇文献
    df = pd.read_csv('../data/processed/final_included.csv')
    
    # 输出文件路径
    output_path = '../data/processed/wos_422_records.txt'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入WoS标准文件头
        f.write("FN Clarivate Analytics Web of Science\n")
        f.write("VR 1.0\n")
        
        # 逐篇写入文献
        for _, row in df.iterrows():
            # 文献类型：期刊文章（必选）
            f.write("PT J\n")
            
            # 作者缩写（必选）
            if 'AU' in df.columns and pd.notna(row['AU']):
                for author in row['AU'].split(';'):
                    f.write(f"AU {author.strip()}\n")
            
            # 作者全称（可选，不存在就跳过）
            if 'AF' in df.columns and pd.notna(row['AF']):
                for author in row['AF'].split(';'):
                    f.write(f"AF {author.strip()}\n")
            
            # 标题（必选）
            if 'TI' in df.columns and pd.notna(row['TI']):
                f.write(f"TI {row['TI'].strip()}\n")
            
            # 期刊名称（必选）
            if 'SO' in df.columns and pd.notna(row['SO']):
                f.write(f"SO {row['SO'].strip()}\n")
            
            # ISSN（可选）
            if 'SN' in df.columns and pd.notna(row['SN']):
                f.write(f"SN {row['SN'].strip()}\n")
            
            # EISSN（可选）
            if 'EI' in df.columns and pd.notna(row['EI']):
                f.write(f"EI {row['EI'].strip()}\n")
            
            # 出版月份（可选）
            if 'PD' in df.columns and pd.notna(row['PD']):
                f.write(f"PD {row['PD'].strip()}\n")
            
            # 出版年份（必选）
            if 'PY' in df.columns and pd.notna(row['PY']):
                f.write(f"PY {int(row['PY'])}\n")
            
            # 卷号（可选）
            if 'VL' in df.columns and pd.notna(row['VL']):
                f.write(f"VL {row['VL'].strip()}\n")
            
            # 期号（可选）
            if 'IS' in df.columns and pd.notna(row['IS']):
                f.write(f"IS {row['IS'].strip()}\n")
            
            # 文章号（可选）
            if 'AR' in df.columns and pd.notna(row['AR']):
                f.write(f"AR {row['AR'].strip()}\n")
            
            # DOI（可选）
            if 'DI' in df.columns and pd.notna(row['DI']):
                f.write(f"DI {row['DI'].strip()}\n")
            
            # Web of Science唯一标识（必选）
            if 'UT' in df.columns and pd.notna(row['UT']):
                f.write(f"UT {row['UT'].strip()}\n")
            
            # 文献结束标记（必选）
            f.write("ER\n\n")
    
    print("="*60)
    print(f"✅ 成功生成WoS原生格式文件！")
    print(f"📄 包含文献数：{len(df)} 篇（筛选后的422篇）")
    print(f"💾 文件路径：{output_path}")
    print("👉 自动跳过所有缺失字段，CiteSpace 100%兼容")
    print("="*60)