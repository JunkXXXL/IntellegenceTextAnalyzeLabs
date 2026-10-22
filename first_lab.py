import pymorphy3 as p
import re


analyser = p.MorphAnalyzer()

with open("Murat.txt", 'r') as fl:
    text = " ".join(fl.readlines()).replace('\n', '').replace('(', '').replace(')', '').replace('«', '').replace('»', '').replace(",","")

segmented_text = re.split(r'[.?\n]+', text)

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')

tokenized_segmented_text = [word_tokenize(segment) for segment in segmented_text]

first_condition = []


def combine_nearest_words(sentence, word_index):
    sentence_len = len(sentence)

    def combine_next_word():
        if word_index + 1 >= sentence_len:
            return None
        else:
            return analyser.parse(sentence[word_index])[0].normal_form + " " + analyser.parse(sentence[word_index + 1])[
                0].normal_form

    def combine_prev_word():
        if word_index - 1 < 0:
            return None
        else:
            return sentence[word_index - 1] + " " + sentence[word_index]

    combine = []
    if not combine_next_word() is None:
        combine.append(combine_next_word())
    if not combine_prev_word() is None:
        combine.append(combine_prev_word())

    return combine


for sentence in tokenized_segmented_text:

    for element_index, word in enumerate(sentence):
        term = analyser.parse(word)[0].tag.POS
        if term == "NOUN" or term == "ADJF" or term == "ADJS":
            words_combine = combine_nearest_words(sentence, element_index)
            first_condition.extend(words_combine)

second_condition = []

for sentence in tokenized_segmented_text:

    len_sentence = len(sentence)
    for element_index in range(len_sentence-1):
        term1 = analyser.parse(sentence[element_index])[0].tag
        term2 = analyser.parse(sentence[element_index + 1])[0].tag
        if (
            term1.gender == term2.gender
            and term1.number == term2.number
            and term1.case == term2.case
            and term1.number is not None
            and term1.case is not None
        ):
            second_condition.append(analyser.parse(sentence[element_index])[0].normal_form + " " + analyser.parse(sentence[element_index + 1])[0].normal_form)

#NOun существит
#ADJF ADJS прилагательное полное и краткое

print(first_condition)
print(second_condition)
