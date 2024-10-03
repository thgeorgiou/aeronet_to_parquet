from pathlib import Path

import click
import pandas as pd


def read_aeronet_file(path: Path) -> pd.DataFrame:
    """Reads an AERONET file into a pandas DataFrame."""

    df = pd.read_csv(
        path,
        skiprows=6,
        delimiter=",",
        encoding="latin-1",
    )

    # Only keep columns that match one of the regex patterns
    vars_to_keep = [
        r"Date\(dd:mm:yyyy\)",
        r"Time\(hh:mm:ss\)",
        r"AOD_\d+nm",
        r".*_Angstrom_Exponent",
        r"AERONET.*",
        r"Site_.*",
    ]
    df = df.filter(regex="|".join(vars_to_keep), axis=1)

    # Replace missing values w/ nan
    df = df.replace(-999.0, pd.NA)

    # Parse date and time columns
    df["timestamp"] = pd.to_datetime(
        df["Date(dd:mm:yyyy)"] + " " + df["Time(hh:mm:ss)"], format="%d:%m:%Y %H:%M:%S"
    )
    df = df.drop(columns=["Date(dd:mm:yyyy)", "Time(hh:mm:ss)"])

    return df


@click.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
@click.argument(
    "output_file",
    type=click.Path(writable=True, file_okay=True, dir_okay=False, path_type=Path),
)
def aeronet_to_parquet(input_file: Path, output_file: Path):
    """Converts an AERONET file to parquet format."""
    df = read_aeronet_file(input_file)
    df.to_parquet(output_file)


if __name__ == "__main__":
    aeronet_to_parquet()
