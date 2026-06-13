from section_common import *


class Scene1(EvalScene):
    scene_number = 1

    def construct(self):
        heading = title("Evaluation is a measurement problem")
        self.play(Write(heading), run_time=1.4)

        shared = panel("shared test set", QUALITY, 2.7, 1.05).move_to(LEFT * 4.1 + UP * 0.85)
        metrics = panel("meaningful metrics", ALIGNMENT, 2.7, 1.05).move_to(UP * 0.85)
        compare = panel("fair comparison", DIVERSITY, 2.7, 1.05).move_to(RIGHT * 4.1 + UP * 0.85)
        arrows = VGroup(edge_arrow(shared, metrics, RIGHT, LEFT), edge_arrow(metrics, compare, RIGHT, LEFT))
        self.cue(2.0)
        self.play(FadeIn(shared), Create(arrows[0]), FadeIn(metrics), Create(arrows[1]), FadeIn(compare), run_time=2.4)
        self.cue(6.2)
        self.play(Indicate(VGroup(shared, metrics, compare), color=WHITE), run_time=1.2)

        prompt_a = panel("paper A\nprompt set", QUALITY, 2.5, 1.0).move_to(LEFT * 2.0 + DOWN * 0.9)
        prompt_b = panel("paper B\nprompt set", TEMPORAL, 2.5, 1.0).move_to(RIGHT * 2.0 + DOWN * 0.9)
        not_equal = MathTex(r"\neq", color=FAILURE).scale(1.4).move_to(DOWN * 0.9)
        broken = Cross(shared, stroke_color=FAILURE, stroke_width=6)
        self.cue(9.8)
        self.play(Create(broken), FadeIn(prompt_a), FadeIn(prompt_b), Write(not_equal), run_time=1.8)
        self.cue(14.5)
        self.play(prompt_a.animate.shift(LEFT * 0.35), prompt_b.animate.shift(RIGHT * 0.35), Indicate(not_equal, color=FAILURE), run_time=1.2)

        target = panel("true video quality?", WHITE, 3.2, 1.15, BODY_SIZE).move_to(UP * 1.15)
        auto = panel("automatic metrics\nfast, heuristic", ALIGNMENT, 3.4, 1.4).move_to(LEFT * 3.25 + DOWN * 0.55)
        human = panel("human studies\nrich, expensive", TEMPORAL, 3.4, 1.4).move_to(RIGHT * 3.25 + DOWN * 0.55)
        instrument_arrows = VGroup(
            edge_arrow(auto, target, UP, LEFT, ALIGNMENT),
            edge_arrow(human, target, UP, RIGHT, TEMPORAL),
        )
        self.cue(19.8)
        self.play(
            FadeOut(shared), FadeOut(metrics), FadeOut(compare), FadeOut(arrows), FadeOut(broken),
            FadeOut(prompt_a), FadeOut(prompt_b), FadeOut(not_equal),
            run_time=0.7,
        )
        self.play(FadeIn(target), FadeIn(auto), Create(instrument_arrows[0]), run_time=1.3)
        metric_names = VGroup(pill("IS", ALIGNMENT), pill("FVD", ALIGNMENT), pill("CLIPScore", ALIGNMENT)).arrange(RIGHT, buff=0.25).next_to(auto, DOWN, buff=0.25)
        self.cue(23.2)
        self.play(LaggedStart(*[FadeIn(m) for m in metric_names], lag_ratio=0.2), run_time=1.4)
        self.cue(26.2)
        self.play(Indicate(metric_names, color=ALIGNMENT), run_time=1.0)
        self.cue(27.5)
        self.play(FadeIn(human), Create(instrument_arrows[1]), run_time=1.6)
        self.cue(30.4)
        self.play(Indicate(human, color=TEMPORAL), run_time=1.0)
        self.cue(31.5)
        self.play(FadeOut(metric_names), run_time=0.4)

        flaws = VGroup(
            pill("study design", FAILURE),
            pill("reproducibility", FAILURE),
            pill("cost + time", FAILURE),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.1)
        self.cue(32.0)
        self.play(LaggedStart(*[FadeIn(f) for f in flaws], lag_ratio=0.18), run_time=1.8)
        toolkit = SurroundingRectangle(VGroup(target, auto, human, instrument_arrows), color=WHITE, buff=0.28)
        self.cue(38.0)
        self.play(FadeOut(flaws), Create(toolkit), run_time=1.5)
        note = label("several imperfect instruments", ALIGNMENT, SECTION_SIZE).to_edge(DOWN, buff=0.35)
        self.cue(42.2)
        self.play(Write(note), Indicate(toolkit, color=WHITE), run_time=1.8)
        self.finish_to_audio()
