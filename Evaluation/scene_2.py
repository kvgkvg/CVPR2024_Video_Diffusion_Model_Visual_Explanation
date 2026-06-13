from section_common import *


class Scene2(EvalScene):
    scene_number = 2

    def construct(self):
        heading = title("Start with the same prompts")
        self.play(Write(heading), run_time=1.4)
        prompt_suite = panel("shared prompt suite", ALIGNMENT, 3.5, 1.15, BODY_SIZE).move_to(UP * 1.7)
        self.cue(2.5)
        self.play(FadeIn(prompt_suite), run_time=1.4)

        tasks = VGroup(
            pill("composition", QUALITY),
            pill("counting", DIVERSITY),
            pill("spatial relations", TEMPORAL),
            pill("unusual combinations", ALIGNMENT),
        ).arrange_in_grid(rows=2, cols=2, buff=(1.0, 0.55)).move_to(DOWN * 0.15)
        task_arrows = VGroup(*[
            anchored_arrow(prompt_suite.get_edge_center(DOWN), task.get_edge_center(UP), task[0].get_stroke_color(), buff=0.08)
            for task in tasks
        ])
        self.cue(6.0)
        self.play(
            LaggedStart(*[Create(a) for a in task_arrows], lag_ratio=0.15),
            LaggedStart(*[FadeIn(t) for t in tasks], lag_ratio=0.15),
            run_time=2.3,
        )
        self.cue(10.0)
        self.play(LaggedStart(*[Indicate(t, color=t[0].get_stroke_color()) for t in tasks], lag_ratio=0.15), run_time=2.0)

        image_req = panel("image benchmark\nappearance", QUALITY, 3.2, 1.25).move_to(LEFT * 3.5 + DOWN * 0.15)
        video_req = panel("video benchmark\nappearance + motion", TEMPORAL, 3.5, 1.25).move_to(RIGHT * 3.5 + DOWN * 0.15)
        extra = VGroup(pill("plausible motion", TEMPORAL), pill("temporal coherence", TEMPORAL)).arrange(DOWN, buff=0.35).next_to(video_req, DOWN, buff=0.35)
        self.cue(15.8)
        self.play(FadeOut(tasks), FadeOut(task_arrows), run_time=0.5)
        self.play(FadeIn(image_req), run_time=1.0)
        self.cue(20.9)
        self.play(FadeIn(video_req), run_time=1.3)
        self.cue(23.5)
        self.play(FadeIn(extra), run_time=1.5)
        motion_dot = Dot(video_req.get_left() + RIGHT * 0.35, color=TEMPORAL, radius=0.09)
        motion_path = Line(video_req.get_left() + RIGHT * 0.35, video_req.get_right() + LEFT * 0.35)
        self.cue(26.0)
        self.play(FadeIn(motion_dot), MoveAlongPath(motion_dot, motion_path), Indicate(extra, color=TEMPORAL), run_time=2.0)

        models = VGroup(*[
            panel(f"model {c}", color, 2.2, 0.9)
            for c, color in zip("ABC", (QUALITY, DIVERSITY, TEMPORAL))
        ]).arrange(RIGHT, buff=1.0).move_to(DOWN * 1.25)
        model_arrows = VGroup(*[
            anchored_arrow(prompt_suite.get_edge_center(DOWN), model.get_edge_center(UP), model[0].get_stroke_color(), buff=0.08)
            for model in models
        ])
        self.cue(29.0)
        self.play(
            FadeOut(image_req), FadeOut(video_req), FadeOut(extra), FadeOut(motion_dot),
            FadeIn(models), LaggedStart(*[Create(a) for a in model_arrows], lag_ratio=0.2),
            run_time=2.2,
        )
        verdict = label("same request  →  meaningful comparison", DIVERSITY, SECTION_SIZE).to_edge(DOWN, buff=0.3)
        self.cue(35.2)
        self.play(FadeOut(model_arrows), models.animate.shift(UP * 0.35), Write(verdict), run_time=1.5)
        self.cue(39.2)
        self.play(Indicate(VGroup(prompt_suite, models), color=WHITE), run_time=1.8)
        self.finish_to_audio()
