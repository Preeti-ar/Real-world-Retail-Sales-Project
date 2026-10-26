from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "retail_sales.csv")
df["date"] = pd.to_datetime(df["date"])

df = df.drop_duplicates()
df = df.dropna()

df["revenue"] = df["units_sold"] * df["unit_price"]
df["profit"] = df["units_sold"] * (
    df["unit_price"] - df["unit_cost"]
)

print("RETAIL SALES ANALYSIS")
print("Total Revenue:", df["revenue"].sum())
print("Total Profit:", df["profit"].sum())

print("\nSales by Category:")
print(df.groupby("category")["revenue"].sum())

print("\nProfit by Region:")
print(df.groupby("region")["profit"].sum())

print("\nTop Products:")
print(df.groupby("product")["revenue"].sum()
      .sort_values(ascending=False))

df.to_csv(OUT / "analyzed_sales.csv", index=False)

df.groupby("category")["revenue"].sum().plot(
    kind="bar", title="Revenue by Category"
)
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUT / "revenue_by_category.png")
plt.close()

df.groupby("region")["profit"].sum().plot(
    kind="bar", title="Profit by Region"
)
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig(OUT / "profit_by_region.png")
plt.close()

df.groupby("date")["revenue"].sum().plot(
    kind="line", marker="o", title="Daily Sales Revenue"
)
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUT / "daily_sales.png")
plt.close()

print("\nAnalysis complete. Check the outputs folder.")
