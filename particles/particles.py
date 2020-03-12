import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation
from numpy.random import uniform, randint
from math import sin, sqrt
import seaborn as sns

class Vector:

    def __getitem__(self, item):
        return self.loc[item]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loc = [x, y]

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y/other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def euclidean(self, other):
        inside = (self.x - other.x) ** 2 - (self.y - other.y) ** 2
        inside = max(0.0001, inside)
        return sqrt(inside)

class Particle:

    def __init__(self, init_velocity, init_posn, extents=(1000, 1000), tail_len=25):

        self.posn = Vector(*init_posn)
        self.velocity = Vector(*init_velocity)
        self.node = None
        self.done = False
        self.tail = [self.posn.loc]
        self.tail_len = tail_len
        self.stepsize = 1
        self.extents = extents

    def update_tail(self, pt):
        self.tail.append(pt.loc)
        if len(self.tail) > self.tail_len:
            self.tail = self.tail[1:]

    def transition(self):

        stepsize = self.stepsize

        self.posn = self.posn + (self.velocity * stepsize)
        self.velocity = self.velocity - (self.accelleration() * stepsize)
        self.update_tail(self.posn)

    def accelleration(self):
        try:
            out = Vector(-max(0, self.posn[0] - self.velocity[0]) ** (1/3), -max(0, self.posn[1] - self.velocity[1]) ** (1/3))
        except:
            out = Vector(10000, 10000)
        return out / 10000

class Canvas:
    def __init__(self, dims, particles):
        numparticles = len(particles)
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=dims[0], ylim=dims[1])
        self.lines = [self.ax.plot([], [], lw=2) for i in range(numparticles)]
        self.data = []
        self.particles = particles
        self.numparticles = numparticles
        for line in self.lines:
            line[0].set_alpha(uniform(0, 0.5))

    def init(self):
        for line in self.lines:
            line[0].set_data([], [])
        self.particles = [p for p in self.particles if not p.done]
        remain = len(self.particles)
        self.particles = self.particles + [make_particle() for i in range(self.numparticles - remain)]
        return [line[0] for line in self.lines]

    def draw(self, j):
        self.data = []
        for p in particles:
            p.transition()
            self.data.append(p.tail)
        for i, datum in enumerate(self.data):
            x = [d[0] for d in datum]
            y = [c[1] for c in datum]
            self.lines[i][0].set_data(x, y)
        return [line[0] for line in self.lines]

    def set_global_stepsize(self, stepsize):
        for p in self.particles:
            p.stepsize = stepsize

matplotlib.use('TkAgg')

def make_particle():
    init_pos = Vector(randint(250, 750), randint(250, 750))
    init_vel = Vector(uniform(-0.5, 0.5), 0)
    return Particle(init_vel.loc, init_pos.loc, tail_len=100)

particles = [make_particle() for i in range(5000)]
canv = Canvas((1000, 1000), particles)
canv.set_global_stepsize(5)
for l in canv.lines:
    l[0].set_sketch_params(scale = 0.5)

anim = animation.FuncAnimation(canv.fig, canv.draw,
                               init_func=canv.init, frames=300, interval=20, blit=True)

anim.save('anim2.gif', fps=30, writer='imagemagick')
plt.show()


