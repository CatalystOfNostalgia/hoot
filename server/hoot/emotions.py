import sys

def concept_search(query, start):
    f = open("output.txt", 'r')
    num = 0
    output = ''

    for line in f:
        if line.startswith(query):
            return (num, line.strip())

        num = num + 1

    return (-1, "NO CONCEPT")
            
def find_concepts(comment, start):
    words = comment.split()

    output = []

    for i in range(0, len(words)): 
        concept = words[i]
        print("looking at: " + concept)
        line, found_concept = concept_search(words[i], start)
        print("found concept: " + found_concept)
        j = i + 1

        while not found_concept == concept and not line == -1 and j < len(words):
            print("entered loop")
            concept = concept + words[j]
            print("looking at: " + concept)
            j = j + 1
            line, found_concept = concept_search(words[i], line)
            print("found concept: " + found_concept)
        if found_concept == concept:
            output.append(found_concept)

    if len(output) == 0:
        return "no concepts found"
    return output

concepts = find_concepts(" ".join(sys.argv), 2)
print("concepts: " + str(concepts))


