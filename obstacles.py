import random
from enum import Enum, auto

from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletBoxShape
from panda3d.bullet import BulletSoftBodyNode, BulletHelper
from panda3d.core import GeomVertexFormat
from panda3d.core import Vec2, Vec3, Point3, LColor, BitMask32
from panda3d.core import NodePath, PandaNode, TransformState, GeomNode, GeomVertexFormat


from scene import make_cube


PATH_SPHERE = 'models/sphere/sphere'
PATH_CARNSX = 'models/carnsx/carnsx'
PATH_SOCCERBALL = 'models/soccerball/soccerball'


class Colors(int, Enum):

    LIME = (0, LColor(0, 1, 0, 1))
    AQUAMARINE = (1, LColor(0.49, 1, 0.83, 1))
    YELLOW = (2, LColor(1, 1, 0, 1))
    GREENYELLOW = (3, LColor(0.67, 1, 0.18, 1))

    def __new__(cls, id_, color):
        obj = int.__new__(cls, id_)
        obj._value_ = id_
        obj.color = color
        return obj

    @classmethod
    def select(cls):
        n = random.randint(0, 3)
        obj = cls(n)
        return obj.color


class ObstaclesHolder:

    def __init__(self, length):
        self.data = [None for _ in range(length)]

    def __len__(self):
        return sum(1 for item in self.data if item is not None)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def empty_idx(self):
        for i, item in enumerate(self.data):
            if not item:
                return i
        return None

    def pop(self, key):
        item = self.data[key]
        self.data[key] = None
        return item


class Obstacles(NodePath):

    def __init__(self, world, objects_holder):
        super().__init__(PandaNode('fallenObjects'))
        self.reparentTo(base.render)
        self.world = world
        self.holder = objects_holder

    def start(self):
        if (idx := self.holder.empty_idx()) is not None:
            obj = self.create(str(idx))
            self.holder[idx] = obj
            # obj.reparentTo(self)
            self.place(obj)
            # self.world.attachRigidBody(obj.node())
            # self.apply_force(obj)


class Spheres(Obstacles):

    def __init__(self, stairs, world, objects_holder):
        super().__init__(world, objects_holder)
        self.stairs = stairs
        self.spheres = [Sphere, SoccerBall]

    def place(self, obj):
        stair_center = self.stairs.top_center()
        y = random.randint(self.stairs.right_edge, self.stairs.left_edge)
        z = stair_center.z + obj.size.z / 2
        pos = Point3(stair_center.x, y, z)
        obj.setPos(pos)

    def apply_force(self, obj):
        y = random.randint(-1, 1)
        z = random.randint(-1, 1)
        # n = 10 if y == 0 else 20
        force = Vec3(-1, y, z).normalized() * 10
        obj.node().applyCentralImpulse(force)

    def create(self, name):
        class_ = random.choice(self.spheres)
        obj = class_(name)

        return obj


class Rectangles(Obstacles):

    def __init__(self, stairs, world, character, objects_holder):
        super().__init__(world, objects_holder)
        self.stairs = stairs
        self.character = character
        self.rectangles = [CarNsx, Box]

    def place(self, obj):
        stair_center = self.stairs.top_center()
        chara_pos = self.character.getPos()
        z = stair_center.z + obj.size.z / 2
        # pos = Point3(stair_center.x, chara_pos.y, z)
        pos = Point3(stair_center.x - 1, chara_pos.y, stair_center.z + 2)
        
        self.np = create_ellipsoid(self, pos, self.world)
        
        # obj.setPos(pos)

    def apply_force(self, obj):
        pass
        # force = Vec3(-1, 0, -1).normalized() * 5
        # obj.node().applyCentralImpulse(force)

    def create(self, name):
        class_ = random.choice(self.rectangles)
        obj = class_(name)

        return obj


class Sphere(NodePath):

    def __init__(self, name):
        super().__init__(BulletRigidBodyNode(name))

        color = Colors.select()
        scale = random.choice([0.1, 0.2])
        mass = scale * 10

        sphere = base.loader.loadModel(PATH_SPHERE)
        sphere.setScale(scale)
        sphere.reparentTo(self)
        end, tip = sphere.getTightBounds()
        self.size = tip - end
        self.node().addShape(BulletSphereShape(self.size.z / 2))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(mass)
        self.node().setRestitution(0.7)
        self.setColor(color)


class Box(NodePath):

    def __init__(self, name):
        super().__init__(BulletRigidBodyNode(name))

        color = Colors.select()
        scale = random.choice([0.5, 1.0])
        mass = scale * 10

        box = self.attachNewNode(make_cube(LColor(1, 1, 1, 1)))
        box.setTwoSided(True)

        box.setScale(scale)
        box.reparentTo(self)
        end, tip = box.getTightBounds()
        self.size = tip - end
        self.node().addShape(BulletBoxShape(self.size / 2))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(1)
        self.node().setRestitution(0.7)
        self.setColor(color)


class CarNsx(NodePath):

    def __init__(self, name):
        super().__init__(BulletRigidBodyNode(name))
        self.reparentTo(base.render)
        car = base.loader.loadModel(PATH_CARNSX)
        car.reparentTo(self)
        car.setScale(0.5)

        end, tip = car.getTightBounds()
        self.size = tip - end
        half = self.size / 2
        center = tip - half

        self.node().addShape(BulletBoxShape(half), TransformState.makePos(center))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(1)
        self.node().setRestitution(0.7)
        self.setH(-90)


class SoccerBall(NodePath):

    def __init__(self, name):
        super().__init__(BulletRigidBodyNode(name))
        self.reparentTo(base.render)
        ball = base.loader.loadModel(PATH_SOCCERBALL)
        ball.reparentTo(self)
        ball.setScale(1.0)

        end, tip = ball.getTightBounds()
        self.size = tip - end

        self.node().addShape(BulletSphereShape(self.size.z / 2))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(1)
        self.node().setRestitution(0.7)



def create_ellipsoid(parent, pos, world):
    info = world.getWorldInfo()
    info.setAirDensity(0)
    info.setWaterDensity(0)
    info.setWaterOffset(0)
    info.setWaterNormal(Vec3(0, 0, 0))

    center = Point3(0, 0, 0)
    radius = Vec3(1, 1, 1) * 0.3
    node = BulletSoftBodyNode.makeEllipsoid(info, center, radius, 128)
    node.setName('ellipsoid')
    node.getMaterial(0).setLinearStiffness(0.1)
    node.getCfg().setDynamicFrictionCoefficient(1)
    node.getCfg().setDampingCoefficient(0.001)
    node.getCfg().setPressureCoefficient(1500)

    # node.getCfg().clearAllCollisionFlags()
    # node.getCfg().setCollisionFlag(BulletSoftBodyConfig.CFClusterSoftSoft, True)
    # node.getCfg().setCollisionFlag(BulletSoftBodyConfig.CFClusterRigidSoft, True)
    # node.getCfg().setCollisionFlag(BulletSoftBodyConfig.CFClusterRigidSoft, True)


    node.setTotalMass(30, True)
    node.setPose(True, False)

    np = base.render.attachNewNode(node)
    np.setPos(pos)

    sphere = base.loader.loadModel(PATH_SPHERE)
    sphere.setTexture(base.loader.loadTexture('models/dot4.jpg'), 1)
    sphere.reparentTo(np)
    sphere.setScale(0.5)

    # import pdb; pdb.set_trace()
    geom = np \
        .findAllMatches('**/+GeomNode').getPath(0).node() \
        .modifyGeom(0)
    node.linkGeom(geom)

    
    # end, tip = sphere.getTightBounds()
    # size = tip - end
    # np.node().addShape(BulletBoxShape(size / 2))
    # np.setCollideMask(BitMask32.bit(1))
    # np.node().setMass(0, 1)
    # np.node().setMass(1, 1)
    world.attachSoftBody(np.node())
   
    return np
    
    
    
    # fmt = GeomVertexFormat.getV3n3t2()
    # geom = BulletHelper.makeGeomFromFaces(node, fmt, True)
    # node.linkGeom(geom)
    # nodeV = GeomNode('ellipsoidVisual')
    # nodeV.addGeom(geom)
    # npV = np.attachNewNode(nodeV)
    # # npV.setColor(0, 0, 0, 0)

    # tex = base.loader.loadTexture('models/envir-rock1.jpg')
    # npV.setTexture(tex)


