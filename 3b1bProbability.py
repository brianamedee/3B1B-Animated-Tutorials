from manim import *
import random

HOME2 = "C:\manim\Manim_7_July\Projects\\assets\SVG_Images"


class Randomising(Scene):
    def construct(self):
        def randomize(number):
            value = random.uniform(0, 1)
            number.set_value(value)
            if value > 0.5:
                number.set_color(BLUE_D)
            else:
                number.set_color(RED_C)

        number = DecimalNumber()

        self.add(number)
        self.play(UpdateFromFunc(number, randomize), run_time=3)
        self.wait(2)


class MoreRandomising(Scene):
    def construct(self):
        def randomize_numbers(numbers):
            for num in numbers:
                value = random.uniform(0, 1)
                num.set_value(value)
                if value > 0.2:
                    num.set_color(GREEN)
                else:
                    num.set_color(RED_C)

        def get_results(numbers):
            results = VGroup()
            for num in numbers:
                if num.get_value() > 0.2:
                    win = SVGMobject(f"{HOME2}\\green_tick.svg").set_color(GREEN)
                    win.set(height=0.4)
                    win.next_to(num, DOWN, buff=0.25)
                    und = Underline(win).match_color(win)
                    results.add(win, und)
                else:
                    loss = SVGMobject(f"{HOME2}\\cross.svg").set_color(RED_C)
                    loss.set(height=0.4)
                    loss.next_to(num, DOWN, buff=0.25)
                    und = Underline(loss).match_color(loss)
                    results.add(loss, und)
            return results

        numbers = VGroup()
        for x in range(10):
            num = DecimalNumber()
            numbers.add(num)
        numbers.arrange(RIGHT).to_edge(UP)

        self.add(numbers)

        for k in range(2):
            self.play(UpdateFromFunc(numbers, randomize_numbers))
            results = get_results(numbers)
            self.play(Create(results))
            self.wait()
            self.play(FadeOut(results))
            self.wait(0.3)


class CoinStack(Scene):
    def construct(self):

        numbers = VGroup()
        for x in range(10):
            num = DecimalNumber()
            numbers.add(num)

        def randomize_numbers(numbers):
            for num in numbers:
                value = random.uniform(0, 1)
                num.set_value(value)
                if value > 0.5:
                    num.set_color(BLUE_D)
                else:
                    num.set_color(RED_C)

        numbers.set(height=0.2)
        numbers.arrange(RIGHT, buff=0.25)
        numbers.to_edge(UL)

        def get_results(numbers):
            results = VGroup()
            for num in numbers:
                if num.get_value() > 0.5:
                    result = Tex("H").set_color(BLUE_D)
                else:
                    result = Tex("T").set_color(RED_C)

                result.set(height=0.4)
                result.next_to(num, UP, buff=0.25)
                results.add(result)
            return results

        for x in range(14):
            k = 0
            self.play(
                numbers.animate.shift(DOWN * 0.5),
                UpdateFromFunc(numbers, randomize_numbers),
            )
            new_results = get_results(numbers)

            for num in numbers:
                if num.get_value() > 0.5:
                    k += 1

            self.play(LaggedStartMap(FadeIn, new_results))
            score = Integer()
            score.set_value(k).next_to(new_results, RIGHT, buff=0.6).set_color(YELLOW_D)
            self.play(Write(score))
            if k == 5:
                box = SurroundingRectangle(score)
                self.play(Create(box))


class Binomial_Simulation(Scene):
    def construct(self):

        ##STARTING WITH ALL THE HELPER FUNCTIONS##
        def get_histogram(possible_outcomes):
            result = VGroup()
            ax = Axes(
                x_range=[0, possible_outcomes],
                x_length=11,
                y_range=[0, 0.5],
                y_length=5,
                tips=False,
            )
            x_nums = VGroup(
                *[
                    Integer()
                    .scale(0.75)
                    .set_value(k)
                    .next_to(ax.c2p(k, 0), DR, buff=0.35)
                    for k in range(possible_outcomes)
                ]
            )
            y_nums = VGroup()
            value = 0
            for i in range(6):
                num = (
                    Integer(value, unit="\\%")
                    .scale(0.5)
                    .next_to(ax.c2p(0, i / 10), LEFT, buff=0.1)
                )
                value += 10
                y_nums.add(num)
            result.add(ax, x_nums, y_nums)
            result.to_edge(DL)
            return result

        def get_random_row(s=0.2, n=10):  # s is the probability of success
            values = np.random.random(n)
            nums = VGroup()
            syms = VGroup()
            for x, value in enumerate(values):
                num = DecimalNumber(value)
                num.set(height=0.25)
                num.move_to(x * RIGHT)
                num.positive = num.get_value() < s
                if num.positive:
                    num.set_color(GREEN)
                    sym = SVGMobject(f"{HOME2}\\green_tick.svg").set_color(GREEN)
                else:
                    num.set_color(RED)
                    sym = SVGMobject(f"{HOME2}\\cross.svg").set_color(RED)
                sym.match_color(num)
                sym.match_height(num)
                sym.positive = num.positive
                sym.next_to(num, DOWN, buff=0.25)

                nums.add(num)
                syms.add(sym)

            row = VGroup(nums, syms)
            row.nums = nums
            row.syms = syms
            row.n_positive = sum([m.positive for m in nums])

            row.center().to_edge(UP, buff=0)
            return row

        def get_bars(histogram, data):
            portions = np.array(data).astype(float)
            total = portions.sum()
            if total == 0:
                portions[:] = 0
            else:
                portions /= total

            bars = VGroup()

            for x, prop in enumerate(portions):
                p1 = VectorizedPoint().move_to(histogram[0].c2p(x, 0))
                p2 = VectorizedPoint().move_to(histogram[0].c2p(x + 1, 0))
                p3 = VectorizedPoint().move_to(histogram[0].c2p(x + 1, prop))
                p4 = VectorizedPoint().move_to(histogram[0].c2p(x, prop))
                points = VGroup(p1, p2, p3, p4)
                bar = Rectangle().replace(points, stretch=True)
                bar.set_style(
                    fill_color=[YELLOW, GREEN],
                    fill_opacity=0.8,
                    stroke_color=[YELLOW, GREEN],
                )
                bars.add(bar)
            return bars

        data = np.zeros(11)  # Possible outcomes as an array
        histogram = get_histogram(possible_outcomes=11)
        row = get_random_row(s=0.2, n=10)
        bars = get_bars(histogram=histogram, data=data)

        text_counter = Tex("Total trials: ").scale(0.6).to_edge(RIGHT, buff=2.5)
        counter = always_redraw(
            lambda: Integer()
            .scale(0.6)
            .set_value(sum(data))
            .next_to(text_counter, RIGHT, buff=0.3)
        )
        arrow = Line(ORIGIN, DOWN * 0.8).add_tip().set_color(BLUE)

        ##THE UPDATER FUNCTION##
        def update(dummy, n_added_data_points=0):
            new_row = get_random_row()
            row.become(new_row)
            count = sum([m.positive for m in new_row.nums])
            data[count] += 1
            if n_added_data_points:
                values = np.random.random((n_added_data_points, 10))
                counts = (values < 0.2).sum(1)
                for i in range(len(data)):
                    data[i] += (counts == i).sum()
            bars.become(get_bars(histogram=histogram, data=data))
            arrow.next_to(bars[count], UP, buff=0.1)
            bars[2].set_style(
                fill_color=[BLUE_B, BLUE_D], fill_opacity=0.8, stroke_color=BLUE
            )

        self.add(histogram, row, bars, counter, arrow, text_counter)

        group = VGroup(row, bars, arrow)
        self.play(UpdateFromFunc(group, update), run_time=2)

        self.play(
            UpdateFromFunc(group, lambda m: update(m, 10)),
            run_time=2,
        )
        self.play(
            UpdateFromFunc(group, lambda m: update(m, 100)),
            run_time=2,
        )
        self.play(
            UpdateFromFunc(group, lambda m: update(m, 1000)),
            run_time=2,
        )
        self.wait()
