from src.engine.realtime_detector import RealTimeDetector
from src.data_pipeline.loader import load_dataset
from src.data_pipeline.preprocess import clean_labels, clean_data, remove_rare_classes

# Load and prepare dataset
df = load_dataset("data/raw")
df = clean_labels(df)
df = clean_data(df)
df = remove_rare_classes(df)

# Drop label to get features only
X = df.drop(columns=['Label'])

# Take ONE real sample
sample_row = X.iloc[0].to_dict()

# Initialize detector
detector = RealTimeDetector()

# Predict
result = detector.predict(sample_row)

print("\nPrediction:")
print(result)