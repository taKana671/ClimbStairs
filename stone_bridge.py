import sys

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import PandaNode, NodePath, CollisionNode
from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3, LColor, BitMask32
from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode

from scene import Scene
from stone import Piece, Stone


class Waker(NodePath):

    def __init__(self):
        super().__init__(PandaNode('walker'))
        self.reparentTo(base.render)
        self.eve = Actor('models/eve/eve',
                         {'walk': 'models/eve/eve_walk',
                          'run': 'models/eve/eve-run',
                          'jump': 'models/eve/eve-jump'})
        self.eve.reparentTo(self)
        self.setScale(0.3)
        self.setPos(Point3(0, 0, 2))


class Candy(NodePath):

    def __init__(self, candy_pos):
        super().__init__(PandaNode('candycane'))
        self.reparentTo(base.render)
        self.candy = base.loader.loadModel('models/candycane/candycane')
        self.candy.reparentTo(self)
        self.setScale(1)
        self.setHpr(45, 90, 0)
        self.setPos(candy_pos)


class StoneBridgeGame(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        base.camera.setPosHpr(0, -12, 8, 0, -35, 0)

        self.scene = Scene()
        self.walker = Waker()
        self.setup_start()
        self.setup_goal()
        self.setup_detection()

        # self.walker.setPos(pos.x, pos.y, 0.5)
        # self.walker.eve.actorInterval('run', playRate=0.5).loop()
        # self.candy = Candy(self.scene.goal_stone.getPos())
        self.piece = Piece(self.scene.board)
        self.total_angle = 0

        self.accept('escape', sys.exit)
        self.accept('mouse1', self.click)
        self.accept('mouse1-up', self.release)
        self.taskMgr.add(self.update, 'update')

    def release(self):
        if (tag := self.detect(self.scene.board, 'square')) is not None:
            print('release', tag)

    def click(self):
        if (tag := self.detect(self.piece, 'stone')) is not None:
            print('click', tag)

    def detect(self, np, key):
        pos = self.mouseWatcherNode.getMouse()
        self.picker_ray.setFromLens(self.camNode, pos.getX(), pos.getY())
        self.picker.traverse(np)

        if self.handler.getNumEntries() > 0:
            self.handler.sortEntries()
            tag = int(self.handler.getEntry(0).getIntoNode().getTag(key))
            return tag
        return None

    def setup_detection(self):
        self.picker = CollisionTraverser()
        self.handler = CollisionHandlerQueue()

        self.picker_node = CollisionNode('mouseRay')
        self.picker_np = self.camera.attachNewNode(self.picker_node)
        self.picker_node.setFromCollideMask(BitMask32.bit(1))
        self.picker_ray = CollisionRay()
        self.picker_node.addSolid(self.picker_ray)
        self.picker.addCollider(self.picker_np, self.handler)

    def setup_start(self):
        grid_center = self.scene.board.grid_center(7, -1)
        self.start_stone = Stone(self.render, grid_center, 'start')
        self.walker.setPos(grid_center.x, grid_center.y, 0.5)

    def setup_goal(self):
        grid_center = self.scene.board.grid_center(5, 8)
        self.goal_stone = Stone(self.render, grid_center, 'goal')
        candy_pos = Point3(grid_center.x - 0.5, grid_center.y + 0.5, 0.5)
        self.candy = Candy(candy_pos)

    def update(self, task):
        # if self.total_angle <= 180:
        #     pt = Point3(-2.05, -1.64 + 0.41, self.piece3.pos_z)
        #     axis = Vec3.left()
        #     angle = 30 * globalClock.getDt()
        #     self.piece1.rotate_around(pt, axis, angle)
        #     self.piece2.rotate_around(pt, axis, angle)
        #     self.piece3.rotate_around(pt, axis, angle)
        #     self.total_angle += angle

        return task.cont


if __name__ == '__main__':
    game = StoneBridgeGame()
    base.run()


# LPoint3f(-2.87, -2.46, -1)
# LPoint3f(-2.05, -2.46, -1)
# LPoint3f(-1.23, -2.46, -1)
# LPoint3f(-0.41, -2.46, -1)
# LPoint3f(0.41, -2.46, -1)
# LPoint3f(1.23, -2.46, -1)
# LPoint3f(2.05, -2.46, -1)
# LPoint3f(2.87, -2.46, -1)
# LPoint3f(-2.87, -1.64, -1)
# LPoint3f(-2.05, -1.64, -1)
# LPoint3f(-1.23, -1.64, -1)
# LPoint3f(-0.41, -1.64, -1)
# LPoint3f(0.41, -1.64, -1)
# LPoint3f(1.23, -1.64, -1)
# LPoint3f(2.05, -1.64, -1)
# LPoint3f(2.87, -1.64, -1)
# LPoint3f(-2.87, -0.82, -1)
# LPoint3f(-2.05, -0.82, -1)
# LPoint3f(-1.23, -0.82, -1)
# LPoint3f(-0.41, -0.82, -1)
# LPoint3f(0.41, -0.82, -1)
# LPoint3f(1.23, -0.82, -1)
# LPoint3f(2.05, -0.82, -1)
# LPoint3f(2.87, -0.82, -1)
# LPoint3f(-2.87, 0, -1)
# LPoint3f(-2.05, 0, -1)
# LPoint3f(-1.23, 0, -1)
# LPoint3f(-0.41, 0, -1)
# LPoint3f(0.41, 0, -1)
# LPoint3f(1.23, 0, -1)
# LPoint3f(2.05, 0, -1)
# LPoint3f(2.87, 0, -1)
# LPoint3f(-2.87, 0.82, -1)
# LPoint3f(-2.05, 0.82, -1)
# LPoint3f(-1.23, 0.82, -1)
# LPoint3f(-0.41, 0.82, -1)
# LPoint3f(0.41, 0.82, -1)
# LPoint3f(1.23, 0.82, -1)
# LPoint3f(2.05, 0.82, -1)
# LPoint3f(2.87, 0.82, -1)
# LPoint3f(-2.87, 1.64, -1)
# LPoint3f(-2.05, 1.64, -1)
# LPoint3f(-1.23, 1.64, -1)
# LPoint3f(-0.41, 1.64, -1)
# LPoint3f(0.41, 1.64, -1)
# LPoint3f(1.23, 1.64, -1)
# LPoint3f(2.05, 1.64, -1)
# LPoint3f(2.87, 1.64, -1)
# LPoint3f(-2.87, 2.46, -1)
# LPoint3f(-2.05, 2.46, -1)
# LPoint3f(-1.23, 2.46, -1)
# LPoint3f(-0.41, 2.46, -1)
# LPoint3f(0.41, 2.46, -1)
# LPoint3f(1.23, 2.46, -1)
# LPoint3f(2.05, 2.46, -1)
# LPoint3f(2.87, 2.46, -1)
# LPoint3f(-2.87, 3.28, -1)
# LPoint3f(-2.05, 3.28, -1)
# LPoint3f(-1.23, 3.28, -1)
# LPoint3f(-0.41, 3.28, -1)
# LPoint3f(0.41, 3.28, -1)
# LPoint3f(1.23, 3.28, -1)
# LPoint3f(2.05, 3.28, -1)
# LPoint3f(2.87, 3.28, -1)






