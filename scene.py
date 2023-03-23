from panda3d.bullet import BulletBoxShape, BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3, LColor, Point3, BitMask32
from panda3d.core import NodePath, PandaNode
from panda3d.core import CardMaker

from geommaker import PolyhedronGeomMaker


BLACK = LColor(0.0, 0.0, 0.0, 0.0)
AMETHYST = LColor(0.6, 0.4, 0.68, 1.0)
MEDIUM_PURPLE = LColor(0.57, 0.43, 0.85, 1.0)


class Stairs(NodePath):

    def __init__(self, world):
        super().__init__(PandaNode('stairs'))
        creater = PolyhedronGeomMaker()
        self.geom_node = creater.make_geomnode('cube', (AMETHYST, BLACK))
        self.world = world
        self.top_stair = -1
        self.setup_stairs()

    def setup_stairs(self):
        self.depth = 1
        self.width = 10
        self.stair_y = 0
        self.left_end = int(self.width / 2)
        self.right_end = -self.left_end

        for _ in range(15):
            self.increase()

    def increase(self):
        self.top_stair += 1
        name = f'stairs_{self.top_stair}'
        scale = Vec3(self.depth, self.width, self.top_stair + 1)

        x = self.depth * self.top_stair
        z = self.depth * (self.top_stair + 1) / 2
        pos = Point3(x, self.stair_y, z)

        stair = Rectangle(name, pos, scale, self.geom_node)
        stair.reparentTo(self)
        self.world.attachRigidBody(stair.node())

    def center(self, n):
        if 0 <= n <= self.top_stair:
            return Point3(self.depth * n, self.stair_y, n + 1)
        return None


class Rectangle(NodePath):

    def __init__(self, name, pos, scale, geom_node):
        super().__init__(BulletRigidBodyNode(name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        np.reparentTo(self)
        end, tip = np.getTightBounds()
        self.node().addShape(BulletBoxShape((tip - end) / 2))
        self.node().setRestitution(1)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(4))
        self.setScale(scale)
        self.setPos(pos)


class Floor(NodePath):

    def __init__(self, start, end):
        super().__init__(BulletRigidBodyNode('floor'))
        model = self.create_floor(start, end)
        model.reparentTo(self)
        self.setCollideMask(BitMask32.bit(3) | BitMask32.bit(4))
        self.node().setRestitution(1)
        self.node().addShape(BulletPlaneShape(Vec3.up(), 0))

    def create_floor(self, start, end):
        model = NodePath(PandaNode('floorModel'))
        card = CardMaker('card')
        card.setFrame(-1, 1, -1, 1)

        for y in range(start + 1, end + 1, 2):
            for x in range(start - 3, end + 3, 2):
                g = model.attachNewNode(card.generate())
                g.setP(-90)
                g.setPos(Point3(x, y, 0))

        model.setColor(AMETHYST)
        model.flattenStrong()
        model.setPos(Point3(0, 0, 0))
        return model


class Wall(NodePath):

    def __init__(self, name, normal, y):
        super().__init__(BulletRigidBodyNode(name))
        self.setCollideMask(BitMask32.bit(1))
        self.node().addShape(BulletPlaneShape(normal, 0))
        self.node().setRestitution(1)
        self.setY(y)


class Scene(NodePath):

    def __init__(self, world):
        super().__init__(PandaNode('scene'))
        # self.reparentTo(base.render)
        base.setBackgroundColor(MEDIUM_PURPLE)
        self.make_scene(world)

    def make_scene(self, world):
        self.stairs = Stairs(world)
        self.stairs.reparentTo(self)

        self.floor = Floor(self.stairs.right_end, self.stairs.left_end)
        self.floor.reparentTo(self)
        world.attachRigidBody(self.floor.node())

        self.left_wall = Wall('wall_left', Vec3.back(), self.stairs.left_end)
        self.left_wall.reparentTo(self)
        world.attachRigidBody(self.left_wall.node())

        self.right_wall = Wall('wall_right', Vec3.forward(), self.stairs.right_end)
        self.right_wall.reparentTo(self)
        world.attachRigidBody(self.right_wall.node())
