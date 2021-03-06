import gameobj, component, pygame, config


class Camera(gameobj.GameObj):
    _MAIN = None
    _SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    @staticmethod
    def renderScene(self, alpha, bounds):
        Camera._SCREEN.fill((150, 150, 150))
        #TODO
        component.Renderable.renderObjects()


    def __init__(self, name="Camera", pos=(0, 0)):
        if not Camera._MAIN:
            Camera._MAIN = self
            name = "MainCamera"

        super(Camera, self).__init__(name, pos, 0)


def newCamera(followed_obj=None):
    if followed_obj:
        cam = Camera(pos=followed_obj.pos())
        CamScript(cam, followed_obj)
        return cam
    else:
        return Camera
