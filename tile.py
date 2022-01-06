from math import sqrt

from matplotlib import rcParams, pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.transforms import Affine2D as T

from svgpath2mpl import parse_path

class Tile(object):
    
    def __init__(self, path = None):
        self.bbox = True
        if not path: path = Path([(0,0)])
        self.path = path

    @classmethod
    def read(cls, name):
        with open('{}.path'.format(name)) as _: 
            return cls(
                parse_path(_.read()).transformed(
                    T().scale(1, -1).translate(0, 1)
                )
            )
            
    @staticmethod
    def union(tile0, tile1):
        return Tile(Path.make_compound_path(tile0.path, tile1.path))
            
    @staticmethod
    def transform(tile, transform):
        return Tile(tile.path.transformed(transform))
            
    def _ipython_display_(self):
        fig, ax = plt.subplots()
        ax.add_patch(PathPatch(self.path, fill = False))
        if self.bbox:
            r = Rectangle((0,0), 1, 1, fill = False, linestyle = 'dotted')
            ax.add_patch(r)
        plt.axis('equal')
        plt.axis('off')
        return fig

blank = Tile()

def flip(tile):
    return Tile.transform(tile, T().scale(-1, 1).translate(1, 0))

def rot(tile):
    return Tile.transform(tile, T().rotate_deg(90).translate(1, 0))

def rot45(tile):
    return Tile.transform(tile,
        T().rotate_deg(45).scale(1 / sqrt(2), 1 / sqrt(2)).translate(1 / 2, 1 / 2)
    )

def over(tile0, tile1):
    return Tile.union(tile0, tile1)

def beside(tile0, tile1, n = 1, m = 1):
    den = n + m
    return Tile.union(
        Tile.transform(tile0, T().scale(n / den, 1)),
        Tile.transform(tile1, T().scale(m / den, 1).translate(n / den, 0))
    )

def above(tile0, tile1, n = 1, m = 1):
    den = n + m
    return Tile.union(
        Tile.transform(tile0, T().scale(1, n / den).translate(0, m / den)),
        Tile.transform(tile1, T().scale(1, m / den))
    )

def quartet(p, q, r, s):
    return above(beside(p, q), beside(r, s))
	
def rectri(n):
    if n == 0: 
        return blank
    else:
        return quartet(rot(triangle), rectri(n - 1), rectri(n - 1), rectri(n - 1))

		
def nonet(p, q, r, s, t, u, v, w, x):
    return above(
            beside(p, beside(q, r), 1, 2),
            above(
                beside(s, beside(t, u), 1, 2),
                beside(v, beside(w, x), 1, 2), 
            ),
            1, 2
    )
	
def side(n,t):
    if n == 0: 
        return blank
    else: 
        return quartet(side(n-1,t), side(n-1,t), rot(t), t)
		
def corner(n,u,t):
    if n == 0:
        return blank
    else:
        return quartet(corner(n-1,u,t), side(n-1,t), rot(side(n-1,t)), u)
		
def squarelimit(n,u,t):
    return nonet(
        corner(n,u,t), 
        side(n,t), 
        rot(rot(rot(corner(n,u,t)))), 
        rot(side(n,t)), 
        u, 
        rot(rot(rot(side(n,t)))),
        rot(corner(n,u,t)), 
        rot(rot(side(n,t))), 
        rot(rot(corner(n,u,t)))
    )