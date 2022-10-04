from enum import Enum, auto
from panda3d.core import CollisionBox
from panda3d.core import PandaNode, NodePath
from panda3d.core import Vec3, Point3, Quat, BitMask32


STONE_PATH = 'models/cylinder/cylinder'
PATH_TEXTURE = 'textures/envir-rock2.jpg'


class State(Enum):

    CONNECTABLE = auto()
    MOVABLE = auto()
    STAY = auto


class Stone(NodePath):

    def __init__(self, parent, grid, tag_name):
        """parent: NodePath
           grid:   Point3
        """
        super().__init__(PandaNode('stone'))
        # self.reparentTo(base.render)
        self.reparentTo(parent)
        self.stone = base.loader.loadModel(STONE_PATH)
        self.stone.setTexture(
            base.loader.loadTexture(PATH_TEXTURE), 1)
        self.stone.reparentTo(self)
        self.setScale(0.42)
        self.pos_z = -0.25
        self.setPos(Point3(grid.x, grid.y, self.pos_z))

        self.stone.find('**/Cylinder').node().setIntoCollideMask(BitMask32.bit(1))
        self.stone.find('**/Cylinder').node().setTag('stone', tag_name)

    def rotate_around(self, pt, axis, angle):
        pos = self.getPos()
        q = Quat()
        q.setFromAxisAngle(angle, axis.normalized())
        r = q.xform(pos - pt)
        rotated_pos = pt + r
        self.setPos(rotated_pos)

        self.setP(self.getP() - angle)


class Stones:

    def __init__(self, size):
        self.data = [[None for _ in range(size)] for _ in range(size)]

    def __getitem__(self, key):
        r, c = key
        return self.data[r][c]

    def __setitem__(self, key, value):
        r, c = key
        self.data[r][c] = value


class Piece(NodePath):

    def __init__(self, board):
        super().__init__(NodePath('pieceRoute'))
        self.reparentTo(base.render)
        self.board = board
        self.piece = [stone for stone in self.create()]

    def create(self):
        for i, (r, c) in enumerate([(0, 0), (0, 1), (1, 1)]):
            grid_center = self.board.grid_center(r, c)
            yield Stone(self, grid_center, str(i))



