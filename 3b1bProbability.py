from manim import *
import scipy.stats as scipy_stats
import random

HOME = "C:\manim\Manim_7_July\Projects\\assets\Images"
HOME2 = "C:\manim\Manim_7_July\Projects\\assets\SVG_Images"


def randomize_number(number):
    value = random.uniform(0, 1)
    number.set_value(value)
    if value < 0.5:
        number.set_color(GREEN)
    else:
        number.set_color(RED)


class test(Scene):
    def construct(self):

        num = DecimalNumber()

        self.add(num)
        self.play(UpdateFromFunc(num, randomize_number))
        self.wait()
