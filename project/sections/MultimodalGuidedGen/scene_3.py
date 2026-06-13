from section_common import *


class Scene3(MultimodalScene):
    scene_number = 3

    def construct(self):
        heading = title("MCDiff: sparse instruction to dense motion")
        sparse = panel("sparse\nstrokes", SECONDARY, 2.0, 1.25).move_to(LEFT * 5.1 + UP * 0.65)
        complete = panel("flow\ncompletion", PURPLE, 2.25, 1.25).move_to(LEFT * 2.1 + UP * 0.65)
        dense = panel("dense\noptical flow", PURPLE, 2.25, 1.25).move_to(RIGHT * 1.05 + UP * 0.65)
        predictor = panel("diffusion\npredictor", PRIMARY, 2.25, 1.25).move_to(RIGHT * 4.25 + UP * 0.65)
        chain = VGroup(sparse, complete, dense, predictor)
        arrows = VGroup(*[edge_arrow(chain[i], chain[i + 1], RIGHT, LEFT, WHITE) for i in range(3)])
        self.play(Write(heading), FadeIn(sparse), run_time=1.8)
        self.wait(1.2)
        self.play(Create(arrows[0]), FadeIn(complete), run_time=2)
        self.play(Create(arrows[1]), FadeIn(dense), run_time=2)
        self.wait(1.2)

        current = pill("current frame", ACCENT).move_to(RIGHT * 4.25 + DOWN * 1.15)
        current_arrow = edge_arrow(current, predictor, UP, DOWN, ACCENT)
        self.play(FadeIn(current), Create(current_arrow), Create(arrows[2]), FadeIn(predictor), run_time=2.5)
        self.wait(1.2)

        next_frame = pill("next frame", SECONDARY).move_to(RIGHT * 1.05 + DOWN * 1.15)
        out_arrow = edge_arrow(predictor, next_frame, DOWN, UP, SECONDARY)
        loop = edge_arrow(next_frame, current, RIGHT, LEFT, SECONDARY)
        repeat = label("repeat", SECONDARY, SMALL_SIZE).next_to(loop, DOWN, buff=0.12)
        self.play(Create(out_arrow), FadeIn(next_frame), run_time=2)
        self.play(Create(loop), Write(repeat), run_time=2)
        self.wait(1.5)
        for _ in range(2):
            self.play(Indicate(current, color=ACCENT), Indicate(predictor, color=PRIMARY), Indicate(next_frame, color=SECONDARY), run_time=2)
        self.finish_to_audio()
