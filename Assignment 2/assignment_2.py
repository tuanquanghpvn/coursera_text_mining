import nltk

## Part 1 - Analyzing Moby Dick


# If you would like to work with the raw text you can use 'moby_raw'
with open('/Users/truong.tuan.quang/nltk_data/corpora/gutenberg/melville-moby_dick.txt', 'r') as f:
    moby_raw = f.read()

# If you would like to work with the novel in nltk.Text format you can use 'text1'
moby_tokens = nltk.word_tokenize(moby_raw)
text1 = nltk.Text(moby_tokens)


### Question 1

# What is the lexical diversity of the given text input? (i.e. ratio of unique tokens to the total number of tokens)
#
# *This function should return a float.*

def answer_one():
    unique_token = len(set(moby_tokens))
    return unique_token / len(moby_tokens)

print("Answer 1: ", answer_one())


### Question 2

# What percentage of tokens is 'whale'or 'Whale'?
#
# *This function should return a float.*

def answer_two():
    whale_number = text1.count('whale') + text1.count('Whale')
    return whale_number * 100 / len(text1.tokens)

print("Answer 2: ", answer_two())


### Question 3

# What are the 20 most frequently occurring (unique) tokens in the text? What is their frequency?
#
# *This function should return a list of 20 tuples where each tuple is of the form `(token, frequency)`. The list should be sorted in descending order of frequency.*

def answer_three():
    dist = nltk.FreqDist(text1)
    tuple_freq = dist.most_common(20)
    return tuple_freq

print("Answer 3: ", answer_three())


### Question 4

# What tokens have a length of greater than 5 and frequency of more than 150?
#
# *This function should return a sorted list of the tokens that match the above constraints. To sort your list, use `sorted()`*

def answer_four():
    dist = nltk.FreqDist(text1)
    freq_words = sorted([w for w in dist.keys() if len(w) > 5 and dist[w] > 150])
    return freq_words

print("Answer 4: ", answer_four())


### Question 5

# Find the longest word in text1 and that word's length.
#
# *This function should return a tuple `(longest_word, length)`.*

def answer_five():
    longest_word = max([(word, len(word)) for word in set(moby_tokens)], key=lambda item: item[1])
    return longest_word

print("Answer 5: ", answer_five())


### Question 6

# What unique words have a frequency of more than 2000? What is their frequency?
#
# "Hint:  you may want to use `isalpha()` to check if the token is a word and not punctuation."
#
# *This function should return a list of tuples of the form `(frequency, word)` sorted in descending order of frequency.*

def answer_six():
    dist = nltk.FreqDist(text1)
    freq_words = [(dist[w], w) for w in dist.keys() if w.isalpha() and dist[w] >= 2000]
    freq_words = sorted(freq_words, key=lambda item: item[0], reverse=True)
    return freq_words

print("Answer 6: ", answer_six())


### Question 7

# What is the average number of tokens per sentence?
#
# *This function should return a float.*

def answer_seven():
    sents = nltk.sent_tokenize(text1)
    return len(text1.tokens) / len(sents)

# print("Answer 7: ", answer_seven())


### Question 8

# What are the 5 most frequent parts of speech in this text? What is their frequency?
#
# *This function should return a list of tuples of the form `(part_of_speech, frequency)` sorted in descending order of frequency.*

def answer_eight():
    pos = nltk.pos_tag(text1)
    freqs = nltk.FreqDist([w[1] for w in pos])
    freqs = sorted([(w, freqs[w]) for w in freqs.keys()], key=lambda item: item[1], reverse=True)[:5]
    return freqs

print("Answer 8: ", answer_eight())


## Part 2 - Spelling Recommender

# For this part of the assignment you will create three different spelling recommenders, that each take a list of misspelled words and recommends a correctly spelled word for every word in the list.
#
# For every misspelled word, the recommender should find find the word in `correct_spellings` that has the shortest distance*, and starts with the same letter as the misspelled word, and return that word as a recommendation.
#
# *Each of the three different recommenders will use a different distance measure (outlined below).
#
# Each of the recommenders should provide recommendations for the three default words provided: `['cormulent', 'incendenece', 'validrate']`.


from nltk.corpus import words

correct_spellings = words.words()

# print(correct_spellings)

### Question 9

# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
#
# **[Jaccard distance](https://en.wikipedia.org/wiki/Jaccard_index) on the trigrams of the two words.**
#
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*

from nltk.metrics.distance import jaccard_distance


def answer_nine(entries=['cormulent', 'incendenece', 'validrate']):
    lst = {}

    for w1 in entries:
        ngram_1 = set(nltk.ngrams(w1, 3))

        for w2 in correct_spellings:
            if w1[0] != w2[0]:
                continue
            ngram_2 = set(nltk.ngrams(w2, 3))
            distance = jaccard_distance(ngram_1, ngram_2)
            tup = (w2, distance)
            if w1 in lst:
                old_tup = lst[w1]
                if old_tup[1] > distance:
                    lst[w1] = tup
            else:
                lst[w1] = tup

    data = [lst[w][0] for w in entries]
    print([lst[w][1] for w in entries])
    return data

print("Answer 9: ", answer_nine())


### Question 10

# For this recommender, your function should provide recommendations for the three default words provided above using the following distance metric:
#
# **[Jaccard distance](https://en.wikipedia.org/wiki/Jaccard_index) on the 4-grams of the two words.**
#
# *This function should return a list of length three:
# `['cormulent_reccomendation', 'incendenece_reccomendation', 'validrate_reccomendation']`.*


def answer_ten(entries=['cormulent', 'incendenece', 'validrate']):
    lst = {}

    for w1 in entries:
        ngram_1 = set(nltk.ngrams(w1, 4))

        for w2 in correct_spellings:
            if w1[0] != w2[0]:
                continue
            ngram_2 = set(nltk.ngrams(w2, 4))
            distance = jaccard_distance(ngram_1, ngram_2)
            tup = (w2, distance)
            if w1 in lst:
                old_tup = lst[w1]
                if old_tup[1] > distance:
                    lst[w1] = tup
            else:
                lst[w1] = tup

    data = [lst[w][0] for w in entries]
    print([lst[w][1] for w in entries])
    return data

print("Answer 10: ", answer_ten())
