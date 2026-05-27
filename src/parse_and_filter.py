import re
import pandas as pd

def parse_wos_full(filepath):
    records = []
    rec = {}
    current_key = None
    current_val = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('FN') or line.startswith('VR'):
                continue
            if line == 'ER':
                if current_key:
                    rec[current_key] = ' '.join(current_val).strip()
                if rec:
                    records.append(rec)
                rec = {}
                current_key = None
                current_val = []
                continue
            match = re.match(r'^([A-Z0-9]{2}) (.*)', line)
            if match:
                if current_key:
                    rec[current_key] = ' '.join(current_val).strip()
                current_key = match.group(1)
                current_val = [match.group(2).strip()]
            else:
                if current_key:
                    current_val.append(line.strip())
    return pd.DataFrame(records)

if __name__ == "__main__":
    df = parse_wos_full("../data/raw/savedrecs_full.txt")
    df["PY"] = pd.to_numeric(df["PY"], errors="coerce")
    df = df[(df["PT"] == "J") & (df["PY"] >= 2020) & (df["PY"] <= 2025)].copy()
    df.to_csv("../data/processed/final_included.csv", index=False, encoding="utf-8")
    print(f"✅ 筛选完成：共 {len(df)} 篇文献")
    print(f"✅ 已保存到 data/processed/final_included.csv")