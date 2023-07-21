with open("kata.txt", 'r') as f:
    words = f.read().split()
    filtered_words = filter(lambda word: len(word)>=3 and "-" not in word, words)


with open("kata_new.txt", 'w') as f:
    f.write("\n".join(filtered_words))