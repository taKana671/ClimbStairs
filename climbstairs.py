import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.core import Vec3, Point3, TextNode
from panda3d.core import PandaNode, NodePath
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBaseGlobal import globalClock
from direct.showbase.InputStateGlobal import inputState

from characters import Characters
from gimmicks import DropGimmicks, PopOutGimmiks
from lights import BasicAmbientLight, BasicDayLight
from scene import Scene


class ScoreDisplay(OnscreenText):

    def __init__(self):
        super().__init__(
            text='',
            parent=base.a2dTopLeft,
            align=TextNode.ALeft,
            pos=(0.05, -0.1),
            scale=0.1,
            mayChange=True
        )


class Instructions(NodePath):

    def __init__(self):
        super().__init__(PandaNode('instructions'))
        self.reparent_to(base.a2dTopLeft)

        self.make_instructions([
            '[ESC]: Quit',
            '[Up Arrow]: Go up',
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
        self.camera.set_pos(Point3(-14.6, -15, 11))
        self.camera.set_hpr(Vec3(-41, -18, 0))

        self.world = BulletWorld()
        self.world.set_gravity(Vec3(0, 0, -9.81))
        self.debug_np = self.render.attach_new_node(BulletDebugNode('debug'))
        self.world.set_debug_node(self.debug_np.node())

        self.scene = Scene(self.world)
        self.scene.reparent_to(self.render)

        self.ambient_light = BasicAmbientLight()
        self.directional_light = BasicDayLight(parent=self.camera)

        self.climber = Characters(self.scene.stairs, self.world)
        self.climber.reparent_to(self.render)

        self.popout_gimmicks = PopOutGimmiks(self.scene.stairs, self.world)
        self.drop_gimmicks = DropGimmicks(self.scene.stairs, self.world)
        self.drop_gimmicks_num = sum(1 if key.endswith('maker') else 0 for key in self.drop_gimmicks.__dict__.keys())

        self.diff = self.camera.get_x() - self.climber.get_x()
        self.timer = 0
        self.next_drop = 0
        self.delete_delay_time = 3

        self.display = ScoreDisplay()
        self.instructions = Instructions()

        inputState.watch_with_modifiers('forward', 'arrow_up')
        inputState.watch_with_modifiers('backward', 'arrow_down')
        inputState.watch_with_modifiers('left', 'arrow_left')
        inputState.watch_with_modifiers('right', 'arrow_right')

        self.accept('d', self.toggle_debug)
        self.accept('i', self.toggle_instructions)
        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, 'update')

    def toggle_debug(self):
        if self.debug_np.is_hidden():
            self.debug_np.show()
        else:
            self.debug_np.hide()

    def toggle_instructions(self):
        if self.instructions.is_hidden():
            self.instructions.show()
        else:
            self.instructions.hide()

    def control_climber(self, dt):
        speed = Vec3(0, 0, 0)

        if inputState.is_set('left'):
            speed.set_x(2.0)
        if inputState.is_set('right'):
            speed.set_x(-2.0)
        if inputState.is_set('forward'):
            speed.set_y(-2.0)
        if inputState.is_set('backward'):
            speed.set_y(2.0)

        self.climber.update(dt, speed)

    def move_camera(self):
        """Change camera x and z with the movement of a climber.
        """
        if (dist := self.diff - (self.camera.get_x() - self.climber.get_x())) != 0:
            pos = self.camera.get_pos() + Vec3(dist, 0, dist)
            self.camera.set_pos(pos)

    def clean_floor(self):
        """Remove polhs and spheres 3 seconds later
           than they collided with the floor.
        """
        result = self.world.contact_test(self.scene.floor.node(), True)

        for con in result.get_contacts():
            if (node := con.get_node0()) != self.climber.node():
                if not self.taskMgr.hasTaskNamed(node.get_name()):
                    self.taskMgr.do_method_later(
                        self.delete_delay_time,
                        self.drop_gimmicks.delete,
                        node.get_name(),
                        extraArgs=[node],
                        appendTask=True
                    )

    def decide_interval(self):
        if self.climber.current_stair >= 40:
            return 1
        elif self.climber.current_stair >= 20:
            return 2
        return 3

    def update(self, task):
        dt = globalClock.get_dt()

        # move climber, and display score
        self.control_climber(dt)
        self.move_camera()
        self.display.setText(str(self.climber.current_stair))

        # increase stair
        if self.scene.stairs.top_stair - self.climber.current_stair < 14:
            self.scene.stairs.increase()

        # control gimmicks
        if task.time > self.timer:
            self.drop_gimmicks.drop(self.climber, self.next_drop)
            self.next_drop = n if (n := self.next_drop + 1) < self.drop_gimmicks_num else 0
            print(self.next_drop)
            interval = self.decide_interval()
            self.timer = task.time + interval

        self.popout_gimmicks.pop_out(dt, self.climber)

        # remove polyhedrons and spheres on the floor.
        self.clean_floor()

        self.world.do_physics(dt)
        return task.cont


if __name__ == '__main__':
    game = ClimbStairs()
    game.run()
