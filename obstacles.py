import random
from enum import Enum, auto

from panda3d.core import Vec3, Point3, LColor
from panda3d.core import NodePath, PandaNode
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait

from polyhedrons import PolyhedronsCreater, ConesCreater, CircularSaw


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


class GimmickRoot(NodePath):

    def __init__(self):
        super().__init__(PandaNode('gimmikRoot'))
        self.reparentTo(base.render)


class TumblingObjects(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__()
        self.world = world
        self.stairs = stairs
        self.creater = PolyhedronsCreater()

    def start(self, node_name, chara_pos):
        polh = self.creater.make_polyhedron(node_name)
        polh.reparentTo(self)
        self.place(polh, chara_pos)
        self.world.attachRigidBody(polh.node())
        self.apply_force(polh)
        return polh

    def place(self, polh, chara_pos):
        stair_center = self.stairs.center(self.stairs.top_stair)
        z = stair_center.z + 2
        pos = Point3(stair_center.x, chara_pos.y, z)
        polh.setPos(pos)

    def apply_force(self, polh):
        force = Vec3(-1, 0, -1).normalized() * 5
        polh.node().applyCentralImpulse(force)


class Gimmick(Enum):

    APPEARING = auto()
    DISAPPEARING = auto()
    DISAPPEAR = auto()


class Cones(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__()
        self.stairs = stairs
        self.world = world
        self.creater = ConesCreater()
        self.cones = [cone for cone in self.make_cones()]
        self.state = None
        self.target_step = -1
        self.set_target_step()

    def make_cones(self):
        n = self.stairs.left_end - self.stairs.right_end
        for i in range(n):
            cone = self.creater.make_cone(f'cones_{i}')
            cone.setR(-90)
            self.world.attachRigidBody(cone.node())
            yield cone

    def set_target_step(self):
        start = self.target_step + 1
        if (end := start + 10) >= self.stairs.top_stair:
            end = self.stairs.top_stair

        next_step = random.randint(start, end)
        self.target_step = next_step
        self.state = Gimmick.DISAPPEAR
        print('next', self.target_step)

    def _make_appear_seq(self, pos):
        for i, cone in enumerate(self.cones):
            y = self.stairs.left_end - (i + 0.5)
            cone.setPos(Point3(pos.x + 2, y, pos.z))
            cone.reparentTo(self)
            seq = Sequence(
                cone.posInterval(1, Point3(pos.x + 0.8, y, pos.z + 0.5)),
                Wait(2)
            )
            yield seq

    def appear(self):
        pos = self.stairs.center(self.target_step)
        self.appear_seq = Parallel(*[seq for seq in self._make_appear_seq(pos)])
        self.appear_seq.start()
        self.state = Gimmick.APPEARING

    def _make_disappear_seq(self, pos):
        for i, cone in enumerate(self.cones):
            y = self.stairs.left_end - (i + 0.5)
            seq = Sequence(
                cone.posInterval(1, Point3(pos.x + 2, y, pos.z + 0.5)),
                Func(lambda: cone.detachNode())
            )
            yield seq

    def disappear(self):
        pos = self.stairs.center(self.target_step)
        self.disappear_seq = Parallel(*[seq for seq in self._make_disappear_seq(pos)])
        self.disappear_seq.start()
        self.state = Gimmick.DISAPPEARING


class CircularSaws(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__()
        self.stairs = stairs
        self.world = world
        self.creater = PolyhedronsCreater()
        self.make_circular_saw()

    def make_circular_saw(self):
        colors = [
            LColor(1, 0, 0, 1),  # red
            LColor(0, 0, 1, 1),
            LColor(0.75, 0.75, 0.75, 1),  # light gray
        ]
        geom_node = self.creater.get_geom_node(
            'octagon_prism', colors
        )
        self.saw = CircularSaw('saw', geom_node)
        self.saw.reparentTo(self)
        self.world.attachRigidBody(self.saw.node())
        self.saw.setPos(-2, 4, 0)


