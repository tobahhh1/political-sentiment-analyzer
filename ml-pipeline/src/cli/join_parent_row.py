from typing import TextIO
import csv
import sys

def join_parent_row(
    input_csv: TextIO,
):
    """
    If the CSV has a parent_id column, join the parent row with the child row,
    prepending each parent column with parent_.
    """
    reader = csv.DictReader(input_csv)
    rows = list(reader)

    id_to_row = {row['id']: row for row in rows}
    output_rows = []

    for row in rows:
        if row['parent_id'] and row['parent_id'] in id_to_row:
            parent_row = id_to_row[row['parent_id']]
            # Create a new row combining parent and child
            combined_row = {}
            for key, value in parent_row.items():
                if key != 'id' and key != 'parent_id':
                    combined_row[f'parent_{key}'] = value
            combined_row.update(row)  # Child row values will overwrite parent values if keys clash
            output_rows.append(combined_row)
        else:
            # No parent found, keep the row as is but add parent_ keys with None
            combined_row = {}
            for key, _ in row.items():
                if key != 'id' and key != 'parent_id':
                    combined_row[f'parent_{key}'] = None
            combined_row.update(row)  
            output_rows.append(combined_row)

    # Write output to stdout as csv
    fieldnames = output_rows[0].keys() if output_rows else []
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)




