from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import Vec3, Point3, BitMask32
from panda3d.core import NodePath, TransformState


SNOWMAN_PATH = 'models/snowman/snowman'


class Characters(NodePath):

    def __init__(self, world, shape, name):
        super().__init__(BulletCharacterControllerNode(shape, 0.4, name))
        self.world = world
        self.setCollideMask(BitMask32.allOn())
        # self.reparentTo(base.render)
        self.world.attachCharacter(self.node())

        self.climbing = True
        self.stair = 0
        self.back_to = None

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
        """Get the height of the stair on which the character is.
        """
        from_pos = self.getPos()
        to_pos = Point3(from_pos.x, from_pos.y, -1)
        result = self.world.rayTestClosest(from_pos, to_pos, BitMask32.bit(4))

        if result.hasHit():
            self.stair = int(result.getHitPos().z)

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

    def do_jump(self):
        self.node().setMaxJumpHeight(2.0)  # 5.0
        self.node().setJumpSpeed(5.0)      # 8.0
        self.node().doJump()

    def update(self, dt, speed):
        self.calc_climbed_steps()

        if self.climbing:
            self.node().setLinearMovement(speed, True)
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