from thinkbayes2 import Suite, EvalNormalPdf
import pygame, time, boat, controller, camera

SCALE_FACTOR = 30


if __name__ == "__main__":
    cont = controller.Input()
    player_boat = boat.newBoat("player")
    model = [player_boat, boat.newBoat("opponent", AI=True)]
    view = camera.newCamera(player_boat)

    #TODO
    sonar_dial = Sonar("sonar_base", S_CENTER)
    dial_radius = sonar_dial.getRadius()
    ping_field = PingField("ping", S_CENTER, dial_radius)

    # Generic Gameloop
    t = 0.0
    dt = 0.01

    current_time = time.clock()
    accumulator = 0.0

    while True:
        # Update clock
        new_time = time.clock()
        frame_time = new_time - current_time

        # Cut losses at 1/4 second
        if frame_time > 0.25:
            frame_time = 0.25
        current_time = new_time
        accumulator += frame_time

        # Handle input
        controller.update()

        # Update Model
        while accumulator >= dt:
            for gameobj in model:
                gameobj.update(dt)

            for gameobj in model:
                gameobj.lateUpdate(dt)

            t += dt
            accumulator -= dt

        alpha = accumulator / dt

        view.render(alpha)
