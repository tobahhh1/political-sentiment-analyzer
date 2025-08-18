import functools
import transformers

def load_bert_model(model_name: str) -> tuple[transformers.BertTokenizer, transformers.BertModel]:

    return transformers.BertTokenizer.from_pretrained(model_name), transformers.BertModel.from_pretrained(model_name)
    
load_bert_simcse = functools.partial(load_bert_model, "princeton-nlp/sup-simcse-roberta-large")
