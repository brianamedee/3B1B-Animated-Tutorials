from manim import *

HOME = "C:\manim\Manim_7_July\Projects\\assets\Images"
HOME2 = "C:\manim\Manim_7_July\Projects\\assets\SVG_Images"
HOME3 = "C:\manim\Manim_7_July\Projects\\assets\Jay_SVG"


class StartingStuff(Scene):
    def construct(self):

        play_icon1 = VGroup(SVGMobject(f"{HOME2}\\youtube_icon.svg")).set_height(0.75)

        self.play(DrawBorderThenFill(play_icon1), run_time=2)
        self.play(play_icon1.animate.to_edge(UL))
        play_icons = (
            VGroup(*[SVGMobject(f"{HOME2}\\youtube_icon.svg") for k in range(10)])
            .set_height(0.75)
            .arrange(RIGHT, buff=0.2)
            .next_to(play_icon1, RIGHT, buff=0.2)
        )

        text = Tex("Vector Span")
        questions = VGroup()
        for i in range(10):
            question = Tex("???").next_to(play_icons[i], DOWN, buff=0.2)
            questions.add(question)

        self.play(Write(text))
        self.wait()
        self.play(
            text.animate.match_width(play_icon1).next_to(play_icon1, DOWN), run_time=2
        )
        self.wait(3)
        self.play(DrawBorderThenFill(play_icons), run_time=5)
        self.wait(2)
        self.play(Write(questions), run_time=3)
        self.wait(2)


def GetSpanningVectors(plane, x=-7, y=-4):
    result = VGroup()
    x = -7
    y = -4
    while x <= 7:
        for y in np.arange(-4, 5):
            if x <= 0:
                point = (
                    Dot(fill_color=[ORANGE, YELLOW], fill_opacity=0.75)
                    .scale(0.5)
                    .move_to(plane.c2p(x, y))
                )
                vec = (
                    Line(
                        start=ORIGIN,
                        end=point.get_center(),
                        tip_length=0.2,
                        stroke_color=[BLUE, PINK],
                    )
                    .add_tip()
                    .set_opacity(0.8)
                )
            else:
                point = (
                    Dot(fill_color=[YELLOW, ORANGE], fill_opacity=0.75)
                    .scale(0.5)
                    .move_to(plane.c2p(x, y))
                )
                vec = (
                    Line(
                        start=ORIGIN,
                        end=point.get_center(),
                        tip_length=0.2,
                        stroke_color=[PINK, BLUE],
                    )
                    .add_tip()
                    .set_opacity(0.8)
                )
            result.add(point, vec)
        x += 1
    return result


class VectorSpan(Scene):
    def construct(self):
        plane1 = NumberPlane()
        self.add(plane1)

        span1 = GetSpanningVectors(plane=plane1, x=-7, y=-4)

        self.play(Create(span1), run_time=2)
        self.wait()


class Thumbnail(Scene):
    def construct(self):

        plane1 = NumberPlane()
        span1 = GetSpanningVectors(plane=plane1, x=-7, y=-4)
        text1 = (
            Tex("3B1B Span Animation Tutorial")
            .scale(2)
            .add_background_rectangle()
            .to_edge(UP)
        )
        self.add(plane1, span1, text1)
        self.wait()
