"""
component.py
----------
The core component set for adding functionality to GameObjs.

"""

from util import *
import pygame


class Component:

    def __init__(self, parent):
        self._parent = parent
        parent.addComponent(self)

    def awake(self):
        pass

    def getDependencies(self):
        return []

    def update(self, dt):
        pass

    def lateUpdate(self, dt):
        pass

    def __str__(self):
        return str(type(self).__name__)


class Renderable(Component):

    def __init__(self, parent, image_path, depth=0):
        super(Renderable, self).__init__(parent)
        self.image = pygame.image.load("{}.png".format(image_path))

    def rotatedImage(self):
        angle = self._parent.rotation()
        return pygame.transform.rotate(self.image, angle)

    def curPos(self, dt):
        return self._parent.pos()

    def centeredPos(self, dt):
        offset = vectorMul(self.image.get_size(), .5)
        return vectorSub(self.curPos(dt), offset)

    def render(self, bounds, dt):
        pos = self.curPos(dt)
        if inBounds(pos, bounds):
            return (self.rotatedImage(), pos)


class Physics(Component):

    def __init__(self, parent, speed, bounds):
        super(Physics, self).__init__(parent)
        self._speed = speed
        self._bounds = bounds

    def speed(self, new_value=None):
        if new_value is None:
            return self._speed
        else:
            self._speed = new_value

    def calcVel(self):
        direction = math.radians(self._parent.rotation() + 90)
        return self._speed * math.cos(direction), self._speed * math.sin(direction)

    def lateUpdate(self, dt):
        new_pos = vectorAdd(self._parent.pos(), self.calcVel())
        if inBounds(new_pos, self._bounds):
            self._parent.pos(new_pos)


class PhysicsRenderable(Renderable):

    def getDependencies(self):
        return [Physics]

    def awake(self):
        self._phys = self._parent.component("Physics")

    def curPos(self, dt):
        return vectorAdd(self._parent.pos(), vectorMul(self._phys.calcVel(), dt))


class FollowScript(Component):

    def __init__(self, parent, target):
        super(FollowScript, self).__init__(parent)
        self._target = target

    def update(self, dt):
        self._parent.pos(self._target.pos())
