from section_common import *


class Scene0(AwareScene):
    scene_number = 0
    intro_pause = 0.5

    def construct(self):
        self.start_scene()
        heading = label("3D-Aware Video Editing", PRIMARY, 58, weight=BOLD).move_to(UP * 2.45)
        question = label(
            "Where should an edit live?",
            ACCENT,
            BODY_SIZE,
        ).move_to(UP * 1.45)
        self.play(Write(heading), run_time=1.6)
        self.cue(3.5)
        self.play(Write(question), run_time=1.3)

        atlas = atlas_grid(ACCENT, 2.5, 1.65).move_to(LEFT * 4.2 + DOWN * 0.45)
        atlas_name = label("Layered Atlas", ACCENT, SMALL_SIZE).next_to(atlas, DOWN, buff=0.22)

        canonical = atlas_grid(PURPLE, 2.2, 1.45).move_to(DOWN * 0.45)
        deformation = VGroup(*[
            Arrow(
                canonical.get_left() + UP * y,
                canonical.get_right() + UP * (y + 0.12 * np.sin(4 * y)),
                color=PURPLE,
                stroke_width=2.5,
                buff=0.08,
                max_tip_length_to_length_ratio=0.08,
            )
            for y in np.linspace(-0.48, 0.48, 4)
        ])
        codef = Group(canonical, deformation)
        codef_name = label("CoDeF", PURPLE, SMALL_SIZE).next_to(canonical, DOWN, buff=0.22)

        nerf = pseudo_volume(SECONDARY, 2.5, 1.8, 0.5).move_to(RIGHT * 4.15 + DOWN * 0.45)
        person = subject_icon(ACCENT, 0.58).move_to(nerf)
        nerf_group = Group(nerf, person)
        nerf_name = label("Dynamic NeRF", SECONDARY, SMALL_SIZE).next_to(nerf, DOWN, buff=0.22)

        concepts = VGroup(atlas, canonical, nerf)
        arrows = VGroup(
            edge_arrow(atlas, canonical, RIGHT, LEFT, PURPLE),
            edge_arrow(canonical, nerf, RIGHT, LEFT, SECONDARY),
        )
        self.cue(18.6)
        self.play(FadeIn(atlas), Write(atlas_name), run_time=1.8)
        self.cue(25.0)
        self.play(Create(arrows[0]), FadeIn(codef), Write(codef_name), run_time=2.2)
        self.cue(27.5)
        self.play(Create(arrows[1]), FadeIn(nerf_group), Write(nerf_name), run_time=2.2)

        dimensions = VGroup(
            label("shared appearance", ACCENT, MIN_SIZE).next_to(atlas_name, DOWN, buff=0.18),
            label("+ deformation", PURPLE, MIN_SIZE).next_to(codef_name, DOWN, buff=0.18),
            label("+ 3D geometry", SECONDARY, MIN_SIZE).next_to(nerf_name, DOWN, buff=0.18),
        )
        self.play(LaggedStart(*[Write(item) for item in dimensions], lag_ratio=0.3), run_time=2.4)
        self.cue(32.6)
        self.play(
            *[obj.animate.set_opacity(0.25) for obj in [atlas, atlas_name, codef, codef_name]],
            Indicate(nerf_group, color=WHITE),
            run_time=2.0,
        )
        self.finish_to_audio()
