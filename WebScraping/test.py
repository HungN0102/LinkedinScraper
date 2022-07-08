words = ["yo", "act", "flop", "tac", "foo", "cat", "oy", "olfp"]

hashmap = {}
for word in words:
    orderedWord = "".join(sorted(word))
    if orderedWord not in hashmap:
        hashmap[orderedWord] = [word]
    else:
        hashmap[orderedWord].append(word)

list(hashmap.values())