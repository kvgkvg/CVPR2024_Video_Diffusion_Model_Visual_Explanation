from section_common import *


class Scene3(EvalScene):
    scene_number = 3

    def construct(self):
        heading = title("Three common metrics, three projections")
        self.play(Write(heading), run_time=1.4)

        video = video_strip(6, WHITE, 7.2, 1.05).move_to(UP * 1.35)
        video_label = label("the same generated videos", WHITE, SMALL_SIZE).next_to(video, UP, buff=0.18)
        self.cue(3.0)
        self.play(FadeIn(video), Write(video_label), run_time=2.0)

        metrics = VGroup(
            panel("Inception Score\nrecognizable + varied", QUALITY, 3.2, 1.25),
            panel("FVD\nreal ↔ generated", TEMPORAL, 3.2, 1.25),
            panel("CLIPScore\nsemantic similarity", ALIGNMENT, 3.2, 1.25),
        ).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.45)
        arrows = VGroup(*[
            anchored_arrow(video.get_edge_center(DOWN), metric.get_edge_center(UP), metric[0].get_stroke_color(), buff=0.08)
            for metric in metrics
        ])
        self.cue(7.0)
        self.play(Create(arrows[0]), FadeIn(metrics[0]), run_time=1.4)
        self.cue(10.0)
        self.play(Create(arrows[1]), FadeIn(metrics[1]), run_time=1.4)
        self.cue(12.0)
        self.play(Create(arrows[2]), FadeIn(metrics[2]), run_time=1.4)
        self.cue(16.0)
        self.play(Indicate(metrics[0], color=QUALITY), run_time=1.0)
        self.cue(18.5)
        self.play(Indicate(metrics[1], color=TEMPORAL), run_time=1.0)
        self.cue(21.0)
        self.play(Indicate(metrics[2], color=ALIGNMENT), run_time=1.0)

        reference = pill("PSNR / perceptual similarity only when a reference exists", DIVERSITY).to_edge(DOWN, buff=0.3)
        self.cue(23.5)
        self.play(FadeIn(reference), run_time=1.5)

        focus = SurroundingRectangle(metrics[0], color=QUALITY, buff=0.12)
        self.cue(29.0)
        self.play(Create(focus), run_time=0.6)
        for metric, color in zip(metrics[1:], (TEMPORAL, ALIGNMENT)):
            new_focus = SurroundingRectangle(metric, color=color, buff=0.12)
            self.play(ReplacementTransform(focus, new_focus), run_time=1.0)
            focus = new_focus

        blind = label("each lens reveals one projection — and hides the rest", FAILURE, BODY_SIZE).to_edge(DOWN, buff=0.3)
        self.cue(35.1)
        self.play(FadeOut(reference), FadeOut(focus), run_time=0.5)
        self.play(Write(blind), run_time=1.1)
        self.cue(38.5)
        self.play(
            *[metric.animate.set_opacity(0.25) for metric in metrics],
            arrows.animate.set_opacity(0.25),
            Indicate(video, color=WHITE),
            run_time=1.5,
        )
        self.finish_to_audio()
