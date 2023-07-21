# load words

WORDS = open("kata_new.txt", 'r').read().split()

def solve(chars):
    # get word that can be builded from chars or part of chars

    result = []
    for word in WORDS:
        if is_buildable(word, chars):
            result.append(word)

    return result

def is_buildable(word, chars):
    # check if word can be builded from chars or part of chars
    if len(word) > len(chars):
        return False
    for char in word:
        if char not in chars:
            return False
        else:
            chars = chars.replace(char, '', 1)

    return True

if __name__ == "__main__":
    chars = input("Enter chars: ")
    print(solve(chars))
