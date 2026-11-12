import gensim
import re

def find_nearest(pos, neg):
    # vec_pos = word2vec.get_vector(pos) + word2vec.get_vector(neg)
    # vec_neg = word2vec.get_vector(pos) * -1 + word2vec.get_vector(neg) * -1
    # neg = [word2vec.most_similar(vec_neg)[0]]
    # pos = [word2vec.most_similar(vec_pos)[0]]
    dist = word2vec.most_similar(positive=pos, negative=neg, topn=10)

    pat = re.compile("(.*)_NOUN")

    for i in dist:
        e = pat.match(i[0])
        if e is not None:
            print(e.group(1))

pos = ["университет_NOUN", "аллея_NOUN"]
target = ["сад_Noun", "факультет_NOUN"]
neg = [] #['кампус_NOUN'] #["перестраховщик_NOUN"]
word2vec = gensim.models.KeyedVectors.load_word2vec_format("cbow.txt", binary=False)

find_nearest(pos, neg)
print()
