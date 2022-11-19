import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.core import Vec3, Point3
from direct.showbase.ShowBaseGlobal import globalClock

from scene import Scene
from gimmicks import Polyhedrons, Cones, CircularSaws, Spheres, EmbeddedGimmiks
from characters import SnowMan


class ClimbStairs(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        # self.camera.setPos(Point3(-14.6, -16, 10.8))
        self.camera.setPos(Point3(-14.6, -15, 11))
        # self.camera.lookAt(5, 7, 4)
        self.camera.setHpr(Vec3(-41, -18, 0))

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.scene = Scene(self.world)

        self.snowman = SnowMan(Point3(-1, 2, 0), self.world)
        self.camera_before_x = self.snowman.getX()

        self.cones = Cones(self.scene.stairs, self.world)
        self.saws = CircularSaws(self.scene.stairs, self.world)
        self.polhs = Polyhedrons(self.scene.stairs, self.world, 50)
        self.spheres = Spheres(self.scene.stairs, self.world, 50)
        self.timer = 0
        self.toggle = True
        self.reset = False

        # *******************************************
        collide_debug = self.render.attachNewNode(BulletDebugNode('debug'))
        self.world.setDebugNode(collide_debug.node())
        collide_debug.show()
        # *******************************************

        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, 'update')

    def move_camera(self):
        """Change camera x and z with the movement of snowman.
        """
        if (distance := self.snowman.getX() - self.camera_before_x) != 0:
            self.camera_before_x = self.snowman.getX()
            pos = self.camera.getPos() + Vec3(distance, 0, distance)
            self.camera.setPos(pos)

    def clean_floor(self):
        """Remove polhs and spheres collided with the floor 3 seconds later.
        """
        result = self.world.contactTest(self.scene.floor.node())
        for con in result.getContacts():
            if (name := con.getNode0().getName()).startswith(('polhs', 'spheres')):
                if not self.taskMgr.hasTaskNamed(name):
                    func = self.polhs.delete if 'polhs' in name else self.spheres.delete
                    self.taskMgr.doMethodLater(
                        3, func, name, extraArgs=[name], appendTask=True)

    def update(self, task):
        dt = globalClock.getDt()

        self.snowman.update(dt)
        # print('self.snowman', self.snowman.stair)
        # increase stair
        if self.scene.stairs.top_stair - self.snowman.stair < 14:
            self.scene.stairs.increase()
        # move camera with the snowman.
        self.move_camera()

        # control gimmicks
        if task.time > self.timer:
            if self.toggle:
                self.polhs.drop(self.snowman.stair, self.snowman.getPos())
            else:
                self.spheres.drop(self.snowman.stair, self.snowman.getPos())
            self.toggle = not self.toggle
            self.timer += 3

        # if self.reset and not self.snowman.falling:
        #     EmbeddedGimmiks.reset(self.cones, self.saws)
        #     self.reset = False

        self.cones.run(dt, self.snowman, self.saws.stair)
        self.saws.run(dt, self.snowman, self.cones.stair)

        if any(obj.stair > self.snowman.stair + 10 for obj in (self.saws, self.cones)):
            self.saws.reset(self.snowman.stair, self.cones)
            self.cones.reset(self.snowman.stair, self.saws)

        # remove polyhedrons and spheres on the floor.
        self.clean_floor()

        self.world.doPhysics(dt)
        return task.cont


if __name__ == '__main__':
    game = ClimbStairs()
    game.run()
