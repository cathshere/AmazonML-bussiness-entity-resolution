import pandas as pd

# Load the files
source1 = pd.read_csv(
    "dataset/train/train_source1.tsv",
    sep="\t"
)

source2 = pd.read_csv(
    "dataset/train/train_source2.tsv",
    sep="\t"
)

source3 = pd.read_csv(
    "dataset/train/train_source3.tsv",
    sep="\t"
)

ground_truth = pd.read_csv(
    "dataset/train/train_ground_truth.tsv",
    sep="\t"
)


# Take the first Source 1 business from ground truth
s1_id = ground_truth.iloc[0]["source1_entity_id"]
print("\nOriginal Source 1 business:")

s1_row = source1[source1["entity_id"] == s1_id]

print(s1_row.to_string(index=False))

print("Source 1 ID:", s1_id)


# Convert the comma-separated IDs into a Python list
matched_ids = ground_truth.iloc[0]["matched_entity_ids"]

matched_ids = matched_ids.split(",")

print("\nActual matching businesses:\n")

# Check each matched ID
for entity_id in matched_ids:

    if entity_id.startswith("S2-"):
        row = source2[source2["entity_id"] == entity_id]

    elif entity_id.startswith("S3-"):
        row = source3[source3["entity_id"] == entity_id]

    else:
        continue

    print(row.to_string(index=False))
    print("-" * 80)