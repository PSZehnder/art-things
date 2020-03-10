import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation
import matplotlib.patches as patches


class PolygonalArtist:

    def __init__(self, polygon, ax):
        self.poly = polygon
        self.ax = ax


    def rotate(self, degs):
        transdata = self.ax.transData
        trans = matplotlib.transforms.Affine2D().rotate_deg(degs) + transdata
        self.poly.set_transform(trans)

    def dilate(self, pct):
fig = plt.figure()
ax = fig.add_subplot(111)

r1 = patches.Rectangle((0, 0), 20, 40, alpha = 0.5)
r2 = patches.Rectangle((0, 0), 20, 40, alpha = 0.5)

t2 = matplotlib.transforms.Affine2D().rotate_deg(-45) + ax.transData

r2.set_transform(t2)

ax.add_patch(r1)
ax.add_patch(r2)

plt.show()
