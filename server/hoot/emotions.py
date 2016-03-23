import sys
import string

# search for a concept given a certain string
def concept_search(query, start):
    f = open('concepts.txt', 'r')
    num = 0
    output = ''

    for line in f:
        if line.startswith(query):
            return (num, line.strip())

        num = num + 1

    return (-1, "NO CONCEPT")
            
# find all the concepts for a comment
def find_concepts(comment, start):
    words = comment.split()

    output = []

    for i in range(0, len(words)): 
        concept = words[i]
        last_concept = None
        print("looking at: " + concept)
        line, found_concept = concept_search(words[i], start)
        print("found concept: " + found_concept)
        j = i + 1

        if found_concept == concept:
            print('\tlast concept = ' + found_concept)
            last_concept = found_concept

        while not line == -1 and j < len(words):
            concept = concept + '_' + words[j]
            print("\tlooking at: " + concept)
            j = j + 1
            line, found_concept = concept_search(concept, line)
            print("\tfound concept: " + found_concept)
            print('\tlooking for:   ' + concept)
            if found_concept == concept:
                print('\tlast concept = ' + found_concept)
                last_concept = found_concept
        
        if last_concept != None:
            print('appending: ' + last_concept)
            output.append(last_concept)
            
    if len(output) == 0:
        return "no concepts found"
    return output

#print(concept_search(sys.argv[1], 0))
#concepts = find_concepts(" ".join(sys.argv), 2)
comment = "What has been said about the Dark Knight cannot be elaborated on - so I won't. The film is muscling its way into my #1 favorite comic movie adaptation of all time. The reason for my review is in hopes of saving you some money. This double disc Special Edition doesn't deliver the price you pay for it. There isn't even deleted scenes!!! I would save your very hard earned dollars and buy the single disc version and wait for the inevitable ULTIMATE re-release that will come later on down the road. But nonetheless, a great film - you will not be dissapointed; I just wish the studio would have given a better Special Edition release than what we have here. So enjoy!"

comment = comment.translate(string.maketrans("",""), string.punctuation)
comment = comment.lower()

concepts = find_concepts(comment, 2)
print("concepts: " + str(concepts))




