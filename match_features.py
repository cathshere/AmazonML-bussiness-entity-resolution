from difflib import SequenceMatcher
import pandas as pd

def text_similarity(text1, text2):

    if not isinstance(text1, str):
        return 0.0

    if not isinstance(text2, str):
        return 0.0

    return SequenceMatcher(
        None,
        text1.lower(),
        text2.lower()
    ).ratio()


def create_features(record1, record2):

    name_score = text_similarity(
        record1["business_name"],
        record2["business_name"]
    )

    address_score = text_similarity(
        record1["business_address"],
        record2["business_address"]
    )

    country_match = int(
        record1["country"] == record2["country"]
    )

    return {
        "name_similarity": name_score,
        "address_similarity": address_score,
        "country_match": country_match
    }


source1 = pd.read_csv(
    "dataset/train/train_source1.tsv",
    sep="\t"
)

source2 = pd.read_csv(
    "dataset/train/train_source2.tsv",
    sep="\t"
)


# Get our Source 1 record
record1 = source1[
    source1["entity_id"] == "S1-965667"
].iloc[0]


# Get one of its known matching Source 2 records
record2 = source2[
    source2["entity_id"] == "S2-681193310"
].iloc[0]


print("SOURCE 1")
print(record1)

print("\nSOURCE 2")
print(record2)

print("\nFEATURES")
print(create_features(record1, record2))