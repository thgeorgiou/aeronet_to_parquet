# AERONET to Parquet Converter

This project provides a simple script to convert AERONET ASCII/CSV files to Parquet format. The main use case is for converting the ALL_POINTS dataset, which becomes significantly smaller when compressed (from ~50GB to 5GB).

```
❯ du -sh ./*
49G     ./AOD20
5.3G    ./AOD20_parquet
5.9G    ./AOD_Level20_All_Points_V3.tar.gz
```

## Installation

Install the required dependencies using pip:

```sh
pip install pandas pyarrow
```

Then grab a copy of `aeronet_to_parquet.py` from this repository.

## Usage

To convert an AERONET ASCII/CSV file to Parquet, use the following command:

```sh
python aeronet_to_parquet.py input_file output_file
```

To convert the whole dataset, use something like `find` or `fd` to find all files in a folder and convert them:

```sh
find /path/to/AERONET -name '*.lev15' -exec python aeronet_to_parquet.py {} {}.parquet \;
# or
fd 'lev15' /path/to/AERONET -x python aeronet_to_parquet.py {} {.}.parquet
```

Only a subset of columns is kept in the output Parquet file. I think they cover most usecases but double check the script if you are missing something.

The resulting Parquet files are easily read with Pandas:

```python
df = pd.read_parquet('output_file.parquet')
```

## License

Script is very simple and thus freely available, with no terms and conditions, except that it is provided "as is", without warranty of any kind.

## Useful links

- [AERONET 'Download all' page](https://aeronet.gsfc.nasa.gov/new_web/download_all_v3_aod.html) for downloading the dataset.