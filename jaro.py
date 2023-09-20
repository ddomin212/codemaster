import jellyfish


def get_duplicates_simple(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines if x.strip()]
    unique_lines = list(set(lines))
    ndup = len(lines) - len(unique_lines)
    print("Found {} duplicates in {} lines.".format(ndup, len(lines)))


def get_duplicates_jaro(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = [(x.strip(), ln + 1) for ln, x in enumerate(lines) if x.strip()]
    jaro_similarities = []
    for i in range(len(lines)):
        for j in range(i):
            if i != j:
                jaro = jellyfish.jaro_similarity(lines[i][0], lines[j][0])
                jaro_similarities.append((lines[i][1], lines[j][1], jaro))
    jaro_similarities = sorted(
        jaro_similarities, key=lambda x: x[2], reverse=True
    )
    for i in jaro_similarities:
        if i[2] == 1.0:
            print(f"Verified duplicate lines: {i[0]} and {i[1]}")
        elif i[2] > 0.9:
            print(f"Possibly duplicate lines: {i[0]} and {i[1]}")


if __name__ == "__main__":
    get_duplicates_jaro("duplicates.txt")
