from section_common import *


class Scene8(AwareScene):
    scene_number = 8

    def construct(self):
        heading = title("What does each representation know?")
        frames = frame_strip(4, GREY, 2.7, 1.25).move_to(LEFT * 4.75 + UP * 0.65)
        frame_name = label("independent frames", GREY, SMALL_SIZE).next_to(frames, UP, buff=0.2)
        visible = label("visible pixels only", ERROR, MIN_SIZE).next_to(frames, DOWN, buff=0.22)

        atlas = atlas_grid(ACCENT, 2.6, 1.65).move_to(LEFT * 1.55 + UP * 0.65)
        atlas_name = label("layered atlas", ACCENT, SMALL_SIZE).next_to(atlas, UP, buff=0.2)
        flat = label("shared, but flat", ACCENT, MIN_SIZE).next_to(atlas, DOWN, buff=0.22)

        codef = atlas_grid(PURPLE, 2.6, 1.65).move_to(RIGHT * 1.55 + UP * 0.65)
        warp = VGroup(*[
            Arrow(codef.get_left() + UP * y, codef.get_right() + UP * (y + 0.15 * np.sin(y * 5)), color=PURPLE, buff=0.1, stroke_width=2)
            for y in np.linspace(-0.5, 0.5, 4)
        ])
        codef_group = Group(codef, warp)
        codef_name = label("CoDeF", PURPLE, SMALL_SIZE).next_to(codef, UP, buff=0.2)
        temporal = label("robust deformation", PURPLE, MIN_SIZE).next_to(codef, DOWN, buff=0.22)

        nerf = pseudo_volume(SECONDARY, 2.5, 1.7, 0.5).move_to(RIGHT * 4.65 + UP * 0.65)
        nerf_name = label("dynamic NeRF", SECONDARY, SMALL_SIZE).next_to(nerf, UP, buff=0.2)
        geometry = label("3D + view dependence", SECONDARY, MIN_SIZE).next_to(nerf, DOWN, buff=0.22)

        groups = [Group(frames, frame_name, visible), Group(atlas, atlas_name, flat), Group(codef_group, codef_name, temporal), Group(nerf, nerf_name, geometry)]
        self.play(Write(heading), run_time=1.4)
        self.play(FadeIn(groups[0]), run_time=1.8)
        self.cue(7.9)
        self.play(FadeIn(groups[1]), run_time=1.8)
        self.cue(14.0)
        self.play(FadeIn(groups[2]), run_time=1.8)
        self.cue(23.1)
        self.play(FadeIn(groups[3]), run_time=1.8)

        hidden = VGroup(
            DashedLine(atlas.get_right(), atlas.get_right() + RIGHT * 0.5, color=ERROR),
            label("?", ERROR, BODY_SIZE).next_to(atlas, RIGHT, buff=0.35),
        )
        self.play(Indicate(frames, color=ERROR), Indicate(atlas, color=ERROR), FadeIn(hidden), run_time=2.2)
        self.play(Indicate(codef_group, color=WHITE), run_time=1.8)
        self.play(
            *[group.animate.set_opacity(0.2) for group in groups[:-1]],
            FadeOut(hidden),
            Indicate(nerf, color=WHITE),
            run_time=2.3,
        )
        tradeoff = VGroup(
            label("stronger view consistency", SECONDARY, BODY_SIZE),
            label("more complex reconstruction", GREY, SMALL_SIZE),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.25)
        self.cue(35.3)
        self.play(LaggedStart(*[Write(item) for item in tradeoff], lag_ratio=0.35), run_time=2.3)
        self.finish_to_audio()
