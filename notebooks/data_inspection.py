from src.data_pipeline.loader import load_dataset
from src.data_pipeline.preprocess import (
    clean_labels,
    clean_data,
    remove_rare_classes
)

def main():
    # Load data
    df = load_dataset("data/raw")

    # Clean labels
    df = clean_labels(df)

    # Clean data (NaN, Inf, duplicates)
    df = clean_data(df)

    # Remove rare classes
    df = remove_rare_classes(df)

    # Outputs
    print("\nFinal Shape:", df.shape)

    print("\nFinal Labels:")
    print(df['Label'].unique())

    print("\nFinal Distribution:")
    print(df['Label'].value_counts())


if __name__ == "__main__":
    main()