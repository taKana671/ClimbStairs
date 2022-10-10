import random
from enum import Enum, auto

from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletBoxShape
from panda3d.core import Vec2, Vec3, Point3, LColor, BitMask32
from panda3d.core import NodePath, PandaNode, TransformState


PATH_SPHERE = 'models/sphere/sphere'
PATH_BOX = 'models/cube/cube'
PATH_CARNSX = 'models/carnsx/carnsx'


class Colors(int, Enum):

    LIME = (0, LColor(0, 1, 0, 1))
    AQUAMARINE = (1, LColor(0.49, 1, 0.83, 1))
    YELLOW = (2, LColor(1, 1, 0, 1))
    GREENYELLOW = (3, LColor(0.67, 1, 0.18, 1))

    def __new__(cls, id_, color):
        obj = int.__new__(cls, id_)
        obj._value_ = id_
        obj.color = color
        return obj

    @classmethod
    def select(cls):
        n = random.randint(0, 3)
        obj = cls(n)
        return obj.color


class Obstacles(NodePath):

    def __init__(self, stairs, world):
        super().__init__(PandaNode('obstacles'))
        self.reparentTo(base.render)
        self.stairs = stairs
        self.world = world


class ShapeObstacles(Obstacles):

    def __init__(self, stairs, world):
        super().__init__(stairs, world)
        self.scales = [0.1, 0.2]
        self.shapes = [Sphere, Box]

    def place(self, obj):
        stair_center = self.stairs.top_center()
        y = random.randint(self.stairs.right_edge, self.stairs.left_edge)
        z = stair_center.z + obj.size.z / 2
        pos = Point3(stair_center.x, y, z)
        obj.setPos(pos)

    def apply_force(self, obj):
        y = random.randint(-1, 1)
        z = random.randint(-1, 1)
        # n = 10 if y == 0 else 20
        force = Vec3(-1, y, z).normalized() * 10
        obj.node().applyCentralImpulse(force)

    def start(self):
        color = Colors.select()
        scale = random.choice(self.scales)
        mass = scale * 10
        shape_class = random.choice(self.shapes)
        obj = shape_class(color, scale, mass)
        obj.reparentTo(self)

        self.place(obj)
        self.world.attachRigidBody(obj.node())
        self.apply_force(obj)


class Sphere(NodePath):

    def __init__(self, color, scale, mass):
        super().__init__(BulletRigidBodyNode('sphere'))
        sphere = base.loader.loadModel(PATH_SPHERE)
        sphere.setScale(scale)
        sphere.reparentTo(self)
        end, tip = sphere.getTightBounds()
        self.size = tip - end
        self.node().addShape(BulletSphereShape(self.size.z / 2))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(mass)
        self.node().setRestitution(0.7)
        self.setColor(color)


class Box(NodePath):

    def __init__(self, color, scale, mass):
        super().__init__(BulletRigidBodyNode('box'))
        box = base.loader.loadModel(PATH_BOX)
        box.setScale(scale)
        box.reparentTo(self)
        end, tip = box.getTightBounds()
        self.size = tip - end
        self.node().addShape(BulletBoxShape(self.size / 2))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(mass)
        self.node().setRestitution(0.7)
        self.setColor(color)


class CarNsx(NodePath):

    def __init__(self, top_stair):
        super().__init__(BulletRigidBodyNode('sphere'))
        self.reparentTo(base.render)
        sphere = base.loader.loadModel(PATH_CARNSX)
        sphere.reparentTo(self)

        end, tip = sphere.getTightBounds()
        size = tip - end
        half = size / 2
        center = tip - half

        self.node().addShape(BulletBoxShape(half), TransformState.makePos(center))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(1)
        self.node().setRestitution(0.7)
        self.setScale(0.5)
        # self.setH(-90)
        self.setR(90)

        pos = Point3(top_stair.x, top_stair.y, top_stair.z + 0.6)
        self.setPos(pos)
