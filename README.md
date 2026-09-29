# 🔎 Business Entity Resolution

> **Same business. Different data. One identity.**

A scalable business entity resolution pipeline that identifies records representing the same real-world business across multiple data sources, even when business names, addresses, and other attributes contain inconsistencies.

---

##  Introduction

Business information collected from different sources is rarely consistent.

The same business may appear with:

- Different spellings
- Different capitalization
- Different punctuation
- Abbreviations
- Missing information
- Incomplete addresses
- Typographical errors
- Different formatting

## Similarity Features

Candidate records can be compared using multiple signals.

1. Business Name Similarity

Possible techniques include:

Levenshtein similarity
Jaccard similarity
Token similarity
TF-IDF similarity2


2. Address Similarity

Addresses can differ in:

Abbreviations
Spelling
Word order
Missing components
Formatting

3. Country Consistency

Country can provide an additional matching signal.

For example:

US → US

provides consistency, while a country mismatch may indicate that two records are less likely to represent the same business.

4. Entity Matching

After candidate generation, the system evaluates the candidate pairs using their similarity features.

Conceptually:

Candidate Pair
      │
      ├── Name similarity
      ├── Address similarity
      ├── Country consistency
      └── Other features
             │
             ▼
       Matching Decision

The goal is to distinguish:

Same real-world entity

from:

Different entities

# 📤 Outputs

The pipeline produces two major types of output.

## Candidate Pairs

### `candidate_pairs.tsv`

Contains the possible matches generated during the blocking stage.

Example:

```text
source1_entity_id    candidate_entity_ids

S1-00001             S2-00047,S2-00193,S3-00812
S1-00002             S3-00004

Final Matching Results
matching_results.tsv

Contains the final predicted entity matches.

Example:

source1_entity_id    matched_entity_ids

S1-00001             S2-00047,S3-00812

The final matches are selected from the candidate set generated during the blocking stage.

```
## Dataset

The project works with three business sources.

Training Data
dataset/
└── train/
    ├── train_source1.tsv
    ├── train_source2.tsv
    ├── train_source3.tsv
    └── train_ground_truth.tsv
Test Data
dataset/
└── test/
    ├── test_source1.tsv
    ├── test_source2.tsv
    └── test_source3.tsv

The train_ground_truth.tsv file contains known relationships between Source 1 entities and their corresponding Source 2 and Source 3 entities.

The dataset is intentionally excluded from this repository because of its size.

## Tech Stack
  Technology	Purpose
  Python	Core implementation
  Pandas	Data loading and processing
  Regular Expressions	Text normalization
  RapidFuzz	Fuzzy string matching
  Git	Version control
  GitHub	Repository hosting and collaboration
  Core Concepts
  Entity Resolution
  Record Linkage
  Data Cleaning
  Text Normalization
  Blocking
  Candidate Generation
  Fuzzy Matching
  Similarity Features
  Large-Scale Data Processing

  
## Project Structure

  AmazonML-bussiness-entity-resolution/
  │
  ├── README.md
  ├── requirements.txt
  │
  ├── final_baseline.py
  ├── blocking.py
  ├── preprocessing.py
  ├── match_features.py
  ├── name_sim.py
  ├── address_sim.py
  │
  ├── inspect_matches.py
  ├── test_data.py
  │
  ├── output/
  │   └── generated results
  │
  └── dataset/
      └── excluded from Git



### Conclusion

This project turns **messy, inconsistent business records into reliable entity matches** using scalable blocking and similarity-based matching—laying the foundation for robust real-world entity resolution.
