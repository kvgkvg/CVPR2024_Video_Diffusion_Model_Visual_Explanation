from manim import *
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from config import *
from utils import *


class Scene2(NarratedScene):
    scene_number = 2

    def construct(self):
        heading = title("LoRA: a low-rank update")
        w = matrix_grid(12, 12, PRIMARY, cell=0.22, opacity=0.62).move_to(LEFT * 3.7)
        w_label = label("W  :  d × d", PRIMARY, SMALL_SIZE).next_to(w, DOWN, buff=0.25)
        frozen = pill("FROZEN", GREY, MIN_SIZE).next_to(w, UP, buff=0.25)
        self.play(Write(heading), run_time=1.2)
        self.play(Create(w), FadeIn(w_label), run_time=2.0)
        self.play(Indicate(w, color=ERROR), run_time=1.4)
        self.wait(0.8)

        b = matrix_grid(12, 3, ACCENT, cell=0.22, opacity=0.82)
        a = matrix_grid(3, 12, SECONDARY, cell=0.22, opacity=0.82)
        times = label("×", WHITE, SECTION_SIZE)
        factors = VGroup(b, times, a).arrange(RIGHT, buff=0.28).move_to(RIGHT * 2.7 + UP * 0.5)
        b_label = label("B", ACCENT, SMALL_SIZE).next_to(b, UP, buff=0.15)
        a_label = label("A", SECONDARY, SMALL_SIZE).next_to(a, UP, buff=0.15)
        rank = label("inner dimension  r << d", ACCENT, SMALL_SIZE).next_to(factors, DOWN, buff=0.3)
        self.play(LaggedStart(FadeIn(b), FadeIn(times), FadeIn(a), lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(b_label), FadeIn(a_label), Write(rank), run_time=1.2)
        self.wait(5.5)

        update = matrix_grid(12, 12, SECONDARY, cell=0.22, opacity=0.42)
        update.move_to(RIGHT * 3.7 + UP * w.get_y())
        update_label = label("low-rank update  BA", SECONDARY, SMALL_SIZE).next_to(update, DOWN, buff=0.25)
        self.play(
            ReplacementTransform(factors, update),
            FadeOut(b_label), FadeOut(a_label), FadeOut(rank),
            FadeIn(update_label),
            run_time=2.0,
        )
        self.wait(0.8)

        equation = MathTex(r"W' = W + BA", r"\qquad r \ll d", font_size=38)
        equation.set_color_by_tex("W", PRIMARY)
        equation.set_color_by_tex("BA", SECONDARY)
        equation.set_color_by_tex("r", ACCENT)
        equation.to_edge(DOWN, buff=0.35)
        self.play(Write(equation), run_time=1.7)
        self.wait(2.2)
        self.play(FadeIn(frozen), Indicate(w, color=WHITE), run_time=1.5)
        self.play(Indicate(update, color=WHITE), run_time=1.3)
        self.finish_to_audio()
