from section_common import *


class Scene0(EvalScene):
    scene_number = 0
    intro_pause = 0.8

    def construct(self):
        self.start_scene()
        heading = label("Evaluating Video Generative Models", PRIMARY, 54, weight=BOLD)
        heading.scale_to_fit_width(12.0).to_edge(UP, buff=0.35)
        question = label("Which model is better?", ALIGNMENT, SECTION_SIZE).next_to(heading, DOWN, buff=0.3)
        self.play(Write(heading), run_time=1.5)
        self.cue(2.0)
        self.play(Write(question), run_time=1.2)
        self.cue(4.5)
        self.play(Indicate(question, color=ALIGNMENT), run_time=1.0)

        test = panel("known answers", QUALITY, 2.6, 1.1).move_to(LEFT * 4.2 + UP * 0.35)
        discrim = panel("discriminative\nmodel", PRIMARY, 2.6, 1.1).move_to(UP * 0.35)
        score = panel("accuracy\nrecall / IoU", DIVERSITY, 2.6, 1.1).move_to(RIGHT * 4.2 + UP * 0.35)
        flow = VGroup(edge_arrow(test, discrim, RIGHT, LEFT), edge_arrow(discrim, score, RIGHT, LEFT))
        self.cue(7.8)
        self.play(FadeIn(test), Create(flow[0]), FadeIn(discrim), run_time=1.8)
        self.cue(13.0)
        self.play(Create(flow[1]), FadeIn(score), run_time=1.5)
        self.cue(15.6)
        self.play(Indicate(score, color=DIVERSITY), run_time=1.0)

        model_a = sample_grid(color=QUALITY).move_to(LEFT * 3.6 + DOWN * 0.15)
        model_b = sample_grid(color=TEMPORAL).move_to(RIGHT * 3.6 + DOWN * 0.15)
        name_a = label("model A outputs", QUALITY, SMALL_SIZE).next_to(model_a, UP, buff=0.18)
        name_b = label("model B outputs", TEMPORAL, SMALL_SIZE).next_to(model_b, UP, buff=0.18)
        no_answer = label("no single correct answer", FAILURE, BODY_SIZE).move_to(DOWN * 1.45)
        self.cue(18.4)
        self.play(
            FadeOut(test), FadeOut(discrim), FadeOut(score), FadeOut(flow),
            FadeIn(model_a), FadeIn(model_b), Write(name_a), Write(name_b), Write(no_answer),
            run_time=2.0,
        )
        self.cue(22.7)
        self.play(Indicate(model_a, color=QUALITY), Indicate(model_b, color=TEMPORAL), run_time=1.2)

        criteria = VGroup(
            pill("sharpness", QUALITY),
            pill("diversity", DIVERSITY),
            pill("prompt match", ALIGNMENT),
            pill("motion", TEMPORAL),
        ).arrange(RIGHT, buff=0.48).move_to(DOWN * 2.0)
        self.cue(27.0)
        self.play(FadeOut(no_answer), LaggedStart(*[FadeIn(c) for c in criteria], lag_ratio=0.18), run_time=2.3)
        self.cue(31.0)
        self.play(LaggedStart(*[Indicate(c, color=c[0].get_stroke_color()) for c in criteria], lag_ratio=0.18), run_time=2.0)

        winner_a = label("winner: A on sharpness", QUALITY, SMALL_SIZE).move_to(DOWN * 1.2)
        winner_b = label("winner: B on motion", TEMPORAL, SMALL_SIZE).move_to(DOWN * 1.2)
        focus_a = SurroundingRectangle(criteria[0], color=QUALITY, buff=0.1)
        focus_b = SurroundingRectangle(criteria[3], color=TEMPORAL, buff=0.1)
        self.cue(34.5)
        self.play(Create(focus_a), Write(winner_a), run_time=1.1)
        self.play(
            ReplacementTransform(focus_a, focus_b),
            ReplacementTransform(winner_a, winner_b),
            run_time=1.1,
        )
        ranking = label("change the dimension  →  change the ranking", FAILURE, BODY_SIZE).to_edge(DOWN, buff=0.25)
        self.cue(37.0)
        self.play(FadeOut(focus_b), Write(ranking), run_time=1.5)
        self.finish_to_audio()
