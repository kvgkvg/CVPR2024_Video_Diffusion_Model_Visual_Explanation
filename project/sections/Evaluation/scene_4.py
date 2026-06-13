from section_common import *


class Scene4(EvalScene):
    scene_number = 4

    def construct(self):
        heading = title("Inception Score: confidence × diversity")
        self.play(Write(heading), run_time=1.4)
        sample = panel("generated sample", QUALITY, 2.8, 1.35).move_to(LEFT * 4.2 + UP * 0.9)
        classifier = panel("pretrained\nclassifier", PRIMARY, 2.6, 1.35).move_to(UP * 0.9)
        probs = VGroup(*[
            metric_gauge(name, color, value, 2.0)
            for name, color, value in (("cat", QUALITY, 0.92), ("dog", DIVERSITY, 0.05), ("car", TEMPORAL, 0.03))
        ]).arrange(DOWN, buff=0.25).move_to(RIGHT * 4.0 + UP * 0.9)
        flow = VGroup(edge_arrow(sample, classifier, RIGHT, LEFT), anchored_arrow(classifier.get_edge_center(RIGHT), probs.get_edge_center(LEFT), QUALITY))
        self.cue(4.5)
        self.play(FadeIn(sample), Create(flow[0]), FadeIn(classifier), run_time=1.7)
        self.cue(10.8)
        self.play(Create(flow[1]), FadeIn(probs), run_time=1.7)
        self.cue(13.5)
        self.play(Indicate(probs[0], color=QUALITY), run_time=1.1)
        confidence = pill("low entropy = confident sample", QUALITY).move_to(DOWN * 0.4)
        self.cue(16.0)
        self.play(FadeIn(confidence), run_time=1.4)

        classes = VGroup(*[pill(name, color) for name, color in (("cat", QUALITY), ("dog", DIVERSITY), ("car", TEMPORAL), ("bird", ALIGNMENT))]).arrange(RIGHT, buff=0.55).move_to(DOWN * 1.35)
        self.cue(20.5)
        self.play(FadeIn(classes), run_time=1.6)
        self.cue(23.5)
        self.play(LaggedStart(*[Indicate(c, color=c[0].get_stroke_color()) for c in classes], lag_ratio=0.15), run_time=1.8)
        diverse = pill("many classes = diverse collection", DIVERSITY).move_to(DOWN * 2.25)
        self.cue(26.0)
        self.play(FadeIn(diverse), run_time=1.4)
        equation = MathTex(
            r"\mathrm{IS}\uparrow",
            r"\Longleftarrow",
            r"H(y\mid x)\downarrow",
            r"\quad\text{and}\quad",
            r"H(y)\uparrow",
            color=WHITE,
        ).scale(0.9).move_to(DOWN * 0.35)
        equation[2].set_color(QUALITY)
        equation[4].set_color(DIVERSITY)
        self.cue(28.5)
        self.play(FadeOut(confidence), Write(equation), run_time=1.8)
        self.cue(33.5)
        self.play(Indicate(equation[2], color=QUALITY), Indicate(equation[4], color=DIVERSITY), run_time=1.3)
        worldview = panel("classifier worldview\nusually ImageNet", FAILURE, 3.6, 1.1).to_edge(DOWN, buff=0.25)
        self.cue(38.0)
        self.play(FadeOut(diverse), FadeIn(worldview), run_time=1.5)
        self.cue(42.0)
        self.play(Indicate(classifier, color=FAILURE), run_time=1.6)
        self.finish_to_audio()
