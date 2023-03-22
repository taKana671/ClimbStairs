from panda3d.core import NodePath, PandaNode
from panda3d.core import Vec3, Point3
from panda3d.core import AmbientLight, DirectionalLight


class BasicAmbientLight(NodePath):

    def __init__(self):
        super().__init__(AmbientLight('ambient_light'))
        self.node().setColor((0.6, 0.6, 0.6, 1))
        base.render.setLight(self)
        self.reparentTo(base.render)


class BasicDayLight(NodePath):

    def __init__(self, parent):
        super().__init__(DirectionalLight('directional_light'))
        self.node().getLens().setFilmSize(100, 100)
        self.node().getLens().setNearFar(1, 100)
        self.node().setColor((1, 1, 1, 1))
        self.setPosHpr(Point3(0, 0, 30), Vec3(-30, -60, 0))
        self.node().setShadowCaster(True, 8192, 8192)

        state = self.node().getInitialState()
        temp = NodePath(PandaNode('temp_np'))
        temp.setState(state)
        temp.setDepthOffset(-2)
        self.node().setInitialState(temp.getState())

        base.render.setLight(self)
        base.render.setShaderAuto()
        self.reparentTo(parent)