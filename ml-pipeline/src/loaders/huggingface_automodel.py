from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils import PreTrainedTokenizer

def load_huggingface_automodel(model_name: str) -> tuple[PreTrainedTokenizer, PreTrainedModel]:
    """Loads an AutoModel of the given name and its tokenizer from HuggingFace"""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model
