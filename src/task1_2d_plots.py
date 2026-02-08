import xarray as xr
import matplotlib.pyplot as plt

from girder_mapping import CENTRAL_GIRDER_ELEMENTS

DATA_PATH = "../data/screening_task.nc"

ds = xr.open_dataset(DATA_PATH)
forces = ds["forces"]

x = []        # distance index
mz_vals = []  # bending moment
vy_vals = []  # shear force

pos = 0

for ele in CENTRAL_GIRDER_ELEMENTS:
    mz_i = forces.sel(Element=ele, Component="Mz_i").item()
    mz_j = forces.sel(Element=ele, Component="Mz_j").item()
    vy_i = forces.sel(Element=ele, Component="Vy_i").item()
    vy_j = forces.sel(Element=ele, Component="Vy_j").item()

    x.extend([pos, pos + 1])
    mz_vals.extend([mz_i, mz_j])
    vy_vals.extend([vy_i, vy_j])

    pos += 1

# Bending Moment Diagram
plt.figure(figsize=(10,4))
plt.plot(x, mz_vals, marker="o")
plt.title("Bending Moment Diagram (Central Girder)")
plt.xlabel("Element Sequence")
plt.ylabel("Bending Moment (Mz)")
plt.grid(True)
plt.tight_layout()
plt.savefig("../outputs/task1_bmd.png")
plt.show()

# Shear Force Diagram
plt.figure(figsize=(10,4))
plt.plot(x, vy_vals, marker="o", color="orange")
plt.title("Shear Force Diagram (Central Girder)")
plt.xlabel("Element Sequence")
plt.ylabel("Shear Force (Vy)")
plt.grid(True)
plt.tight_layout()
plt.savefig("../outputs/task1_sfd.png")
plt.show()