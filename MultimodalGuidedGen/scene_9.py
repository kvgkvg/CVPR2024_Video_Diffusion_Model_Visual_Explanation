from section_common import *


class Scene9(MultimodalScene):
    scene_number = 9
    pause_after_narration = 2.0

    def construct(self):
        heading = title("A condition constrains what matters")
        results = framed_image(asset("fmri_results.png", width=11.5), PRIMARY).move_to(DOWN * 0.05)
        self.play(Write(heading), FadeIn(results), run_time=2.2)
        self.play(Indicate(results, color=ERROR), run_time=1.5)
        self.play(Indicate(results, color=SECONDARY), run_time=2)
        self.wait(1.4)

        self.play(FadeOut(results), run_time=1.8)
        center = model_block("generated\nvideo", PRIMARY, 2.5, 1.3)
        controls = VGroup(
            pill("motion", SECONDARY),
            pill("viewpoint", PURPLE),
            pill("timing", ACCENT),
            pill("appearance", PRIMARY),
            pill("experience", ERROR),
        )
        positions = [LEFT * 4.6 + UP * 1.7, RIGHT * 4.6 + UP * 1.7, RIGHT * 4.8 + DOWN * 1.65, ORIGIN + DOWN * 2.2, LEFT * 4.8 + DOWN * 1.65]
        for control, position in zip(controls, positions):
            control.move_to(position)
        self.play(FadeIn(center), LaggedStart(*[FadeIn(c) for c in controls], lag_ratio=0.22), run_time=3)
        edge_pairs = [(RIGHT, LEFT), (LEFT, RIGHT), (LEFT, RIGHT), (UP, DOWN), (RIGHT, LEFT)]
        arrows = VGroup(*[
            edge_arrow(c, center, source_edge, target_edge, c[0].get_stroke_color())
            for c, (source_edge, target_edge) in zip(controls, edge_pairs)
        ])
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=3)
        self.wait(1.4)

        close = label("choose the signal that answers your control question", WHITE, BODY_SIZE).to_edge(DOWN, buff=0.25)
        close.scale_to_fit_width(11.5)
        self.play(Write(close), run_time=2.5)
        self.play(*[c.animate.set_opacity(0.28) for c in controls], Indicate(center, color=WHITE), run_time=2)
        self.finish_to_audio()
