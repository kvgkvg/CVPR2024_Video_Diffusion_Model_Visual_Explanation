from section_common import *


class Scene7(MultimodalScene):
    scene_number = 7

    def construct(self):
        heading = title("Image guidance: preserve appearance, invent motion")
        keyframe = RoundedRectangle(width=3.2, height=2.1, corner_radius=0.12, color=PRIMARY, fill_opacity=0.15).move_to(LEFT * 4.5 + UP * 0.45)
        subject = VGroup(Circle(radius=0.32, color=ACCENT), Line(DOWN * 0.05, DOWN * 0.8, color=ACCENT)).move_to(keyframe)
        key_label = label("input keyframe", PRIMARY, SMALL_SIZE).next_to(keyframe, DOWN, buff=0.25)
        self.play(Write(heading), FadeIn(keyframe), FadeIn(subject), Write(key_label), run_time=2)
        self.wait(1.2)

        futures = VGroup(
            panel("subject turns", SECONDARY, 2.2, 1.0),
            panel("camera pushes in", PURPLE, 2.45, 1.0),
            panel("background moves", ACCENT, 2.45, 1.0),
        ).arrange(DOWN, buff=0.5).move_to(RIGHT * 3.5 + UP * 0.25)
        arrows = VGroup(*[edge_arrow(keyframe, future, RIGHT, LEFT, future[0].get_stroke_color()) for future in futures])
        self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(f)) for a, f in zip(arrows, futures)], lag_ratio=0.3), run_time=4)
        self.wait(1.5)

        preserve = label("preserve identity and composition", PRIMARY, BODY_SIZE).to_edge(DOWN, buff=0.32)
        self.play(Write(preserve), Indicate(keyframe, color=WHITE), run_time=2)
        evidence = framed_image(asset("image_guided.png", width=9.6), PRIMARY).move_to(DOWN * 0.5)
        self.play(FadeOut(keyframe, subject, key_label, futures, arrows, preserve), FadeIn(evidence), run_time=2.7)
        drift = label("motion without content drift", SECONDARY, SMALL_SIZE).to_edge(DOWN, buff=0.22)
        self.play(Write(drift), run_time=1.5)
        self.finish_to_audio()
