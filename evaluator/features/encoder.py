import numpy as np
from transformers import AutoModel, AutoTokenizer
from transformers.pipelines import FeatureExtractionPipeline
from sklearn.metrics.pairwise import cosine_similarity


def encode(pretrained_model_name, text):
    print("Loading pretrained model...")
    model = AutoModel.from_pretrained(pretrained_model_name)
    print("Prepair the tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
    print("Set the pipeline.")
    nlp = FeatureExtractionPipeline(model=model, tokenizer=tokenizer)
    print("Inference start.")
    # shape: (batch_size, number_of_token, vector_size)
    vector = nlp(text)
    vector = np.array(vector)
    # get [CLS] tokens (added by add_special_tokens)
    features = np.squeeze(vector[:, 0, :])
    return features


feature = encode("bert-base-japanese-whole-word-masking",
                 ["おいしそうなリンゴを買ってきた。",
                  "明日は晴れだと思うので、外に行きたい。",
                  "私は歌手です。",
                  "スーパーでリンゴを買ってきた。",
                  "焼き肉は石川さんが詳しい。"])

print(feature.shape)
X = np.reshape(feature[0, :], (1, -1))
y = feature[1:, :]

distance = cosine_similarity(X, y)
print(distance)
print(np.argmax(distance))
