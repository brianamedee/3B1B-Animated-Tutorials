from manim import *


def get_epsilon_lines(x, dx, graph, axes, line_length=20, color=WHITE):
    result = VGroup()
    line1 = (
        DashedLine(start=ORIGIN, end=line_length * RIGHT)
        .move_to(axes.c2p(x + dx, graph.underlying_function(x + dx)))
        .set_color(color)
    )
    dot1 = (
        Circle(radius=0.07)
        .set_color(color)
        .move_to(axes.c2p(x + dx, graph.underlying_function(x + dx)))
    )

    line2 = (
        DashedLine(start=ORIGIN, end=line_length * RIGHT)
        .move_to(axes.c2p(x - dx, graph.underlying_function(x - dx)))
        .set_color(color)
    )
    dot2 = (
        Circle(radius=0.07)
        .set_color(color)
        .move_to(axes.c2p(x - dx, graph.underlying_function(x - dx)))
    )
    result.add(line1, line2, dot1, dot2)
    return result


def get_delta_lines(x, dx, axes, line_length=20, color=WHITE):
    result = VGroup()
    line1 = (
        DashedLine(start=ORIGIN, end=line_length * UP)
        .move_to(axes.c2p(x + dx, 0))
        .set_color(color)
    )
    line2 = (
        DashedLine(start=ORIGIN, end=line_length * UP)
        .move_to(axes.c2p(x - dx, 0))
        .set_color(color)
    )
    result.add(line1, line2)
    return result


def get_faded_undefined_epsilon_delta_lines(
    x, graph, axes, line_length=20, color=WHITE, opacity=0.5
):
    result = VGroup()
    epsilon_line = (
        DashedLine(start=ORIGIN, end=line_length * RIGHT)
        .set_color(color)
        .move_to(
            axes.c2p(x + 0.0000001, graph.underlying_function(x + 0.0000001))
        )  # NEED to add the +0.000001 as undefined point otherwise
        .set_opacity(opacity)
    )
    delta_line = (
        DashedLine(start=ORIGIN, end=line_length * UP)
        .set_color(color)
        .move_to(axes.c2p(x, 0))
        .set_opacity(opacity)
    )
    result.add(epsilon_line, delta_line)
    return result


def get_output_limit_range(x, graph, dx, range, axes):
    result = VGroup()
    dot = (
        Circle(radius=0.07)
        .set_color(YELLOW)
        .move_to(
            axes.c2p(x + 0.000001, graph.underlying_function(x + 0.000001))
        )  # Need to +0.00001 as point is undefined otherwise
    )
    result.add(dot)
    for x in np.arange(x - range, x + range, dx):
        if 0 - dx < x < 0 + dx:
            line = VectorizedPoint
        else:
            line = Line(
                start=axes.c2p(x, graph.underlying_function(x)),
                end=axes.c2p((x + dx), graph.underlying_function(x + dx)),
            ).set_color(YELLOW)
            result.add(line)
    return result


class ED(Scene):
    def construct(self):

        axes = Axes(
            x_range=[-8, 6, 2],
            x_length=10,
            y_range=[0, 21, 5],
            y_length=6,
            axis_config={"include_numbers": True, "include_tip": False},
        ).set_color(GREY)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.get_graph(
            lambda x: (((2 + x) ** 3 - 8)) / x, x_range=[-8, 2], color=BLUE
        )

        graph_label = (
            MathTex("f(x)=\\frac{(2+x)^3 - 8}{x}")
            .set_color(BLUE)
            .next_to(graph, RIGHT, buff=0.5)
        )

        dx = ValueTracker(1)

        epsilon_lines = always_redraw(
            lambda: get_epsilon_lines(x=0, dx=dx.get_value(), graph=graph, axes=axes)
        )

        delta_lines = always_redraw(
            lambda: get_delta_lines(x=0, dx=dx.get_value(), axes=axes)
        )

        faded_undefined = get_faded_undefined_epsilon_delta_lines(
            x=0, graph=graph, axes=axes
        )

        input_range = VGroup()
        input_line = Line(start=axes.c2p(-1, 0), end=axes.c2p(1, 0)).set_color(YELLOW)
        input_circle = Circle(radius=0.05).move_to(axes.c2p(0, 0)).set_color(YELLOW)
        input_range.add(input_circle, input_line)

        output_range = get_output_limit_range(
            x=0, graph=graph, dx=0.02, range=0.5, axes=axes
        )

        self.add(
            axes,
            axes_labels,
            graph,
            graph_label,
            epsilon_lines,
            delta_lines,
            faded_undefined,
        )
        self.wait()
        self.play(dx.animate.set_value(0.01), run_time=6, rate_func=there_and_back)
        self.play(Create(input_range))
        self.play(ReplacementTransform(input_range, output_range), run_time=2)
        self.wait()
        self.play(dx.animate.set_value(0.01), run_time=6, rate_func=there_and_back)
