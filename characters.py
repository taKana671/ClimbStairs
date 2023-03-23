from panda3d.bullet import BulletCapsuleShape, ZUp
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.core import Vec3, Point3, BitMask32
from panda3d.core import NodePath, TransformState


SNOWMAN_PATH = 'models/snowman/snowman'


class Characters(NodePath):

    def __init__(self, stairs, world):
        height, radius = 7.0, 1.5
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)
        super().__init__(BulletCharacterControllerNode(shape, 0.4, 'snowman'))
        self.world = world
        self.stairs = stairs

        model = base.loader.loadModel(SNOWMAN_PATH)
        model.setTransform(TransformState.makePos(Vec3(0, 0, -3)))
        model.reparentTo(self)
        self.set_pos(Point3(-1.0, 0.0, 0.0))
        self.set_scale(0.3)
        self.set_h(90)
        self.set_collide_mask(BitMask32.allOn())
        self.world.attachCharacter(self.node())

        self.climbing = True
        self.current_stair = 0
        self.back_to = None

    def detect_collision(self):
        go_back = 0
        result = self.world.contact_test(self.node())

        for con in result.get_contacts():
            nd_name = con.get_node1().get_name()
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
                self.back_to = self.current_stair - 1 - go_back
                if self.back_to < -1:
                    self.back_to = -1
                self.climbing = False
                break

    def calc_climbed_steps(self):
        """Get the height of the stair on which the character is.
           For example, the character is on the floor if the current_stair is 0,
           the character is on the 1st step (np: render/scene/stairs/stairs_0),
           if the current_stair is 1.
        """
        from_pos = self.get_pos()
        to_pos = Point3(from_pos.x, from_pos.y, -1)
        result = self.world.ray_test_closest(from_pos, to_pos, BitMask32.bit(4))

        if result.hasHit():
            self.current_stair = int(result.getHitPos().z)

    def is_jump(self, stair):
        """Return True if the character is jumping onto the next stair.
           Args:
                stair: index of the stair.
        """
        if stair == self.current_stair and \
                not self.node().is_on_ground():
            return True

    def fall(self, dt):
        distance = dt * 10
        if (x := self.get_x() - distance) >= self.back_to:
            self.set_x(x)
        else:
            self.set_x(self.back_to)
            if self.current_stair == self.back_to + 1:
                self.climbing = True

    def do_jump(self):
        self.node().set_max_jump_height(2.0)  # 5.0
        self.node().set_jump_speed(5.0)       # 8.0
        self.node().do_jump()

    def update(self, dt, speed):
        self.calc_climbed_steps()

        if self.climbing:
            if speed.y < 0:  # go forward
                stair_np = self.stairs.get_child(self.current_stair)
                result = self.world.contact_test_pair(self.node(), stair_np.node())
                if result.getNumContacts() > 0:
                    self.do_jump()
                    speed.y = 0

            self.node().set_linear_movement(speed, True)
            self.detect_collision()
        else:
            self.fall(dt)