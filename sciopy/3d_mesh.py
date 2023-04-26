# TBD
import numpy as np

import pyvista as pv
from pyvista import CellType

from tempfile import NamedTemporaryFile

import numpy as np

import pyvista
from pyvista import examples


# There are 10 cells here, each cell is [4, INDEX0, INDEX1, INDEX2, INDEX3]
# where INDEX is one of the corners of the tetrahedron.
#
# Note that the array does not need to be shaped like this, we could have a
# flat array, but it's easier to make out the structure of the array this way.
cells = np.array(
    [
        [4, 6, 5, 8, 7],
        [4, 7, 3, 8, 9],
        [4, 7, 3, 1, 5],
        [4, 9, 3, 1, 7],
        [4, 2, 6, 5, 8],
        [4, 2, 6, 0, 4],
        [4, 6, 2, 0, 8],
        [4, 5, 2, 8, 3],
        [4, 5, 3, 8, 7],
        [4, 2, 6, 4, 5],
    ]
)

celltypes = np.full(10, fill_value=CellType.TETRA, dtype=np.uint8)

# These are the 10 points. The number of cells does not need to match the
# number of points, they just happen to in this example
points = np.array(
    [
        [-0.0, 0.0, -0.5],
        [0.0, 0.0, 0.5],
        [-0.43, 0.0, -0.25],
        [-0.43, 0.0, 0.25],
        [-0.0, 0.43, -0.25],
        [0.0, 0.43, 0.25],
        [0.43, 0.0, -0.25],
        [0.43, 0.0, 0.25],
        [0.0, -0.43, -0.25],
        [0.0, -0.43, 0.25],
    ]
)

# Create and plot the unstructured grid
grid = pv.UnstructuredGrid(cells, celltypes, points)
grid.plot(show_edges=True)

split_cells = grid.explode(1.5)
split_cells.plot(show_edges=True, ssao=True)
