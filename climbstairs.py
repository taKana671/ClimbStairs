import sys

from direct.gui.DirectGui import DirectButton
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.core import Vec3, Point3, TextNode
from panda3d.core import PandaNode, NodePath
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBaseGlobal import globalClock

from scene import Scene
from characters import SnowMan
from gimmicks import Polyhedrons, Spheres, Cones, CircularSaws, Piles


class ClimbStairs(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.camera.setPos(Point3(-14.6, -15, 11))
        self.camera.setHpr(Vec3(-41, -18, 0))

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.scene = Scene(self.world)

        self.climber = SnowMan(Point3(-1, 0, 0), self.world)
        self.camera_before_x = self.climber.getX()

        self.cones = Cones(self.scene.stairs, self.world)
        self.saws = CircularSaws(self.scene.stairs, self.world)
        self.piles = Piles(self.scene.stairs, self.world)
        self.polhs = Polyhedrons(self.scene.stairs, self.world, 50)
        self.spheres = Spheres(self.scene.stairs, self.world, 50)

        self.interval = None
        self.timer = 0
        self.toggle = True
        self.play = False

        self.display = OnscreenText(
            text='',
            parent=self.a2dTopLeft,
            align=TextNode.ALeft,
            pos=(0.05, -0.1),
            scale=0.1,
            mayChange=True
        )

        # *******************************************
        # collide_debug = self.render.attachNewNode(BulletDebugNode('debug'))
        # self.world.setDebugNode(collide_debug.node())
        # collide_debug.show()
        # *******************************************

        self.start_screen = StartScreen(self.a2dTopLeft, self.game_start)

        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, 'update')

    def game_start(self, task):
        self.start_screen.removeNode()
        self.play = True
        return task.done

    def move_camera(self):
        """Change camera x and z with the movement of a climber.
        """
        if (distance := self.climber.getX() - self.camera_before_x) != 0:
            self.camera_before_x = self.climber.getX()
            pos = self.camera.getPos() + Vec3(distance, 0, distance)
            self.camera.setPos(pos)

    def clean_floor(self):
        """Remove polhs and spheres 3 seconds later than they collided with the floor.
        """
        result = self.world.contactTest(self.scene.floor.node())
        for con in result.getContacts():
            if (name := con.getNode0().getName()).startswith(('polhs', 'spheres')):
                if not self.taskMgr.hasTaskNamed(name):
                    func = self.polhs.delete if 'polhs' in name else self.spheres.delete
                    self.taskMgr.doMethodLater(
                        3, func, name, extraArgs=[name], appendTask=True)

    def decide_interval(self):
        if self.climber.stair >= 40:
            return 1
        elif self.climber.stair >= 20:
            return 2
        return 3

    def update(self, task):
        dt = globalClock.getDt()

        if self.play:
            self.climber.update(dt)
            self.display.setText(str(self.climber.stair))

            # increase stair
            if self.scene.stairs.top_stair - self.climber.stair < 14:
                self.scene.stairs.increase()

            # move camera with the climber.
            self.move_camera()

            # control gimmicks
            self.interval = self.decide_interval()

            if task.time > self.timer:
                if self.toggle:
                    self.polhs.drop(self.climber)
                else:
                    self.spheres.drop(self.climber)
                self.toggle = not self.toggle
                self.timer = task.time + self.interval

            self.cones.run(dt, self.climber, self.saws.stair, self.piles.stair)
            self.saws.run(dt, self.climber, self.cones.stair, self.piles.stair)
            self.piles.run(dt, self.climber, self.cones.stair, self.saws.stair)

            # remove polyhedrons and spheres on the floor.
            self.clean_floor()

        self.world.doPhysics(dt)
        return task.cont


class StartScreen(NodePath):

    def __init__(self, parent, game_start):
        super().__init__(PandaNode('startScreen'))
        self.reparentTo(parent)

        OnscreenText(
            text='Climb Stairs',
            parent=self,
            align=TextNode.ALeft,
            pos=(0.15, -0.3),
            scale=0.2,
        )
        DirectButton(
            pos=(0.7, 0, -0.5),
            scale=0.07,
            parent=self,
            frameSize=(-2, 2, -0.7, 0.7),
            frameColor=(0.75, 0.75, 0.75, 1),
            text="START",
            text_pos=(0, -0.3),
            command=lambda: base.taskMgr.doMethodLater(0.5, game_start, 'gameStart')
        )
        self.show_instructions([
            '[ESC]: Quit',
            '[Enter]: Jump',
            '[Enter] + [Up Arrow]: Go up',
            '[Left Arrow]: Go to the left',
            '[Right Arrow]: Go to the right',
            '[Down Arrow]: Go to the back'
        ])

    def show_instructions(self, instructions):
        pos = -1.6

        for text in instructions:
            OnscreenText(
                text=text,
                parent=self,
                align=TextNode.ALeft,
                pos=(0.15, pos),
                scale=0.05,
                fg=(1, 1, 1, 1),
            )
            pos += -0.05


if __name__ == '__main__':
    game = ClimbStairs()
    game.run()
