
"""
Steps to text summarization:
    - Text Cleaning 
    - Sentence Tokenization
    - Word Tokenization
    - word-frequency table
    - Summarization
"""
import sys
import spacy
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS

stopwords = STOP_WORDS

# Create the nlp object
nlp = spacy.load('en_core_web_sm')


sample_text = """
There are broadly two types of extractive summarization tasks depending on what the summarization program focuses on. The first is generic summarization, which focuses on obtaining a generic summary or abstract of the collection (whether documents, or sets of images, or videos, news stories etc.). The second is query relevant summarization, sometimes called query-based summarization, which summarizes objects specific to a query. Summarization systems are able to create both query relevant text summaries and generic machine-generated summaries depending on what the user needs.

An example of a summarization problem is document summarization, which attempts to automatically produce an abstract from a given document. Sometimes one might be interested in generating a summary from a single source document, while others can use multiple source documents (for example, a cluster of articles on the same topic). This problem is called multi-document summarization. A related application is summarizing news articles. Imagine a system, which automatically pulls together news articles on a given topic (from the web), and concisely represents the latest news as a summary.

Image collection summarization is another application example of automatic summarization. It consists in selecting a representative set of images from a larger set of images.[4] A summary in this context is useful to show the most representative images of results in an image collection exploration system. Video summarization is a related domain, where the system automatically creates a trailer of a long video. This also has applications in consumer or personal videos, where one might want to skip the boring or repetitive actions. Similarly, in surveillance videos, one would want to extract important and suspicious activity, while ignoring all the boring and redundant frames captured.
"""

unfiltered_tokens = sample_text.split()
unfiltered_text = " ".join(unfiltered_tokens)

doc = nlp(unfiltered_text)
# print each individual token found in our document from the nlp object
tokens = [token for token in doc]

# Data Cleaning - remove punctuation and stop words:
word_frequencies = {}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

max_freq = max(word_frequencies.values())

# we need to noramlized the word frequencies by dividing the frerquencies by the max_freq
for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word]/max_freq

# create sentence tokens, not word level tokesn
sent_tokens = [sent for sent in doc.sents]

# Create a sentence score by adding the noramlzied value of our word freqs based on the sentence
sentence_score = {}

for sentence in sent_tokens:
    for word in sentence:
        if word.text.lower() in word_frequencies.keys():
            if sentence not in sentence_score.keys():
                sentence_score[sentence] = word_frequencies[word.text.lower()]
            else:
                sentence_score[sentence] += word_frequencies[word.text.lower()]

# At this point we have sentences with the most used sentences - this is a Bag of Word style
sorted_sentence = sorted(sentence_score, key=sentence_score.get, reverse=True)
print(sorted_sentence[0:4])

