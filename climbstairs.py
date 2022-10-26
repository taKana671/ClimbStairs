import random
import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletRigidBodyNode, BulletCharacterControllerNode, BulletDebugNode
from panda3d.core import Vec2, Vec3, LColor, BitMask32, Point3
from panda3d.core import NodePath, PandaNode, TransformState
from panda3d.core import AmbientLight, DirectionalLight
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.showbase.ShowBaseGlobal import globalClock
from direct.showbase.InputStateGlobal import inputState

from scene import Scene
from obstacles import Shapes, ObstaclesHolder, Cones


class SnowMan(NodePath):

    def __init__(self, world):
        model = base.loader.loadModel('models/snowman/snowman')
        model.setScale(0.3)
        height, radius = 2.0, 0.5
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)
        super().__init__(BulletCharacterControllerNode(shape, 0.4, 'snowman'))
        self.reparentTo(base.render)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(1))
        self.setPos(-1, 2, 0)
        self.setH(90)
        model.reparentTo(self)
        model.setPos(0, 0, -1)
        self.climbed_steps = -1

        world.attachCharacter(self.node())

    def calc_climbed_steps(self):
        """Because the center z of snowman is about 0.95,
           int(z) - 1 means index of the stair on which snowman is.
        """
        if self.node().isOnGround():
            self.climbed_steps = int(self.getPos().z) - 1


class ClimbStairs(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()

        self.look_x = 5
        self.look_y = 7
        self.look_z = 4
        self.camera.setPos(-11, -16, 13)
        # self.camera.setPos(-11, -16, 20)
        # self.camera.lookAt(self.look_x, self.look_y, 10)
        self.camera.lookAt(
            self.look_x, self.look_y, self.look_z)

        # self.setup_lights()

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.scene = Scene(self.world)

        self.character = SnowMan(self.world)

        self.holder = ObstaclesHolder(100)
        self.shapes = Shapes(self.scene.stairs, self.world, self.character, self.holder)
        self.cones = Cones(self.scene.stairs, self.world, self.character, self.holder)
        self.cones.set_target_step()

        self.spheres_wait_time = 0
        self.cones_wait_time = 0

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

        self.accept('z', self.move_camera, ['z', 'up'])
        self.accept('shift-z', self.move_camera, ['z', 'down'])
        self.accept('x', self.move_camera, ['x', 'up'])
        self.accept('shiht-x', self.move_camera, ['x', 'down'])
        self.accept('y', self.move_camera, ['y', 'up'])
        self.accept('shift-y', self.move_camera, ['y', 'down'])

        self.accept('a', self.move_camera, ['h', 'up'])
        self.accept('shift-a', self.move_camera, ['h', 'down'])
        self.accept('s', self.move_camera, ['p', 'up'])
        self.accept('shift-s', self.move_camera, ['p', 'down'])
        self.accept('d', self.move_camera, ['r', 'up'])
        self.accept('shift-d', self.move_camera, ['r', 'down'])

        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, 'update')

    def setup_lights(self):
        ambient_light = self.render.attachNewNode(AmbientLight('ambientLight'))
        ambient_light.node().setColor(LColor(1, 1, 1, 1))
        self.render.setLight(ambient_light)
        directional_light = self.render.attachNewNode(DirectionalLight('directionalLight'))
        directional_light.node().getLens().setFilmSize(200, 200)
        directional_light.node().getLens().setNearFar(1, 100)
        directional_light.node().setColor(LColor(1, 1, 1, 1))
        directional_light.setPos(Point3(0, 0, 50))
        # directional_light.node().setDirection(Vec3(0, 45, -45))
        # directional_light.setPosHpr(Point3(0, 0, 30), Vec3(-30, -45, 0))
        directional_light.node().setShadowCaster(True)
        self.render.setShaderAuto()
        self.render.setLight(directional_light)

    def control_character(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0

        if inputState.isSet('jump'):
            self.character.node().setMaxJumpHeight(2.0)  # 5.0
            self.character.node().setJumpSpeed(5.0)      # 8.0
            self.character.node().doJump()
            return
        elif inputState.isSet('left'):
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

        self.character.node().setAngularMovement(omega)
        self.character.node().setLinearMovement(speed, True)

    def update(self, task):
        dt = globalClock.getDt()
        self.control_character(dt)
        self.character.calc_climbed_steps()
        # print(self.character.node().isOnGround())
        # print(self.character.climbed_steps)

        if task.time > self.spheres_wait_time:
            self.shapes.start()
            self.spheres_wait_time += 3

        if self.cones.hidden and not self.cones.appeared:
            if self.cones.target_step - 1 == self.character.climbed_steps and \
                    not self.character.node().isOnGround():
                self.cones.appear()
                self.cones.hidden = False
                self.cones.appeared = True
        elif not self.cones.hidden and self.cones.appeared:
            if not self.cones.appear_seq.isPlaying():
                self.cones.hide()
                self.cones.appeared = False
        elif not self.cones.hidden and not self.cones.appeared:
            if not self.cones.hide_seq.isPlaying():
                self.cones.set_target_step()
                self.cones.hidden = True
                self.cones.appeared = False

        result = self.world.contactTest(self.scene.floor.node())
        for con in result.getContacts():
            if (name := con.getNode0().getName()) != 'snowman':
                print(name)
                np = self.holder.pop(int(name))
                self.world.remove(np.node())
                np.removeNode()


        result = self.world.contactTest(self.character.node())
        for con in result.getContacts():
            if not (name := con.getNode1().getName()).startswith('stairs'):
                mp = con.getManifoldPoint()
                # print(name)
                # print('B', mp.getPositionWorldOnB())

      

        self.character.calc_climbed_steps()
        # print(self.character.node().isOnGround())
        # print(self.character.climbed_steps)

        self.world.doPhysics(dt)
        return task.cont

    def move_camera(self, direction, move):
        if direction == 'z':
            z = self.camera.getZ()
            if move == 'up':
                self.camera.setZ(z + 1)
            elif move == 'down':
                self.camera.setZ(z - 1)
        elif direction == 'x':
            x = self.camera.getX()
            if move == 'up':
                self.camera.setX(x + 1)
            elif move == 'down':
                self.camera.setX(x - 1)
        elif direction == 'y':
            y = self.camera.getY()
            if move == 'up':
                self.camera.setY(y + 1)
            elif move == 'down':
                self.camera.setY(y - 1)
        elif direction == 'h':
            if move == 'up':
                self.look_x += 1
            elif move == 'down':
                self.look_x -= 1
            self.camera.lookAt(self.look_x, self.look_y, self.look_z)
        elif direction == 'p':
            if move == 'up':
                self.look_y += 1
            elif move == 'down':
                self.look_y -= 1
            self.camera.lookAt(self.look_x, self.look_y, self.look_z)
        elif direction == 'r':
            if move == 'up':
                self.look_z += 1
            elif move == 'down':
                self.look_z -= 1
            self.camera.lookAt(self.look_x, self.look_y, self.look_z)

        # elif direction == 'h':
        #     h = self.camera.getH()
        #     if move == 'up':
        #         self.camera.setH(h + 1)
        #     elif move == 'down':
        #         self.camera.setH(h - 1)
        # elif direction == 'p':
        #     p = self.camera.getP()
        #     if move == 'up':
        #         self.camera.setP(p + 1)
        #     elif move == 'down':
        #         self.camera.setP(p - 1)
        # elif direction == 'r':
        #     r = self.camera.getR()
        #     if move == 'up':
        #         self.camera.setR(r + 1)
        #     elif move == 'down':
        #         self.camera.setR(r - 1)

if __name__ == '__main__':
    game = ClimbStairs()
    game.run()
