# Text Summarization App

Automatic text summarization is the process of shortening a text document to create one with only the major points of the original document. Technologies that can make a coherent summary take into account variables such as length, writing style and syntax.

Text summarization is part of machine learning and data mining. The main idea of summarization is to find a subset of data which contains the information of the entire set. Such techniques are widely used in industry today. Search engines are an example; others include summarization of documents, image collections and videos. Document summarization tries to create a representative summary or abstract of the entire document, by finding the most informative sentences, while in image summarization the system finds the most representative and important (i.e. salient) images. For surveillance videos, one might want to extract the important events from an otherwise uneventful context.

There are two general approaches to automatic summarization: `extraction` and `abstraction`. Extraction methods work by selecting a subset of existing words, phrases, or sentences in the original text to form the summary (i.e., NLP). In contrast, abstraction methods build an internal semantic representation and use natural language generation techniques to create a summary that is closer to what a human might express (i.e., NLU and NLG). Research to date has focused primarily on NLP-basedf extraction methods, which are appropriate for simple text summarization, image collection summarization and video summarization.

The code for doing text summarization with `gensim` is extremely simple:

```python
gensim_summary_list = summarize('... long text ...', ratio=0.2, split=True)
```

With `sumy` it's equally easy:

```python
parser = PlaintextParser.from_string('... long text ...',Tokenizer("english"))
lex_summarizer = LexRankSummarizer()
sumy_lex_rank = lex_summarizer(parser.document,10)
sumy_summary_list = [str(sentence) for sentence in sumy_lex_rank]
```

However, we're going to implement this from scratch!

Our homegrown `Tf-Idf`-based method has 6 simple steps:

1. __Calculate sentence term frequency matrix.__

  Term frequency (TF) is how often a word appears in the document, divided by how many words there are in the document.

2. __Calculate global (all sentences) term frequency matrix__.
3. __Calculate IDF__.

  Inverse document frequency (IDF) is how unique or rare a word is.

4. __Calculate TF-IDF__.
5. __Score sentences__ using average of normalised TF-IDF of terms in each sentence.
6. __Generate summary__ using a threshold value to prune low-scoring sentences.

Enjoy!
