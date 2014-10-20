import pygame, time, boat, gameobj, component, util, config, pingfield

# TODO:
# * make ping_field again (old code: ping_field = PingField("ping", S_CENTER, dial_radius))
# * make GUI overlay for sonar or specialize bounds for ping_field
# * enable firing for boats


def centeredPos(img, pos):
    offset = util.vectorMul(img.get_size(), .5)
    return util.vectorSub(pos, offset)


def render(alpha, model, screen, center):
    bounds = util.vectorMul(SCREEN.get_size(), 1/config.SCALE_FACTOR)
    midpoint = util.vectorMul(screen.get_size(), .5)

    screen.fill((150, 150, 150))

    for item in model:
        renderer = item.componentType(component.Renderable)
        if renderer:
            data_list = renderer.render(bounds, alpha)
            for data in data_list:
                # Reorient view to center around given center point
                data = (data[0], util.vectorSub(data[1], center))

                # Transform from model to screen space
                data = (data[0], util.vectorMul(data[1], config.SCALE_FACTOR))

                # Center blit around coordinate
                data = (data[0], centeredPos(*data))

                # Reorient (0, 0) to lie in the middle of the screen
                data = (data[0], util.vectorAdd(midpoint, data[1]))

                screen.blit(*data)
    pygame.display.flip()


if __name__ == "__main__":
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    player_boat = boat.newBoat("player")
    sonar_dial = gameobj.GameObj("sonar", player_boat.pos())
    component.Renderable(sonar_dial, "sonar_base")
    component.FollowScript(sonar_dial, player_boat)
    model = [sonar_dial,
             player_boat,
             boat.newBoat("opponent", AI=True),
             pingfield.newPingField()]

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

        render(alpha, model, SCREEN, player_boat.pos())
