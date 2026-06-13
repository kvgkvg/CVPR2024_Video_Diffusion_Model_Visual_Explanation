from manim import *
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from config import *
from utils import *


class Scene6(NarratedScene):
    scene_number = 6
    pause_after_narration = 2.0

    def construct(self):
        heading = title("ControlNet supports many conditions")
        names = VGroup(*[
            pill(text, color, SMALL_SIZE)
            for text, color in [
                ("sketch", PRIMARY),
                ("normal", PURPLE),
                ("depth", GREY),
                ("Canny edge", ACCENT),
                ("segmentation", SECONDARY),
                ("human pose", ERROR),
            ]
        ]).arrange(RIGHT, buff=0.25).scale_to_fit_width(12.2).to_edge(UP, buff=1.4)
        self.play(Write(heading), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(name, shift=DOWN * 0.15) for name in names], lag_ratio=0.12), run_time=2.0)
        self.wait(6.0)

        grid = image_asset("controlnet_condition_grid.png", width=10.5).move_to(DOWN * 0.15)
        border = SurroundingRectangle(grid, color=PRIMARY, buff=0.07)
        self.play(FadeOut(names), FadeIn(grid), Create(border), run_time=2.0)
        self.wait(1.0)

        takeaway = label("choose the condition that represents the structure you need", WHITE, BODY_SIZE)
        takeaway.scale_to_fit_width(11.8)
        takeaway.to_edge(DOWN, buff=0.25)
        self.play(grid.animate.set_opacity(0.42), run_time=1.2)
        self.play(Write(takeaway), run_time=1.7)
        self.finish_to_audio()
