from typing import Sequence
import torch
from torch import nn



NliOutputRaw = torch.Tensor

"""
Tensor of shape (batch_size, 3).
output[i, 0] is the score for the hypothesis being true,
output[i, 1] is the score for the hypothesis being neutral,
output[i, 2] is the score for the hypothesis being false.
"""

class INliModel(nn.Module):
    """Interface for a zero-shot language inference model
    """

    def forward(self, premise: str | Sequence[str], hypothesis: str | Sequence[str]) -> NliOutputRaw:
        """Forward pass for zero-shot language inference.

        Args:
            premise: The premise or premises to evaluate.
            hypothesis: The hypothesis or hypotheses to evaluate against the premise(s).
        Returns:
            ZeroShotLanguageOutput: A tensor containing the scores for each hypothesis.
            It is a Tensor of shape (batch_size, 3).
            output[i, 0] is the score for the hypothesis being true,
            output[i, 1] is the score for the hypothesis being neutral,
            output[i, 2] is the score for the hypothesis being false.
        """
        raise NotImplementedError()
    
    def __call__(self, premise: str | Sequence[str], hypothesis: str | Sequence[str]) -> NliOutputRaw:
        """Forward pass for zero-shot language inference.

        Args:
            premise: The premise or premises to evaluate.
            hypothesis: The hypothesis or hypotheses to evaluate against the premise(s).
        Returns:
            ZeroShotLanguageOutput: A tensor containing the scores for each hypothesis.
            It is a Tensor of shape (batch_size, 3).
            output[i, 0] is the score for the hypothesis being true,
            output[i, 1] is the score for the hypothesis being neutral,
            output[i, 2] is the score for the hypothesis being false.
        """
        return super(INliModel, self).__call__(premise, hypothesis)

