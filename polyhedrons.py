import random
from enum import Enum

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletBoxShape, BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec2, Vec3, LColor, Point3, BitMask32
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, NodePath, PandaNode
from panda3d.core import CardMaker

from panda3d.bullet import BulletCylinderShape, BulletBoxShape, BulletConvexHullShape
from panda3d.bullet import BulletRigidBodyNode
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from panda3d.core import PandaNode, NodePath, TransformState
from panda3d.core import Quat, Vec3, LColor, BitMask32, Point3
from panda3d.bullet import BulletWorld, BulletDebugNode

from polyhedrons_data import POLYHEDRONS


class Colors(Enum):

    RED = LColor(1, 0, 0, 1)
    BLUE = LColor(0, 0, 1, 1)
    YELLOW = LColor(1, 1, 0, 1)
    GREEN = LColor(0, 0.5, 0, 1)
    ORANGE = LColor(1, 0.549, 0, 1)
    MAGENTA = LColor(1, 0, 1, 1)
    PURPLE = LColor(0.501, 0, 0.501, 1)
    LIME = LColor(0, 1, 0, 1)
    VIOLET = LColor(0.54, 0.16, 0.88, 1)
    SKY = LColor(0, 0.74, 1, 1)

    @classmethod
    def select(cls, n):
        return random.sample([m.value for m in cls], n)


TEXCOORDS = [
    (0.0, 1.0),
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0),
]


class PolyhedronsCreater:

    def __init__(self):
        self.idx = 0
        self.polh_names = tuple(POLYHEDRONS.keys())

    def create_polyhedron(self, rb_node_name):
        if self.idx >= len(self.polh_names):
            self.idx = 0
        polh_name = self.polh_names[self.idx]
        self.idx += 1

        self.data = POLYHEDRONS[polh_name]
        self.colors = self.select_colors()
        geom_node = self.make_geom_node()
        return Polyhedron(rb_node_name, geom_node)

    def get_geom_node(self, key, colors=None):
        self.data = POLYHEDRONS[key]
        self.colors = colors if colors else self.select_colors()
        node = self.make_geom_node()
        return node

    def faces(self):
        vertices = self.data['vertices']
        faces = self.data['faces']
        color_pattern = self.data['color_pattern']

        for idxes, n in zip(faces, color_pattern):
            yield ((Vec3(*vertices[i]) for i in idxes), self.colors[n])

    def select_colors(self):
        n = max(self.data['color_pattern'])
        return Colors.select(n + 1)

    @property
    def num_rows(self):
        return sum(len(face) for face in self.data['faces'])

    def geom_vertices(self):
        i = 0
        for face in self.data['faces']:
            if (pts := len(face)) == 3:
                yield (i, i + 1, i + 2)
                i += pts
            elif pts == 4:
                for x, y, z in [(0, 1, 3), (1, 2, 3)]:
                    yield (i + x, i + y, i + z)
                i += pts
            elif pts >= 5:
                for j in range(2, pts):
                    if j == 2:
                        yield (i, i + j - 1, i + j)
                    else:
                        yield (i + j - 1, i, i + j)
                i += pts

    def make_geom_node(self):
        format_ = GeomVertexFormat.getV3n3cpt2()  # getV3n3c4
        vdata = GeomVertexData('triangle', format_, Geom.UHStatic)
        vdata.setNumRows(self.num_rows)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        # texcoord = GeomVertexWriter(vdata, 'texcoord')

        for face, rgba in self.faces():
            for pt in face:
                vertex.addData3(pt)
                normal.addData3(pt.normalize())
                color.addData4f(rgba)
                # texcoord.addData2f(tex)

        node = GeomNode('geomnode')
        tris = GeomTriangles(Geom.UHStatic)

        for vertices in self.geom_vertices():
            tris.addVertices(*vertices)

            geom = Geom(vdata)
            geom.addPrimitive(tris)
            node.addGeom(geom)

        return node


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
        self.setCollideMask(BitMask32.bit(1))
        self.setScale(0.7)
        # self.setScale(2)


class TestShape(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('testShape'))
        self.reparentTo(base.render)
        creater = PolyhedronsCreater()
        node = creater.get_geom_node('augmented_truncated_tetrahedron')
        obj = self.attachNewNode(node)
        obj.setTwoSided(True)
        obj.reparentTo(self)
        shape = BulletConvexHullShape()
        shape.addGeom(node.getGeom(0))
        self.node().addShape(shape)
        self.setCollideMask(BitMask32(1))
        self.setScale(2)


class Game(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.camera.setPos(10, 10, 10)  # 20, -20, 5
        self.camera.lookAt(0, 0, 0) 
        self.world = BulletWorld()

        # *******************************************
        # collide_debug = self.render.attachNewNode(BulletDebugNode('debug'))
        # self.world.setDebugNode(collide_debug.node())
        # collide_debug.show()
        # *******************************************

        shape = TestShape()
        self.world.attachRigidBody(shape.node())
        shape.hprInterval(5, (360, 360, 360)).loop()
        self.taskMgr.add(self.update, 'update')

    def update(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont


if __name__ == '__main__':
    # base = ShowBase()
    # base.disableMouse()
    # base.camera.setPos(10, 10, 10)  # 20, -20, 5
    # base.camera.lookAt(0, 0, 0)  # 5, 0, 3
    # # scene = Scene()
    # test()
    # base.run()
    game = Game()
    game.run()

