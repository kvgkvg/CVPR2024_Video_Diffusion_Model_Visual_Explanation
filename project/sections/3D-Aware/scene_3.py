from section_common import *


class Scene3(AwareScene):
    scene_number = 3

    def construct(self):
        heading = title("Atlas editing with diffusion")
        keyframes = panel("selected\nkeyframes", PRIMARY, 2.0, 1.25).move_to(LEFT * 5.0 + UP * 0.8)
        diffusion = panel("diffusion\nediting", PURPLE, 2.0, 1.25).move_to(LEFT * 2.25 + UP * 0.8)
        atlases = panel("aggregate into\nshared atlases", ACCENT, 2.35, 1.25).move_to(RIGHT * 0.8 + UP * 0.8)
        video = panel("consistent\nvideo", SECONDARY, 2.0, 1.25).move_to(RIGHT * 4.35 + UP * 0.8)
        chain = VGroup(keyframes, diffusion, atlases, video)
        arrows = VGroup(*[
            edge_arrow(chain[i], chain[i + 1], RIGHT, LEFT, chain[i + 1][0].get_stroke_color())
            for i in range(3)
        ])

        self.play(Write(heading), run_time=1.4)
        self.cue(5.5)
        self.play(FadeIn(keyframes), run_time=1.2)
        self.play(Create(arrows[0]), FadeIn(diffusion), run_time=1.8)
        self.play(Indicate(diffusion, color=WHITE), run_time=1.5)
        self.cue(9.8)
        self.play(Create(arrows[1]), FadeIn(atlases), run_time=1.8)
        self.cue(14.0)
        self.play(Create(arrows[2]), FadeIn(video), run_time=1.8)

        stable = label("shared appearance across time", SECONDARY, BODY_SIZE).next_to(chain, DOWN, buff=0.5)
        self.cue(18.9)
        self.play(Write(stable), Indicate(video, color=WHITE), run_time=1.8)

        flat = atlas_grid(ACCENT, 4.2, 2.0).move_to(DOWN * 1.55)
        warped = flat.copy()
        warped.apply_function(
            lambda p: p
            + np.array([
                0.28 * np.sin(2.2 * p[1]) + 0.18 * p[1],
                0.08 * np.sin(3 * p[0]),
                0,
            ])
        )
        flat_label = label("a flat 2D atlas", ACCENT, SMALL_SIZE).next_to(flat, DOWN, buff=0.18)
        self.cue(29.0)
        self.play(FadeOut(stable), FadeOut(chain), FadeOut(arrows), FadeIn(flat), Write(flat_label), run_time=2.0)
        self.play(Transform(flat, warped), run_time=2.2)
        limits = VGroup(
            label("non-rigid detail is compressed", ERROR, SMALL_SIZE),
            label("hidden surfaces do not exist", ERROR, SMALL_SIZE),
        ).arrange(DOWN, buff=0.25).next_to(flat, RIGHT, buff=0.45)
        self.cue(34.6)
        self.play(LaggedStart(*[Write(item) for item in limits], lag_ratio=0.35), run_time=2.4)
        self.cue(37.7)
        self.play(Indicate(flat, color=ERROR), run_time=1.6)
        self.finish_to_audio()
