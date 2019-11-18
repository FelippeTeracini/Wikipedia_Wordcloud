import pickle

with open('teste_final.pickle', 'rb') as f:
    word_dict = dict(pickle.load(f))

print(word_dict)
