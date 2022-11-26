import os

from s3fs import S3FileSystem

S3 = S3FileSystem(anon=True)


def download_data(uri: str, data_dir: str = "data/") -> None:
    """Download data from s3 to target directory

    Args:
        uri (str): s3 uri
        data_dir (str, optional): Defaults to "data/".

    Raises:
        FileNotFoundError: raised when file does not exist on remote object storage
    """
    if not S3.isfile(uri):
        raise FileNotFoundError(f"{uri} not found. Make sure to pass valid s3 uri")

    print(f"Downloading {os.path.basename(uri)} to {data_dir} ...")
    S3.get(uri, data_dir)


uri = "s3://era5-pds/2022/05/data/precipitation_amount_1hour_Accumulation.nc"
download_data(uri)
