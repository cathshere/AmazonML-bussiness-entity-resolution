import os
import re
import pandas as pd

from collections import defaultdict
from rapidfuzz.fuzz import ratio, token_set_ratio


# ============================================================
# SETTINGS
# ============================================================

MAX_TOKEN_FREQUENCY = 5000

NAME_THRESHOLD = 88
ADDRESS_THRESHOLD = 88
COMBINED_THRESHOLD = 70


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokens(text):

    text = normalize(text)

    if not text:
        return []

    return [
        word
        for word in text.split()
        if len(word) >= 4
    ]


# ============================================================
# LOAD DATA
# ============================================================

print("Loading data...")

s1 = pd.read_csv(
    "dataset/test/test_source1.tsv",
    sep="\t"
)

s2 = pd.read_csv(
    "dataset/test/test_source2.tsv",
    sep="\t"
)

s3 = pd.read_csv(
    "dataset/test/test_source3.tsv",
    sep="\t"
)

print("Source 1:", len(s1))
print("Source 2:", len(s2))
print("Source 3:", len(s3))


# ============================================================
# PREPARE SOURCE 2 + SOURCE 3
# ============================================================

others = pd.concat(
    [s2, s3],
    ignore_index=True
)

others["norm_name"] = (
    others["business_name"]
    .fillna("")
    .map(normalize)
)

others["norm_address"] = (
    others["business_address"]
    .fillna("")
    .map(normalize)
)


# ============================================================
# NAME INDEX
# ============================================================

print("Building name index...")

name_index = defaultdict(list)

for idx, row in others.iterrows():

    name = row["norm_name"]

    if name:
        key = (row["country"], name)

        name_index[key].append(idx)


# ============================================================
# ADDRESS TOKEN INDEX
# ============================================================

print("Building address index...")

address_index = defaultdict(list)

for idx, row in others.iterrows():

    address = row["norm_address"]

    if not address:
        continue

    for word in set(tokens(address)):

        key = (row["country"], word)

        address_index[key].append(idx)


# ============================================================
# REMOVE VERY COMMON ADDRESS TOKENS
# ============================================================

print("Filtering common address tokens...")

useful_address_index = {}

for key, ids in address_index.items():

    if len(ids) <= MAX_TOKEN_FREQUENCY:

        useful_address_index[key] = ids


print(
    "Useful address blocks:",
    len(useful_address_index)
)


# ============================================================
# MATCH ONE SOURCE 1 RECORD
# ============================================================

def get_candidates(row):

    candidates = set()

    country = row["country"]

    name = normalize(row["business_name"])

    address = normalize(row["business_address"])


    # --------------------------------------------------------
    # BLOCK 1: EXACT NORMALIZED NAME
    # --------------------------------------------------------

    if name:

        key = (country, name)

        for idx in name_index.get(key, []):

            candidates.add(idx)


    # --------------------------------------------------------
    # BLOCK 2: RARE ADDRESS TOKENS
    # --------------------------------------------------------

    address_words = tokens(address)

    # Get token frequencies

    token_info = []

    for word in set(address_words):

        key = (country, word)

        ids = useful_address_index.get(key)

        if ids:

            token_info.append(
                (len(ids), word, ids)
            )


    # Use the rarest address tokens first

    token_info.sort(
        key=lambda x: x[0]
    )


    # Only use the 2 most informative tokens

    for _, word, ids in token_info[:2]:

        candidates.update(ids)


    return candidates


# ============================================================
# SCORE CANDIDATE
# ============================================================

def score_pair(source_record, candidate_record):

    name1 = normalize(
        source_record["business_name"]
    )

    name2 = candidate_record["norm_name"]


    address1 = normalize(
        source_record["business_address"]
    )

    address2 = candidate_record["norm_address"]


    # Name similarity

    if name1 and name2:

        name_score = token_set_ratio(
            name1,
            name2
        )

    else:

        name_score = 0


    # Address similarity

    if address1 and address2:

        address_score = token_set_ratio(
            address1,
            address2
        )

    else:

        address_score = 0


    # Country

    country_match = (
        source_record["country"]
        ==
        candidate_record["country"]
    )


    # Combined score

    if name_score == 0:

        combined = address_score

    elif address_score == 0:

        combined = name_score

    else:

        combined = (
            0.60 * name_score
            +
            0.40 * address_score
        )


    return (
        name_score,
        address_score,
        combined,
        country_match
    )


# ============================================================
# PROCESS TEST DATA
# ============================================================

print("\nStarting matching...")

matching_results = []

candidate_results = []


for counter, (_, row) in enumerate(
    s1.iterrows(),
    start=1
):

    candidates = get_candidates(row)


    matched = []

    scored_candidates = []


    for idx in candidates:

        candidate = others.iloc[idx]

        (
            name_score,
            address_score,
            combined,
            country_match
        ) = score_pair(
            row,
            candidate
        )


        scored_candidates.append(
            (
                idx,
                name_score,
                address_score,
                combined
            )
        )


    # --------------------------------------------------------
    # SAVE CANDIDATES
    # --------------------------------------------------------

    candidate_ids = [
        others.iloc[idx]["entity_id"]
        for idx, _, _, _ in scored_candidates
    ]


    candidate_results.append(
        {
            "source1_entity_id": row["entity_id"],
            "candidate_entity_ids": ",".join(
                candidate_ids
            )
        }
    )


    # --------------------------------------------------------
    # SELECT MATCHES
    # --------------------------------------------------------

    for (
        idx,
        name_score,
        address_score,
        combined
    ) in scored_candidates:

        candidate = others.iloc[idx]


        # Strong name match

        strong_name = (
            name_score >= NAME_THRESHOLD
        )


        # Strong address match

        strong_address = (
            address_score >= ADDRESS_THRESHOLD
        )


        # Combined match

        good_combined = (
            combined >= COMBINED_THRESHOLD
        )


        if (
            strong_name
            or
            (
                strong_address
                and good_combined
            )
            or
            (
                name_score >= 75
                and address_score >= 80
            )
        ):

            matched.append(
                candidate["entity_id"]
            )


    # Remove duplicates

    matched = list(
        dict.fromkeys(matched)
    )


    matching_results.append(
        {
            "source1_entity_id":
                row["entity_id"],

            "matched_entity_ids":
                ",".join(matched)
        }
    )


    if counter % 10000 == 0:

        print(
            "Processed:",
            counter,
            "/",
            len(s1)
        )


# ============================================================
# SAVE OUTPUT
# ============================================================

os.makedirs(
    "output",
    exist_ok=True
)


matching_df = pd.DataFrame(
    matching_results
)


candidate_df = pd.DataFrame(
    candidate_results
)


matching_df.to_csv(
    "output/matching_results.tsv",
    sep="\t",
    index=False
)


candidate_df.to_csv(
    "output/candidate_pairs.tsv",
    sep="\t",
    index=False
)


print("\nDONE!")

print(
    "Created:",
    "output/matching_results.tsv"
)

print(
    "Created:",
    "output/candidate_pairs.tsv"
)

print(
    "\nRows in matching_results:",
    len(matching_df)
)

print(
    "Rows in candidate_pairs:",
    len(candidate_df)
)