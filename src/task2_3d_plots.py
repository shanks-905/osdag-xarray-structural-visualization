import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from girder_mapping import GIRDERS
import matplotlib.cm as cm

from data.node import nodes
from data.element import members

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "screening_task.nc")

ds = xr.open_dataset(DATA_PATH)
forces = ds["forces"]

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111, projection="3d")

# Generate distinct colors for each girder
colors = cm.get_cmap("tab10", len(GIRDERS))

for idx, (girder_name, elements) in enumerate(GIRDERS.items()):
    color = colors(idx)

    for ele in elements:
        n1, n2 = members[ele]

        x = [nodes[n1][0], nodes[n2][0]]
        y = [nodes[n1][1], nodes[n2][1]]
        z = [nodes[n1][2], nodes[n2][2]]

        ax.plot(x, y, z, color=color, linewidth=3)

# Axis labels for clarity
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Bridge Geometry with Highlighted Girders")

# Ensure outputs directory exists
output_dir = os.path.join(PROJECT_ROOT, "outputs")
os.makedirs(output_dir, exist_ok=True)

# Save the figure
output_path = os.path.join(output_dir, "task2_bridge_geometry.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")


#
# =========================
# 3D SHEAR FORCE DIAGRAM
# =========================
#

fig_sfd = plt.figure(figsize=(10, 6))
ax_sfd = fig_sfd.add_subplot(111, projection="3d")

# Scaling factor for visualization (tweak if needed)
SCALE_VY = 0.05

for idx, (girder_name, elements) in enumerate(GIRDERS.items()):
    color = colors(idx)

    for ele in elements:
        # Element nodes
        n1, n2 = members[ele]

        # Node coordinates
        x1, y1, z1 = nodes[n1]
        x2, y2, z2 = nodes[n2]

        # Midpoint of the element (X-Z plane)
        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2
        zm = (z1 + z2) / 2

        # Extract shear force (Vy) from Xarray
        vy_i = forces.sel(Element=ele, Component="Vy_i").item()
        vy_j = forces.sel(Element=ele, Component="Vy_j").item()
        vy = 0.5 * (vy_i + vy_j)

        # Vertical extrusion (Y-direction)
        ax_sfd.plot(
            [xm, xm],
            [ym, ym + vy * SCALE_VY],
            [zm, zm],
            color=color,
            linewidth=3
        )

# Axis labels and title
ax_sfd.set_xlabel("X")
ax_sfd.set_ylabel("Shear Force (Vy)")
ax_sfd.set_zlabel("Z")
ax_sfd.set_title("3D Shear Force Diagram (SFD)")

# Save SFD figure
output_path_sfd = os.path.join(output_dir, "task2_3d_sfd.png")
plt.savefig(output_path_sfd, dpi=300, bbox_inches="tight")

#
# =========================
# 3D BENDING MOMENT DIAGRAM
# =========================
#

fig_bmd = plt.figure(figsize=(10, 6))
ax_bmd = fig_bmd.add_subplot(111, projection="3d")

# Scaling factor for visualization
SCALE_MZ = 0.02   # Adjust if diagram looks too large/small

for idx, (girder_name, elements) in enumerate(GIRDERS.items()):
    color = colors(idx)

    for ele in elements:
        # Element nodes
        n1, n2 = members[ele]

        # Node coordinates
        x1, y1, z1 = nodes[n1]
        x2, y2, z2 = nodes[n2]

        # Element midpoint
        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2
        zm = (z1 + z2) / 2

        # Extract bending moment from dataset
        mz_i = forces.sel(Element=ele, Component="Mz_i").item()
        mz_j = forces.sel(Element=ele, Component="Mz_j").item()

        # Average bending moment
        mz = 0.5 * (mz_i + mz_j)

        # Vertical extrusion
        ax_bmd.plot(
            [xm, xm],
            [ym, ym + mz * SCALE_MZ],
            [zm, zm],
            color=color,
            linewidth=3
        )

# Labels
ax_bmd.set_xlabel("X")
ax_bmd.set_ylabel("Bending Moment (Mz)")
ax_bmd.set_zlabel("Z")
ax_bmd.set_title("3D Bending Moment Diagram (BMD)")

# Save BMD plot
output_path_bmd = os.path.join(output_dir, "task2_3d_bmd.png")
plt.savefig(output_path_bmd, dpi=300, bbox_inches="tight")
plt.show()