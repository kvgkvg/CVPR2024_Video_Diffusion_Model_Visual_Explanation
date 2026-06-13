from section_common import *


class Scene10(EvalScene):
    scene_number = 10

    def construct(self):
        heading = title("Better depends on what matters")
        self.play(Write(heading), run_time=1.4)

        model_a = panel("model A", QUALITY, 2.4, 1.0, BODY_SIZE).move_to(LEFT * 3.4 + UP * 1.35)
        model_b = panel("model B", TEMPORAL, 2.4, 1.0, BODY_SIZE).move_to(RIGHT * 3.4 + UP * 1.35)
        question = label("Which generated set is better?", WHITE, BODY_SIZE).move_to(UP * 2.2)
        self.cue(2.0)
        self.play(Write(question), FadeIn(model_a), FadeIn(model_b), run_time=1.5)

        criteria = VGroup(
            pill("quality", QUALITY),
            pill("alignment", ALIGNMENT),
            pill("aesthetics", PURPLE),
            pill("fairness", DIVERSITY),
            pill("toxicity", FAILURE),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.15)
        self.cue(8.0)
        self.play(LaggedStart(*[FadeIn(c) for c in criteria], lag_ratio=0.16), run_time=2.0)

        focus = SurroundingRectangle(criteria[0], color=QUALITY, buff=0.1)
        winner = label("quality selected  →  model A wins", QUALITY, BODY_SIZE).move_to(DOWN * 1.15)
        self.cue(12.0)
        self.play(Create(focus), Write(winner), model_a.animate.set_fill(QUALITY, opacity=0.3), run_time=1.4)

        next_focus = SurroundingRectangle(criteria[3], color=DIVERSITY, buff=0.1)
        next_winner = label("fairness selected  →  model B wins", DIVERSITY, BODY_SIZE).move_to(DOWN * 1.15)
        self.cue(15.5)
        self.play(
            ReplacementTransform(focus, next_focus),
            ReplacementTransform(winner, next_winner),
            model_a.animate.set_fill(QUALITY, opacity=0.09),
            model_b.animate.set_fill(TEMPORAL, opacity=0.3),
            run_time=1.5,
        )
        focus, winner = next_focus, next_winner

        video_dims = VGroup(pill("motion quality", TEMPORAL), pill("temporal consistency", TEMPORAL)).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.05)
        self.cue(18.5)
        self.play(FadeIn(video_dims), run_time=1.3)
        self.cue(21.0)
        self.play(Indicate(video_dims, color=TEMPORAL), run_time=1.2)

        scalar = panel("one perfect score", WHITE, 3.6, 1.0, BODY_SIZE).move_to(DOWN * 0.2)
        scalar_cross = Cross(scalar, stroke_color=FAILURE, stroke_width=7)
        self.cue(23.5)
        self.play(
            FadeOut(model_a), FadeOut(model_b), FadeOut(question), FadeOut(criteria),
            FadeOut(focus), FadeOut(winner), FadeOut(video_dims), FadeIn(scalar),
            run_time=1.4,
        )
        self.cue(25.5)
        self.play(Create(scalar_cross), run_time=1.2)

        toolkit = VGroup(
            panel("shared\nprompts", QUALITY, 2.3, 1.15),
            panel("complementary\nmetrics", ALIGNMENT, 2.3, 1.15),
            panel("human\nstudies", TEMPORAL, 2.3, 1.15),
            panel("safety\nanalysis", FAILURE, 2.3, 1.15),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.25)
        self.cue(27.5)
        self.play(FadeOut(scalar), FadeOut(scalar_cross), LaggedStart(*[FadeIn(t) for t in toolkit], lag_ratio=0.18), run_time=2.2)
        self.cue(31.0)
        self.play(LaggedStart(*[Indicate(t, color=t[0].get_stroke_color()) for t in toolkit], lag_ratio=0.16), run_time=2.0)

        lens = label("each instrument is a different lens", ALIGNMENT, SECTION_SIZE).move_to(DOWN * 1.55)
        reveal = label("reveals", DIVERSITY, BODY_SIZE).move_to(LEFT * 2.5 + DOWN * 2.35)
        hide = label("hides", FAILURE, BODY_SIZE).move_to(RIGHT * 2.5 + DOWN * 2.35)
        self.cue(35.0)
        self.play(Write(lens), run_time=1.3)
        self.cue(38.0)
        self.play(Write(reveal), Write(hide), run_time=1.3)
        intended = label("judge blind spots against the intended use", WHITE, BODY_SIZE).to_edge(DOWN, buff=0.25)
        self.cue(41.0)
        self.play(FadeOut(reveal), FadeOut(hide), Write(intended), Indicate(toolkit, color=WHITE), run_time=1.7)
        self.finish_to_audio()
