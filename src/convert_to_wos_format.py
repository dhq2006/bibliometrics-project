import pandas as pd

df = pd.read_csv("../data/processed/final_included.csv")
out_path = "../data/processed/wos_for_citespace.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("FN Clarivate Analytics Web of Science\nVR 1.0\n")
    for _, row in df.iterrows():
        # 写入所有CiteSpace需要的核心字段
        for k in ["PT","AU","AF","TI","SO","PY","DE","ID","C1","CR","DI","UT"]:
            if pd.notna(row.get(k)):
                val = str(row[k]).strip()
                if k in ["AU","AF","CR"]:
                    # 处理多值字段（作者、参考文献）
                    for item in val.split(";"):
                        if item.strip():
                            f.write(f"{k} {item.strip()}\n")
                elif k == "PY":
                    f.write(f"PY {int(row[k])}\n")
                else:
                    f.write(f"{k} {val}\n")
        f.write("ER\n\n")

print("="*60)
print("✅ CiteSpace专用文件已生成！")
print("✅ 包含：关键词DE/ID、机构C1、参考文献CR")
print("✅ 路径：data/processed/wos_for_citespace.txt")
print("="*60)