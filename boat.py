from gameobj import *
from component import *
from util import *
import config, random, pygame, pingfield


class BoatScript(Component):

    def __init__(self, parent, ping_model):
        super(BoatScript, self).__init__(parent)
        self._fire_radius = 15.0    # Nodes
        self._max_speed = 2         # Nodes/sec
        self._max_accel = .5        # Nodes/sec^2
        self._turn_speed = 60.0     # Degrees/sec
        self._ping_model = ping_model
        self._fire_cooldown = 2
        self._cooldown_timer = 0
        self._dir = 1
        self._phys = self._parent.component("Physics")

    def getDependencies(self):
        return [Physics]

    def fire(self, shot_loc, target):
        if self._cooldown_timer <= 0:
            self._cooldown_timer = self._fire_cooldown
            dist_mean = distance(shot_loc, target.pos())
            error = dist_mean/12 + .5
            data = (shot_loc, random.gauss(dist_mean, error), error)
            self._ping_model.Update(data)


class AIBoatScript(BoatScript):
    def __init__(self, parent):
        super(AIBoatScript, self).__init__(parent, pingfield.Predictions(config.OCEAN_SIZE))

    def update(self, dt):
        # Update Physics based on random quantities
        self._phys.speed(self._phys.speed() + self._dir * self._max_accel * dt)
        self._parent.rotation(self._parent.rotation() + (random.random() - .5) * 2 * self._turn_speed * dt)


class PlayerBoatScript(BoatScript):
    def __init__(self, parent, ping_model):
        super(PlayerBoatScript, self).__init__(parent, ping_model)

    def update(self, dt):
        if self._cooldown_timer > 0:
            self._cooldown_timer -= dt

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


def newBoat(name, ping_model=None):
    if not ping_model:
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
    if not ping_model:
        AIBoatScript(boat)
    else:
        PhysicsRenderable(boat, "boat_icon")
        PlayerBoatScript(boat, ping_model)

    return boat

if __name__ == "__main__":
    player_boat = newBoat("Player", False)
    opp_boat = newBoat("Opponent", True)

    print(player_boat)
    print(opp_boat)
