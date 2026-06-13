from manim import *
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "shared"))
from config import *
from utils import *


def subject_icon(color, scale=1.0):
    head = Circle(radius=0.34, color=color, fill_color=color, fill_opacity=0.18)
    ears = VGroup(
        Triangle(color=color, fill_color=color, fill_opacity=0.25).scale(0.22).rotate(0.3),
        Triangle(color=color, fill_color=color, fill_opacity=0.25).scale(0.22).rotate(-0.3),
    )
    ears[0].next_to(head, UL, buff=-0.12)
    ears[1].next_to(head, UR, buff=-0.12)
    eyes = VGroup(Dot(radius=0.035), Dot(radius=0.035)).arrange(RIGHT, buff=0.16).move_to(head).shift(UP * 0.05)
    return VGroup(ears, head, eyes).scale(scale)


class Scene3(NarratedScene):
    scene_number = 3

    def construct(self):
        heading = title("DreamBooth: personalize a subject")
        generic = VGroup(*[subject_icon(c) for c in [PRIMARY, SECONDARY, PURPLE, ERROR]]).arrange(RIGHT, buff=0.6)
        generic.move_to(UP * 1.1)
        dog_token = pill('"dog"', GREY, BODY_SIZE).next_to(generic, DOWN, buff=0.35)
        self.play(Write(heading), run_time=1.2)
        self.play(LaggedStart(*[Create(icon) for icon in generic], lag_ratio=0.2), FadeIn(dog_token), run_time=2.0)
        self.wait(5.5)

        examples = VGroup(*[subject_icon(ACCENT, 0.58) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.15)
        examples.move_to(LEFT * 4 + DOWN * 1.25)
        binder = model_block("few-shot\nfine-tuning", SECONDARY, 2.3, 1.15).move_to(DOWN * 1.25)
        token = pill('"[V] dog"', ACCENT, BODY_SIZE).move_to(RIGHT * 4 + DOWN * 1.25)
        arrow_a = edge_arrow(examples, binder, RIGHT, LEFT, SECONDARY)
        arrow_b = edge_arrow(binder, token, RIGHT, LEFT, ACCENT)
        self.play(FadeIn(examples), FadeIn(binder), Create(arrow_a), run_time=1.5)
        self.play(Create(arrow_b), FadeIn(token), run_time=1.3)
        self.wait(3.2)

        self.play(
            FadeOut(generic), FadeOut(dog_token),
            FadeOut(examples), FadeOut(binder), FadeOut(token),
            FadeOut(arrow_a), FadeOut(arrow_b),
            run_time=1.2,
        )
        contexts = VGroup(
            pill("on the beach", PRIMARY, SMALL_SIZE),
            pill("wearing glasses", PURPLE, SMALL_SIZE),
            pill("in a painting", SECONDARY, SMALL_SIZE),
        ).arrange(RIGHT, buff=0.45).to_edge(UP, buff=1.5)
        identities = VGroup(*[subject_icon(ACCENT, 0.75) for _ in contexts])
        for identity, context in zip(identities, contexts):
            identity.next_to(context, DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(c) for c in contexts], lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[Create(i) for i in identities], lag_ratio=0.2), run_time=1.5)
        preserve = label('keep "dog" broad; make "[V] dog" specific', WHITE, SMALL_SIZE).to_edge(DOWN, buff=0.25)
        self.play(Write(preserve), run_time=1.5)
        self.finish_to_audio()
