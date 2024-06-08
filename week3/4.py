from string import punctuation
import re

def find_most_frequent_words(input:str):
    #removing punctuations and seperating words
    #input = input.translate(str.maketrans('', '', punctuation)).split()
    #or a better way
    input = re.findall(r'\b\w+\b', input)

    #counting each word
    frequency_dict = dict()
    for word in input:
        word = word.lower()
        frequency_dict[word] = 1 + frequency_dict.get(word , 0)
    #finding max frquency
    result_frequency = 0
    result_words = []
    for word, value in frequency_dict.items():
        if result_frequency < value: 
            result_frequency = value
            result_words = [word]
        elif result_frequency == value:
            result_words += [word]
    # or simpler but slower way
    # result_frequency = max(frequency_dict.values())
    # result_words = [i for i in frequency_dict if frequency_dict[i] == result_frequency]
    
    return result_words , result_frequency
    
input_paragraph = """This is a simple paragraph. It contains several words, some of 
which are repeated. This is a good exercise to find the most frequent words."""

result_words, result_frequency = find_most_frequent_words(input_paragraph)


print("most frequent word(s):", result_words)
print("frequency:", result_frequency)
