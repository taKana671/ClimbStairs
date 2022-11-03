import math
import random
from enum import Enum

from panda3d.core import Vec3, LColor
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode

from panda3d.core import BitMask32
from panda3d.core import NodePath
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletRigidBodyNode
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


class GeomMaker:

    def triangle(self, start):
        return (start, start + 1, start + 2)

    def square(self, start):
        for x, y, z in [(0, 1, 3), (1, 2, 3)]:
            yield (start + x, start + y, start + z)

    def polygon(self, start, vertices_num):
        for i in range(2, vertices_num):
            if i == 2:
                yield (start, start + i - 1, start + i)
            else:
                yield (start + i - 1, start, start + i)


class PolyhedronGeomMaker(GeomMaker):

    def __init__(self):
        self.idx = 0
        self.polh_names = tuple(POLYHEDRONS.keys())

    def next_geomnode(self):
        if self.idx >= len(self.polh_names):
            self.idx = 0
        polh_name = self.polh_names[self.idx]
        self.idx += 1

        self.data = POLYHEDRONS[polh_name]
        self.colors = self.select_colors()
        geomnode = self._make_geomnode()
        return geomnode

    def make_geomnode(self, key, colors=None):
        self.data = POLYHEDRONS[key]
        self.colors = colors if colors else self.select_colors()
        node = self._make_geomnode()
        return node

    def faces(self):
        vertices = self.data['vertices']
        faces = self.data['faces']
        color_pattern = self.data['color_pattern']

        for idxes, n in zip(faces, color_pattern):
            yield ((Vec3(vertices[i]) for i in idxes), self.colors[n])

    def select_colors(self):
        n = max(self.data['color_pattern'])
        return Colors.select(n + 1)

    @property
    def num_rows(self):
        return sum(len(face) for face in self.data['faces'])

    def prim_vertices(self):
        start = 0
        for face in self.data['faces']:
            if (vertices_num := len(face)) == 3:
                yield self.triangle(start)
            elif vertices_num == 4:
                yield from self.square(start)
            elif vertices_num >= 5:
                yield from self.polygon(start, vertices_num)
            start += vertices_num

    def _make_geomnode(self):
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
                # normal.addData3(pt.normalize())
                normal.addData3(pt.normalized())
                color.addData4f(rgba)
                # texcoord.addData2f(tex)

        node = GeomNode('geomnode')
        prim = GeomTriangles(Geom.UHStatic)

        for vertices in self.prim_vertices():
            prim.addVertices(*vertices)

        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node.addGeom(geom)

        return node


class PyramidGeomMaker(GeomMaker):

    def __init__(self, length=2, cycle=12, radius=0.5):
        self.cone_length = length
        self.cycle = cycle
        self.cone_radius = radius
        self.faces = [face for face in self.get_faces()]

    def get_faces(self):
        point = Vec3(0, 0, self.cone_length)

        bottom = []
        for i in range(self.cycle):
            theta = i * (2 * math.pi / self.cycle)
            x = self.cone_radius * math.sin(theta)
            y = self.cone_radius * math.cos(theta)
            bottom.append(Vec3(x, y, 0))

        yield bottom

        for i in range(0, len(bottom)):
            if i == len(bottom) - 1:
                yield (point, bottom[0], bottom[i])
            else:
                yield (point, bottom[i], bottom[i + 1])

    def prim_vertices(self):
        start = 0
        for face in self.faces:
            if (vertices_num := len(face)) == 3:
                yield self.triangle(start)
            else:
                yield from self.polygon(start, vertices_num)
            start += vertices_num

    def make_geomnode(self):
        format_ = GeomVertexFormat.getV3n3cpt2()   #getV3n3c4()
        vdata = GeomVertexData('triangle', format_, Geom.UHStatic)
        vdata.setNumRows(self.cycle + 1)
        vertex = GeomVertexWriter(vdata, 'vertex')
        # color = GeomVertexWriter(vdata, 'color')

        for face in self.faces:
            for pt in face:
                vertex.addData3(pt)

        prim = GeomTriangles(Geom.UHStatic)
        for vertices in self.prim_vertices():
            prim.addVertices(*vertices)

        node = GeomNode('geomnode')
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node.addGeom(geom)

        return node


class SphereGeomMaker(GeomMaker):

    def __init__(self):
        self.data = POLYHEDRONS['icosahedron']
        self.divnum = 3

    def make_geomnode(self, colors=None):
        self.colors = colors if colors else Colors.select(2)
        node = self._make_geomnode()
        return node

    @property
    def num_rows(self):
        """One triangle is subdivided into 4.
           The number of subdivide repetition is self.divnum.
           An icosahedron has 20 faces and a face has 3 vertices.
        """
        return 4 ** self.divnum * 20 * 3

    def calc_midpoints(self, face):
        """face: A list of Vec3, having 3 elements.
        """
        # (i, j): [(0, 1), (1, 2), (2, 0)]
        for i, pt1 in enumerate(face):
            j = i + 1 if i < len(face) - 1 else 0
            pt2 = face[j]
            mid_pt = (pt1 + pt2) / 2

            yield mid_pt

    def subdivide(self, face, divnum=0):
        if divnum == self.divnum:
            yield face
        else:
            midpoints = [pt for pt in self.calc_midpoints(face)]

            for i, vertex in enumerate(face):
                j = len(face) - 1 if i == 0 else i - 1
                face = [vertex, midpoints[i], midpoints[j]]
                yield from self.subdivide(face, divnum + 1)
            yield from self.subdivide(midpoints, divnum + 1)

    def faces(self):
        vertices = self.data['vertices']
        faces = self.data['faces']

        for tup in faces:
            face = [Vec3(vertices[n]) for n in tup]
            for subdiv_face in self.subdivide(face):
                idx = 0 if any(pt.z == 0 for pt in subdiv_face) else 1
                yield (subdiv_face, self.colors[idx])

    def _make_geomnode(self):
        format_ = GeomVertexFormat.getV3n3cpt2()   #getV3n3c4()
        vdata = GeomVertexData('triangle', format_, Geom.UHStatic)
        vdata.setNumRows(self.num_rows)
        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')

        prim = GeomTriangles(Geom.UHStatic)

        start = 0
        for face, rgba in self.faces():
            for pt in face:
                vertex.addData3(pt.normalized())
                color.addData4f(rgba)

            prim_vertices = self.triangle(start)
            prim.addVertices(*prim_vertices)
            start += 3

        node = GeomNode('geomnode')
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node.addGeom(geom)

        return node


class TestShape(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('testShape'))
        self.reparentTo(base.render)

        maker = SphereGeomMaker()
        node = maker.make_geomnode()

        # maker = PyramidGeomMaker()
        # node = maker.make_geomnode()

        # creater = PolyhedronGeomMaker()
        # node = creater.make_geomnode('triaugmented_hexagonal_prism')

        obj = self.attachNewNode(node)
        obj.setTwoSided(True)
        obj.reparentTo(self)
        shape = BulletConvexHullShape()
        shape.addGeom(node.getGeom(0))
        self.node().addShape(shape)
        self.setCollideMask(BitMask32(1))
        self.setScale(1)
        self.setColor(Colors.RED.value)


class Game(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.camera.setPos(10, 10, 10)  # 20, -20, 5
        self.camera.lookAt(0, 0, 0)

        self.world = BulletWorld()

        # *******************************************
        collide_debug = self.render.attachNewNode(BulletDebugNode('debug'))
        self.world.setDebugNode(collide_debug.node())
        collide_debug.show()
        # *******************************************

        # icosahedron

        shape = TestShape()
        self.world.attachRigidBody(shape.node())
        shape.hprInterval(8, (360, 720, 360)).loop()
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

