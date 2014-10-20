"""
gameobj.py
----------
A super class for all objects that exist in model-space.
Functionality can primarily be added to GameObjs through
the addition of components.

"""

from component import *


class GameObj:

    def __init__(self, name, pos=(0, 0), rotatation=0):
        self._name = name
        self._pos = pos
        self._rotatation = rotatation
        self._components = []

    def addComponent(self, component):
        if isinstance(component, Component) and self.checkDependencies(component):
            self._components.append(component)
            component.awake()

    def checkDependencies(self, cmpt):
        for needed_dependency in cmpt.getDependencies():
            if not self.component(needed_dependency.__name__):
                return False
        return True

    def component(self, type_name):
        str(type_name).lower()
        for cmpt in self._components:
            if str(type_name).lower() == type(cmpt).__name__.lower():
                return cmpt

    def componentType(self, type):
        for cmpt in self._components:
            if isinstance(cmpt, type):
                return cmpt

    def update(self, dt):
        for cmpt in self._components:
            cmpt.update(dt)

    def lateUpdate(self, dt):
        for cmpt in self._components:
            cmpt.lateUpdate(dt)

    def name(self):
        return self._name

    def pos(self, new_value=None):
        if new_value is not None:
            self._pos = new_value
        else:
            return self._pos

    def rotation(self, new_value=None):
        if new_value is not None:
            self._rotatation = new_value
        else:
            return self._rotatation

    def __str__(self):
        data = "{} at pos: {}, rotation: {}".format(self.name(), self.pos(), self.rotation())
        if self._components:
            cmpt_data = ["    Components:"]
            for cmpt in self._components:
                cmpt_data.append("      {}".format(cmpt))
            data = "{}\n{}".format(data, '\n'.join(cmpt_data))

        return data


if __name__ == "__main__":
    g = GameObj("Test1")
    Physics(g)
    PhysicsRenderable(g, "boat_icon")
    print(g)
