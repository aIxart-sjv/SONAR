from src.data_pipeline.loader import load_dataset

df = load_dataset("data/raw")

print("\nShape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nUnique Labels:")
print(df['Label'].unique())

print("\nClass Distribution:")
print(df['Label'].value_counts())