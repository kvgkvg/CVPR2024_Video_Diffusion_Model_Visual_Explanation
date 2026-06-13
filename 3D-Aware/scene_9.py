from section_common import *


class Scene9(AwareScene):
    scene_number = 9

    def construct(self):
        heading = title("3D-Aware editing: the representation matters")
        frames = panel("frames\npixels", GREY, 2.35, 1.2).move_to(LEFT * 4.85 + UP * 0.45)
        atlases = panel("layered atlases\nshared appearance", ACCENT, 2.7, 1.2).move_to(LEFT * 1.75 + UP * 0.45)
        codef = panel("CoDeF\nappearance + motion", PURPLE, 2.7, 1.2).move_to(RIGHT * 1.65 + UP * 0.45)
        nerf = panel("dynamic NeRF\n3D geometry", SECONDARY, 2.55, 1.2).move_to(RIGHT * 4.85 + UP * 0.45)
        progression = VGroup(frames, atlases, codef, nerf)
        arrows = VGroup(*[
            edge_arrow(progression[i], progression[i + 1], RIGHT, LEFT, progression[i + 1][0].get_stroke_color())
            for i in range(3)
        ])

        self.play(Write(heading), run_time=1.4)
        self.cue(2.7)
        self.play(FadeIn(frames), run_time=1.6)
        self.cue(8.2)
        self.play(Create(arrows[0]), FadeIn(atlases), run_time=2.0)
        self.cue(13.9)
        self.play(Create(arrows[1]), FadeIn(codef), run_time=2.0)
        self.cue(18.3)
        self.play(Create(arrows[2]), FadeIn(nerf), run_time=2.0)

        questions = VGroup(
            label("repeat identity?", GREY, MIN_SIZE).next_to(frames, DOWN, buff=0.28),
            label("where is appearance?", ACCENT, MIN_SIZE).next_to(atlases, DOWN, buff=0.28),
            label("how does it move?", PURPLE, MIN_SIZE).next_to(codef, DOWN, buff=0.28),
            label("what exists in 3D?", SECONDARY, MIN_SIZE).next_to(nerf, DOWN, buff=0.28),
        )
        self.play(LaggedStart(*[Write(item) for item in questions], lag_ratio=0.25), run_time=3.0)
        self.cue(27.8)
        self.play(
            *[item.animate.set_opacity(0.22) for item in progression[:-1]],
            *[item.animate.set_opacity(0.22) for item in questions[:-1]],
            Indicate(nerf, color=WHITE),
            run_time=2.2,
        )
        close = VGroup(
            label("one edit needs a stable place to live", ACCENT, BODY_SIZE),
            label("that is the idea of 3D-aware video editing", WHITE, SMALL_SIZE),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.28)
        self.cue(30.2)
        self.play(LaggedStart(*[Write(item) for item in close], lag_ratio=0.35), run_time=2.5)
        self.finish_to_audio()
