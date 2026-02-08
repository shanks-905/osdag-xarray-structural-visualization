import xarray as xr

DATA_PATH = "../data/screening_task.nc"

ds = xr.open_dataset(DATA_PATH)

print(ds)
print(ds.data_vars)
print(ds.coords)
print(ds.dims)