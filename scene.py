from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletSphereShape, BulletBoxShape
from panda3d.bullet import BulletWorld, BulletDebugNode
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec2, Vec3, Vec4, LVector3
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import GeomNode, NodePath, PandaNode


class Stairs(NodePath):

    def __init__(self):
        super().__init__(PandaNode('stairs'))
        self.reparentTo(base.render)

        cube_node = self.create_cube_node()
        cube = self.attachNewNode(cube_node)
        cube.setTwoSided(True)

        cube.setHpr(45, 45, 45)
        # cube.setScale(0.5, 2, 2)

        new_np = NodePath(PandaNode('stairs2'))
        cube.copyTo(new_np)
        new_np.reparentTo(self)
        new_np.setPos(-2, -2, 0)
        new_np.setScale(0.2, 0.2, 0.2)


    def create_cube_node(self):
        square_sides = [
            [Vec3(-1, -1, -1), Vec3(1, -1, -1), Vec3(1, -1, 1), Vec3(-1, -1, 1)],
            [Vec3(-1, 1, -1), Vec3(1, 1, -1), Vec3(1, 1, 1), Vec3(-1, 1, 1)],
            [Vec3(-1, 1, 1), Vec3(1, 1, 1), Vec3(1, -1, 1), Vec3(-1, -1, 1)],
            [Vec3(-1, 1, -1), Vec3(1, 1, -1), Vec3(1, -1, -1), Vec3(-1, -1, -1)],
            [Vec3(-1, -1, -1), Vec3(-1, 1, -1), Vec3(-1, 1, 1), Vec3(-1, -1, 1)],
            [Vec3(1, -1, -1), Vec3(1, 1, -1), Vec3(1, 1, 1), Vec3(1, -1, 1)],
        ]
        texcoords = [Vec2(0.0, 1.0), Vec2(0.0, 0.0), Vec2(1.0, 0.0), Vec2(1.0, 1.0)]

        cube_node = GeomNode('square')

        for i, side in enumerate(square_sides):
            print(i)
            format_ = GeomVertexFormat.getV3n3cpt2()
            vdata = GeomVertexData('square', format_, Geom.UHStatic)

            vertex = GeomVertexWriter(vdata, 'vertex')
            normal = GeomVertexWriter(vdata, 'normal')
            color = GeomVertexWriter(vdata, 'color')
            texcoord = GeomVertexWriter(vdata, 'texcoord')
            for pt, coord in zip(side, texcoords):
                vertex.addData3(pt)
                normal.addData3(pt.normalize())
                if i == 2:
                    color.addData4f(1.0, 0.0, 0.0, 1.0)
                else:
                    color.addData4f(0.0, 0.0, 0.0, 0.0)

                texcoord.addData2f(coord)

            tris = GeomTriangles(Geom.UHStatic)
            tris.addVertices(0, 1, 3)
            tris.addVertices(1, 2, 3)

            square = Geom(vdata)
            square.addPrimitive(tris)

            cube_node.addGeom(square)

        return cube_node
        

if __name__ == '__main__':
    base = ShowBase()
    base.disableMouse()
    base.camera.setPos(0, -10, 0)
    Stairs()
    base.run()

