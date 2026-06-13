from section_common import *


class Scene1(MultimodalScene):
    scene_number = 1
    intro_pause = 1.5

    def construct(self):
        self.start_scene()
        heading = title("What does the video need to obey?")
        prompt = pill('"a car on a mountain road"', WHITE, SMALL_SIZE).move_to(UP * 1.5)
        model = model_block("video diffusion", PRIMARY, 4.4, 1.25)
        output = video_strip(5, SECONDARY, 5.6, 1.15).move_to(DOWN * 2.15)
        prompt_arrow = edge_arrow(prompt, model, DOWN, UP, WHITE)
        output_arrow = edge_arrow(model, output, DOWN, UP, SECONDARY)
        self.play(Write(heading), run_time=1.4)
        self.play(FadeIn(prompt), Create(prompt_arrow), FadeIn(model), run_time=2)
        self.play(Create(output_arrow), LaggedStart(*[FadeIn(f) for f in output], lag_ratio=0.15), run_time=2.2)
        self.wait(1.5)

        question = label("plausible ... but underspecified", GREY, SMALL_SIZE).next_to(output, DOWN, buff=0.24)
        self.play(Write(question), run_time=1.4)
        self.wait(1.5)

        controls = VGroup(
            panel("motion", SECONDARY, 2.2, 0.65, MIN_SIZE),
            panel("camera", PURPLE, 2.2, 0.65, MIN_SIZE),
            panel("sound", ACCENT, 2.2, 0.65, MIN_SIZE),
            panel("image", PRIMARY, 2.2, 0.65, MIN_SIZE),
            panel("brain activity", ERROR, 2.2, 0.65, MIN_SIZE),
        ).arrange(RIGHT, buff=0.2).move_to(UP * 1.65)
        target_x = np.linspace(-1.8, 1.8, len(controls))
        arrows = VGroup(*[
            anchored_arrow(
                control.get_edge_center(DOWN),
                model.get_edge_center(UP) + RIGHT * x,
                control[0].get_stroke_color(),
            )
            for control, x in zip(controls, target_x)
        ])
        self.play(
            FadeOut(question), FadeOut(prompt), FadeOut(prompt_arrow),
            LaggedStart(*[FadeIn(c) for c in controls], lag_ratio=0.25),
            run_time=3,
        )
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.22), run_time=2.5)
        self.wait(1.5)
        questions = VGroup(
            label("where?", SECONDARY, SMALL_SIZE),
            label("viewpoint?", PURPLE, SMALL_SIZE),
            label("when?", ACCENT, SMALL_SIZE),
            label("appearance?", PRIMARY, SMALL_SIZE),
            label("experience?", ERROR, SMALL_SIZE),
        )
        for q, c in zip(questions, controls):
            q.next_to(c, UP, buff=0.2)
        self.play(LaggedStart(*[Write(q) for q in questions], lag_ratio=0.22), run_time=3)
        self.finish_to_audio()
