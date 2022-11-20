from enum import Enum, auto

from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import Vec3, Point3, BitMask32
from panda3d.core import NodePath, TransformState
from direct.showbase.InputStateGlobal import inputState


class State(Enum):

    FALLING = auto()
    CLIMBING = auto()
    GRAVITATING = auto()


class Characters(NodePath):

    def __init__(self, stairs, world, shape, name):
        super().__init__(BulletCharacterControllerNode(shape, 0.4, name))
        self.world = world
        self.stairs = stairs
        self.reparentTo(base.render)
        self.setCollideMask(BitMask32.bit(1) | BitMask32.bit(2))
        # self.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.node())

        # self.state = None
        self.climbing = True
        self.stair = 0
        self.stair_before = 0
        self.back_to = None

        inputState.watchWithModifiers('forward', 'arrow_up')
        inputState.watchWithModifiers('backward', 'arrow_down')
        inputState.watchWithModifiers('left', 'arrow_left')
        inputState.watchWithModifiers('right', 'arrow_right')
        inputState.watchWithModifiers('jump', 'enter')
        inputState.watchWithModifiers('turn_right', 'q')
        inputState.watchWithModifiers('turn_left', 'w')

    def control_character(self):
        if inputState.isSet('jump'):
            self.node().setMaxJumpHeight(2.0)  # 5.0
            self.node().setJumpSpeed(5.0)      # 8.0
            self.node().doJump()
        else:
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

            self.node().setAngularMovement(omega)
            self.node().setLinearMovement(speed, True)

    def detect_collision(self):
        go_back = 0
        result = self.world.contactTest(self.node())

        for con in result.getContacts():
            nd_name = con.getNode1().getName()
            if (prefix := nd_name.split('_')[0]) == 'spheres':
                go_back += 2
            elif prefix == 'cones':
                go_back += 4
            elif prefix == 'saws':
                go_back += 5
            elif prefix == 'polhs':
                go_back += 3

            # print('collision', nd_name)
            if go_back > 0:
                self.back_to = self.stair - 1 - go_back
                if self.back_to < -1:
                    self.back_to = -1
                self.climbing = False
                break

    def calc_climbed_steps(self):
        """Calculate the stair on which character is.
           Because the gap between the steps is 1 and the z of character's center
           is about 0.95, int(z) means the stair on which character is.
        """
        if self.node().isOnGround():
            if (z := int(self.getPos().z)) != self.stair:
                self.stair_before = self.stair
                self.stair = z

        # if self.node().isOnGround():
        #     self.stair = int(self.getPos().z)

    def is_jump(self, stair):
        """Return True if character is jumping onto the next stair
           in which gimmicks are embeded.
           Args:
                stair: index of stair in which gimmicks are embeded.
                The index of stairs starts with 0, but character's stair starts with 1.
        """
        if stair == self.stair and \
                not self.node().isOnGround():
            return True

    def fall(self, dt):
        distance = dt * 10
        if (x := self.getX() - distance) >= self.back_to:
            self.setX(x)
        else:
            self.setX(self.back_to)
            if self.stair == self.back_to + 1:
                self.climbing = True

    def update(self, dt):
        self.calc_climbed_steps()

        if self.climbing:
            self.control_character()
            self.detect_collision()
        else:
            self.fall(dt)

class SnowMan(Characters):

    def __init__(self, pos, world, stairs):
        height, radius = 7.0, 1.5
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)
        super().__init__(stairs, world, shape, 'snowman')
        model = base.loader.loadModel('models/snowman/snowman')
        model.setTransform(TransformState.makePos(Vec3(0, 0, -3)))
        model.reparentTo(self)
        self.setPos(pos)
        self.setScale(0.3)
        self.setH(90)