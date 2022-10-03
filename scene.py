from direct.showbase.ShowBase import ShowBase
from panda3d.core import PandaNode, NodePath, CardMaker, TransparencyAttrib
from panda3d.core import Vec3, Point3, LColor


SQUARE_PATH = 'models/square/square'
SKY_PATH = 'models/blue-sky/blue-sky-sphere'
GROUND_PATH = 'textures/ground.jpg'
PATH_AXIS = 'models/zup-axis'


class Axis(NodePath):

    def __init__(self):
        super().__init__(PandaNode('axis'))
        self.reparentTo(base.render)
        axis = base.loader.loadModel(PATH_AXIS)
        axis.setScale(0.5)
        axis.reparentTo(self)


class Stone(NodePath):

    def __init__(self):
        super().__init__(PandaNode('stone'))
        self.reparentTo(base.render)
        self.stone = base.loader.loadModel('models/cylinder/cylinder')
        self.stone.setTexture(
            base.loader.loadTexture('textures/envir-rock2.jpg'), 1)
        self.stone.reparentTo(self)
        self.setScale(0.42)
        self.pos_z = -0.25

        # self.setPos(Point3(-2.87, 3.28, -0.25))
        # self.setPos(Point3(-2.87, -2.46, -0.25))
        # self.setPos(Point3(-2.87 - 0.82, 3.28, -0.25))


class Sky(NodePath):

    def __init__(self):
        super().__init__(PandaNode('sky'))
        self.reparentTo(base.render)
        sky = base.loader.loadModel(SKY_PATH)
        self.setColor(2, 2, 2, 1)
        self.setScale(0.02)
        sky.reparentTo(self)


class Board(NodePath):

    def __init__(self):
        super().__init__(PandaNode('board'))
        self.reparentTo(base.render)
        self.edge = 0.82
        self.start_x = -3.5
        self.start_y = -3
        self.pos_z = -1
        self.size = 8

        self.create_board()

    def create_board(self):
        for i in range(64):
            square = base.loader.loadModel(SQUARE_PATH)
            square.reparentTo(self)
            square.setScale(0.25)
            square.setP(-90)

            c = i % 8
            r = i // 8

            pos = Point3(
                (c + self.start_x) * self.edge, (r + self.start_y) * self.edge, self.pos_z)
            color = self.get_color(r, c)
            # print(pos)
            square.setPos(pos)
            square.setColor(color)

    def get_color(self, r, c):
        if ((r % 2) + c) % 2:
            return LColor(1, 1, 1, 1)
        else:
            return LColor(0.82, 0.82, 0.82, 1)


class Pond(NodePath):

    def __init__(self):
        super().__init__(PandaNode('pond'))
        self.reparentTo(base.render)
        pond = base.loader.loadModel('models/cube/cube')
        pond.reparentTo(self)
        self.setTransparency(TransparencyAttrib.M_alpha)
        # self.setH(45)
        self.setScale(10, 3, 3)
        self.setColor(LColor(0.25, 0.41, 1, 0.4))
        self.setPos(Point3(0, 0, -5))


class Scene:

    def __init__(self):
        # axis = Axis()
        self.pond = Pond()
        self.board = Board()
        self.sky = Sky()
        self.start_point()
        self.goal_point(5)

    def start_point(self, r=7):
        self.start_stone = Stone()
        pos = Point3(
            self.board.start_x * self.board.edge - self.board.edge,
            (r + self.board.start_y) * self.board.edge,
            self.start_stone.pos_z
        )
        self.start_stone.setPos(pos)

    def goal_point(self, r):
        self.goal_stone = Stone()
        pos = Point3(
            (8 + self.board.start_x) * self.board.edge,
            (r + self.board.start_y) * self.board.edge,
            self.start_stone.pos_z
        )
        self.goal_stone.setPos(pos)



if __name__ == '__main__':
    base = ShowBase()
    base.disableMouse()
    base.camera.setPosHpr(0, -12, 8, 0, -35, 0)  # 20, -20, 5
    # base.camera.setPos(20, -20, 8)  # 20, -20, 5
    # base.camera.setP(-80)
    # base.camera.lookAt(0, 0, 0)  # 5, 0, 3
    # board = Board()
    scene = Scene()
    # stone = Stone()
    base.run()