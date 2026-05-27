import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/processed/final_included.csv")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]

# 年度发文趋势图
annual = df["PY"].value_counts().sort_index()
plt.figure(figsize=(10,5))
annual.plot(marker="o", color="#2E86AB")
plt.title("Annual Publications 2020-2025")
plt.xlabel("Year")
plt.ylabel("Count")
plt.grid(alpha=0.3)
plt.savefig("../outputs/figures/annual_trend.png", dpi=300, bbox_inches="tight")
plt.close()

# Top10作者表
df["AU"].str.split("; ").explode().value_counts().head(10).to_csv("../outputs/tables/top10_authors.csv")
# Top10期刊表
df["SO"].value_counts().head(10).to_csv("../outputs/tables/top10_journals.csv")

print("✅ 图表与表格已全部生成！")