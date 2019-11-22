import pickle
import matplotlib.pyplot as plt
from wordcloud import WordCloud

with open('final.pickle', 'rb') as f:
    word_dict = dict(pickle.load(f))


print(word_dict.keys())
word = str(input("Word: "))
wc = WordCloud()
wc.generate_from_frequencies(word_dict[word])
plt.imshow(wc)
plt.show()
