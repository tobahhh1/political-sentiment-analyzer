import torch

def guard_logits(logits: torch.FloatTensor | None):
    """Raise an exception if the output logits from an NLI model are incorrect."""
    assert logits is not None, "Invalid nli model: returned logits must not be None"
    assert logits.dim() <= 2 and logits.dim() > 0, "Invalid nli model: returned logits must be a 1D or 2D tensor"
    assert logits.shape[-1] in {2, 3}, "Invalid nli model: returned logits must have 2 classes (entailment, contradiction) or 3 classes (positive, negative, neutral)"


