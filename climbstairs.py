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

    READY = auto()
    APPEARING = auto()
    APPEAR = auto()
    DISAPPEARING = auto()
    DISAPPEAR = auto()
    MOVING = auto()



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
        self.stair = 0
        self.stair_before = 0
        world.attachCharacter(self.node())

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

        self.character = SnowMan(self.world)

        self.holder = ObstaclesHolder(100)
        self.polhs = Polyhedrons(self.scene.stairs, self.world)
        self.spheres = Spheres(self.scene.stairs, self.world)
        self.drop_timer = 0
        self.drop_polh = True

        self.cones = Cones(self.scene.stairs, self.world)
        self.cones.state = Status.DISAPPEAR
        self.cones_timer = 0

        self.saws = CircularSaws(self.scene.stairs, self.world)
        self.saws.state = Status.DISAPPEAR

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

        self.accept('z', self.test_move_camera, ['z', 'up'])
        self.accept('shift-z', self.test_move_camera, ['z', 'down'])
        self.accept('x', self.test_move_camera, ['x', 'up'])
        self.accept('shiht-x', self.test_move_camera, ['x', 'down'])
        self.accept('y', self.test_move_camera, ['y', 'up'])
        self.accept('shift-y', self.test_move_camera, ['y', 'down'])

        self.accept('a', self.test_move_camera, ['h', 'up'])
        self.accept('shift-a', self.test_move_camera, ['h', 'down'])
        self.accept('s', self.test_move_camera, ['p', 'up'])
        self.accept('shift-s', self.test_move_camera, ['p', 'down'])
        self.accept('d', self.test_move_camera, ['r', 'up'])
        self.accept('shift-d', self.test_move_camera, ['r', 'down'])

        self.accept('f', self.test_move_camera, ['f', 'print'])

        self.taskMgr.add(self.update, 'update')

    def do_jump(self):
        self.character.node().setMaxJumpHeight(2.0)  # 5.0
        self.character.node().setJumpSpeed(5.0)      # 8.0
        self.character.node().doJump()

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

        self.character.node().setAngularMovement(omega)
        self.character.node().setLinearMovement(speed, True)

    def decide_stair(self, *gimmicks):
        """Decide a stair in which to make a gimmick. The stair is between
           a step where snowman is and the 10th from the step.
           If snowman goes down, reset the stair.
        """
        start = self.character.stair
        end = start + 10

        for gimmick in gimmicks:
            if gimmick.state == Status.DISAPPEAR or \
                    (gimmick.state == Status.READY and gimmick.stair > end):
                stairs = [g.stair for g in gimmicks if g != gimmick]
                gimmick.stair = random.choice([n for n in range(start, end) if n not in stairs])
                gimmick.state = Status.READY
                print('cones', self.cones.stair, 'saws', self.saws.stair)

    def control_saws(self, dt):
        if self.saws.state == Status.READY:
            if self.character.is_jump(self.saws.stair):
                self.saws.setup(self.character.getPos())
                self.saws.state = Status.APPEARING
        elif self.saws.state == Status.APPEARING:
            if self.saws.appear(dt):
                self.saws.state = Status.MOVING
        elif self.saws.state == Status.MOVING:
            if self.saws.move(dt):
                self.saws.state = Status.DISAPPEARING
        elif self.saws.state == Status.DISAPPEARING:
            if self.saws.disappear(dt):
                self.saws.state = Status.DISAPPEAR

    def control_cones(self, dt):
        if self.cones.state == Status.READY:
            if self.character.is_jump(self.cones.stair):
                self.cones.setup()
                self.cones.state = Status.APPEARING
        elif self.cones.state == Status.APPEARING:
            if self.cones.appear(dt):
                self.cones_timer = globalClock.getFrameCount() + 20
                self.cones.state = Status.APPEAR
        elif self.cones.state == Status.APPEAR:
            if globalClock.getFrameCount() > self.cones_timer:
                self.cones_timer = 0
                self.cones.state = Status.DISAPPEARING
        elif self.cones.state == Status.DISAPPEARING:
            if self.cones.disappear(dt):
                self.cones.state = Status.DISAPPEAR

    def drop_gimmicks(self, drop_polh):
        """Drop polyhedron and sphere alternately.
        """
        if (idx := self.holder.empty_idx()) is not None:
            pos = self.character.getPos()
            drop_stair = self.character.stair + 11

            if drop_polh:
                obj = self.polhs.drop(idx, pos, drop_stair)
            else:
                obj = self.spheres.drop(idx, pos, drop_stair)

            self.holder[idx] = obj

            return True

    def move_camera(self):
        """Change camera x and z with the movement of snowman.
           The width and height of stairs increase by one like below.
            idx      pos
             0   LPoint3f(0, 0, 1)
             1   LPoint3f(1, 0, 2)
             2   LPoint3f(2, 0, 3)
             3   LPoint3f(3, 0, 4)
        """
        if (x := self.character.getX()) <= 2:
            self.camera_before_x = x
        elif (distance := self.character.getX() - self.camera_before_x) != 0:
            self.camera_before_x = self.character.getX()
            pos = self.camera.getPos()
            self.camera.setPos(pos.x + distance, pos.y, pos.z + distance)

    def update(self, task):
        dt = globalClock.getDt()
        self.control_character()
        self.character.calc_climbed_steps()
        # print('now', self.character.stair, 'before', self.character.stair_before)

        # increase stair
        if self.scene.stairs.top_stair - self.character.stair < 14:
            self.scene.stairs.increase()

        # move camera with the game character.
        self.move_camera()

        # drop gimmicks
        if task.time > self.drop_timer:
            if self.drop_gimmicks(self.drop_polh):
                self.drop_polh = not self.drop_polh
            self.drop_timer += 3

        # Decide a stair in which to make cones and saws, and control them.
        self.decide_stair(self.cones, self.saws)
        self.control_cones(dt)
        self.control_saws(dt)

        result = self.world.contactTest(self.scene.floor.node())
        for con in result.getContacts():
            name = con.getNode0().getName()
            if name.startswith('spheres') or name.startswith('polhs'):
            # if (name := con.getNode0().getName()) != 'snowman': # and not name.startswith('saw'):
                # print([cone.getPos() for cone in self.cones.cones])
                # print(name)
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

    def test_move_camera(self, direction, move):
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
