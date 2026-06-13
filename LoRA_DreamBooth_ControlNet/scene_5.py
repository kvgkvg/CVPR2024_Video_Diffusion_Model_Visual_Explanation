from manim import *
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from config import *
from utils import *


class Scene5(NarratedScene):
    scene_number = 5

    def construct(self):
        heading = title("ControlNet: locked base, trainable copy")
        x = pill("x", WHITE, BODY_SIZE).move_to(LEFT * 5.6 + UP * 1.2)
        base = model_block("pretrained block", PRIMARY, 2.6, 1.2).move_to(LEFT * 2.6 + UP * 1.2)
        fusion = pill("+", WHITE, BODY_SIZE).move_to(RIGHT * 0.4 + UP * 1.2)
        output = pill("controlled output", SECONDARY, SMALL_SIZE).move_to(RIGHT * 4.3 + UP * 1.2)
        top_arrows = VGroup(
            edge_arrow(x, base, RIGHT, LEFT, WHITE),
            edge_arrow(base, fusion, RIGHT, LEFT, PRIMARY),
            edge_arrow(fusion, output, RIGHT, LEFT, SECONDARY),
        )
        locked = pill("LOCKED", GREY, MIN_SIZE).next_to(base, DOWN, buff=0.22)
        self.play(Write(heading), run_time=1.2)
        self.play(FadeIn(x), FadeIn(base), FadeIn(fusion), FadeIn(output), LaggedStart(*[Create(a) for a in top_arrows], lag_ratio=0.2), FadeIn(locked), run_time=2.2)
        self.wait(2.0)

        condition = pill("condition c", ACCENT, SMALL_SIZE).move_to(LEFT * 5.75 + DOWN * 1.35)
        zero_in = pill("zero conv", ACCENT, MIN_SIZE).move_to(LEFT * 3.45 + DOWN * 1.35)
        copy = model_block("trainable\ncopy", PURPLE, 2.0, 1.2).move_to(LEFT * 0.5 + DOWN * 1.35)
        zero_out = pill("zero conv", ACCENT, MIN_SIZE).move_to(RIGHT * 2.5 + DOWN * 1.35)
        branch_arrows = VGroup(
            edge_arrow(condition, zero_in, RIGHT, LEFT, ACCENT),
            edge_arrow(zero_in, copy, RIGHT, LEFT, PURPLE),
            edge_arrow(copy, zero_out, RIGHT, LEFT, PURPLE),
            edge_arrow(zero_out, fusion, UP, DOWN, SECONDARY),
        )
        self.play(
            FadeIn(condition), FadeIn(copy),
            run_time=1.5,
        )
        self.wait(3.2)
        self.play(FadeIn(zero_in), FadeIn(zero_out), run_time=1.2)
        self.play(LaggedStart(*[Create(a) for a in branch_arrows], lag_ratio=0.18), run_time=2.0)
        self.wait(5.0)

        note_a = label("starts with almost no effect", GREY, SMALL_SIZE)
        note_b = label("gradually learns structural control", SECONDARY, SMALL_SIZE)
        notes = VGroup(note_a, note_b).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.25)
        self.play(Write(note_a), run_time=1.2)
        self.wait(2.0)
        self.play(Write(note_b), Indicate(copy, color=WHITE), run_time=1.5)
        self.finish_to_audio()
