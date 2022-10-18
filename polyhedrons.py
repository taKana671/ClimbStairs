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
]


class GeomNodeCreater:

    def create_node(self, nd_name):
        vdata = self.get_vdata()
        node = self.get_node(nd_name, vdata)

        return node

    def get_vdata(self):
        format_ = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('triangle', format_, Geom.UHStatic)

        n = sum(len(face) for face in self.faces)
        vdata.setNumRows(n)

        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        for face, coords, rgba in zip(self.faces, self.texcoords, self.colors):
            for pt, coord in zip(face, coords):
                vertex.addData3(pt)
                normal.addData3(pt.normalize())
                color.addData4f(rgba)
                texcoord.addData2f(coord)
        return vdata

    def get_node(self, name, vdata):
        node = GeomNode(name)
        tris = GeomTriangles(Geom.UHStatic)

        for vertices in self.geom_vertices:
            tris.addVertices(*vertices)

        geom = Geom(vdata)
        geom.addPrimitive(tris)
        node.addGeom(geom)

        return node

    def get_geom_vertex(self, face):
        if (length := len(face)) == 3:
            geom_vertex = (self.cnt, self.cnt + 1, self.cnt + 2)
            self.cnt += length
            return geom_vertex


class RegularTerahedron(GeomNodeCreater):

    def __init__(self):
        # data = POLYHEDRONS['tetrahedron']
        data = POLYHEDRONS['octahedron']

        vertices = data['vertices']
        faces = data['faces']
        self.faces = [[Vec3(*vertices[i]) for i in idxes] for idxes in faces]
        self.texcoords = [[Vec2(TEXCOORDS[i]) for i in range(len(face))] for face in self.faces]

        # self.colors = [LColor(0, 0.5, 0, 1), LColor(1, 1, 0, 1), LColor(1, 0, 0, 1), LColor(0, 0, 1, 1)]

        color_pattern = data['color_pattern']
        colors = Colors.select(max(color_pattern) + 1)
        self.colors = [colors[i] for i in color_pattern]

        self.cnt = 0
        self.geom_vertices = [self.get_geom_vertex(face) for face in self.faces]


def create_regular_tetrahedron():
    a = Vec3(0, 0, 1)
    b = Vec3(0, 0.9428090416, -0.3333333333)
    c = Vec3(0.8164965809, -0.4714045208, -0.3333333333)
    d = Vec3(-0.8164965809, -0.4714045208, -0.3333333333)

    # a = Vec3(1, -1, 1)
    # b = Vec3(-1, 1, 1)
    # c = Vec3(-1, -1, -1)
    # d = Vec3(1, 1, -1)

    sides = [
        (a, b, c),
        (a, c, d),
        (a, b, d),
        (b, d, c),
    ]

    TEXCOORDS = [
        Vec2(0.0, 1.0),
        Vec2(0.0, 0.0),
        Vec2(1.0, 0.0)
    ]
    colors = [LColor(0, 0.5, 0, 1), LColor(1, 1, 0, 1), LColor(1, 0, 0, 1), LColor(0, 0, 1, 1)]

    node = GeomNode('tetrahedron')

    format_ = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('triangle', format_, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')
    tris = GeomTriangles(Geom.UHStatic)

    j = 0

    for i, side in enumerate(sides):
        c = colors[i]

        for pt, coord in zip(side, TEXCOORDS):
            vertex.addData3(pt)
            normal.addData3(pt.normalize())
            color.addData4f(c)
            texcoord.addData2f(coord)


        # tris.addVertices(j, j + 1, j + 2)
        # j += 3
        tris.addVertices(0, 1, 2)

    triangle = Geom(vdata)
    triangle.addPrimitive(tris)
    node.addGeom(triangle)

    return node



class TestShape(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('testShape'))
        self.reparentTo(base.render)
        # node = create_regular_tetrahedron()
        shape = RegularTerahedron()
        node = shape.create_node('tetrahedron')
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
        collide_debug = self.render.attachNewNode(BulletDebugNode('debug'))
        self.world.setDebugNode(collide_debug.node())
        collide_debug.show()
        # *******************************************

        shape = TestShape()
        self.world.attachRigidBody(shape.node())
        shape.hprInterval(5, (360, 360, 360)).loop()
        self.taskMgr.add(self.update, 'update')

    def update(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont


def test():
    root = NodePath(PandaNode('test'))
    root.reparentTo(base.render)
    node, _ = create_regular_tetrahedron()
    obj = root.attachNewNode(node)
    obj.setTwoSided(True)
    obj.reparentTo(root)
    root.setScale(1)
    # root.setHpr(45, 30, 45)
    root.setPos(0, 0, 0)
    root.hprInterval(5, (360, 360, 360)).loop()



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

