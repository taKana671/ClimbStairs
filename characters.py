from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import Vec3, Point3, BitMask32
from panda3d.core import NodePath, TransformState
from direct.showbase.InputStateGlobal import inputState

SNOWMAN_PATH = 'models/snowman/snowman'


class Characters(NodePath):

    def __init__(self, world, shape, name):
        super().__init__(BulletCharacterControllerNode(shape, 0.4, name))
        self.world = world
        self.reparentTo(base.render)
        self.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.node())

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
        speed = Vec3(0, 0, 0)
        omega = 0.0

        if inputState.isSet('jump'):
            self.node().setMaxJumpHeight(2.0)  # 5.0
            self.node().setJumpSpeed(5.0)      # 8.0
            self.node().doJump()
        if inputState.isSet('left'):
            speed.setX(2.0)
        if inputState.isSet('right'):
            speed.setX(-2.0)
        if inputState.isSet('forward'):
            speed.setY(-2.0)
        if inputState.isSet('backward'):
            speed.setY(2.0)
        if inputState.isSet('turn_right'):
            omega += -120
        if inputState.isSet('turn_left'):
            omega += 120

        self.node().setAngularMovement(omega)
        self.node().setLinearMovement(speed, True)

    def detect_collision(self):
        go_back = 0
        result = self.world.contactTest(self.node())

        for con in result.getContacts():
            nd_name = con.getNode1().getName()
            if (prefix := nd_name.split('_')[0]) == 'spheres':
                go_back += 3
            elif prefix == 'cones':
                go_back += 1
            elif prefix == 'saws':
                go_back += 4
            elif prefix == 'polhs':
                go_back += 5
            elif prefix == 'piles':
                go_back += 2

            if go_back > 0:
                self.back_to = self.stair - 1 - go_back
                if self.back_to < -1:
                    self.back_to = -1
                self.climbing = False
                break

    def calc_climbed_steps(self):
        """Calculate the stair on which the character is.
           Because the gap between the steps is 1 and the z of character's center
           is about 0.95, int(z) means the stair on which the character is.
        """
        if self.node().isOnGround():
            if (z := int(self.getPos().z)) != self.stair:
                self.stair_before = self.stair
                self.stair = z

    def is_jump(self, stair):
        """Return True if the character is jumping onto the next stair
           in which gimmicks are embeded.
           Args:
                stair: index of the stair in which gimmicks are embeded. The index of
                scene.stairs starts with 0, but the character's stair starts with 1.
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

    def __init__(self, pos, world):
        height, radius = 7.0, 1.5
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)
        super().__init__(world, shape, 'snowman')
        model = base.loader.loadModel(SNOWMAN_PATH)
        model.setTransform(TransformState.makePos(Vec3(0, 0, -3)))
        model.reparentTo(self)
        self.setPos(pos)
        self.setScale(0.3)
        self.setH(90)