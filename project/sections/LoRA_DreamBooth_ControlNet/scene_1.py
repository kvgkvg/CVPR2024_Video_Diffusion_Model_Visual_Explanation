from manim import *
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from config import *
from utils import *


class Scene1(NarratedScene):
    scene_number = 1

    def construct(self):
        heading = title("LoRA: efficient adaptation")
        base = model_block("pretrained\ndiffusion model", PRIMARY, 2.7, 1.4).move_to(LEFT * 4)
        request = pill("new style or domain", ACCENT, SMALL_SIZE).next_to(base, UP, buff=0.45)
        self.play(Write(heading), run_time=1.2)
        self.play(FadeIn(base), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(request), run_time=1.0)
        self.wait(3.1)

        full = model_block("full fine-tuned\ncheckpoint", ERROR, 2.8, 1.4).move_to(RIGHT * 3.8 + UP * 1.25)
        full_arrow = edge_arrow(base, full, RIGHT, LEFT, ERROR)
        full_size = label("large copy", ERROR, SMALL_SIZE).next_to(full, DOWN, buff=0.2)
        self.play(Create(full_arrow), FadeIn(full), Write(full_size), run_time=1.7)
        self.wait(4.0)

        adapter = model_block("compact\nLoRA adapter", SECONDARY, 2.5, 1.25).move_to(RIGHT * 3.8 + DOWN * 1.4)
        adapter_arrow = edge_arrow(base, adapter, RIGHT, LEFT, SECONDARY)
        adapter_size = label("small and shareable", SECONDARY, SMALL_SIZE).next_to(adapter, DOWN, buff=0.2)
        self.play(Create(adapter_arrow), FadeIn(adapter), Write(adapter_size), run_time=1.7)
        self.wait(3.0)

        self.play(
            full.animate.set_opacity(0.2),
            full_arrow.animate.set_opacity(0.2),
            full_size.animate.set_opacity(0.2),
            Indicate(adapter, color=WHITE),
            run_time=1.6,
        )
        takeaway = label("freeze the base model; train only the adapter", WHITE, BODY_SIZE)
        takeaway.to_edge(DOWN, buff=0.35)
        self.play(Write(takeaway), run_time=1.6)
        self.finish_to_audio()
