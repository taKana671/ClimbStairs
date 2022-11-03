import random
import sys
from enum import Enum, auto

from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletRigidBodyNode, BulletCharacterControllerNode, BulletDebugNode
from panda3d.bullet import BulletHelper
from panda3d.core import Vec2, Vec3, LColor, BitMask32, Point3
from panda3d.core import NodePath, PandaNode, TransformState
from panda3d.core import AmbientLight, DirectionalLight
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.showbase.ShowBaseGlobal import globalClock
from direct.showbase.InputStateGlobal import inputState

from scene import Scene
from gimmicks import Polyhedrons, Cones, CircularSaws, Spheres


class Status(Enum):

    # for gimmicks
    READY = auto()
    APPEARING = auto()
    APPEAR = auto()
    DISAPPEARING = auto()
    DISAPPEAR = auto()
    MOVING = auto()
    # for camera
    STAY = auto()
    GO_UP = auto()
    GO_DOWN = auto()


class ObstaclesHolder:

    def __init__(self, length):
        self.data = [None for _ in range(length)]

    def __len__(self):
        return sum(1 for item in self.data if item is not None)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def empty_idx(self):
        for i, item in enumerate(self.data):
            if not item:
                return i
        return None

    def pop(self, key):
        item = self.data[key]
        self.data[key] = None
        return item


class SnowMan(NodePath):

    def __init__(self, world):
        model = base.loader.loadModel('models/snowman/snowman')
        model.setScale(0.3)
        height, radius = 2.0, 0.5
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)
        super().__init__(BulletCharacterControllerNode(shape, 0.4, 'snowman'))
        self.reparentTo(base.render)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2))
        # self.setCollideMask(BitMask32.allOn())
        self.setPos(-1, 2, 0)
        self.setH(90)
        model.reparentTo(self)
        model.setPos(0, 0, -1)
        self.stair = -1

        world.attachCharacter(self.node())

    def calc_climbed_steps(self):
        """Because the center z of snowman is about 0.95,
           int(z) - 1 means index of the stair on which snowman is.
        """
        if self.node().isOnGround():
            self.stair = int(self.getPos().z) - 1

    def is_jump(self, stair):
        if stair == self.stair and \
                not self.node().isOnGround():
            return True

    def not_jump(self, stair):
        if stair == self.stair and \
                self.node().isOnGround():
            return True


class ClimbStairs(ShowBase):

    def __init__(self):
        super().__init__()
        self.disableMouse()

        self.camera.setPos(-11, -16, 13)
        # self.camera.setPos(-11, -16, 20)
        # self.camera.lookAt(5, 7, 10)

        # self.camera.lookAt(5, 7, 4)
        self.camera.setHpr(-35, -18, 0)
        self.camera_stair = 0
        self.camera_abs_distance = 0
        self.camera_state = Status.STAY

        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.scene = Scene(self.world)

        self.character = SnowMan(self.world)

        self.holder = ObstaclesHolder(100)
        self.polhs = Polyhedrons(self.scene.stairs, self.world)
        self.spheres = Spheres(self.scene.stairs, self.world)
        self.drop_timer = 0
        self.drop_polh = True

        self.cones = Cones(self.scene.stairs, self.world)
        self.cones_state = Status.DISAPPEAR
        self.cones_timer = 0

        self.saws = CircularSaws(self.scene.stairs, self.world)
        self.saws_state = Status.DISAPPEAR


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

        self.accept('f', self.move_camera, ['f', 'print'])

        self.accept('escape', sys.exit)
        self.taskMgr.add(self.update, 'update')

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

    def select_gimmick_stair(self, exp=None):
        start = self.character.stair + 1
        end = self.scene.stairs.top_stair
        return random.choice([n for n in range(start, end) if n != exp])

    def control_camera(self, dt):
        distance = dt * 5

        if self.camera_state == Status.GO_UP:
            move = Vec3(distance, 0, distance)
        else:
            move = Vec3(-distance, 0, -distance)

        pos = self.camera.getPos() + move
        self.camera.setPos(pos)
        self.camera_abs_distance -= distance

        if self.camera_abs_distance < 0:
            self.camera_state = Status.STAY

    def update(self, task):
        dt = globalClock.getDt()
        self.control_character(dt)
        self.character.calc_climbed_steps()

        # When snowman is on floor, self.character.stair is -1.
        if self.camera_state == Status.STAY:
            if (diff := abs(self.character.stair) // 6 - self.camera_stair) != 0:
                if diff > 0:
                    self.camera_state = Status.GO_UP
                else:
                    self.camera_state = Status.GO_DOWN
                # Move camera up and down every 6 stairs.
                self.camera_abs_distance = abs(diff) * 6
                self.camera_stair += diff

        if self.camera_state != Status.STAY:
            self.control_camera(dt)

        if task.time > self.drop_timer:
            if (idx := self.holder.empty_idx()) is not None:
                pos = self.character.getPos()
                if self.drop_polh:
                    obj = self.polhs.drop(idx, pos)
                else:
                    obj = self.spheres.drop(idx, pos)
                self.holder[idx] = obj
                self.drop_polh = not self.drop_polh
            self.drop_timer += 3

        if self.cones_state == Status.READY:
            if self.character.is_jump(self.cones.stair - 1):
                self.cones.setup()
                self.cones_state = Status.APPEARING
        elif self.cones_state == Status.APPEARING:
            if self.cones.appear(dt):
                self.cones_timer = task.time + 1
                self.cones_state = Status.APPEAR
        elif self.cones_state == Status.APPEAR:
            if task.time > self.cones_timer:
                self.cones_timer = 0
                self.cones_state = Status.DISAPPEARING
        elif self.cones_state == Status.DISAPPEARING:
            if self.cones.disappear(dt):
                self.cones_state = Status.DISAPPEAR
        elif self.cones_state == Status.DISAPPEAR:
            self.cones.stair = self.select_gimmick_stair(self.saws.stair)
            self.cones_state = Status.READY
            print('cone_trap', self.cones.stair)

        if self.saws_state == Status.READY:
            if self.character.is_jump(self.saws.stair - 1):
                self.saws.setup(self.character.getPos())
                self.saws_state = Status.APPEARING
        elif self.saws_state == Status.APPEARING:
            if self.saws.appear(dt):
                self.saws_state = Status.MOVING
        elif self.saws_state == Status.MOVING:
            if self.saws.move(dt):
                self.saws_state = Status.DISAPPEARING
        elif self.saws_state == Status.DISAPPEARING:
            if self.saws.disappear(dt):
                self.saws_state = Status.DISAPPEAR
        elif self.saws_state == Status.DISAPPEAR:
            self.saws.stair = self.select_gimmick_stair(self.cones.stair)
            self.saws_state = Status.READY
            print('saw_trap', self.saws.stair)

        result = self.world.contactTest(self.scene.floor.node())
        for con in result.getContacts():
            name = con.getNode0().getName()
            if name.startswith('spheres') or name.startswith('polhs'):
            # if (name := con.getNode0().getName()) != 'snowman': # and not name.startswith('saw'):
                # print([cone.getPos() for cone in self.cones.cones])
                print(name)
                idx = name.split('_')[1]
                np = self.holder.pop(int(idx))
                self.world.remove(np.node())
                np.removeNode()

        result = self.world.contactTest(self.character.node())
        for con in result.getContacts():
            if not (name := con.getNode1().getName()).startswith('stairs'):
                mp = con.getManifoldPoint()
                # print(name)
                # print('B', mp.getPositionWorldOnB())

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
        elif direction == 'f':
            print('pos', self.camera.getPos())
            print('hpr', self.camera.getHpr())

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
