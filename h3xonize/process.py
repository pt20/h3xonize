from pathlib import Path

import numpy as np
import rioxarray  # noqa: F401
import xarray as xr
from affine import Affine
from h3ronpy.raster import nearest_h3_resolution, raster_to_dataframe


def prepare_dataset(file_path: str | Path) -> xr.Dataset:
    """given path to a file that xarray can open, open and clean a bit

    Args:
        file_path (str | Path): xarray compliant fpath

    Returns:
        xr.Dataset: cleaned dataset
    """
    xr_ds = xr.open_dataset(file_path)
    xr_ds = xr_ds.drop_dims("nv")
    xr_ds = xr_ds.rename({"time1": "time"})

    return xr_ds


def get_dataset_transform(dataset: xr.Dataset) -> Affine:
    return dataset.rio.transform()


def get_h3_resolution(dataset: xr.Dataset, transform: Affine, data_var_name: str) -> int:

    ds_subset_shape = np.squeeze(dataset.isel(time=slice(None, 1))[data_var_name].values).shape
    h3_res: int = nearest_h3_resolution(
        ds_subset_shape, transform, search_mode="smaller_than_pixel"
    )
    return h3_res


def to_parquet(dataset: xr.Dataset, data_var_name: str, dest_dir: str) -> None:
    transform = get_dataset_transform(dataset)
    h3_res = get_h3_resolution(dataset, transform, data_var_name)

    for val in dataset.time.values:
        xr_ds_sub = dataset.sel(time=val)
        in_raster = np.squeeze(xr_ds_sub[data_var_name].values)

        print("converting", val)
        df = raster_to_dataframe(
            in_raster, transform=transform, h3_resolution=h3_res, compacted=False
        )
        df.rename({"h3index": f"lvl{h3_res}_idx"})
        df["timestamp"] = val

        pq_fname = f"{dest_dir}/{val}.parquet"
        print("saving ...")
        df.to_parquet(
            pq_fname,
            engine="pyarrow",
            index=False,
            compression="zstd",
        )


ds = prepare_dataset(
    "/home/prayag/projects/h3xonize/data/precipitation_amount_1hour_Accumulation.nc"
)
data_var = "precipitation_amount_1hour_Accumulation"
dest_dir = "data/"

to_parquet(ds, data_var, dest_dir)
