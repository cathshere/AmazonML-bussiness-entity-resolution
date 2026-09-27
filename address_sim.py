from difflib import SequenceMatcher


def similarity(address1, address2):
    # Handle missing addresses
    if not isinstance(address1, str):
        return 0.0

    if not isinstance(address2, str):
        return 0.0

    return SequenceMatcher(
        None,
        address1.lower(),
        address2.lower()
    ).ratio()


address1 = "85 Wayne Avenue, Ticonderoga, NY"

address2 = "85 Wanye Avenue, Ticonderoga Townshiip, New York"

score = similarity(address1, address2)

print("Address 1:", address1)
print("Address 2:", address2)
print("Similarity:", score)