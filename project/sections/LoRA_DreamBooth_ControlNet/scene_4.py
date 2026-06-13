from manim import *
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from config import *
from utils import *


class Scene4(NarratedScene):
    scene_number = 4

    def construct(self):
        heading = title("ControlNet: explicit spatial guidance")
        prompt = pill("text prompt", PRIMARY, BODY_SIZE).move_to(LEFT * 4.2 + UP * 1.15)
        model = model_block("diffusion\nmodel", PRIMARY, 2.3, 1.2).move_to(ORIGIN + UP * 1.15)
        output = pill("generated image", PRIMARY, BODY_SIZE).move_to(RIGHT * 4.2 + UP * 1.15)
        path_a = edge_arrow(prompt, model, RIGHT, LEFT, PRIMARY)
        path_b = edge_arrow(model, output, RIGHT, LEFT, PRIMARY)
        self.play(Write(heading), run_time=1.2)
        self.play(FadeIn(prompt), FadeIn(model), FadeIn(output), Create(path_a), Create(path_b), run_time=2.0)
        self.wait(6.5)

        condition = model_block("edge / pose\ncondition", ACCENT, 2.7, 1.2).move_to(LEFT * 4.5 + DOWN * 1.35)
        control = model_block("ControlNet", PURPLE, 2.3, 1.2).move_to(DOWN * 1.35)
        guided = model_block("structure\npreserved", SECONDARY, 2.7, 1.2).move_to(RIGHT * 4.5 + DOWN * 1.35)
        path_c = edge_arrow(condition, control, RIGHT, LEFT, ACCENT)
        path_d = edge_arrow(control, guided, RIGHT, LEFT, SECONDARY)
        self.play(FadeIn(condition), FadeIn(control), FadeIn(guided), Create(path_c), Create(path_d), run_time=2.0)
        self.wait(0.8)

        examples = image_asset("controlnet_edge_examples.png", width=11.5).move_to(DOWN * 0.2)
        border = SurroundingRectangle(examples, color=ACCENT, buff=0.08)
        caption = label("appearance varies; supplied structure remains", WHITE, SMALL_SIZE).next_to(examples, DOWN, buff=0.2)
        self.play(
            FadeOut(prompt), FadeOut(model), FadeOut(output), FadeOut(path_a), FadeOut(path_b),
            FadeOut(condition), FadeOut(control), FadeOut(guided), FadeOut(path_c), FadeOut(path_d),
            FadeIn(examples), Create(border),
            run_time=2.0,
        )
        self.play(Write(caption), run_time=1.4)
        self.finish_to_audio()
