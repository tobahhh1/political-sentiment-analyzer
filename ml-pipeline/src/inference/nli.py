import itertools
from typing import Iterable, Sequence, TypedDict
from model.nli.interface import INliModel
from model.nli.interpret import interpret_raw, NliOutput


class PremiseAndHypothesis(TypedDict):
    """
    Dictionary containing input information for NLI inference.
    """
    premise: str
    """
    'Premise' is the context or statement that provides the basis for evaluating the hypothesis.
    """
    hypothesis: str
    """
    'Hypothesis' is an assumption about the premise
    """
    


def perform_zero_shot_nli(model: INliModel, dataset: Iterable[PremiseAndHypothesis], batch_size: int | None = None) -> list[NliOutput]:
    """
    Perform NLI inference on the dataset.

    Args:
        model: Zero Shot language model from the models package.
        dataset: Dataset to perform NLI on.
        batch_size: 
    """

    if batch_size is None:
        # TODO One of the biggest performance gains possible is with batching.
        # By setting a batch size as close as possible to an amount that will maximize VRAM consumption
        # without crashing, we squeeze as much performance as possible out of a resource-limited environment.
        # To implement this, need to live-monitor resource consumption and estimate resource use
        # per data row.
        # Can also gain a lot by batching togetheer sequences of similar lengths,
        # as, e.g., if you have a batch with 4 entries and [1, 1, 50, 1] tokens,
        # then due to padding you will end up submitting a batch with 200 tokens when there are
        # only 53 you are actually processing.
        raise ValueError("Smart batching is not yet implemented, please specify a batch size")

    result: list[NliOutput] = []
    for batch in itertools.batched(dataset, batch_size):
        hypotheses = []
        premises = []
        for row in batch:
            hypotheses.append(row["hypothesis"])
            premises.append(row["premise"])
        out = model(premises, hypotheses)
        interpreted = interpret_raw(out, premises, hypotheses)
        assert isinstance(interpreted, Sequence), "Interpreted results on batched inputs must be a sequence."
        result.extend(interpreted)
    return result
