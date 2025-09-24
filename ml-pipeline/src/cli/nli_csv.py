import sys
import typing
import csv
import torch

from tqdm import tqdm
from model.nli.interface import INliModel
from model.nli.model_types import NliModelType
from inference.nli import perform_zero_shot_nli, PremiseAndHypothesis
from prompt.format_from_dict import format_from_dict

def nli_csv(
    nli_model_hf: str,
    nli_model_type: NliModelType,
    batch_size: int,
    premise_format: str,
    hypothesis_formats: list[str],
    input_csv: typing.TextIO,
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
    max_tokens: int = 512
):
    """
    Run NLI on a CSV file read from stdin, passing columns in a format string.
    Write the output to stdout
    """
    reader = csv.DictReader(input_csv)
    rows = list(reader)
    if not rows:
        print("No data found in the input CSV.")
        return

    model: INliModel
    
    if nli_model_type == NliModelType.DEBERTA_V2.value:
        from model.nli.impls.transformers import TransformersNli
        model = TransformersNli.load_from_hf(nli_model_hf, max_length=max_tokens).to(device)
    else:
        raise ValueError(f"Unsupported NLI model type: {nli_model_type}")

    dataset: list[PremiseAndHypothesis] = [
        {
            "hypothesis": format_from_dict(row, hypothesis),
            "premise": format_from_dict(row, premise_format)
        }
        for row in rows
        for hypothesis in hypothesis_formats
    ]

    result = perform_zero_shot_nli(model, tqdm(dataset), batch_size)

    # Write results to CSV
    output_csv = csv.DictWriter(
        sys.stdout,
        fieldnames=result[0].keys()
    )
    output_csv.writeheader()
    for row in result:
        output_csv.writerow(row)
    




    
    



    
