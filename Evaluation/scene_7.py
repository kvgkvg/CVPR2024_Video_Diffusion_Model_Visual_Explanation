from section_common import *


class Scene7(EvalScene):
    scene_number = 7

    def construct(self):
        heading = title("CLIPScore measures semantic similarity")
        self.play(Write(heading), run_time=1.4)

        frames = video_strip(6, QUALITY, 8.0, 1.25).move_to(UP * 1.15)
        moving_dots = VGroup(*[
            Dot(frame.get_center() + LEFT * 0.32 + RIGHT * (0.13 * i), radius=0.09, color=DIVERSITY)
            for i, frame in enumerate(frames)
        ])
        links = VGroup(*[
            edge_arrow(a, b, RIGHT, LEFT, ALIGNMENT, buff=0.05)
            for a, b in zip(frames[:-1], frames[1:])
        ])
        self.cue(4.0)
        self.play(FadeIn(frames), FadeIn(moving_dots), run_time=1.5)
        self.cue(8.0)
        self.play(LaggedStart(*[Create(link) for link in links], lag_ratio=0.15), run_time=2.0)
        frame_score = pill("frame ↔ frame cosine similarity", ALIGNMENT).move_to(DOWN * 0.15)
        self.cue(11.5)
        self.play(FadeIn(frame_score), run_time=1.4)
        self.cue(13.5)
        self.play(LaggedStart(*[Indicate(pair, color=ALIGNMENT) for pair in links], lag_ratio=0.12), run_time=1.5)

        static_dots = VGroup(*[
            Dot(frame.get_center(), radius=0.09, color=DIVERSITY)
            for frame in frames
        ])
        static_note = label("static video can still score highly", FAILURE, BODY_SIZE).move_to(DOWN * 0.9)
        self.cue(16.0)
        self.play(Transform(moving_dots, static_dots), Indicate(frame_score, color=FAILURE), Write(static_note), run_time=1.8)

        prompt = panel('"a dog runs through snow"', TEMPORAL, 4.2, 1.0).move_to(LEFT * 3.2 + DOWN * 1.65)
        prompt_score = pill("text ↔ frame similarity", TEMPORAL).move_to(RIGHT * 3.2 + DOWN * 1.65)
        text_arrow = edge_arrow(prompt, prompt_score, RIGHT, LEFT, TEMPORAL)
        self.cue(21.3)
        self.play(FadeOut(static_note), FadeIn(prompt), Create(text_arrow), FadeIn(prompt_score), run_time=1.8)
        self.cue(25.0)
        self.play(Indicate(prompt, color=TEMPORAL), run_time=1.1)
        self.cue(27.3)
        self.play(Indicate(frames, color=QUALITY), run_time=1.1)
        self.cue(29.3)
        self.play(Indicate(VGroup(prompt, frames), color=WHITE), run_time=1.7)

        blind = VGroup(
            pill("motion", FAILURE),
            pill("event order", FAILURE),
            pill("long-term structure", FAILURE),
        ).arrange(RIGHT, buff=0.65).move_to(DOWN * 0.65)
        self.cue(34.0)
        self.play(
            FadeOut(frame_score), FadeOut(prompt), FadeOut(prompt_score), FadeOut(text_arrow),
            FadeIn(blind),
            run_time=1.8,
        )
        self.cue(38.3)
        self.play(Indicate(blind, color=WHITE), run_time=1.5)
        self.finish_to_audio()
