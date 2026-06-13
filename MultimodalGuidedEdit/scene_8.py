from section_common import *


class Scene8(GuidedScene):
    scene_number = 8

    def construct(self):
        heading = title("Use the signal that directly expresses the edit")
        self.play(Write(heading), run_time=1.4)
        controls = VGroup(
            panel("instruction\nsemantic change", INSTRUCTION, 2.6, 1.25),
            panel("audio\nevent timing", AUDIO, 2.6, 1.25),
            panel("reference\nappearance", APPEARANCE, 2.6, 1.25),
            panel("pose\nmotion structure", MOTION, 2.6, 1.25),
        ).arrange(RIGHT, buff=0.45).move_to(UP * 1.35)
        self.cue(4.7)
        self.play(FadeIn(controls[0]), run_time=1.2)
        self.cue(8.3)
        self.play(FadeIn(controls[1]), run_time=1.2)
        self.cue(12.5)
        self.play(FadeIn(controls[2]), run_time=1.2)
        self.cue(14.9)
        self.play(FadeIn(controls[3]), run_time=1.2)

        time_bar = timeline(9, TIME, 9.8).move_to(DOWN * 0.15)
        self.cue(21.3)
        self.play(Create(time_bar), run_time=1.8)
        connectors = VGroup(*[
            anchored_arrow(control.get_edge_center(DOWN), time_bar[0].point_from_proportion(p), control[0].get_stroke_color())
            for control, p in zip(controls, (0.12, 0.38, 0.62, 0.88))
        ])
        self.cue(23.9)
        self.play(LaggedStart(*[Create(a) for a in connectors], lag_ratio=0.18), run_time=2.2)

        mechanisms = VGroup(
            pill("cross-frame attention", PRIMARY),
            pill("anchor features", ACCENT),
            pill("appearance encoder", APPEARANCE),
            pill("Pose ControlNet", MOTION),
            pill("overlapping windows", TIME),
        ).arrange(RIGHT, buff=0.3).scale(0.82).move_to(DOWN * 1.25)
        self.cue(27.3)
        self.play(LaggedStart(*[FadeIn(m) for m in mechanisms], lag_ratio=0.15), run_time=2.6)
        coherent = frame_strip(8, SECONDARY, 8.5, 0.95).to_edge(DOWN, buff=0.25)
        self.cue(36.8)
        self.play(FadeIn(coherent), run_time=1.8)
        self.cue(40.5)
        self.play(
            *[obj.animate.set_opacity(0.25) for obj in mechanisms],
            Indicate(coherent, color=WHITE),
            run_time=2.0,
        )
        final = label("precision  +  temporal modeling  =  coherent video", ACCENT, SECTION_SIZE).move_to(DOWN * 2.05)
        final.scale_to_fit_width(11.8)
        self.cue(44.3)
        self.play(FadeOut(mechanisms), FadeOut(coherent), Write(final), run_time=2.0)
        self.cue(49.7)
        self.play(Indicate(final, color=WHITE), run_time=1.8)
        self.finish_to_audio()
