#from thinkbayes2 import Suite, EvalNormalPdf
import pygame, time, boat, controller, gameobj, component

SCALE_FACTOR = 30


if __name__ == "__main__":
    cont = controller.Input()
    player_boat = boat.newBoat("player")
    sonar_dial = gameobj.GameObj("Sonar", player_boat.pos())
    component.Renderable(sonar_dial, "sonar_base")
    component.FollowScript(sonar_dial, player_boat)
    model = [sonar_dial, player_boat, boat.newBoat("opponent", AI=True)]


    #TODO
    #sonar_dial = Sonar("sonar_base", S_CENTER)
    #dial_radius = sonar_dial.getRadius()
    #ping_field = PingField("ping", S_CENTER, dial_radius)

    # Generic Gameloop
    t = 0.0
    dt = 0.01

    current_time = time.clock()
    accumulator = 0.0

    while True:
        SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        S_WIDTH, S_HEIGHT = SCREEN.get_size()
        S_CENTER = (S_WIDTH/2, S_HEIGHT/2)

        # Update clock
        new_time = time.clock()
        frame_time = new_time - current_time

        # Cut losses at 1/4 second
        if frame_time > 0.25:
            frame_time = 0.25
        current_time = new_time
        accumulator += frame_time

        # Handle input
        #cont.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

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
