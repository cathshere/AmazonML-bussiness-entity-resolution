from difflib import SequenceMatcher


def similarity(name1, name2):
    return SequenceMatcher(
        None,
        name1,
        name2
    ).ratio()


name1 = "Maure Williams Colombier Inc"
name2 = "Maure Wilblims Colombier Inc"

score = similarity(name1, name2)

print("Name 1:", name1)
print("Name 2:", name2)
print("Similarity:", score)