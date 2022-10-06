from direct.showbase.ShowBase import ShowBase
from panda3d.core import PandaNode, NodePath, CardMaker
from panda3d.core import Vec3, Point3, LPlanef
from panda3d.core import CollisionNode, BitMask32, CollisionPlane, CollisionBox

from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletPlaneShape


PATH_AXIS = 'models/zup-axis'
PATH_GROUND = 'textures/ground.jpg'
PATH_SKY = 'models/blue-sky/blue-sky-sphere'
PATH_NET = 'models/tennisnet/tennisnet'


class Axis(NodePath):

    def __init__(self):
        super().__init__(PandaNode('axis'))
        self.reparentTo(base.render)
        axis = base.loader.loadModel(PATH_AXIS)
        axis.setScale(0.5)
        axis.reparentTo(self)


class Sky(NodePath):

    def __init__(self):
        super().__init__(PandaNode('sky'))
        self.reparentTo(base.render)
        sky = base.loader.loadModel(PATH_SKY)
        sky.setColor(2, 2, 2, 1)
        sky.setScale(0.02)
        sky.reparentTo(self)


class Ground(NodePath):

    def __init__(self):
        super().__init__(BulletRigidBodyNode('ground'))
        self.reparentTo(base.render)
        # ground = self.create_ground()
        # ground.reparentTo(self)
        self.setCollideMask(BitMask32.bit(1))
        self.node().addShape(BulletPlaneShape(Vec3.up(), 0))

    def create_ground(self):
        model = NodePath(PandaNode('groundModel'))
        card = CardMaker('card')
        size = 2
        half = size / 2
        card.setFrame(-half, half, -half, half)
        max_card = 50

        for y in range(max_card):
            for x in range(max_card):
                g = model.attachNewNode(card.generate())
                g.setP(-90)
                pt = Point3((x - max_card / 2) * size, (y - max_card / 2) * size, 0)
                g.setPos(pt)

        texture = base.loader.loadTexture(PATH_GROUND)
        model.setTexture(texture)
        model.flattenStrong()
        model.setPos(Point3(0, 0, 0))  # 0, 30, 0

        return model

class Scene:

    def __init__(self, world):
        self.sky = Sky()
        self.ground = Ground()
        world.attachRigidBody(self.ground.node())


if __name__ == '__main__':
    base = ShowBase()
    base.disableMouse()
    base.camera.setPos(30, -30, 10)
    base.camera.lookAt(-10, 20, 5)

    # base.camera.setPosHpr(0, -8, 2.5, 0, -9, 0)

    scene = Scene()
    base.run()
