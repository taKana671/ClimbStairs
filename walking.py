import sys

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import PandaNode, NodePath
from direct.actor.Actor import Actor
from panda3d.core import Vec3, Point3, LColor, Quat

from scene import Scene, Stone


class Piece(Stone):

    def __init__(self):
        super().__init__()

    def rotate_around(self, pt, axis, angle):
        pos = self.getPos()
        q = Quat()
        q.setFromAxisAngle(angle, axis.normalized())
        r = q.xform(pos - pt)
        rotated_pos = pt + r
        self.setPos(rotated_pos)

        self.setP(self.getP() - angle)

        # forward = axis.cross(r)
        # if angle < 0:
        #     forward *= -1
        # self.lookAt(rotated_pos + forward, axis)


class Waker(NodePath):

    def __init__(self):
        super().__init__(PandaNode('walker'))
        self.reparentTo(base.render)
        self.eve = Actor('models/eve/eve',
                         {'walk': 'models/eve/eve_walk',
                          'run': 'models/eve/eve_run',
                          'jump': 'models/eve/eve-jump'})
        self.eve.reparentTo(self)
        self.setScale(0.3)
        self.setPos(Point3(0, 0, 2))


class Candy(NodePath):

    def __init__(self, goal):
        super().__init__(PandaNode('candycane'))
        self.reparentTo(base.render)
        self.candy = base.loader.loadModel('models/candycane/candycane')
        self.candy.reparentTo(self)
        self.setScale(1)
        self.setHpr(45, 90, 0)
        self.setPos(Point3(goal.x - 0.5, goal.y + 0.5, 0.5))


class Walking(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        base.camera.setPosHpr(0, -12, 8, 0, -35, 0)

        self.scene = Scene()
        self.walker = Waker()
        pos = self.scene.start_stone.getPos()
        self.walker.setPos(pos.x, pos.y, 0.5)
        # self.walker.eve.actorInterval('jump', playRate=0.5).loop()
        self.candy = Candy(self.scene.goal_stone.getPos())
        self.set_stones()
        self.total_angle = 0

        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, 'update')

    def set_stones(self):
        self.piece1 = Piece()
        pos = Point3(-2.87, -2.46, self.piece1.pos_z)
        self.piece1.setPos(pos)

        self.piece2 = Piece()
        pos = Point3(-2.05, -2.46, self.piece2.pos_z)
        self.piece2.setPos(pos)

        self.piece3 = Piece()
        pos = Point3(-2.05, -1.64, self.piece3.pos_z)
        self.piece3.setPos(pos)
        # self.piece3.stone.hprInterval(5, Vec3(0, -360, 0)).start()

    def update(self, task):
        if self.total_angle <= 180:
            pt = Point3(-2.05, -1.64 + 0.41, self.piece3.pos_z)
            axis = Vec3.left()
            angle = 30 * globalClock.getDt()
            self.piece1.rotate_around(pt, axis, angle)
            self.piece2.rotate_around(pt, axis, angle)
            self.piece3.rotate_around(pt, axis, angle)
            self.total_angle += angle

        return task.cont


if __name__ == '__main__':
    walking = Walking()
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






