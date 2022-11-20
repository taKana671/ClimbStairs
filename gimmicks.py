import random

from collections import UserList
from enum import Enum, auto

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape, BulletSphereShape
from panda3d.core import Vec3, Point3, LColor, BitMask32
from panda3d.core import NodePath, PandaNode
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.showbase.ShowBaseGlobal import globalClock


from geommaker import PolyhedronGeomMaker, PyramidGeomMaker, SphereGeomMaker


RED = LColor(1, 0, 0, 1)
BLUE = LColor(0, 0, 1, 1)
LIGHT_GRAY = LColor(0.75, 0.75, 0.75, 1)


class Holder(UserList):

    def __init__(self, data):
        super().__init__(data)

    def id(self):
        for i, item in enumerate(self.data):
            if not item:
                return i
        return None

    def pop(self, i):
        item = self.data[i]
        self.data[i] = None
        return item

    def find_space(self):
        for i, item in enumerate(self.data):
            if not item:
                return i
        return None


class GimmickRoot(NodePath):

    def __init__(self):
        super().__init__(PandaNode('gimmikRoot'))
        self.reparentTo(base.render)


class DropGimmicks(GimmickRoot):

    def __init__(self, stairs, world, capacity):
        super().__init__()
        self.world = world
        self.stairs = stairs
        self.holder = Holder([None for _ in range(capacity)])

    def drop(self, snowman_stair, snowman_pos):
        if (index := self.holder.find_space()) is not None:
            drop_stair = snowman_stair + 11
            stair_center = self.stairs.center(drop_stair)

            pos = Point3(stair_center.x, snowman_pos.y, stair_center.z + 3)
            self.drop_start(index, pos)

    def delete(self, name, task):
        index = name.split('_')[1]
        np = self.holder.pop(int(index))
        self.world.remove(np.node())
        np.removeNode()
        return task.done

    def drop_start(self, index, pos):
        """Override in subclasses.
        """
        raise NotImplementedError()


class Polyhedrons(DropGimmicks):

    def __init__(self, stairs, world, capacity):
        super().__init__(stairs, world, capacity)
        self.polh_maker = PolyhedronGeomMaker()

    def drop_start(self, index, pos):
        geomnode = self.polh_maker.next_geomnode()
        polh = Polyhedron(geomnode, f'polhs_{index}')
        polh.setPos(pos)
        polh.reparentTo(self)
        self.holder[index] = polh

        self.world.attachRigidBody(polh.node())
        force = Vec3(-1, 0, -1)
        polh.node().applyCentralImpulse(force)


class Spheres(DropGimmicks):

    def __init__(self, stairs, world, capacity):
        super().__init__(stairs, world, capacity)
        self.scales = [0.3, 0.4, 0.5, 0.6]
        self.sphere_maker = SphereGeomMaker()

    def drop_start(self, index, pos):
        geomnode = self.sphere_maker.make_geomnode()
        scale = random.choice(self.scales)
        sphere = Sphere(geomnode, f'spheres_{index}', scale)
        self.setPos(pos)
        sphere.reparentTo(self)
        self.holder[index] = sphere

        self.world.attachRigidBody(sphere.node())
        force = Vec3(-1, 0, -1) * 2
        apply_pt = pos + Vec3(0, 0, 0.3)
        sphere.node().applyImpulse(force, apply_pt)


class State(Enum):

    READY = auto()
    APPEAR = auto()
    DISAPPEAR = auto()
    MOVE = auto()
    STAY = auto()
    WAIT = auto()


class EmbeddedGimmiks(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__()
        self.stairs = stairs
        self.world = world
        self.stair = None
        self.state = State.WAIT

        self.reset = False

    def decide_stair(self, start, *stairs):
        """Decide a stair in which to make a gimmick. The stair is between
           start and the 10th from the start.
        """
        self.stair = random.choice(
            [n for n in range(start, start + 10) if n not in stairs]
        )
        self.state = State.READY

        print(self.__class__.__name__, self.stair, 'start:', start, 'end', start + 10)

    def run(self, dt, snowman, *trick_stairs):
        if self.state == State.READY:
            # if self.stair > snowman.stair + 10:
            if not snowman.climbing:
                print(self.__class__.__name__, 'reset', snowman.climbing)
                self.reset = True
                self.state = State.WAIT
            elif snowman.is_jump(self.stair):
                self.setup(snowman.getPos())
        elif self.state == State.APPEAR:
            self.appear(dt)
        elif self.state == State.STAY:
            self.stay()
        elif self.state == State.MOVE:
            self.move(dt)
        elif self.state == State.DISAPPEAR:
            self.disappear(dt)
        elif self.state == State.WAIT:
            # self.decide_stair(snowman.stair, self.stair, *trick_stairs)
            if snowman.climbing:
                if self.reset:
                    print('reset', self.__class__.__name__, 'snowman stair', snowman.stair, snowman.climbing)
                    self.reset = False
                self.decide_stair(snowman.stair, *trick_stairs)


class Cones(EmbeddedGimmiks):

    def __init__(self, stairs, world):
        super().__init__(stairs, world)
        self.cone_maker = PyramidGeomMaker()
        n = self.stairs.left_end - self.stairs.right_end
        self.cones = [None for _ in range(n)]
        self.timer = 0

    def make_cone(self, i, pos):
        geomnode = self.cone_maker.make_geomnode()
        cone = Pyramid(geomnode, f'cones_{i}', pos)
        self.world.attachRigidBody(cone.node())

        return cone

    def setup(self, chara_pos):
        stair_center = self.stairs.center(self.stair)
        self.x_start = stair_center.x + 2.2
        self.x_stop = stair_center.x + 0.9
        z = stair_center.z + 0.5

        for i, cone in enumerate(self.cones):
            y = self.stairs.left_end - (i + 0.5)
            pos = Point3(self.x_start, y, z)
            if cone:
                cone.setPos(pos)
            else:
                cone = self.make_cone(i, pos)
                self.cones[i] = cone
            cone.reparentTo(self)

        self.state = State.APPEAR

    def appear(self, dt):
        distance = dt
        for cone in self.cones:
            x = cone.getX() - distance
            cone.setX(x)

        if x < self.x_stop:
            self.timer = globalClock.getFrameCount() + 30
            self.state = State.STAY

    def stay(self):
        if globalClock.getFrameCount() > self.timer:
            self.timer = 0
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt
        for cone in self.cones:
            x = cone.getX() + distance
            cone.setX(x)

        if x > self.x_start:
            self.finish()
            self.state = State.WAIT

    def finish(self):
        for cone in self.cones:
            cone.detachNode()


class CircularSaws(EmbeddedGimmiks):

    def __init__(self, stairs, world):
        super().__init__(stairs, world)
        self.creater = PolyhedronGeomMaker()
        self.colors = (RED, BLUE, LIGHT_GRAY)
        self.saws = dict(left=None, right=None)

    def make_saw(self, key, pos):
        geom_node = self.creater.make_geomnode('octagon_prism', self.colors)
        saw = SlimPrism(geom_node, f'saws_{key}', pos)
        self.world.attachRigidBody(saw.node())

        return saw

    def start_xy(self, stair_center, key, from_center):
        if key == 'left':
            x = stair_center.x - 0.1
        else:
            x = stair_center.x + 0.1

        if from_center:
            y = stair_center.y
        else:
            if key == 'left':
                y = self.stairs.left_end - 0.5
            else:
                y = self.stairs.right_end + 0.5

        return x, y

    def setup(self, chara_pos):
        stair_center = self.stairs.center(self.stair)
        self.z_start = stair_center.z - 1.2
        self.z_stop = stair_center.z

        from_center = False
        if self.stairs.right_end / 2 < chara_pos.y < self.stairs.left_end / 2:
            from_center = True

        for key, saw in self.saws.items():
            x, y = self.start_xy(stair_center, key, from_center)
            pos = Point3(x, y, self.z_start)
            if saw:
                saw.setPos(pos)
            else:
                saw = self.make_saw(key, pos)
                self.saws[key] = saw
            saw.reparentTo(self)

        self.state = State.APPEAR

    def appear(self, dt):
        distance = dt * 2
        for saw in self.saws.values():
            z = saw.getZ() + distance
            saw.setZ(z)

        if z > self.z_stop:
            self.state = State.MOVE

    def move(self, dt):
        distance = dt * 2
        angle = dt * 100

        for key, saw in self.saws.items():
            if key == 'left':
                y = saw.getY() - distance
            else:
                y = saw.getY() + distance
            saw.setY(y)
            saw.np.setH(saw.np.getH() + angle)

        if self.saws['left'].getY() < self.stairs.right_end + 0.5:
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt * 2

        for saw in self.saws.values():
            z = saw.getZ() - distance
            saw.setZ(z)

        if z < self.z_start:
            self.finish()
            self.state = State.WAIT

    def finish(self):
        for saw in self.saws.values():
            saw.detach_node()


class Polyhedron(NodePath):

    def __init__(self, geom_node, name):
        super().__init__(BulletRigidBodyNode(name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        np.reparentTo(self)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setMass(1)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2))
        self.setScale(0.7)


class Pyramid(NodePath):

    def __init__(self, geom_node, node_name, pos):
        super().__init__(BulletRigidBodyNode(node_name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        np.reparentTo(self)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(2))
        # self.setCollideMask(BitMask32.allOn())
        self.setColor(LIGHT_GRAY)
        self.setScale(0.7)
        self.setR(-90)
        self.setPos(pos)
        self.node().setKinematic(True)


class SlimPrism(NodePath):

    def __init__(self, geom_node, node_name, pos):
        super().__init__(BulletRigidBodyNode(node_name))
        self.np = self.attachNewNode(geom_node)
        self.np.setTwoSided(True)
        self.np.reparentTo(self)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setRestitution(0.7)
        # self.setCollideMask(BitMask32.allOn())
        self.setCollideMask(BitMask32.bit(2))
        self.setScale(0.5, 0.5, 0.3)
        self.setHpr(90, 90, 0)
        self.setPos(pos)
        self.node().setKinematic(True)


class Sphere(NodePath):

    def __init__(self, geom_node, node_name, scale):
        super().__init__(BulletRigidBodyNode(node_name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        np.reparentTo(self)
        end, tip = np.getTightBounds()
        size = tip - end
        self.node().addShape(BulletSphereShape(size.z / 2))
        self.node().setMass(scale * 10)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2))
        self.setScale(scale)