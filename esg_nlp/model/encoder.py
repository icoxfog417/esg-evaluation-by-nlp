import numpy as np
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer
from transformers.pipelines import FeatureExtractionPipeline
from sklearn.metrics.pairwise import cosine_similarity


class DistilBertFeatureExtractionPipeline(FeatureExtractionPipeline):
    
    def preprocess(self, inputs, truncation=True):
        # Make truncation=True
        # https://huggingface.co/docs/transformers/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.__call__.truncation
        return_tensors = self.framework
        if truncation is None:
            kwargs = {}
        else:
            kwargs = {"truncation": truncation}
        # Refer the issue
        # https://github.com/huggingface/transformers/issues/2702
        model_inputs = self.tokenizer(inputs, return_token_type_ids=False,
                                      return_tensors=return_tensors, **kwargs)
        return model_inputs


def encode(pretrained_model_name, text, batch_size=10, pretrained_tokenizer_name=""):
    print("Loading pretrained model...")
    model = AutoModel.from_pretrained(pretrained_model_name)
    print("Prepair the tokenizer...")
    tokenizer_name = pretrained_tokenizer_name if pretrained_tokenizer_name else pretrained_model_name
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    print("Set the pipeline.")
    nlp = DistilBertFeatureExtractionPipeline(model=model, tokenizer=tokenizer)
    print("Inference start.")
    # shape: (batch_size, number_of_token, vector_size)
    features = None
    if isinstance(text, str):
        vector = nlp(text, add_special_tokens=False)
        vector = np.array(vector)
        # Take mean of embedding not [CLS] tokens (added by add_special_tokens)
        # https://www.ogis-ri.co.jp/otc/hiroba/technical/similar-document-search/part9.html
        # features = np.squeeze(vector[:, 0, :])  # for CLS
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
            # for CLS token
            #vector = nlp(batch, add_special_tokens=True)
            #feature = np.array([v[0][0] for v in vector])
            features.append(feature)

        features = np.vstack(features)
        features = features[np.argsort(indexes)]

    return features


if __name__ == "__main__":
    feature = encode("bandainamco-mirai/distilbert-base-japanese",
                    ["スーパーでリンゴを買ってきた。",
                     "明日は晴れだと思うので、スーパーに行きたい。",
                     "おいしそうなリンゴを買ってきた。",
                     "私は歌手です。",
                     "焼き肉は石川さんが詳しい。"],
                     batch_size=2,
                     pretrained_tokenizer_name="cl-tohoku/bert-base-japanese-whole-word-masking")

    print(feature.shape)
    print(np.max(feature, axis=1))
    X = np.reshape(feature[0, :], (1, -1))
    y = feature[1:, :]

    distance = cosine_similarity(X, y)
    print(distance)
    print(np.argmax(distance))
