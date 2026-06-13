from section_common import *


class Scene2(MultimodalScene):
    scene_number = 2

    def construct(self):
        heading = title("MCDiff: draw the motion you want")
        start = RoundedRectangle(width=3.4, height=2.25, corner_radius=0.12, color=PRIMARY, fill_opacity=0.12).move_to(LEFT * 3.9 + UP * 0.55)
        ball = Circle(radius=0.3, color=ACCENT, fill_opacity=0.7).move_to(start.get_center() + LEFT * 0.65)
        self.play(Write(heading), FadeIn(start), FadeIn(ball), run_time=2)
        self.wait(1.2)

        sparse = VGroup(
            Arrow(ball.get_center(), ball.get_center() + RIGHT * 1.15 + UP * 0.35, color=SECONDARY, buff=0.05),
            Arrow(start.get_center() + LEFT * 1.0 + DOWN * 0.65, start.get_center() + LEFT * 0.35 + DOWN * 0.25, color=SECONDARY, buff=0.05),
            Arrow(start.get_center() + RIGHT * 0.25 + DOWN * 0.7, start.get_center() + RIGHT * 0.85 + DOWN * 0.25, color=SECONDARY, buff=0.05),
        )
        note = label("sparse user directions", SECONDARY, SMALL_SIZE).next_to(start, DOWN, buff=0.28)
        self.play(LaggedStart(*[GrowArrow(a) for a in sparse], lag_ratio=0.3), Write(note), run_time=2.8)
        self.wait(1.4)

        field_box = RoundedRectangle(width=3.4, height=2.25, corner_radius=0.12, color=PURPLE, fill_opacity=0.08).move_to(RIGHT * 3.9 + UP * 0.55)
        dense = VGroup()
        for y in [-0.65, -0.2, 0.25, 0.7]:
            for x in [-1.15, -0.55, 0.05, 0.65]:
                p = field_box.get_center() + RIGHT * x + UP * y
                dense.add(Arrow(p, p + RIGHT * 0.42 + UP * (0.08 + x * 0.04), color=PURPLE, buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.25))
        flow_label = label("optical flow", PURPLE, SMALL_SIZE).next_to(field_box, DOWN, buff=0.28)
        bridge = edge_arrow(start, field_box, RIGHT, LEFT, WHITE)
        self.play(Create(bridge), FadeIn(field_box), LaggedStart(*[GrowArrow(a) for a in dense], lag_ratio=0.04), Write(flow_label), run_time=3.5)
        self.wait(1.5)

        strip = video_strip(6, SECONDARY, 7.6, 1.15).to_edge(DOWN, buff=0.35)
        dots = VGroup(*[ball.copy().scale(0.62).move_to(frame.get_center() + RIGHT * (-0.3 + i * 0.12)) for i, frame in enumerate(strip)])
        self.play(FadeOut(note), FadeOut(flow_label), FadeOut(bridge), FadeIn(strip), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2), run_time=3)
        same_start = label("same start, controlled evolution", SECONDARY, SMALL_SIZE).next_to(strip, UP, buff=0.2)
        self.play(Write(same_start), run_time=1.5)
        self.finish_to_audio()
