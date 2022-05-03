from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel

# Create a corpus from a list of texts
print(common_texts)

common_dictionary = Dictionary(common_texts)
common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]

# Train the model on the corpus.
lda = LdaModel(common_corpus, num_topics=10)

print(common_dictionary)
print(common_corpus)


# 打印前5个topic的词分布
topic_list = lda.print_topics(5)
print("10个主题的单词分布为：\n")
for topic in topic_list:
    print(topic)
# 打印id为5的topic的词分布
lda.print_topic(5)

#模型的保存/ 加载
lda.save('./lda_model/example_lda.model')
lda = LdaModel.load('./lda_model/example_lda.model')