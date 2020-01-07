from tqdm import tqdm
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers.pipelines import QuestionAnsweringPipeline


def answer(pretrained_model_name, question_context_pair):
    print("Loading pretrained model...")
    model = AutoModelForQuestionAnswering.from_pretrained(pretrained_model_name)
    print("Prepair the tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
    print("Set the pipeline.")
    nlp = QuestionAnsweringPipeline(model=model, tokenizer=tokenizer, modelcard=None)
    print("Answer start.")
    # shape: (batch_size, number_of_token, vector_size)
    answers = []
    for qc in tqdm(question_context_pair):
        q, c = qc
        a = nlp({
            "question": q,
            "context": c
        })
        answers.append(a)

    return answers


if __name__ == "__main__":
    question_contexts = (
        ["What is the name of the repository ?",
         "Pipeline have been included in the huggingface/transformers repository"],
        ["In what country is Normandy located?",
         "The Normans (Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. They were descended from Norse ('Norman' comes from 'Norseman') raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries."]
    )
    answers = answer("distilbert-base-uncased-distilled-squad", question_contexts)
    print(answers)
