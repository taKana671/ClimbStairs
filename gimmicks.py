import random
from enum import Enum, auto

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape, BulletSphereShape
from panda3d.core import Vec3, Point3, LColor, BitMask32, Quat
from panda3d.core import NodePath, PandaNode
from direct.showbase.ShowBaseGlobal import globalClock


from geommaker import PolyhedronGeomMaker, PyramidGeomMaker, SphereGeomMaker


RED = LColor(1, 0, 0, 1)
BLUE = LColor(0, 0, 1, 1)
LIGHT_GRAY = LColor(0.75, 0.75, 0.75, 1)


class GimmickRoot(NodePath):

    def __init__(self, name):
        super().__init__(PandaNode(name))
        self.reparentTo(base.render)


class DropGimmicks(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__('drop_gimmicks')
        self.world = world
        self.stairs = stairs
        self.sphere_maker = Spheres()
        self.polh_maker = Polyhedrons()
        self.index = 0

    def drop(self, climber, drop_sphere):
        """Drops sphere or polyhedron.
           Args:
                climer: Characters class instance
                drop_sphere: bool
        """
        drop_stair = climber.stair + 11
        stair_center = self.stairs.center(drop_stair)
        pos = Point3(stair_center.x, climber.getY(), stair_center.z + 3)

        if drop_sphere:
            gimmick = self.sphere_maker.drop_start(self.index, pos)
        else:
            gimmick = self.polh_maker.drop_start(self.index)

        gimmick.setPos(pos)
        gimmick.reparentTo(self)
        self.world.attachRigidBody(gimmick.node())
        self.index += 1

    def delete(self, node, task):
        np = NodePath(node)
        self.world.remove(node)
        np.removeNode()

        return task.done


class Polyhedrons:

    def __init__(self):
        self.polh_maker = PolyhedronGeomMaker()

    def drop_start(self, index):
        geomnode = self.polh_maker.next_geomnode()
        polh = Polyhedron(geomnode, f'polhs_{index}')

        force = Vec3(-1, 0, -1)
        polh.node().applyCentralImpulse(force)

        return polh


class Spheres:

    def __init__(self):
        self.scales = [0.3, 0.4, 0.5, 0.6]
        self.sphere_maker = SphereGeomMaker()

    def drop_start(self, index, pos):
        geomnode = self.sphere_maker.make_geomnode()
        scale = random.choice(self.scales)
        sphere = Sphere(geomnode, f'spheres_{index}', scale)

        force = Vec3(-1, 0, -1) * 2
        apply_pt = pos + Vec3(0, 0, 0.3)
        sphere.node().applyImpulse(force, apply_pt)

        return sphere


class State(Enum):

    READY = auto()
    APPEAR = auto()
    DISAPPEAR = auto()
    MOVE = auto()
    STAY = auto()
    WAIT = auto()


class PopOutGimmiks(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__('popout_gimmicks')
        self.cones = Cones(stairs, world)
        self.cones.reparentTo(self)
        self.saws = CircularSaws(stairs, world)
        self.saws.reparentTo(self)
        self.piles = Piles(stairs, world)
        self.piles.reparentTo(self)

    def pop_out(self, dt, climber):
        self.cones.run(dt, climber, self.saws.stair, self.piles.stair)
        self.saws.run(dt, climber, self.cones.stair, self.piles.stair)
        self.piles.run(dt, climber, self.cones.stair, self.saws.stair)


class EmbeddedPieces(NodePath):

    def __init__(self, name, stairs, world):
        super().__init__(PandaNode(name))
        self.stairs = stairs
        self.world = world
        self.stair = None
        self.state = State.WAIT

    def __init_subclass__(cls):
        super().__init_subclass__()
        for method in ('setup', 'appear', 'disappear'):
            if method not in cls.__dict__:
                raise NotImplementedError()

    def decide_stair(self, start, *stairs):
        """Decide a stair in which to make a gimmick. The stair is between
           start and the 15th from the start.
        """
        self.stair = random.choice(
            [n for n in range(start, start + 15) if n not in stairs])
        self.state = State.READY

    def run(self, dt, climber, *trick_stairs):
        match self.state:
            case State.READY:
                if not climber.climbing:
                    self.state = State.WAIT
                elif climber.is_jump(self.stair):
                    self.setup(climber.getPos())
            case State.APPEAR:
                self.appear(dt)
            case State.STAY:
                self.stay()
            case State.MOVE:
                self.move(dt)
            case State.DISAPPEAR:
                self.disappear(dt)
            case State.WAIT:
                if climber.climbing:
                    self.decide_stair(climber.stair, *trick_stairs)


class Cones(EmbeddedPieces):

    def __init__(self, stairs, world):
        super().__init__('cones', stairs, world)
        self.cone_maker = PyramidGeomMaker()
        self.cones = [cone for cone in self.make_cones()]
        self.timer = 0

    def make_cones(self):
        n = self.stairs.left_end - self.stairs.right_end

        for i in range(n):
            geomnode = self.cone_maker.make_geomnode()
            cone = Pyramid(geomnode, f'cones_{i}')
            yield cone

    def setup(self, chara_pos):
        stair_center = self.stairs.center(self.stair)
        self.x_start = stair_center.x + 2.2
        self.x_stop = stair_center.x + 0.9
        z = stair_center.z + 0.5

        for i, cone in enumerate(self.cones):
            y = self.stairs.left_end - (i + 0.5)
            pos = Point3(self.x_start, y, z)
            cone.setPos(pos)
            cone.reparentTo(self)
            self.world.attach(cone.node())

        self.state = State.APPEAR

    def appear(self, dt):
        distance = dt
        for cone in self.cones:
            cone.setX(cone.getX() - distance)

        if self.cones[-1].getX() < self.x_stop:
            self.timer = globalClock.getFrameCount() + 30
            self.state = State.STAY

    def stay(self):
        if globalClock.getFrameCount() > self.timer:
            self.timer = 0
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt
        for cone in self.cones:
            cone.setX(cone.getX() + distance)

        if self.cones[-1].getX() > self.x_start:
            self.finish()
            self.state = State.WAIT

    def finish(self):
        for cone in self.cones:
            cone.detachNode()
            self.world.remove(cone.node())


class CircularSaws(EmbeddedPieces):

    def __init__(self, stairs, world):
        super().__init__('saws', stairs, world)
        self.creater = PolyhedronGeomMaker()
        self.colors = (RED, BLUE, LIGHT_GRAY)
        self.saws = {key: val for key, val in self.make_saws()}

    def make_saws(self):
        for key in ('left', 'right'):
            geom_node = self.creater.make_geomnode('octagon_prism', self.colors)
            saw = SlimPrism(geom_node, f'saws_{key}')
            yield (key, saw)

    def start_xy(self, stair_center, chara_pos, key):
        delta = -0.1 if key == 'left' else 0.1
        x = stair_center.x + delta

        if self.stairs.right_end / 2 < chara_pos.y < self.stairs.left_end / 2:
            y = stair_center.y
        else:
            if key == 'left':
                y = self.stairs.left_end - 0.7
            else:
                y = self.stairs.right_end + 0.7

        return (x, y)

    def setup(self, chara_pos):
        stair_center = self.stairs.center(self.stair)
        self.z_start = stair_center.z - 1.5
        self.z_stop = stair_center.z

        for key, saw in self.saws.items():
            x, y = self.start_xy(stair_center, chara_pos, key)
            pos = Point3(x, y, self.z_start)
            saw.setPos(pos)
            saw.reparentTo(self)
            self.world.attach(saw.node())

        self.state = State.APPEAR

    def appear(self, dt):
        distance = dt * 3
        for saw in self.saws.values():
            saw.setZ(saw.getZ() + distance)

        if self.saws['right'].getZ() > self.z_stop:
            self.state = State.MOVE

    def move(self, dt):
        distance = dt * 5
        angle = dt * 500

        for key, saw in self.saws.items():
            if key == 'left':
                y = saw.getY() - distance
            else:
                y = saw.getY() + distance
            saw.setY(y)

            q = Quat()
            axis = Vec3.down()
            q.setFromAxisAngle(angle, axis.normalized())
            saw.setQuat(saw, q)

        if self.saws['left'].getY() < self.stairs.right_end + 0.7:
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt * 2
        for saw in self.saws.values():
            saw.setZ(saw.getZ() - distance)

        if self.saws['right'].getZ() < self.z_start:
            self.finish()
            self.state = State.WAIT

    def finish(self):
        for saw in self.saws.values():
            saw.detach_node()
            self.world.remove(saw.node())


class Piles(EmbeddedPieces):

    def __init__(self, stairs, world):
        super().__init__('piles', stairs, world)
        self.polh_maker = PolyhedronGeomMaker()
        self.colors = (BLUE, RED)
        self.piles = [pile for pile in self.make_piles()]
        self.timer = 0

    def make_piles(self):
        for i in range(2):
            geomnode = self.polh_maker.make_geomnode('octahedron', self.colors)
            pile = Octahedron(geomnode, f'piles_{i}')
            yield pile

    def setup(self, chara_pos):
        stair_center = self.stairs.center(self.stair)
        self.z_start = stair_center.z - 1.3
        self.z_stop = stair_center.z

        pos = Point3(stair_center.x, chara_pos.y, self.z_start)

        if self.stairs.right_end + 1 <= chara_pos.y <= self.stairs.left_end - 1:
            positions = [pos + Vec3(0, 0.3, 0), pos + Vec3(0, -0.3, 0)]
        elif self.stairs.left_end - 1 <= chara_pos.y:
            positions = [pos + Vec3(0, 0, 0), pos + Vec3(0, -0.6, 0)]
        elif chara_pos.y <= self.stairs.right_end + 1:
            positions = [pos + Vec3(0, 0.6, 0), pos + Vec3(0, 0, 0)]

        for i, pile in enumerate(self.piles):
            pos = positions[i]
            pile.setPos(pos)
            pile.reparentTo(self)
            self.world.attach(pile.node())

        self.state = State.APPEAR

    def rotate(self, pile, angle):
        q = Quat()
        axis = Vec3.up()
        q.setFromAxisAngle(angle, axis.normalized())
        pile.setQuat(pile, q)

    def appear(self, dt):
        distance = dt
        angle = dt * 1000

        for pile in self.piles:
            pile.setZ(pile.getZ() + distance)
            self.rotate(pile, angle)

        if self.piles[-1].getZ() > self.z_stop:
            self.timer = globalClock.getFrameCount() + 30
            self.state = State.STAY

    def stay(self):
        if globalClock.getFrameCount() > self.timer:
            self.timer = 0
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt
        angle = dt * 1000

        for pile in self.piles:
            pile.setZ(pile.getZ() - distance)
            self.rotate(pile, angle)

        if self.piles[-1].getZ() < self.z_start:
            self.finish()
            self.state = State.WAIT

    def finish(self):
        for pile in self.piles:
            pile.detachNode()
            self.world.remove(pile.node())


class Polyhedron(NodePath):

    def __init__(self, geom_node, name):
        super().__init__(BulletRigidBodyNode(name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setMass(1)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2) | BitMask32.bit(3))
        self.setScale(0.7)


class Sphere(NodePath):

    def __init__(self, geom_node, node_name, scale):
        super().__init__(BulletRigidBodyNode(node_name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        end, tip = np.getTightBounds()
        size = tip - end
        self.node().addShape(BulletSphereShape(size.z / 2))
        self.node().setMass(scale * 10)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2) | BitMask32.bit(3))
        self.setScale(scale)


class Pyramid(NodePath):

    def __init__(self, geom_node, node_name):
        super().__init__(BulletRigidBodyNode(node_name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(2))
        self.setColor(LIGHT_GRAY)
        self.setScale(0.7)
        self.setR(-90)
        self.node().setKinematic(True)


class SlimPrism(NodePath):

    def __init__(self, geom_node, node_name):
        super().__init__(BulletRigidBodyNode(node_name))
        self.np = self.attachNewNode(geom_node)
        self.np.setTwoSided(True)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(2))
        self.setScale(0.5, 0.5, 0.3)
        self.setHpr(90, 90, 0)
        self.node().setKinematic(True)


class Octahedron(NodePath):

    def __init__(self, geom_node, node_name):
        super().__init__(BulletRigidBodyNode(node_name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(2))
        self.setScale(0.3, 0.3, 1.2)
        self.node().setKinematic(True)