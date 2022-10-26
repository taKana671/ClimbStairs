import random
from enum import Enum, auto

from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletBoxShape
from panda3d.bullet import BulletSoftBodyNode, BulletHelper
from panda3d.core import GeomVertexFormat
from panda3d.core import Vec2, Vec3, Point3, LColor, BitMask32
from panda3d.core import NodePath, PandaNode, TransformState, GeomNode, GeomVertexFormat

from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait

from polyhedrons import PolyhedronsCreater, ConesCreater


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


class ObstaclesHolder:

    def __init__(self, length):
        self.data = [None for _ in range(length)]

    def __len__(self):
        return sum(1 for item in self.data if item is not None)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def empty_idx(self):
        for i, item in enumerate(self.data):
            if not item:
                return i
        return None

    def pop(self, key):
        item = self.data[key]
        self.data[key] = None
        return item


class Obstacles(NodePath):

    def __init__(self, world, objects_holder):
        super().__init__(PandaNode('fallenObjects'))
        self.reparentTo(base.render)
        self.world = world
        self.holder = objects_holder

    def start(self):
        if (idx := self.holder.empty_idx()) is not None:
            obj = self.create(str(idx))
            self.holder[idx] = obj
            obj.reparentTo(self)
            self.place(obj)
            self.world.attachRigidBody(obj.node())
            self.apply_force(obj)


class Shapes(Obstacles):

    def __init__(self, stairs, world, character, objects_holder):
        super().__init__(world, objects_holder)
        self.stairs = stairs
        self.character = character
        self.creater = PolyhedronsCreater()

    def place(self, obj):
        stair_center = self.stairs.center(self.stairs.top_stair)
        chara_pos = self.character.getPos()
        end, tip = obj.getTightBounds()
        size = tip - end
        z = stair_center.z + size.z / 2
        pos = Point3(stair_center.x, chara_pos.y, z)
        obj.setPos(pos)

    def apply_force(self, obj):
        force = Vec3(-1, 0, -1).normalized() * 5
        obj.node().applyCentralImpulse(force)

    def create(self, name):
        obj = self.creater.create_polyhedron(name)

        return obj


class Cones(Obstacles):

    def __init__(self, stairs, world, character, objects_holder):
        super().__init__(world, objects_holder)
        self.stairs = stairs
        self.character = character
        self.creater = ConesCreater()
        self.cones = [cone for cone in self.make_cones()]
        self.appeared = False
        self.hidden = True
        self.target_step = -1

    def set_target_step(self):
        start = self.target_step + 1
        if (end := start + 10) >= self.stairs.top_stair:
            end = self.stairs.top_stair
        next_step = random.randint(start, end)
        self.target_step = next_step
        print('next', self.target_step)

    def make_cones(self):
        n = self.stairs.left_end - self.stairs.right_end
        for _ in range(n):
            cone = self.creater.create_cone()
            cone.setR(-90)
            self.world.attachRigidBody(cone.node())
            yield cone

    def appear(self):

        pos = self.stairs.center(self.target_step)

        self.appear_seq = Parallel()
        for i, cone in enumerate(self.cones):
            y = self.stairs.left_end - (i + 0.5)
            cone.setPos(Point3(pos.x + 2, y, pos.z))
            cone.reparentTo(self)
            seq = Sequence(
                cone.posInterval(1, Point3(pos.x + 0.8, y, pos.z + 0.5)),
                Wait(2)
            )
            self.appear_seq.append(seq)

        self.appear_seq.start()

    def hide(self):
        pos = self.stairs.center(self.target_step)

        self.hide_seq = Parallel()

        for i, cone in enumerate(self.cones):
            y = self.stairs.left_end - (i + 0.5)
            seq = Sequence(
                cone.posInterval(1, Point3(pos.x + 2, y, pos.z + 0.5)),
                Func(lambda: cone.detachNode()))
            self.hide_seq.append(seq)
        self.hide_seq.start()



    
