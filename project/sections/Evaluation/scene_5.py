from section_common import *


class Scene5(EvalScene):
    scene_number = 5

    def construct(self):
        heading = title("Inception Score inherits classifier blind spots")
        self.play(Write(heading), run_time=1.4)

        samples = sample_grid(rows=2, cols=5, color=QUALITY, cell=0.75).move_to(UP * 1.2)
        model_a = panel("classifier A\nscore: 63.7", QUALITY, 2.7, 1.1).move_to(LEFT * 2.2 + DOWN * 0.35)
        model_b = panel("classifier B\nscore: 65.9", TEMPORAL, 2.7, 1.1).move_to(RIGHT * 2.2 + DOWN * 0.35)
        self.cue(3.5)
        self.play(FadeIn(samples), run_time=1.4)
        self.cue(6.2)
        self.play(FadeIn(model_a), FadeIn(model_b), run_time=1.6)
        same = label("same samples  →  different score", FAILURE, BODY_SIZE).to_edge(DOWN, buff=0.45)
        self.cue(9.0)
        self.play(Write(same), run_time=1.4)
        self.cue(10.5)
        self.play(Indicate(VGroup(model_a, model_b), color=FAILURE), run_time=1.0)

        classifier = panel("classifier worldview", ALIGNMENT, 3.2, 1.15, BODY_SIZE).move_to(UP * 1.2)
        outside = panel("unfamiliar content\nunreliable confidence", ALIGNMENT, 3.6, 1.4).move_to(LEFT * 3.3 + DOWN * 0.45)
        adversarial = panel("meaningless image\n99.9% confident", FAILURE, 3.6, 1.4).move_to(RIGHT * 3.3 + DOWN * 0.45)
        arrows = VGroup(
            edge_arrow(outside, classifier, UP, LEFT, ALIGNMENT),
            edge_arrow(adversarial, classifier, UP, RIGHT, FAILURE),
        )
        self.cue(11.0)
        self.play(
            FadeOut(samples), FadeOut(model_a), FadeOut(model_b), FadeOut(same),
            run_time=0.6,
        )
        self.play(FadeIn(classifier), FadeIn(outside), Create(arrows[0]), run_time=1.2)
        self.cue(17.2)
        self.play(FadeIn(adversarial), Create(arrows[1]), run_time=1.5)
        self.cue(21.5)
        self.play(Indicate(adversarial, color=WHITE), run_time=1.6)
        self.cue(24.0)
        self.play(Indicate(classifier, color=FAILURE), run_time=1.0)

        video = video_strip(6, TEMPORAL, 7.2, 1.15).move_to(UP * 0.75)
        motion_cross = Cross(video, stroke_color=FAILURE, stroke_width=6)
        self.cue(26.0)
        self.play(FadeOut(classifier), FadeOut(outside), FadeOut(adversarial), FadeOut(arrows), run_time=0.7)
        self.play(FadeIn(video), run_time=1.3)
        self.cue(30.5)
        self.play(Create(motion_cross), run_time=1.2)
        self.cue(32.2)
        self.play(video.animate.shift(RIGHT * 0.18), run_time=0.5)
        self.play(video.animate.shift(LEFT * 0.36), run_time=0.5)
        self.play(video.animate.shift(RIGHT * 0.18), run_time=0.5)
        failures = VGroup(
            pill("identity drift", FAILURE),
            pill("nonsensical action", FAILURE),
            pill("incoherent motion", FAILURE),
        ).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.75)
        self.cue(34.4)
        self.play(LaggedStart(*[FadeIn(f) for f in failures], lag_ratio=0.18), run_time=1.7)
        summary = label("quick, but frame-based and brittle", ALIGNMENT, SECTION_SIZE).to_edge(DOWN, buff=0.3)
        self.cue(38.0)
        self.play(Write(summary), run_time=1.4)
        self.finish_to_audio()
