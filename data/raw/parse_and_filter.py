import re
import csv
from collections import defaultdict
import os

def parse_wos_file(file_path):
    """解析Web of Science导出的纯文本格式文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按文献分割（每篇文献以PT开头，ER结尾）
    records = re.split(r'^ER\n', content, flags=re.M)
    parsed_records = []
    
    for record in records:
        if not record.strip():
            continue
        
        data = defaultdict(str)
        current_field = None
        current_value = []
        
        for line in record.split('\n'):
            line = line.rstrip('\n')
            if not line.strip():
                continue
            
            # 识别字段（WoS格式：前两个字符是字段码，后跟空格）
            # 修复：访问line[2]需要长度至少为3
            if len(line) >= 3 and line[2] == ' ':
                if current_field:
                    data[current_field] = ' '.join(current_value).strip()
                
                current_field = line[:2].strip()
                current_value = [line[3:].strip()]
            else:
                # 多行字段的续行
                current_value.append(line.strip())
        
        if current_field:
            data[current_field] = ' '.join(current_value).strip()
        
        # 只保留有UT编号的有效文献
        if 'UT' in data and data['UT'].startswith('WOS:'):
            parsed_records.append(dict(data))
    
    return parsed_records

def save_to_csv(records, output_path):
    """将解析结果保存为CSV文件"""
    if not records:
        print("没有解析到有效文献")
        return
    
    # 创建输出目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 获取所有出现过的字段
    all_fields = set()
    for record in records:
        all_fields.update(record.keys())
    
    # 按常用字段排序
    field_order = ['UT', 'TI', 'AU', 'AF', 'SO', 'PY', 'AB', 'DE', 'ID', 'CR', 'DI', 'C1', 'RP', 'TC', 'Z9']
    fields = field_order + [f for f in sorted(all_fields) if f not in field_order]
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

if __name__ == '__main__':
    # 输入输出路径
    input_file = 'savedrecs.txt'
    output_file = '../processed/raw_records.csv'
    
    # 解析并保存
    records = parse_wos_file(input_file)
    save_to_csv(records, output_file)
    
    # 输出统计信息（关键检查）
    print(f"✅ 成功解析 {len(records)} 篇文献")
    print(f"📄 输出文件：{output_file}")