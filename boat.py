from gameobj import *
from component import *
from util import *
import config, random, pygame


class BoatScript(Component):

    def __init__(self, parent):
        super(BoatScript, self).__init__(parent)
        self._fire_radius = 15.0    # Nodes
        self._max_speed = 3         # Nodes/sec
        self._max_accel = .5        # Nodes/sec^2
        self._turn_speed = 60.0     # Degrees/sec
        self._dir = 1
        self._phys = self._parent.component("Physics")

    def getDependencies(self):
        return [Physics]


class AIBoatScript(BoatScript):

    def update(self, dt):
        # Update Physics based on random quantities
        self._phys.speed(self._phys.speed() + self._dir * self._max_accel * dt)
        self._parent.rotation(self._parent.rotation() + (random.random() - .5) * 2 * self._turn_speed * dt)


class PlayerBoatScript(BoatScript):

    def update(self, dt):
        # Update Physics based on input
        pressed = pygame.key.get_pressed()
        axes = [0, 0]

        if pressed[pygame.K_d]: axes[0] += 1
        if pressed[pygame.K_a]: axes[0] -= 1
        if pressed[pygame.K_w]: axes[1] -= 1
        if pressed[pygame.K_s]: axes[1] += 1

        self._phys.speed(self._phys.speed() + axes[1] * self._max_accel * dt)
        self._parent.rotation(self._parent.rotation() + axes[0] * self._turn_speed * dt)

        if self._phys.speed() > self._max_speed:
            self._phys.speed(self._max_speed)


def newBoat(name, AI=False):
    if AI:
        # Randomize position, heading, and speed
        pos = tuple(random.random() * config.OCEAN_SIZE[i] for i in range(2))
        heading = random.random() * 360.0
        speed = 0.0
    else:
        pos = vectorMul(config.OCEAN_SIZE, .5)
        heading = 0.0
        speed = 0.0

    boat = GameObj(name, pos, heading)
    Physics(boat, speed, bounds=config.OCEAN_SIZE)
    if AI:
        AIBoatScript(boat)
    else:
        PhysicsRenderable(boat, "boat_icon")
        PlayerBoatScript(boat)

    return boat

if __name__ == "__main__":
    player_boat = newBoat("Player", False)
    opp_boat = newBoat("Opponent", True)

    print(player_boat)
    print(opp_boat)
