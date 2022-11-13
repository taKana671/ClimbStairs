import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletCharacterControllerNode, BulletDebugNode
from panda3d.core import Vec3, BitMask32
from panda3d.core import NodePath, TransformState
# from panda3d.core import AmbientLight, DirectionalLight
from direct.showbase.ShowBaseGlobal import globalClock
from direct.showbase.InputStateGlobal import inputState

from scene import Scene
from gimmicks import Polyhedrons, Cones, CircularSaws, Spheres, EmbeddedGimmiks


class SnowMan(NodePath):

    def __init__(self, world):
        self.model = base.loader.loadModel('models/snowman/snowman')
        self.model.setTransform(TransformState.makePos(Vec3(0, 0, -3)))
        height, radius = 7.0, 1.5
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)
        super().__init__(BulletCharacterControllerNode(shape, 0.4, 'snowman'))
        self.reparentTo(base.render)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2))
        # self.setCollideMask(BitMask32.allOn())
        self.setPos(-1, 2, 0)
        self.setH(90)
        world.attachCharacter(self.node())
        self.model.reparentTo(self)
        self.setScale(0.3)

        self.stair = 0
        self.stair_before = 0
        self.falling = False

    def calc_climbed_steps(self):
        """Calculate the stair on which snowman is.
           Because the gap between the steps is 1 and the z of snowman's center
           is about 0.95, int(z) means the stair on which snowman is.
        """
        if self.node().isOnGround():
            if (z := int(self.getPos().z)) != self.stair:
                self.stair_before = self.stair
                self.stair = z

        # if self.node().isOnGround():
        #     self.stair = int(self.getPos().z)

    def is_jump(self, stair):
        """Return True if snowman is jumping onto the next stair
           in which gimmicks are embeded.
           Args:
                stair: index of stair in which gimmicks are embeded.
                The index of stairs starts with 0, but snowman's stair starts with 1.
        """
        if stair == self.stair and \
                not self.node().isOnGround():
            return True

    def fall(self, dt):
        distance = dt * 5

        if (x := self.getX() - distance) < -1:
            self.falling = False
        else:
            self.setX(x)


class ClimbStairs(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.camera.setPos(-11, -16, 13)

        # self.camera.setPos(-11, -16, 20)
        # self.camera.lookAt(5, 7, 10)

        # self.camera.lookAt(5, 7, 4)
        self.camera.setHpr(-35, -18, 0)
        self.camera_before_x = 0

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.scene = Scene(self.world)

        self.snowman = SnowMan(self.world)

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

        inputState.watchWithModifiers('forward', 'arrow_up')
        inputState.watchWithModifiers('backward', 'arrow_down')
        inputState.watchWithModifiers('left', 'arrow_left')
        inputState.watchWithModifiers('right', 'arrow_right')
        inputState.watchWithModifiers('jump', 'enter')
        inputState.watchWithModifiers('turn_right', 'q')
        inputState.watchWithModifiers('turn_left', 'w')
        self.accept('enter', self.do_jump)
        self.accept('escape', sys.exit)

        self.taskMgr.add(self.update, 'update')

    def do_jump(self):
        self.snowman.node().setMaxJumpHeight(2.0)  # 5.0
        self.snowman.node().setJumpSpeed(5.0)      # 8.0
        self.snowman.node().doJump()

    def control_character(self):
        speed = Vec3(0, 0, 0)
        omega = 0.0

        if inputState.isSet('left'):
            speed.setX(2.0)
        elif inputState.isSet('right'):
            speed.setX(-2.0)
        elif inputState.isSet('forward'):
            speed.setY(-2.0)
        elif inputState.isSet('backward'):
            speed.setY(2.0)
        elif inputState.isSet('turn_right'):
            omega = -120
        elif inputState.isSet('turn_left'):
            omega = 120

        self.snowman.node().setAngularMovement(omega)
        self.snowman.node().setLinearMovement(speed, True)

    def move_camera(self):
        """Change camera x and z with the movement of snowman.
           The width and height of stairs increase by one like below.
            idx      pos
             0   LPoint3f(0, 0, 1)
             1   LPoint3f(1, 0, 2)
             2   LPoint3f(2, 0, 3)
             3   LPoint3f(3, 0, 4)
        """
        if (x := self.snowman.getX()) <= 2:
            self.camera_before_x = x
        elif (distance := self.snowman.getX() - self.camera_before_x) != 0:
            self.camera_before_x = self.snowman.getX()
            pos = self.camera.getPos()
            self.camera.setPos(pos.x + distance, pos.y, pos.z + distance)

    def update(self, task):
        dt = globalClock.getDt()

        if self.snowman.falling:
            self.snowman.fall(dt)
        self.control_character()
        self.snowman.calc_climbed_steps()

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

        if self.reset and not self.snowman.falling:
            EmbeddedGimmiks.reset(self.cones, self.saws)
            self.reset = False
        self.cones.run(dt, self.snowman, self.saws.stair)
        self.saws.run(dt, self.snowman, self.cones.stair)

        # remove polyhedrons and spheres on the floor.
        result = self.world.contactTest(self.scene.floor.node())
        for con in result.getContacts():
            if (name := con.getNode0().getName()).startswith('polhs'):
                self.polhs.delete(name)
            elif name.startswith('spheres'):
                self.spheres.delete(name)

        if not self.snowman.falling:
            result = self.world.contactTest(self.snowman.node())
            for con in result.getContacts():
                name = con.getNode1().getName()
                if name.split('_')[0] in {'spheres', 'cones', 'saws', 'polhs'}:
                    print('collision', name)
                    self.reset = True
                    self.snowman.falling = True
                    break

        self.world.doPhysics(dt)
        return task.cont


if __name__ == '__main__':
    game = ClimbStairs()
    game.run()
