from gameobj import *
from component import *
from config import *
from thinkbayes2 import Suite, EvalNormalPdf
import pygame, util


def newPingField(sonar_img_path):
    r = min(pygame.image.load(sonar_img_path + ".png").get_size())
    sonar_radius = r/(SCALE_FACTOR*2) - 1
    ping_field = GameObj("ping_field")
    PingFieldScript(ping_field, "ping", OCEAN_SIZE, sonar_radius)
    return ping_field


class PingFieldScript(Renderable):

    def __init__(self, parent, image_path, grid_size, rad):
        super(PingFieldScript, self).__init__(parent, image_path)
        self._bayesian = Predictions(grid_size)
        self._render_radius = rad

    # def updateModel(self, data):
    #     self._bayesian.Update(data)

    def render(self, bounds, dt):
        if self._bayesian.changed():
            self._render_list = []
            max_prob, items = self._bayesian.getProbData()
            scaling = SCALE_FACTOR/(2*max_prob)

            for loc, prob in items:
                if int(prob*scaling) > 1:
                    size = (int(prob*scaling), int(prob*scaling))
                else:
                    size = (2, 2)
                img = pygame.transform.smoothscale(self._image, size)
                self._render_list.append((img, loc))

        return_list = []
        for item in self._render_list:
            if util.distance(item[1], bounds) < self._render_radius:
                return_list.append(item)

        return return_list


class Predictions(Suite):

    def __init__(self, size):
        hypos = [(x, y) for x in range(size[0]) for y in range(size[1])]
        super(Predictions, self).__init__(hypos)
        self._changed = True

    def Update(self, data):
        self._changed = True
        super(Predictions, self).Update(data)

    def Likelihood(self, data, hypo):
        # Unpack Variables
        ship_location = hypo
        shot_location, mean_distance, error = data

        # Calculate Distance from Hypo Point
        d = util.distance(shot_location, ship_location)

        # Evaluate Normal Distribution near Ship
        return EvalNormalPdf(d, mean_distance, error) + 0.05

    def getProbData(self):
        self._changed = False
        max_prob = self.Prob(self.MaximumLikelihood())
        return max_prob, self.Items()

    def changed(self):
        return self._changed

    def __str__(self):
        return str(self.getProbData())


if __name__ == "__main__":
    pf = newPingField("sonar_base")
    print(pf.component("PingFieldScript")._bayesian.MaximumLikelihood())
    data1 = ((10, 10), 5, 1)
    #pf.component("PingFieldScript").updateModel(data1)

    #print(pf.component("PingFieldScript")._bayesian)
    print(pf.component("PingFieldScript")._bayesian.MaximumLikelihood())