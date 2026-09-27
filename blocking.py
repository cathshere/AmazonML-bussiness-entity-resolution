import pandas as pd
import re


# ==========================================
# 1. Load data
# ==========================================

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


# ==========================================
# 2. Normalize text
# ==========================================

def normalize_text(text):

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ==========================================
# 3. Name blocking key
# ==========================================

def name_block_key(row):

    name = normalize_text(row["business_name"])

    if not name:
        return None

    first_word = name.split()[0]

    return (
        row["country"],
        first_word[:4]
    )


# ==========================================
# 4. Address tokens
# ==========================================

def address_tokens(address):

    if not isinstance(address, str):
        return []

    address = normalize_text(address)

    words = address.split()

    # Keep words with at least 4 characters
    words = [
        word for word in words
        if len(word) >= 4
    ]

    return words


# ==========================================
# 5. Build name index
# ==========================================

def build_name_index(df):

    index = {}

    for _, row in df.iterrows():

        key = name_block_key(row)

        if key is None:
            continue

        if key not in index:
            index[key] = set()

        index[key].add(row["entity_id"])

    return index


source2_name_index = build_name_index(source2)
source3_name_index = build_name_index(source3)


# ==========================================
# 6. Build address index
# ==========================================

def build_address_index(df):

    index = {}

    for _, row in df.iterrows():

        tokens = address_tokens(
            row["business_address"]
        )

        for token in tokens:

            key = (
                row["country"],
                token
            )

            if key not in index:
                index[key] = set()

            index[key].add(
                row["entity_id"]
            )

    return index


source2_address_index = build_address_index(source2)
source3_address_index = build_address_index(source3)


# ==========================================
# 7. Get candidates
# ==========================================

def get_candidates(record):

    candidates = set()

    # --------------------------------------
    # BLOCK 1: Name
    # --------------------------------------

    name_key = name_block_key(record)

    if name_key in source2_name_index:

        candidates.update(
            source2_name_index[name_key]
        )

    if name_key in source3_name_index:

        candidates.update(
            source3_name_index[name_key]
        )


    # --------------------------------------
    # BLOCK 2: Address
    # --------------------------------------

    address_words = address_tokens(
        record["business_address"]
    )

    print("\nAddress tokens and candidate counts:")

    for word in address_words:

        key = (
            record["country"],
            word
        )

        s2_count = len(
            source2_address_index.get(
                key,
                set()
            )
        )

        s3_count = len(
            source3_address_index.get(
                key,
                set()
            )
        )

        print(
            word,
            "-> Source 2:",
            s2_count,
            "Source 3:",
            s3_count,
            "Total:",
            s2_count + s3_count
        )

        # Maximum number of records
        # we allow one address token to contribute

        MAX_TOKEN_FREQUENCY = 20000


        # Source 2

        s2_matches = source2_address_index.get(
            key,
            set()
        )

        if 0 < len(s2_matches) <= MAX_TOKEN_FREQUENCY:

            candidates.update(s2_matches)


        # Source 3

        s3_matches = source3_address_index.get(
            key,
            set()
        )

        if 0 < len(s3_matches) <= MAX_TOKEN_FREQUENCY:

            candidates.update(s3_matches)


    return candidates


# ==========================================
# 8. Test with our Source 1 record
# ==========================================

target = source1[
    source1["entity_id"] == "S1-965667"
].iloc[0]


candidates = get_candidates(target)


print("\nSource 1:")
print(target)


print("\nNumber of candidates:")
print(len(candidates))


print("\nIs Dréxkor a candidate?")


target_id = "S3-775321672"


if target_id in candidates:

    print("YES - Dréxkor was found!")

else:

    print("NO - Dréxkor was NOT found!")