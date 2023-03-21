import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.core import Vec3, Point3, TextNode
from panda3d.core import PandaNode, NodePath
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBaseGlobal import globalClock
from direct.showbase.InputStateGlobal import inputState

from scene import Scene
from characters import SnowMan
from gimmicks import DropGimmicks, PopOutGimmiks


class ScoreDisplay(OnscreenText):

    def __init__(self):
        super().__init__(
            text='',
            # parent=base.a2dTopLeft,
            align=TextNode.ALeft,
            pos=(0.05, -0.1),
            scale=0.1,
            mayChange=True
        )


class Instructions(NodePath):

    def __init__(self):
        super().__init__(PandaNode('instructions'))

        self.make_instructions([
            '[ESC]: Quit',
            '[Enter]: Jump',
            '[Enter] + [Up Arrow]: Go up',
            '[Left Arrow]: Go to the left',
            '[Right Arrow]: Go to the right',
            '[Down Arrow]: Go to the back'
        ])

    def make_instructions(self, instructions):
        pos = -0.2

        for text in instructions:
            OnscreenText(
                text=text,
                parent=self,
                align=TextNode.ALeft,
                pos=(0.05, pos),
                scale=0.05,
                fg=(1, 1, 1, 1),
            )
            pos += -0.05


class ClimbStairs(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.camera.setPos(Point3(-14.6, -15, 11))
        self.camera.setHpr(Vec3(-41, -18, 0))

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        self.debug_np = self.render.attachNewNode(BulletDebugNode('debug'))
        self.world.setDebugNode(self.debug_np.node())

        self.scene = Scene(self.world)
        self.climber = SnowMan(Point3(-1.0, 0.0, 0.0), self.world)
        self.popout_gimmicks = PopOutGimmiks(self.scene.stairs, self.world)
        self.drop_gimmicks = DropGimmicks(self.scene.stairs, self.world)

        self.diff = self.camera.getX() - self.climber.getX()
        self.timer = 0
        self.drop_sphere = True
        self.delete_delay_time = 3

        inputState.watchWithModifiers('forward', 'arrow_up')
        inputState.watchWithModifiers('backward', 'arrow_down')
        inputState.watchWithModifiers('left', 'arrow_left')
        inputState.watchWithModifiers('right', 'arrow_right')
        inputState.watchWithModifiers('jump', 'enter')

        self.display = ScoreDisplay()
        self.display.reparentTo(self.a2dTopLeft)
        self.instructions = Instructions()
        self.instructions.reparentTo(self.a2dTopLeft)

        self.accept('d', self.toggle_debug)
        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, 'update')

    def toggle_debug(self):
        if self.debug_np.isHidden():
            self.debug_np.show()
        else:
            self.debug_np.hide()

    def control_climber(self, dt):
        speed = Vec3(0, 0, 0)

        if inputState.isSet('jump'):
            self.climber.do_jump()

        if inputState.isSet('left'):
            speed.setX(2.0)
        if inputState.isSet('right'):
            speed.setX(-2.0)
        if inputState.isSet('forward'):
            speed.setY(-2.0)
        if inputState.isSet('backward'):
            speed.setY(2.0)

        self.climber.update(dt, speed)

    def move_camera(self):
        """Change camera x and z with the movement of a climber.
        """
        if (dist := self.diff - (self.camera.getX() - self.climber.getX())) != 0:
            pos = self.camera.getPos() + Vec3(dist, 0, dist)
            self.camera.setPos(pos)

    def clean_floor(self):
        """Remove polhs and spheres 3 seconds later
           than they collided with the floor.
        """
        result = self.world.contactTest(self.scene.floor.node(), True)

        for con in result.getContacts():
            if (node := con.getNode0()) != self.climber.node():
                if not self.taskMgr.hasTaskNamed(node.getName()):
                    self.taskMgr.doMethodLater(
                        self.delete_delay_time,
                        self.drop_gimmicks.delete,
                        node.getName(),
                        extraArgs=[node],
                        appendTask=True
                    )

    def decide_interval(self):
        if self.climber.stair >= 40:
            return 1
        elif self.climber.stair >= 20:
            return 2
        return 3

    def update(self, task):
        dt = globalClock.getDt()

        # move climber and display score
        self.control_climber(dt)
        self.move_camera()
        self.display.setText(str(self.climber.stair))

        # increase stair
        if self.scene.stairs.top_stair - self.climber.stair < 14:
            self.scene.stairs.increase()

        # control gimmicks
        if task.time > self.timer:
            self.drop_gimmicks.drop(self.climber, self.drop_sphere)
            self.drop_sphere = not self.drop_sphere
            interval = self.decide_interval()
            self.timer = task.time + interval

        self.popout_gimmicks.pop_out(dt, self.climber)

        # remove polyhedrons and spheres on the floor.
        self.clean_floor()

        self.world.doPhysics(dt)
        return task.cont


if __name__ == '__main__':
    game = ClimbStairs()
    game.run()
