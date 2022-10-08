from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletBoxShape
from panda3d.core import Vec2, Vec3, Point3, LColor, BitMask32
from panda3d.core import NodePath, PandaNode, TransformState


PATH_SPHERE = 'models/sphere/sphere'
PATH_CARNSX = 'models/carnsx/carnsx'
 

class Sphere(NodePath):

    def __init__(self, top_stair):
        super().__init__(BulletRigidBodyNode('sphere'))
        self.reparentTo(base.render)
        sphere = base.loader.loadModel(PATH_SPHERE)
        sphere.reparentTo(self)
        end, tip = sphere.getTightBounds()
        self.node().addShape(BulletSphereShape((tip - end).z / 2))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(1)
        self.node().setRestitution(0.7)
        self.setScale(0.1)
        self.setColor(0, 1, 0, 1)  # Lime

        pos = Point3(top_stair.x, top_stair.y, top_stair.z + 5)
        self.setPos(pos)


class CarNsx(NodePath):

    def __init__(self, top_stair):
        super().__init__(BulletRigidBodyNode('sphere'))
        self.reparentTo(base.render)
        sphere = base.loader.loadModel(PATH_CARNSX)
        sphere.reparentTo(self)

        end, tip = sphere.getTightBounds()
        size = tip - end
        half = size / 2
        center = tip - half

        self.node().addShape(BulletBoxShape(half), TransformState.makePos(center))
        self.setCollideMask(BitMask32.bit(1))
        self.node().setMass(1)
        self.node().setRestitution(0.7)
        self.setScale(0.5)
        # self.setH(-90)
        self.setR(90)

        pos = Point3(top_stair.x, top_stair.y, top_stair.z + 0.6)
        self.setPos(pos)
