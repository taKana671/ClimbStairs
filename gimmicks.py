import random

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletConvexHullShape
from panda3d.core import Vec3, Point3, LColor, BitMask32
from panda3d.core import NodePath, PandaNode
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait

from geommaker import PolyhedronGeomMaker, ConeGeomMaker


class GimmickRoot(NodePath):

    def __init__(self):
        super().__init__(PandaNode('gimmikRoot'))
        self.reparentTo(base.render)


class Polyhedrons(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__()
        self.world = world
        self.stairs = stairs
        self.polh_maker = PolyhedronGeomMaker()

    def start(self, node_name, chara_pos):
        geomnode = self.polh_maker()
        polh = Polyhedron(node_name, geomnode)
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


class Cones(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__()
        self.stairs = stairs
        self.world = world
        self.stair = 0
        self.cone_maker = ConeGeomMaker()
        self.cones = [cone for cone in self.make_cones()]
        self.setup()

    def make_cones(self):
        n = self.stairs.left_end - self.stairs.right_end
        for i in range(n):
            geomnode = self.cone_maker.make_geomnode()
            cone = Cone(f'cones_{i}', geomnode)
            cone.node().setKinematic(True)
            self.world.attachRigidBody(cone.node())
            yield cone

    def setup(self):
        self.stair = random.randint(
            self.stair + 1, self.stairs.top_stair - 1)
        print('trap', self.stair)
        stair_center = self.stairs.center(self.stair)
        self.start_x = stair_center.x + 2
        self.stop_x = stair_center.x + 0.8

        for i, cone in enumerate(self.cones):
            y = self.stairs.left_end - (i + 0.5)
            z = stair_center.z + 0.5
            cone.setPos(Point3(self.start_x, y, z))
            cone.reparentTo(self)

    def appear(self, dt):
        distance = dt
        for cone in self.cones:
            x = cone.getX() - distance
            cone.setX(x)

        if x < self.stop_x:
            return True

    def disappear(self, dt):
        distance = dt
        for cone in self.cones:
            x = cone.getX() + distance
            cone.setX(x)

        if x > self.start_x:
            return True

    def finish(self):
        for cone in self.cones:
            cone.detachNode()


class CircularSaws(GimmickRoot):

    def __init__(self, stairs, world):
        super().__init__()
        self.stairs = stairs
        self.world = world
        self.creater = PolyhedronGeomMaker()
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


class Polyhedron(NodePath):

    def __init__(self, name, geom_node):
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


class Cone(NodePath):

    def __init__(self, name, geom_node):
        super().__init__(BulletRigidBodyNode(name))
        np = self.attachNewNode(geom_node)
        np.setTwoSided(True)
        np.reparentTo(self)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(2))
        self.setColor(LColor(0.75, 0.75, 0.75, 1))
        self.setScale(0.7)
        self.setR(-90)


class CircularSaw(NodePath):

    def __init__(self, name, geom_node):
        super().__init__(BulletRigidBodyNode(name))
        self.np = self.attachNewNode(geom_node)
        self.np.setTwoSided(True)
        self.np.reparentTo(self)
        shape = BulletConvexHullShape()
        shape.addGeom(geom_node.getGeom(0))
        self.node().addShape(shape)
        self.node().setRestitution(0.7)
        self.setCollideMask(BitMask32.bit(2))
        self.setScale(0.5, 0.5, 0.25)
        self.setHpr(90, 90, 0)

        self.node().setKinematic(True)

