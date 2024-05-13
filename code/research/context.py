import re

from gensim.models import KeyedVectors

GOOGLE_WORD2VEC_PATH = '../data/GoogleNews-vectors-negative300.bin'
GERMAN_WORD2VEC_PATH = '../data/german.model'


def get_similar_sentence(word, n=5):
    model = KeyedVectors.load_word2vec_format(GERMAN_WORD2VEC_PATH, binary=False)
    # similar_words = model.most_similar(positive=[word], topn=2, )
    # print(similar_words)
    similar_words = [word]
    output_sentences = []

    corpus = model.corpus  # This is a list of sentences used to train the model

    sentences = []
    for sentence in corpus:
        if re.search(r'\b' + word + r'\b', sentence, re.IGNORECASE):
            sentences.append(sentence)
            if len(sentences) >= n:
                break
    return sentences



if __name__ == '__main__':
    word = "Hund"
    print(get_similar_sentence(word))