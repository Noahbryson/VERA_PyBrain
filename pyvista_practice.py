import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from modules.functions import functions


funcs = functions()
points = [[0, 0, 0],
          [1, 0, 0],
          [0.5, 0.667, 0],
          [0, 0, 1],
          [1, 0, 1],
          [0.5, 0.667, 1]]
mesh = pv.PolyData(points)
# mesh.plot(show_bounds=True, cpos='xy', point_size=20)
# cells = [[0, 1, 2],[3, 4, 5],[0,2,5,3],[2,1,4,5],[3,4,1,0]]
cells = [[0, 1, 2],[3, 4, 5]]
cells =  funcs.flattenCells(cells)
lines = [[1,4],[3,0],[2,5]]
lines = funcs.flattenCells(lines)
mesh = pv.PolyData(points,faces=cells,lines=lines)
pl = pv.Plotter()
pl.add_mesh(mesh, show_edges=True, line_width=5)
label_coords = mesh.points + [0, 0, 0.01]
pl.add_point_labels(label_coords, [f'Point {i}' for i in range(mesh.n_points)],
                    font_size=20, point_size=20)
pl.add_point_labels([0.43, 0.2, 0], ['Cell 0'], font_size=20)
# pl.camera_position = 'xy'
print(mesh)
pl.show()




def flattenCells(cells):
      output = []
      if len(np.shape(cells)) > 1:
            for entry in cells:
                  numel = len(entry)
                  t = entry.insert(numel, 0)
                  output += t
      else:
            pass
      return output