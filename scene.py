from panda3d.bullet import BulletBoxShape, BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3, LColor, Point3, BitMask32
from panda3d.core import NodePath, PandaNode
from panda3d.core import CardMaker

from geommaker import PolyhedronGeomMaker


BLACK = LColor(0.0, 0.0, 0.0, 0.0)
AMETHYST = LColor(0.6, 0.4, 0.68, 1.0)


class Stairs(NodePath):

    def __init__(self, scene, world):
        super().__init__(PandaNode('stairs'))
        self.reparentTo(scene)
        cube_root = NodePath(PandaNode('cubeRoot'))

        creater = PolyhedronGeomMaker()
        geom_node = creater.make_geomnode('cube', [AMETHYST, BLACK])
        self.np_cube = cube_root.attachNewNode(geom_node)
        self.np_cube.setTwoSided(True)

        self.world = world
        self.top_stair = -1
        self.edge = 1
        self.stairs = []
        self.setup_stairs()

        stair = self.stairs[self.top_stair]
        end, tip = stair.getTightBounds()
        self.left_end = int(tip.y)
        self.right_end = int(end.y)

    def setup_stairs(self):
        for _ in range(15):
            self.increase()

    def increase(self):
        self.top_stair += 1
        name = f'stairs_{self.top_stair}'
        scale = Vec3(1, 12, self.top_stair + 1)
        pos = Point3(self.edge * self.top_stair, 0, self.edge / 2 * (self.top_stair + 1))
        stair = Cube(name, pos, scale, self.np_cube)
        stair.reparentTo(self)
        self.world.attachRigidBody(stair.node())
        self.stairs.append(stair)

    def center(self, n):
        if n < len(self.stairs):
            return Point3(self.edge * n, 0, n + 1)
        return None

    # 0 LPoint3f(0, 0, 1)
    # 1 LPoint3f(1, 0, 2)
    # 2 LPoint3f(2, 0, 3)
    # 3 LPoint3f(3, 0, 4)
    # 4 LPoint3f(4, 0, 5)
    # 5 LPoint3f(5, 0, 6)
    # 6 LPoint3f(6, 0, 7)
    # 7 LPoint3f(7, 0, 8)
    # 8 LPoint3f(8, 0, 9)
    # 9 LPoint3f(9, 0, 10)
    # 10 LPoint3f(10, 0, 11)
    # 11 LPoint3f(11, 0, 12)
    # 12 LPoint3f(12, 0, 13)
    # 13 LPoint3f(13, 0, 14)
    # 14 LPoint3f(14, 0, 15)


class Cube(NodePath):

    def __init__(self, name, pos, scale, np_cube):
        super().__init__(BulletRigidBodyNode(name))
        self.cube = np_cube.copyTo(self)
        end, tip = self.cube.getTightBounds()
        self.node().addShape(BulletBoxShape((tip - end) / 2))
        self.node().setRestitution(1)
        self.setCollideMask(BitMask32.bit(1))
        self.setScale(scale)
        self.setPos(pos)


class Floor(NodePath):

    def __init__(self, scene):
        super().__init__(BulletRigidBodyNode('floor'))
        self.reparentTo(scene)
        model = self.create_floor(scene.stairs)
        model.reparentTo(self)
        self.setCollideMask(BitMask32.bit(1))
        self.node().addShape(BulletPlaneShape(Vec3.up(), 0))

    def create_floor(self, stairs):
        model = NodePath(PandaNode('floorModel'))
        card = CardMaker('card')
        card.setFrame(-1, 1, -1, 1)
        start, end = stairs.right_end, stairs.left_end

        for y in range(start + 1, end, 2):
            for x in range(start - 1, 0, 2):
                g = model.attachNewNode(card.generate())
                g.setP(-90)
                g.setPos(Point3(x, y, 0))

        model.setColor(LColor(0.6, 0.4, 0.68, 1.0))
        model.flattenStrong()
        model.setPos(Point3(0, 0, 0))
        return model


class Wall(NodePath):

    def __init__(self, scene, name, normal, y):
        super().__init__(BulletRigidBodyNode(name))
        self.reparentTo(scene)
        self.setCollideMask(BitMask32.bit(1))
        self.node().addShape(BulletPlaneShape(normal, 0))
        self.node().setRestitution(1)
        self.setY(y)


class Scene(NodePath):

    def __init__(self, world):
        super().__init__(PandaNode('scene'))
        self.reparentTo(base.render)
        base.setBackgroundColor(LColor(0.57, 0.43, 0.85, 1.0))  # MediumPurple

        self.stairs = Stairs(self, world)
        self.floor = Floor(self)
        self.left_wall = Wall(self, 'left_wall', Vec3.back(), self.stairs.left_end)
        self.right_wall = Wall(self, 'right_wall', Vec3.forward(), self.stairs.right_end)

        world.attachRigidBody(self.floor.node())
        world.attachRigidBody(self.left_wall.node())
        world.attachRigidBody(self.right_wall.node())
