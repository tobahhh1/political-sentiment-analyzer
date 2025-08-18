from .huggingface_autoseqmodel import load_huggingface_auto_seq_model
from transformers import DebertaV2ForSequenceClassification
from transformers.tokenization_utils_base import PreTrainedTokenizerBase



def load_deberta_v2(model_name: str) -> tuple[PreTrainedTokenizerBase, DebertaV2ForSequenceClassification]:
    """Loads a DeBERTa v2 model and its tokenizer from Hugging Face."""
    tokenizer, model = load_huggingface_auto_seq_model(model_name)
    if not isinstance(tokenizer, PreTrainedTokenizerBase):
        raise TypeError(f"Expected tokenizer to be of type PreTrainedTokenizerBase, but got {type(tokenizer)}")
    if not isinstance(model, DebertaV2ForSequenceClassification):
        raise TypeError(f"Expected model to be of type DebertaV2ForSequenceClassification, but got {type(model)}")
    return tokenizer, model


