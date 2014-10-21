import pygame, time, boat, gameobj, component, util, config, pingfield

# TODO:
# * Reenable firing for boats


def centeredPos(img, pos):
    offset = util.vectorMul(img.get_size(), .5)
    return util.vectorSub(pos, offset)


def render(alpha, model, screen, center):
    bounds = center
    midpoint = util.vectorMul(screen.get_size(), .5)

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
    SCREEN.fill((50, 50, 50))

    player_boat = boat.newBoat("player")
    sonar_dial = gameobj.GameObj("sonar", player_boat.pos())
    component.Renderable(sonar_dial, "sonar_base")
    component.FollowScript(sonar_dial, player_boat)
    model = [sonar_dial,
             player_boat,
             boat.newBoat("opponent", AI=True),
             pingfield.newPingField("sonar_base")]

    # Generic Gameloop
    t = 0.0
    dt = 0.01

    accumulated_time = 0
    samples = 0

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
                    print(avg_frame_time)
                    exit()

        # Update Model
        while accumulator >= dt:
            for obj in model:
                obj.update(dt)

            for obj in model:
                obj.lateUpdate(dt)

            t += dt
            accumulator -= dt

        alpha = accumulator / dt
        render(alpha, model, SCREEN, player_boat.pos())

        samples += 1
        accumulated_time += frame_time
        avg_frame_time = accumulated_time/samples
