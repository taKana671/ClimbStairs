from panda3d.bullet import BulletBoxShape, BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec2, Vec3, LColor, Point3, BitMask32
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, NodePath, PandaNode


BLACK = LColor(0.0, 0.0, 0.0, 0.0)

SQUARE_SIDES = [
    [Vec3(-1, -1, -1), Vec3(1, -1, -1), Vec3(1, -1, 1), Vec3(-1, -1, 1)],
    [Vec3(-1, 1, -1), Vec3(1, 1, -1), Vec3(1, 1, 1), Vec3(-1, 1, 1)],
    [Vec3(-1, 1, 1), Vec3(1, 1, 1), Vec3(1, -1, 1), Vec3(-1, -1, 1)],
    [Vec3(-1, 1, -1), Vec3(1, 1, -1), Vec3(1, -1, -1), Vec3(-1, -1, -1)],
    [Vec3(-1, -1, -1), Vec3(-1, 1, -1), Vec3(-1, 1, 1), Vec3(-1, -1, 1)],
    [Vec3(1, -1, -1), Vec3(1, 1, -1), Vec3(1, 1, 1), Vec3(1, -1, 1)],
]

TEXCOORDS = [
    Vec2(0.0, 1.0),
    Vec2(0.0, 0.0),
    Vec2(1.0, 0.0),
    Vec2(1.0, 1.0)
]


def make_cube(top_color):
    node = GeomNode('cube')

    for i, side in enumerate(SQUARE_SIDES):
        format_ = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('square', format_, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        for pt, coord in zip(side, TEXCOORDS):
            vertex.addData3(pt)
            normal.addData3(pt.normalize())
            if i == 2:
                color.addData4f(top_color)
            else:
                color.addData4f(BLACK)
            texcoord.addData2f(coord)

        tris = GeomTriangles(Geom.UHStatic)
        tris.addVertices(0, 1, 3)
        tris.addVertices(1, 2, 3)

        square = Geom(vdata)
        square.addPrimitive(tris)
        node.addGeom(square)

    return node


class Stairs(NodePath):

    def __init__(self, world):
        super().__init__(PandaNode('stairs'))
        self.reparentTo(base.render)
        self.setH(5)

        cube_root = NodePath(PandaNode('cubeRoot'))
        node = make_cube(LColor(0.6, 0.4, 0.68, 1.0))  # Amethyst 0.8
        self.cube = cube_root.attachNewNode(node)
        self.cube.setTwoSided(True)

        self.world = world
        self.stair_cnt = -1
        self.edge = 1

        for _ in range(15):
            self.make_stair()

    def make_stair(self):
        self.stair_cnt += 1
        name = f'stairs_{self.stair_cnt}'
        new_cube = NodePath(BulletRigidBodyNode(name))
        self.cube.copyTo(new_cube)
        end, tip = new_cube.getTightBounds()
        new_cube.node().addShape(BulletBoxShape((tip - end) / 2))

        new_cube.node().setRestitution(1)

        new_cube.setCollideMask(BitMask32.bit(1))
        new_cube.setScale(0.5, 6, 0.5 * (self.stair_cnt + 1))
        new_cube.setPos(self.edge * self.stair_cnt, 0, self.edge / 2 * (self.stair_cnt + 1))
        new_cube.reparentTo(self)
        self.world.attachRigidBody(new_cube.node())

    @property
    def top_pos(self):
        np = self.getChild(self.stair_cnt)
        _, tip = np.getTightBounds()
        return Point3(self.edge * self.stair_cnt, 0, tip.z)


class Floor(NodePath):

    def __init__(self, world):
        super().__init__(BulletRigidBodyNode('floor'))
        self.reparentTo(base.render)
        self.setCollideMask(BitMask32.bit(1))
        self.node().addShape(BulletPlaneShape(Vec3.up(), 0))
        world.attachRigidBody(self.node())


class Scene():

    def __init__(self, world):
        base.setBackgroundColor(LColor(0.57, 0.43, 0.85, 1.0))  # MediumPurple
        self.stairs = Stairs(world)
        self.floor = Floor(world)
