# load words
import random
WORDS = open("kata_new.txt", 'r').read().split()

def solve(chars):
    # get word that can be builded from chars or part of chars

    result = []
    for word in WORDS:
        if is_buildable(word, chars):
            result.append(word)

    # shuffle
    random.shuffle(result)
    result = arrange_strings_by_length(result)
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

def arrange_strings_by_length(strings):
    # Separate the strings based on their lengths using a dictionary
    strings_by_length = {}
    for string in strings:
        length = len(string)
        if length in strings_by_length:
            strings_by_length[length].append(string)
        else:
            strings_by_length[length] = [string]

    # Sort each group of strings with the same length

    # Combine the sorted groups back into a single list
    arranged_list = []

    # get keys
    keys = list(strings_by_length.keys())
    keys.sort(reverse=True)

    i = 0
    # while strings_by_length is not empty
    while len(keys) > 0:
        # get the first key
        key = keys[i%len(keys)]
        # get the first value of the key
        value = strings_by_length[key][0]
        # add the value to the arranged list
        arranged_list.append(value)
        # remove the value from the dictionary
        strings_by_length[key].remove(value)
        # if the value is empty
        if len(strings_by_length[key]) == 0:
            # remove the key
            keys.remove(key)
        # else
        else:
            # sort the value
            strings_by_length[key].sort()
        
        i += 1
    
    return arranged_list
if __name__ == "__main__":
    chars = input("Enter chars: ")
    print(solve(chars))
