import numpy as np
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer
from transformers.pipelines import FeatureExtractionPipeline
from sklearn.metrics.pairwise import cosine_similarity


def encode(pretrained_model_name, text, batch_size=10):
    print("Loading pretrained model...")
    model = AutoModel.from_pretrained(pretrained_model_name)
    print("Prepair the tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
    print("Set the pipeline.")
    nlp = FeatureExtractionPipeline(model=model, tokenizer=tokenizer)
    print("Inference start.")
    # shape: (batch_size, number_of_token, vector_size)
    features = None
    if isinstance(text, str):
        vector = nlp(text)
        vector = np.array(vector)
        # get [CLS] tokens (added by add_special_tokens)
        # [CLS] tokens does not suitable for sentence representation?
        # https://huggingface.co/transformers/model_doc/bert.html
        # features = np.squeeze(vector[:, 0, :])
        features = np.mean(vector, axis=1)
    else:
        features = []
        indexes = [i for i, s in
                   sorted(enumerate(text), key=lambda x: len(x[1]))]
        _text = sorted(text, key=lambda s: len(s))
        for i in tqdm(range(0, len(_text), batch_size)):
            batch = _text[i:i + batch_size]
            vector = nlp(batch, add_special_tokens=False)
            feature = np.array([np.mean(v[0], axis=0) for v in vector])
            features.append(feature)

        features = np.vstack(features)
        features = features[np.argsort(indexes)]

    return features


if __name__ == "__main__":
    feature = encode("cl-tohoku/bert-base-japanese-whole-word-masking",
                    ["スーパーでリンゴを買ってきた。",
                     "明日は晴れだと思うので、スーパーに行きたい。",
                     "おいしそうなリンゴを買ってきた。",
                     "私は歌手です。",
                     "焼き肉は石川さんが詳しい。"], batch_size=2)

    print(feature.shape)
    print(np.max(feature, axis=1))
    X = np.reshape(feature[0, :], (1, -1))
    y = feature[1:, :]

    distance = cosine_similarity(X, y)
    print(distance)
    print(np.argmax(distance))
