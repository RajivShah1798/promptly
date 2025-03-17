import pandas as pd

df = pd.read_csv("data/user_queries_with_embeddings.csv")

# Check first few rows
print(df.head())

# Check embedding type
print("\nData type of 'embedding' column:", type(df["embedding"][0]))