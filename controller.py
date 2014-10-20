import pygame


class Input:

    _instance = None
    _KEYMAP = {pygame.K_ESCAPE: exit}
    _AXES_MAP = {"v+": [pygame.K_w, pygame.K_UP],
                 "v-": [pygame.K_s, pygame.K_DOWN],
                 "h+": [pygame.K_d, pygame.K_RIGHT],
                 "h-": [pygame.K_a, pygame.K_LEFT]}

    def __new__(self):
        if not Input._instance:
            Input._instance = self
        else:
            return Input._instance

    def update(self):
        self._clicks = []

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in Input._KEYMAP:
                    Input._KEYMAP[event.key]()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._clicks.append(event.pos)

    @staticmethod
    def getClicks(self):
        return Input._instance._clicks

    @staticmethod
    def getAxes(self):
        pressed = pygame.key.get_pressed()
        axes = [0, 0]

        for item in Input._AXES_MAP["h+"]:
            if item in pressed:
                axes[0] += 1
                break

        for item in Input._AXES_MAP["h-"]:
            if item in pressed:
                axes[0] -= 1
                break

        for item in Input._AXES_MAP["v+"]:
            if item in pressed:
                axes[1] += 1
                break

        for item in Input._AXES_MAP["v-"]:
            if item in pressed:
                axes[1] -= 1
                break

        return self._axes
