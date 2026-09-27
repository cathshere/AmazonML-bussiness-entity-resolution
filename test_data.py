import pandas as pd

# Load all training files
source1 = pd.read_csv("dataset/train/train_source1.tsv", sep="\t")
source2 = pd.read_csv("dataset/train/train_source2.tsv", sep="\t")
source3 = pd.read_csv("dataset/train/train_source3.tsv", sep="\t")
ground_truth = pd.read_csv("dataset/train/train_ground_truth.tsv", sep="\t")


# Show basic information
print("\n===== SOURCE 1 =====")
print(source1.head())
print(source1.shape)

print("\n===== SOURCE 2 =====")
print(source2.head())
print(source2.shape)

print("\n===== SOURCE 3 =====")
print(source3.head())
print(source3.shape)

print("\n===== GROUND TRUTH =====")
print(ground_truth.head())

print(ground_truth.shape)

print("\n===== COLUMN NAMES =====")
print("Source 1:", source1.columns.tolist())
print("Source 2:", source2.columns.tolist())
print("Source 3:", source3.columns.tolist())
print("Ground Truth:", ground_truth.columns.tolist())