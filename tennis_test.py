from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletWorld, BulletDebugNode
from panda3d.bullet import BulletCapsuleShape, BulletCylinderShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp

from panda3d.core import NodePath, PandaNode
from panda3d.core import Point3, Vec3, BitMask32
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait


from scene_test import Scene


# class TennisBall(NodePath):

#     def __init__(self, traverser, queue):
#         super().__init__(PandaNode('tennisBall'))
#         self.reparentTo(base.render)
#         self.model = base.loader.loadModel('models/tennisball/tennisball')
#         self.model.reparentTo(self)
#         self.setScale(2)
#         self.create_collision_detector(traverser, queue)

#     def create_collision_detector(self, traverser, queue):
#         col_sphere = CollisionSphere(center=(0, 0, 0), radius=0.2)
#         col_node = CollisionNode('ball')
#         col_node.setFromCollideMask(BitMask32.bit(1))
#         col_path = self.model.attachNewNode(col_node)
#         col_path.node().addSolid(col_sphere)
#         traverser.addCollider(col_path, queue)
#         col_path.show()

    #     # ground_ray = CollisionRay(Point3(0, 0, 0), Vec3(0, 0, -1))
    #     # ground_col = CollisionNode('ballRay')
    #     # ground_col.setIntoCollideMask(BitMask32.bit(1))
    #     # ground_col_path = self.model.attachNewNode(ground_col)
    #     # ground_col_path.node().addSolid(ground_ray)
    #     # traverser.addCollider(ground_col_path, queue)

    #     # ground_col_path.show()


class Eve(NodePath):

    def __init__(self, world):
        super().__init__(PandaNode('eve'))
        self.reparentTo(base.render)

        self.eve = Actor('models/eve/eve.egg', {
                         'walk': 'models/eve/eve-walk',
                         'run': 'models/eve/eve-run',
                         'jump': 'models/eve/eve-jump'})

        end, tip = self.eve.getTightBounds()
        # h, w = 1.75, 0.4
        # import pdb; pdb.set_trace()
        # shape = BulletCapsuleShape((tip - end) / 2, tip - end, ZUp)
        shape = BulletCylinderShape((tip - end) / 2)
        self.character = BulletCharacterControllerNode(shape, 0.4, 'player')
        self.character_np = self.attachNewNode(self.character)
        self.character_np.setPos(-2, 0, 14)
        self.character_np.setCollideMask(BitMask32.bit(1))
        world.attachCharacter(self.character)
        self.eve.reparentTo(self.character_np)
        self.eve.setPos(0, 0, -2.5)
        # self.eve.actorInterval('jump', duration=0.5).loop()
        
        

        # self.character.setScale(1.5)
        # self.character.setPos(0, 0, 0.5)


class Tennis(ShowBase):

    def __init__(self):
        super().__init__(self)
        self.disableMouse()
        self.camLens.setFov(60)
        self.camera.setPos(0, -40, 10)
        self.camera.lookAt(0, 20, 5)

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.scene = Scene(self.world)
        self.eve = Eve(self.world)

        self.crouching = False
        
        # *******************************************
        collide_debug = self.render.attachNewNode(BulletDebugNode('debug'))
        self.world.setDebugNode(collide_debug.node())
        collide_debug.show()
        # *******************************************

        taskMgr.add(self.update, 'update')


    def move(self):
        speed = Vec3(0, 0, 0)
        omega = 0.0

        speed.setY(3.0)

        self.eve.character.setAngularMovement(omega)
        self.eve.character.setLinearMovement(speed, True)

    def jump(self):
        self.eve.character.setMaxJumpHeight(5.0)
        self.eve.character.setJumpSpeed(8.0)
        self.eve.character.doJump()

   
    def update(self, task):
        dt = globalClock.getDt()

        # result = self.world.contactTest(self.scene.ground.node())
        result = self.world.contactTest(self.eve.character)

        # for name in set(con.getNode0().getName() for con in result.getContacts()):
        for name in set(con.getNode1().getName() for con in result.getContacts()):
            print(name)
        self.doCrouch()
        # self.move()
        # self.jump()

        # for entry in self.collision_handler.entries:
        #     print(entry.getIntoNode().name)
        #     print('get into node path', entry.getIntoNodePath())
        #     print('get from node path', entry.getFromNodePath())
        #     print('surface point render', entry.getSurfacePoint(self.render))
        #     print('surface normal render', entry.getSurfaceNormal(self.render))
        #     print('surface point into obj', entry.getSurfacePoint(entry.getIntoNodePath()))
        #     print('surface normal into obj', entry.getSurfaceNormal(entry.getIntoNodePath()))
        self.world.doPhysics(dt)
        return Task.cont




if __name__ == '__main__':
    tennis = Tennis()
    tennis.run()
