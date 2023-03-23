import array
import math
import random
from enum import Enum

from panda3d.core import Vec3, LColor
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexArrayFormat
from panda3d.core import Geom, GeomNode, GeomTriangles

#**************************************
from panda3d.core import NodePath, BitMask32
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletWorld, BulletDebugNode
#*************************************

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
        for x, y, z in [(2, 1, 0), (0, 3, 2)]:
            yield (start + x, start + y, start + z)

    def polygon(self, start, vertices_num):
        for i in range(2, vertices_num):
            if i == 2:
                yield (start, start + i - 1, start + i)
            else:
                yield (start + i - 1, start, start + i)

    def prim_indices(self, start, num):
        match num:
            case 3:
                yield self.triangle(start)
            case 4:
                yield from self.square(start)
            case _:
                yield from self.polygon(start, num)


class PolyhedronGeomMaker(GeomMaker):

    def __init__(self):
        self.idx = 0
        self.polh_names = tuple(POLYHEDRONS.keys())
        self.make_format()

    def make_format(self):
        arr_format = GeomVertexArrayFormat()
        arr_format.add_column('vertex', 3, Geom.NTFloat32, Geom.CPoint)
        arr_format.add_column('color', 4, Geom.NTFloat32, Geom.CColor)
        arr_format.add_column('normal', 3, Geom.NTFloat32, Geom.CNormal)
        self.format_ = GeomVertexFormat.register_format(arr_format)

    def next_geomnode(self):
        if self.idx >= len(self.polh_names):
            self.idx = 0
        polh_name = self.polh_names[self.idx]
        self.idx += 1
        geom_node = self.make_geomnode(polh_name)
        return geom_node

    def make_geomnode(self, key, colors=None):
        self.data = POLYHEDRONS[key]
        self.colors = colors if colors else self.select_colors()
        geom_node = self._make_geomnode()
        return geom_node

    def faces(self):
        vertices = self.data['vertices']
        faces = self.data['faces']
        color_pattern = self.data['color_pattern']
        normals = self.data['normals']

        for idxes, n, normal in zip(faces, color_pattern, normals):
            vert = (vertices[i] for i in idxes)
            if normal is None:
                normal = (Vec3(vertices[i]).normalized() for i in idxes)

            yield (vert, self.colors[n], normal, len(idxes))

    def select_colors(self):
        n = max(self.data['color_pattern'])
        return Colors.select(n + 1)

    def num_rows(self):
        return sum(len(face) for face in self.data['faces'])

    def _make_geomnode(self):
        vdata_values = array.array('f', [])
        prim_indices = array.array("H", [])
        start = 0

        for verts, rgba, norms, num_verts in self.faces():
            for pt, norm in zip(verts, norms):
                vdata_values.extend(pt)
                vdata_values.extend(rgba)
                vdata_values.extend(norm)

            for indices in self.prim_indices(start, num_verts):
                prim_indices.extend(indices)
            start += num_verts

        vdata = GeomVertexData('polyhedron', self.format_, Geom.UHStatic)
        vdata.unclean_set_num_rows(self.num_rows())
        vdata_mem = memoryview(vdata.modify_array(0)).cast('B').cast('f')
        vdata_mem[:] = vdata_values

        prim = GeomTriangles(Geom.UHStatic)
        prim_array = prim.modify_vertices()
        prim_array.unclean_set_num_rows(len(prim_indices))
        prim_mem = memoryview(prim_array).cast('B').cast('H')
        prim_mem[:] = prim_indices

        node = GeomNode('geomnode')
        geom = Geom(vdata)
        geom.add_primitive(prim)
        node.add_geom(geom)

        return node


class PyramidGeomMaker(GeomMaker):

    def __init__(self, length=2, cycle=12, radius=0.5):
        self.cone_length = length
        self.cycle = cycle
        self.cone_radius = radius
        self.make_format()

    def make_format(self):
        arr_format = GeomVertexArrayFormat()
        arr_format.add_column('vertex', 3, Geom.NTFloat32, Geom.CPoint)
        arr_format.add_column('normal', 3, Geom.NTFloat32, Geom.CNormal)
        self.format_ = GeomVertexFormat.register_format(arr_format)

    def num_rows(self):
        return self.cycle + 3 * self.cycle

    def faces(self):
        point = Vec3(0, 0, self.cone_length)

        bottom = []
        for i in range(self.cycle):
            theta = i * (2 * math.pi / self.cycle)
            x = self.cone_radius * math.sin(theta)
            y = self.cone_radius * math.cos(theta)
            bottom.append(Vec3(x, y, 0.0))

        yield bottom

        for i in range(0, len(bottom)):
            if i == len(bottom) - 1:
                yield (point, bottom[0], bottom[i])
            else:
                yield (point, bottom[i], bottom[i + 1])

    def make_geomnode(self):
        vdata_values = array.array('f', [])
        prim_indices = array.array("H", [])
        start = 0

        for face in self.faces():
            for pt in face:
                vdata_values.extend(pt)
                normal = Vec3(0, 0, -1) if len(face) == self.cycle else pt.normalized()
                vdata_values.extend(normal)

            for indices in self.prim_indices(start, len(face)):
                prim_indices.extend(indices)
            start += len(face)

        vdata = GeomVertexData('pyramid', self.format_, Geom.UHStatic)
        vdata.unclean_set_num_rows(self.num_rows())
        vdata_mem = memoryview(vdata.modify_array(0)).cast('B').cast('f')
        vdata_mem[:] = vdata_values

        prim = GeomTriangles(Geom.UHStatic)
        prim_array = prim.modify_vertices()
        prim_array.unclean_set_num_rows(len(prim_indices))
        prim_mem = memoryview(prim_array).cast('B').cast('H')
        prim_mem[:] = prim_indices

        node = GeomNode('geomnode')
        geom = Geom(vdata)
        geom.add_primitive(prim)
        node.add_geom(geom)

        return node


class SphereGeomMaker(GeomMaker):

    def __init__(self):
        self.data = POLYHEDRONS['icosahedron']
        self.divnum = 3
        self.make_format()

    def make_format(self):
        arr_format = GeomVertexArrayFormat()
        arr_format.add_column('vertex', 3, Geom.NTFloat32, Geom.CPoint)
        arr_format.add_column('color', 4, Geom.NTFloat32, Geom.CColor)
        arr_format.add_column('normal', 3, Geom.NTFloat32, Geom.CNormal)
        self.format_ = GeomVertexFormat.register_format(arr_format)

    def make_geomnode(self, colors=None):
        self.colors = colors if colors else Colors.select(2)
        node = self._make_geomnode()
        return node

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
        vdata_values = array.array('f', [])
        prim_indices = array.array("H", [])
        start = 0

        for face, rgba in self.faces():
            for pt in face:
                n = pt.normalized()
                vdata_values.extend(n)
                vdata_values.extend(rgba)
                vdata_values.extend(n)

            indices = self.triangle(start)
            prim_indices.extend(indices)
            start += 3

        vdata = GeomVertexData('sphere', self.format_, Geom.UHStatic)
        vdata.unclean_set_num_rows(self.num_rows())
        vdata_mem = memoryview(vdata.modify_array(0)).cast('B').cast('f')
        vdata_mem[:] = vdata_values

        prim = GeomTriangles(Geom.UHStatic)
        prim_array = prim.modify_vertices()
        prim_array.unclean_set_num_rows(len(prim_indices))
        prim_mem = memoryview(prim_array).cast('B').cast('H')
        prim_mem[:] = prim_indices

        node = GeomNode('geomnode')
        geom = Geom(vdata)
        geom.add_primitive(prim)
        node.add_geom(geom)

        return node


class TorusGeomMaker(GeomMaker):

    def __init__(self, segs_r=24, segs_s=12, ring_radius=1.2, section_radius=0.5):
        self.segs_r = segs_r
        self.segs_s = segs_s
        self.ring_radius = ring_radius
        self.section_radius = section_radius
        self.make_format()

    def make_format(self):
        arr_format = GeomVertexArrayFormat()
        arr_format.add_column('vertex', 3, Geom.NTFloat32, Geom.CPoint)
        arr_format.add_column('color', 4, Geom.NTFloat32, Geom.CColor)
        arr_format.add_column('normal', 3, Geom.NTFloat32, Geom.CColor)
        arr_format.add_column('texcoord', 2, Geom.NTFloat32, Geom.CTexcoord)
        self.format_ = GeomVertexFormat.register_format(arr_format)

    def make_geomnode(self):
        self.colors = Colors.select(2)
        geomnode = self._make_geomnode()
        return geomnode

    def _make_geomnode(self):
        vdata_values = array.array('f', [])
        prim_indices = array.array('H', [])

        delta_angle_h = 2.0 * math.pi / self.segs_r
        delta_angle_v = 2.0 * math.pi / self.segs_s

        for i in range(self.segs_r + 1):
            angle_h = delta_angle_h * i
            u = i / self.segs_r

            color = self.colors[0] if i // 2 % 2 == 0 else self.colors[1]

            for j in range(self.segs_s + 1):
                angle_v = delta_angle_v * j
                r = self.ring_radius - self.section_radius * math.cos(angle_v)
                c = math.cos(angle_h)
                s = math.sin(angle_h)

                x = r * c
                y = r * s
                z = self.section_radius * math.sin(angle_v)
                nx = x - self.ring_radius * c
                ny = y - self.ring_radius * s
                normal_vec = Vec3(nx, ny, z).normalized()
                v = 1.0 - j / self.segs_s

                vdata_values.extend((x, y, z))
                vdata_values.extend(color)
                vdata_values.extend(normal_vec)
                vdata_values.extend((u, v))

        for i in range(self.segs_r):
            for j in range(0, self.segs_s):
                idx = j + i * (self.segs_s + 1)
                prim_indices.extend([idx, idx + 1, idx + self.segs_s + 1])
                prim_indices.extend([idx + self.segs_s + 1, idx + 1, idx + 1 + self.segs_s + 1])

        vdata = GeomVertexData('torous', self.format_, Geom.UHStatic)
        rows = (self.segs_r + 1) * (self.segs_s + 1)
        vdata.unclean_set_num_rows(rows)
        vdata_mem = memoryview(vdata.modify_array(0)).cast('B').cast('f')
        vdata_mem[:] = vdata_values

        prim = GeomTriangles(Geom.UHStatic)
        prim_array = prim.modify_vertices()
        prim_array.unclean_set_num_rows(len(prim_indices))
        prim_mem = memoryview(prim_array).cast('B').cast('H')
        prim_mem[:] = prim_indices

        node = GeomNode('geomnode')
        geom = Geom(vdata)
        geom.add_primitive(prim)
        node.add_geom(geom)

        return node




class PolhModel(NodePath):

    def __init__(self, geomnode):
        super().__init__(geomnode)
        self.setTwoSided(True)


class TestShape(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('testShape'))
        self.reparentTo(base.render)
        # maker = SphereGeomMaker()
        # node = maker.make_geomnode()

        # maker = PyramidGeomMaker()
        # node = maker.make_geomnode()

        # creater = PolyhedronGeomMaker()
        # node = creater.make_geomnode('icosidodecahedron')
        # obj = self.attachNewNode(node)
        # obj.setTwoSided(True)

        # node = creater.make_geomnode('cube')
        # cube = NodePath(node)
        # cube.setTwoSided(True)
        # model = cube.copyTo(self)

        maker = TorusGeomMaker()
        node = maker.make_geomnode()
        obj = self.attachNewNode(node)
        obj.setTwoSided(True)

        # obj.reparentTo(self) <= いらない
        shape = BulletConvexHullShape()
        shape.addGeom(node.getGeom(0))
        self.node().addShape(shape)
        self.setCollideMask(BitMask32(1))
        self.setScale(0.3)
        self.setColor(Colors.RED.value)


class Test(ShowBase):

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
        # shape.hprInterval(8, (360, 720, 360)).loop()
        self.taskMgr.add(self.update, 'update')

    def update(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont


if __name__ == '__main__':
    test = Test()
    test.run()
