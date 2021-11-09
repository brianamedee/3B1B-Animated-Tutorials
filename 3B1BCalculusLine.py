from manim import *


def dx_circle(x_min=0, x_max=3, dx=0.1):
    circles = VGroup()
    for x in np.arange(x_min, x_max, dx):
        c = Circle(radius=x, stroke_width=4, stroke_color=[BLUE, GREEN])
        circles.add(c)
    return circles


def dx_circumferences(x_min=0, x_max=3, dx=0.1):
    circumferences = VGroup()
    for x in np.arange(x_min, x_max, dx):
        circumf = Rectangle(
            width=2 * x * PI,
            height=dx,
            stroke_color=[BLUE, GREEN],
            fill_color=[BLUE, GREEN],
            fill_opacity=0.75,
        )
        circumferences.add(circumf)
    circumferences.arrange(DOWN, buff=0.1).to_edge(DL)
    return circumferences


class CircleCalculus(Scene):
    def construct(self):

        axes = Axes(
            x_range=[0, 1.01],
            x_length=1,
            y_range=[0, 7],
            y_length=7,
            axis_config={"include_numbers": True, "include_tip": False},
        ).to_edge(RIGHT, buff=2)

        k = ValueTracker(0.2)

        circles = always_redraw(lambda: dx_circle(x_min=0, x_max=1, dx=k.get_value()))
        circumferences = always_redraw(
            lambda: dx_circumferences(x_min=0, x_max=1, dx=k.get_value())
        )

        self.add(circles, circumferences)
        self.wait()
        self.play(DrawBorderThenFill(axes))
        self.play(k.animate.set_value(0.05), run_time=5)

        self.play(
            Wiggle(
                VGroup(circles[6], circles[14], circumferences[6], circumferences[14])
            )
        )
        self.play(
            circumferences[6]
            .copy()
            .animate.rotate(PI / 2)
            .move_to(axes.c2p(6 / 20, 0))
            .shift(UP * (circumferences[6].get_width()) / 2),
            circumferences[14]
            .copy()
            .animate.rotate(PI / 2)
            .move_to(axes.c2p(14 / 20, 0))
            .shift(UP * (circumferences[14].get_width()) / 2),
            run_time=2,
        )

        area_under_curve = VGroup()
        for p in range(20):
            rect = (
                circumferences[p]
                .copy()
                .rotate(PI / 2)
                .move_to(axes.c2p(p / 20, 0))
                .shift(UP * (circumferences[p].get_width()) / 2)
            )
            area_under_curve.add(rect)

        self.play(Transform(circumferences.copy(), area_under_curve), run_time=2)

        self.wait()


class Thumbnail(Scene):
    def construct(self):

        text = (
            Tex("3B1B Circle Calculus Tutorial")
            .scale(2)
            .add_background_rectangle()
            .to_edge(UP)
        )

        axes = Axes(
            x_range=[0, 1.01],
            x_length=1,
            y_range=[0, 7],
            y_length=7,
            axis_config={"include_numbers": True, "include_tip": False},
        ).to_edge(RIGHT, buff=2)

        k = ValueTracker(0.05)

        circles = always_redraw(lambda: dx_circle(x_min=0, x_max=2, dx=k.get_value()))
        circumferences = always_redraw(
            lambda: dx_circumferences(x_min=0, x_max=1, dx=k.get_value())
        )

        self.add(circles, circumferences, axes)
        area_under_curve = VGroup()
        for p in range(20):
            rect = (
                circumferences[p]
                .copy()
                .rotate(PI / 2)
                .move_to(axes.c2p(p / 20, 0))
                .shift(UP * (circumferences[p].get_width()) / 2)
            )
            area_under_curve.add(rect)

        self.add(area_under_curve, text)

        self.wait()
