import functools
from typing import Protocol, Self, Sequence, Callable, TypedDict, Optional

import torch
from transformers.configuration_utils import PretrainedConfig
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers.tokenization_utils_base import BatchEncoding

from loaders.huggingface_automodel import load_huggingface_automodel 
from ..guards import guard_logits

from ..interface import INliModel, NliOutputRaw


ITransformersSequenceClassificationTokenizer = Callable[[str | Sequence[str], str | Sequence[str]], BatchEncoding]
"""Tokenizer that encodes a string into the input format expected by Deberta V2 models."""

class ITransformersSequenceClassificationModelInput(TypedDict):
    """Input type for sequence classification models in the Transformers library."""
    input_ids: torch.Tensor
    attention_mask: torch.Tensor | None
    token_type_ids: torch.Tensor | None
    position_ids: torch.Tensor | None
    head_mask: torch.Tensor | None
    inputs_embeds: torch.Tensor | None
    labels: torch.Tensor | None

class ITransformersSequenceClassificationModel(Protocol):
    """Interface for sequence classification models in the Transformers library, which
    would be compatible with the TransformersNli class."""
    def __call__(self, **kwargs) -> SequenceClassifierOutput: ...
    config: PretrainedConfig
    @property
    def device(self) -> torch.device: ...

class TransformersNli(INliModel):
    """NLI model using the Deberta V2 architecture for sequence classification."""
    def __init__(self, model: ITransformersSequenceClassificationModel, tokenizer: ITransformersSequenceClassificationTokenizer):
        model.device
        super().__init__()
        assert model.config.num_labels in {2, 3}, f"Deberta V2 model must have 3 labels (positive, negative, neutral) to be compatible with zero shot classification. Found {model.config.num_labels} labels."
        self.model = model
        self.tokenizer = tokenizer

    def forward(self, premise: str | Sequence[str], hypothesis: str | Sequence[str]) -> NliOutputRaw:
        inputs = self.tokenizer(premise, hypothesis).to(self.model.device)
        outputs = self.model(**inputs)
        guard_logits(outputs.logits)
        assert outputs.logits is not None, "Unreachable error: guard_logits should have raised an exception if logts were None"
        return outputs.logits

    @classmethod
    def load_from_hf(cls, model_name: str, max_length: Optional[int] = None) -> Self:
        tokenizer, model = load_huggingface_automodel(model_name)
        return cls(model, functools.partial(tokenizer, return_tensors="pt", max_length=max_length, padding=True, truncation=True))
