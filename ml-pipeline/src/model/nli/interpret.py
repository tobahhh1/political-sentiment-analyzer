from typing import Callable, Optional, TypedDict
from .interface import NliOutputRaw
from .guards import guard_logits

from torch.nn.functional import softmax

class NliOutput(TypedDict):
    """
    Output type for zero-shot language inference, after it has been interpreted.
    """
    premise: str
    """
    'Premise' is the context or statement that provides the basis for evaluating the hypothesis.
    """
    hypothesis: str
    """
    'Hypothesis' is an assumption about the premise
    """
    entailment_score: float
    """
    'Entailment score' is the model's confidence that the hypothesis is true given the premise.
    """
    neutral_score: Optional[float]
    """
    'Neutral score' is the model's confidence that the hypothesis is neither true nor false given the premise. Optional as not all models provide this score.
    """
    contradiction_score: float
    """
    'Contradiction score' is the model's confidence that the hypothesis is false given the premise.
    """

def default_transform_scores(raw: NliOutputRaw) -> NliOutputRaw:
    return softmax(raw, dim=-1)

def interpret_raw(raw: NliOutputRaw, premise: str | list[str] | tuple[str, ...] | None = None, hypothesis: str | list[str] | tuple[str, ...] | None = None, transform_scores: Callable[[NliOutputRaw], NliOutputRaw] = default_transform_scores) -> NliOutput | list[NliOutput]:
    """
    Interpret the raw output of a NLI model into a readable dictionary format.
    """
    transformed_scores = transform_scores(raw)
    guard_logits(raw)

    flat = False

    if transformed_scores.dim() == 1:
        flat = True
        transformed_scores = transformed_scores.unsqueeze(0)

    output = []
    has_neutral = transformed_scores.shape[-1] == 3
    for i, scores in enumerate(transformed_scores):
        if premise is None:
            premise_text = ""
        elif isinstance(premise, (list, tuple)):
            premise_text = premise[i] if i < len(premise) else ""
        else:
            premise_text = premise

        if hypothesis is None:
            hypothesis_text = ""
        elif isinstance(hypothesis, (list, tuple)):
            hypothesis_text = hypothesis[i] if i < len(hypothesis) else ""
        else:
            hypothesis_text = hypothesis

        output.append(
            NliOutput(
                premise=premise_text,
                hypothesis=hypothesis_text,
                entailment_score=scores[0].item() if has_neutral else scores[1].item(),
                neutral_score=scores[1].item() if has_neutral else None,
                contradiction_score=scores[2].item() if has_neutral else scores[0].item()
            )
        )

    if flat:
        return output[0]
    
    return output
    




