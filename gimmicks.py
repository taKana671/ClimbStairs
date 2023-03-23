import random
from enum import Enum, auto

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape, BulletSphereShape
from panda3d.core import Vec3, Point3, LColor, BitMask32, Quat
from panda3d.core import NodePath, PandaNode
from direct.showbase.ShowBaseGlobal import globalClock

from geommaker import PolyhedronGeomMaker, SphereGeomMaker
from geommaker import PyramidGeomMaker, TorusGeomMaker


RED = LColor(1, 0, 0, 1)
BLUE = LColor(0, 0, 1, 1)
LIGHT_GRAY = LColor(0.75, 0.75, 0.75, 1)


class GimmickRoot(NodePath):

    def __init__(self, name):
        super().__init__(PandaNode(name))
        self.reparent_to(base.render)


class DropGimmicks(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__('drop_gimmicks')
        self.world = world
        self.stairs = stairs
        self.index = 0
        self.sphere_scales = [0.3, 0.4, 0.5, 0.6]

        self.sphere_maker = SphereGeomMaker()
        self.polh_maker = PolyhedronGeomMaker()
        self.torus_maker = TorusGeomMaker()

    def drop(self, climber, next_drop):
        """Drops sphere, polyhedron, or torus.
           Args:
                climer: Characters class instance
                drop_sphere: int
        """
        drop_stair = climber.current_stair + 11
        stair_center = self.stairs.center(drop_stair)
        pos = Point3(stair_center.x, climber.get_y(), stair_center.z + 3)

        match next_drop:
            case 0:
                geomnode = self.sphere_maker.make_geomnode()
                scale = random.choice(self.sphere_scales)
                obj = Sphere(geomnode, self.index, scale, pos)
            case 1:
                geomnode = self.polh_maker.next_geomnode()
                obj = Polyhedron(geomnode, self.index)
            case 2:
                geomnode = self.torus_maker.make_geomnode()
                obj = Torus(geomnode, self.index)

        obj.set_pos(pos)
        obj.reparent_to(self)
        self.world.attach(obj.node())
        self.index += 1

    def delete(self, node, task):
        np = NodePath(node)
        self.world.remove(node)
        np.remove_node()

        return task.done


class Polyhedron(NodePath):

    def __init__(self, geomnode, index):
        super().__init__(BulletRigidBodyNode(f'polh_{index}'))
        np = self.attach_new_node(geomnode)
        np.set_two_sided(True)
        shape = BulletConvexHullShape()
        shape.add_geom(geomnode.get_geom(0))
        self.node().add_shape(shape)
        self.node().set_mass(1)
        self.node().set_restitution(0.7)
        self.set_collide_mask(BitMask32.bit(1) | BitMask32.bit(2) | BitMask32.bit(3))
        self.set_scale(0.7)

        force = Vec3(-1, 0, -1)
        self.node().apply_central_impulse(force)


class Sphere(NodePath):

    def __init__(self, geomnode, index, scale, pos):
        super().__init__(BulletRigidBodyNode(f'sphere_{index}'))
        np = self.attach_new_node(geomnode)
        np.set_two_sided(True)
        end, tip = np.get_tight_bounds()
        size = tip - end
        self.node().add_shape(BulletSphereShape(size.z / 2))
        self.node().set_mass(scale * 10)
        self.node().set_restitution(0.7)
        self.set_collide_mask(BitMask32.bit(1) | BitMask32.bit(2) | BitMask32.bit(3))
        self.set_scale(scale)

        force = Vec3(-1, 0, -1) * 2
        apply_pt = pos + Vec3(0, 0, 0.3)
        self.node().apply_impulse(force, apply_pt)


class Torus(NodePath):

    def __init__(self, geomnode, index):
        super().__init__(BulletRigidBodyNode(f'torus_{index}'))
        np = self.attach_new_node(geomnode)
        np.set_two_sided(True)
        shape = BulletConvexHullShape()
        shape.add_geom(geomnode.get_geom(0))
        self.node().add_shape(shape)
        self.node().set_mass(1)
        self.node().set_restitution(0.7)
        self.set_collide_mask(BitMask32.bit(1) | BitMask32.bit(2) | BitMask32.bit(3))
        self.set_scale(0.3)

        self.node().apply_torque_impulse(Vec3.up() * 10)
        self.node().apply_central_impulse(Vec3.left() * 5)


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
        self.cones.reparent_to(self)
        self.saws = CircularSaws(stairs, world)
        self.saws.reparent_to(self)
        self.piles = Piles(stairs, world)
        self.piles.reparent_to(self)

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
                    self.setup(climber.get_pos())
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
                    self.decide_stair(climber.current_stair, *trick_stairs)


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
            cone.set_pos(pos)
            cone.reparent_to(self)
            self.world.attach(cone.node())

        self.state = State.APPEAR

    def appear(self, dt):
        distance = dt
        for cone in self.cones:
            cone.set_x(cone.get_x() - distance)

        if self.cones[-1].get_x() < self.x_stop:
            self.timer = globalClock.get_frame_count() + 30
            self.state = State.STAY

    def stay(self):
        if globalClock.get_frame_count() > self.timer:
            self.timer = 0
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt
        for cone in self.cones:
            cone.set_x(cone.get_x() + distance)

        if self.cones[-1].getX() > self.x_start:
            self.finish()
            self.state = State.WAIT

    def finish(self):
        for cone in self.cones:
            cone.detach_node()
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
            saw.set_pos(pos)
            saw.reparent_to(self)
            self.world.attach(saw.node())

        self.state = State.APPEAR

    def appear(self, dt):
        distance = dt * 3
        for saw in self.saws.values():
            saw.set_z(saw.get_z() + distance)

        if self.saws['right'].get_z() > self.z_stop:
            self.state = State.MOVE

    def move(self, dt):
        distance = dt * 5
        angle = dt * 500

        for key, saw in self.saws.items():
            if key == 'left':
                y = saw.get_y() - distance
            else:
                y = saw.get_y() + distance
            saw.set_y(y)

            q = Quat()
            axis = Vec3.down()
            q.set_from_axis_angle(angle, axis.normalized())
            saw.set_quat(saw, q)

        if self.saws['left'].get_y() < self.stairs.right_end + 0.7:
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt * 2
        for saw in self.saws.values():
            saw.set_z(saw.get_z() - distance)

        if self.saws['right'].get_z() < self.z_start:
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
            pile.set_pos(pos)
            pile.reparent_to(self)
            self.world.attach(pile.node())

        self.state = State.APPEAR

    def rotate(self, pile, angle):
        q = Quat()
        axis = Vec3.up()
        q.set_from_axis_angle(angle, axis.normalized())
        pile.set_quat(pile, q)

    def appear(self, dt):
        distance = dt
        angle = dt * 1000

        for pile in self.piles:
            pile.set_z(pile.get_z() + distance)
            self.rotate(pile, angle)

        if self.piles[-1].getZ() > self.z_stop:
            self.timer = globalClock.get_frame_count() + 30
            self.state = State.STAY

    def stay(self):
        if globalClock.get_frame_count() > self.timer:
            self.timer = 0
            self.state = State.DISAPPEAR

    def disappear(self, dt):
        distance = dt
        angle = dt * 1000

        for pile in self.piles:
            pile.set_z(pile.get_z() - distance)
            self.rotate(pile, angle)

        if self.piles[-1].get_z() < self.z_start:
            self.finish()
            self.state = State.WAIT

    def finish(self):
        for pile in self.piles:
            pile.detach_node()
            self.world.remove(pile.node())


class Pyramid(NodePath):

    def __init__(self, geom_node, node_name):
        super().__init__(BulletRigidBodyNode(node_name))
        np = self.attach_new_node(geom_node)
        np.set_two_sided(True)
        shape = BulletConvexHullShape()
        shape.add_geom(geom_node.getGeom(0))
        self.node().add_shape(shape)
        self.node().set_restitution(0.7)
        self.set_collide_mask(BitMask32.bit(2))
        self.set_color(LIGHT_GRAY)
        self.set_scale(0.7)
        self.set_r(-90)
        self.node().set_kinematic(True)


class SlimPrism(NodePath):

    def __init__(self, geom_node, node_name):
        super().__init__(BulletRigidBodyNode(node_name))
        self.np = self.attach_new_node(geom_node)
        self.np.set_two_sided(True)
        shape = BulletConvexHullShape()
        shape.add_geom(geom_node.get_geom(0))
        self.node().add_shape(shape)
        self.node().set_restitution(0.7)
        self.set_collide_mask(BitMask32.bit(2))
        self.set_scale(0.5, 0.5, 0.3)
        self.set_hpr(90, 90, 0)
        self.node().set_kinematic(True)


class Octahedron(NodePath):

    def __init__(self, geom_node, node_name):
        super().__init__(BulletRigidBodyNode(node_name))
        np = self.attach_new_node(geom_node)
        np.set_two_sided(True)
        shape = BulletConvexHullShape()
        shape.add_geom(geom_node.get_geom(0))
        self.node().add_shape(shape)
        self.node().set_restitution(0.7)
        self.set_collide_mask(BitMask32.bit(2))
        self.set_scale(0.3, 0.3, 1.2)
        self.node().set_kinematic(True)