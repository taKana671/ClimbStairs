import sys

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletRigidBodyNode, BulletCharacterControllerNode, BulletDebugNode
from panda3d.core import Vec2, Vec3, LColor, BitMask32
from panda3d.core import NodePath, PandaNode
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.showbase.ShowBaseGlobal import globalClock
from direct.showbase.InputStateGlobal import inputState

from scene import Scene
from falling_objects import Sphere, CarNsx


class SnowMan(NodePath):

    def __init__(self, world):
        model = base.loader.loadModel('models/snowman/snowman')
        model.setScale(0.3)
        end, tip = model.getTightBounds()
        size = tip - end
        height = size.z / 2
        radius = size.x / 2
        shape = BulletCapsuleShape(radius, height, ZUp)
        super().__init__(BulletCharacterControllerNode(shape, 0.4, 'snowman'))
        self.reparentTo(base.render)
        self.setCollideMask(BitMask32.bit(1))
        self.setPos(-1, 2, 0)
        self.setH(90)

        model.reparentTo(self)
        model.setPos(0, 0, -1)

        world.attachCharacter(self.node())


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

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.scene = Scene(self.world)

        self.character = SnowMan(self.world)

        self.ball = Sphere(self.scene.stairs.top_pos)
        self.world.attachRigidBody(self.ball.node())
        self.ball.node().setMass(0)

        
        # now_pos = ball.getPos()
        # vec = Vec3(now_pos.x - 2, -6, now_pos.z)
        # ball.node().setActive(True)
        # ball.node().applyImpulse(ball.getPos(), vec)
        # ball.node().applyForce(ball.getPos(), Vec3.right() * 20)

        # car = CarNsx(self.scene.stairs.top_pos)
        # self.world.attachRigidBody(car.node())

        # car.node().setActive(True)
        # car.node().applyForce(car.getPos(), Vec3.right() * 20)

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

    def control_character(self, dt):
        speed = Vec3(0, 0, 0)
        omega = 0.0

        if inputState.isSet('jump'):
            self.character.node().setMaxJumpHeight(5.0)
            self.character.node().setJumpSpeed(8.0)
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
        # print('camera_pos', self.camera.getPos())
        # print('camera_lookat', self.look_x, self.look_y, self.look_z)
        # # print('camera_hpr', self.camera.getHpr())
        # print('----------------------')

        self.world.doPhysics(dt)
        return task.cont

    def move_camera(self, direction, move):
        if direction == 'z':
            vec = Vec3(-1, 3, -2)
            self.ball.node().setMass(1)
            self.ball.node().setActive(True)
            self.ball.node().applyImpulse(vec.normalized() * 20, self.ball.getPos())
            # z = self.camera.getZ()
            # if move == 'up':
            #     self.camera.setZ(z + 1)
            # elif move == 'down':
            #     self.camera.setZ(z - 1)
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
