from section_common import *


class Scene7(GuidedScene):
    scene_number = 7

    def construct(self):
        heading = title("Long videos need shared boundaries")
        self.play(Write(heading), run_time=1.4)
        long_line = timeline(14, TIME, 10.5).move_to(UP * 1.55)
        self.cue(3.7)
        self.play(Create(long_line), run_time=1.8)
        drift = label("short coherent clip  →  long-term drift", ERROR, BODY_SIZE).next_to(long_line, DOWN, buff=0.35)
        self.cue(6.0)
        self.play(Write(drift), run_time=1.4)

        windows = VGroup(*[
            RoundedRectangle(width=4.0, height=1.1, corner_radius=0.12, color=color, fill_color=color, fill_opacity=0.1)
            for color in (PRIMARY, MOTION, APPEARANCE)
        ])
        windows[0].move_to(LEFT * 3.2 + DOWN * 0.2)
        windows[1].move_to(DOWN * 0.2)
        windows[2].move_to(RIGHT * 3.2 + DOWN * 0.2)
        self.cue(8.9)
        self.play(FadeOut(drift), LaggedStart(*[FadeIn(w) for w in windows], lag_ratio=0.22), run_time=2.0)
        overlap_a = Intersection(windows[0], windows[1], color=ACCENT, fill_opacity=0.38, stroke_width=0)
        overlap_b = Intersection(windows[1], windows[2], color=ACCENT, fill_opacity=0.38, stroke_width=0)
        self.cue(12.2)
        self.play(FadeIn(overlap_a), FadeIn(overlap_b), run_time=1.3)

        same_noise = pill("same noise initialization", PRIMARY).move_to(DOWN * 1.3)
        average = pill("average overlap", ACCENT).move_to(DOWN * 2.1)
        self.cue(14.6)
        self.play(FadeIn(same_noise), run_time=1.3)
        self.cue(18.9)
        self.play(FadeIn(average), Indicate(VGroup(overlap_a, overlap_b), color=WHITE), run_time=1.8)

        joined = frame_strip(12, SECONDARY, 10.8, 0.9).move_to(DOWN * 0.2)
        self.cue(21.3)
        self.play(
            FadeOut(windows), FadeOut(overlap_a), FadeOut(overlap_b),
            FadeOut(same_noise), FadeOut(average), FadeIn(joined),
            run_time=2.2,
        )
        handshake = label("overlap = handshake between neighboring clips", ACCENT, BODY_SIZE).next_to(joined, DOWN, buff=0.35)
        self.cue(22.5)
        self.play(Write(handshake), run_time=1.5)
        self.cue(25.0)
        self.play(Indicate(joined, color=WHITE), run_time=1.8)

        domains = VGroup(
            panel("photo", APPEARANCE, 2.0, 1.0),
            panel("painting", APPEARANCE, 2.0, 1.0),
            panel("stylized", APPEARANCE, 2.0, 1.0),
        ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.25)
        self.cue(28.5)
        self.play(FadeOut(handshake), FadeIn(domains), run_time=1.8)
        self.cue(34.0)
        self.play(LaggedStart(*[Indicate(d, color=WHITE) for d in domains], lag_ratio=0.25), run_time=2.2)
        principle = label("share enough information across windows", SECONDARY, SECTION_SIZE).move_to(DOWN * 1.55)
        self.cue(39.9)
        self.play(Write(principle), run_time=1.6)
        self.cue(45.7)
        self.play(Indicate(VGroup(joined, principle), color=ACCENT), run_time=2.0)
        self.finish_to_audio()
