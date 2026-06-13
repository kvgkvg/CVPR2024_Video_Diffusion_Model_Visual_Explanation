from section_common import *


class Scene3(GuidedScene):
    scene_number = 3

    def construct(self):
        heading = title("Fairy: link editing decisions across time")
        self.play(Write(heading), run_time=1.4)
        frames = frame_strip(6, PRIMARY, 9.0, 1.55).move_to(UP * 1.05)
        helmets = VGroup()
        for index, frame in enumerate(frames):
            helmet = Arc(radius=0.23 + 0.025 * (index % 3), start_angle=0, angle=PI, color=ERROR, stroke_width=5)
            helmet.move_to(frame.get_center() + UP * 0.05 + RIGHT * 0.04 * ((index % 2) * 2 - 1))
            helmets.add(helmet)
        self.cue(4.0)
        self.play(FadeIn(frames), run_time=1.5)
        self.cue(6.6)
        self.play(LaggedStart(*[Create(h) for h in helmets], lag_ratio=0.12), run_time=1.8)
        drift = label("independent edits drift", ERROR, BODY_SIZE).next_to(frames, DOWN, buff=0.3)
        self.cue(10.0)
        self.play(Write(drift), run_time=1.2)

        links = attention_links(frames, MOTION)
        self.cue(12.4)
        self.play(FadeOut(drift), LaggedStart(*[Create(link) for link in links], lag_ratio=0.14), run_time=2.2)
        cross = label("cross-frame attention", MOTION, BODY_SIZE).next_to(frames, DOWN, buff=0.3)
        self.cue(18.3)
        self.play(Write(cross), run_time=1.3)

        anchors = VGroup(*[
            SurroundingRectangle(frames[index], color=ACCENT, buff=0.1)
            for index in (0, 3, 5)
        ])
        qkv = VGroup(*[pill(name, ACCENT) for name in ("Q", "K", "V")]).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.4)
        self.cue(26.2)
        self.play(LaggedStart(*[Create(a) for a in anchors], lag_ratio=0.25), run_time=1.8)
        self.cue(28.9)
        self.play(FadeIn(qkv), run_time=1.3)
        self.cue(31.9)
        self.play(
            *[helmet.animate.set_color(ACCENT).scale(0.92 / helmet.width) for helmet in helmets],
            run_time=2.2,
        )
        linked = label("one temporally linked edit", SECONDARY, SECTION_SIZE).move_to(DOWN * 1.65)
        self.cue(35.0)
        self.play(ReplacementTransform(cross, linked), run_time=1.5)
        self.cue(42.2)
        self.play(Indicate(VGroup(frames, helmets, links, anchors), color=WHITE), run_time=2.0)
        self.finish_to_audio()
