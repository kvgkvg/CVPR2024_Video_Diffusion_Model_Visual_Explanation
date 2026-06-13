from section_common import *


class Scene6(EvalScene):
    scene_number = 6

    def construct(self):
        heading = title("FVD: compare distributions in video feature space")
        self.play(Write(heading), run_time=1.4)
        generated_only = sample_grid(color=TEMPORAL).move_to(UP * 1.2)
        is_label = label("Inception Score sees generated samples alone", QUALITY, BODY_SIZE).next_to(generated_only, DOWN, buff=0.25)
        self.cue(2.0)
        self.play(FadeIn(generated_only), Write(is_label), run_time=1.7)

        real = video_strip(5, QUALITY, 4.5, 0.9).move_to(LEFT * 3.7 + UP * 0.8)
        fake = video_strip(5, TEMPORAL, 4.5, 0.9).move_to(RIGHT * 3.7 + UP * 0.8)
        real_label = label("real videos", QUALITY, SMALL_SIZE).next_to(real, UP, buff=0.18)
        fake_label = label("generated videos", TEMPORAL, SMALL_SIZE).next_to(fake, UP, buff=0.18)
        self.cue(7.0)
        self.play(FadeOut(generated_only), FadeOut(is_label), FadeIn(real), FadeIn(fake), Write(real_label), Write(fake_label), run_time=1.8)
        i3d = panel("I3D\nspace + time features", ALIGNMENT, 3.0, 1.2).move_to(UP * -0.35)
        in_arrows = VGroup(
            anchored_arrow(real.get_edge_center(DOWN), i3d.get_edge_center(LEFT), QUALITY),
            anchored_arrow(fake.get_edge_center(DOWN), i3d.get_edge_center(RIGHT), TEMPORAL),
        )
        self.cue(12.5)
        self.play(Indicate(real, color=QUALITY), run_time=1.1)
        self.cue(15.8)
        self.play(Indicate(fake, color=TEMPORAL), run_time=1.1)
        self.cue(20.0)
        self.play(FadeIn(i3d), Create(in_arrows), run_time=1.8)
        self.cue(24.0)
        self.play(Indicate(i3d, color=ALIGNMENT), run_time=1.2)

        real_dist = distribution(LEFT * 2.5 + DOWN * 2.0, QUALITY, 1.1)
        fake_dist = distribution(RIGHT * 2.2 + DOWN * 2.0, TEMPORAL, 1.25)
        distance = DoubleArrow(real_dist.get_right(), fake_dist.get_left(), color=ALIGNMENT, buff=0.1)
        fvd = label("FVD distance", ALIGNMENT, BODY_SIZE).next_to(distance, UP, buff=0.15)
        self.cue(28.8)
        self.play(FadeIn(real_dist), FadeIn(fake_dist), run_time=1.6)
        self.cue(33.5)
        self.play(Create(distance), Write(fvd), run_time=1.4)
        self.cue(37.0)
        closer_dist = fake_dist.copy().shift(LEFT * 1.2)
        closer_arrow = DoubleArrow(real_dist.get_right(), closer_dist.get_left(), color=ALIGNMENT, buff=0.1)
        closer_label = label("lower FVD", ALIGNMENT, BODY_SIZE).next_to(closer_arrow, UP, buff=0.15)
        self.play(
            Transform(fake_dist, closer_dist),
            ReplacementTransform(distance, closer_arrow),
            ReplacementTransform(fvd, closer_label),
            run_time=2.0,
        )
        blind = VGroup(pill("long-term failure", FAILURE), pill("identity deformation", FAILURE), pill("flicker / sharpness", FAILURE)).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.25)
        self.cue(40.4)
        self.play(FadeOut(real), FadeOut(fake), FadeOut(real_label), FadeOut(fake_label), FadeOut(i3d), FadeOut(in_arrows), FadeOut(real_dist), FadeOut(fake_dist), FadeOut(closer_arrow), FadeOut(closer_label), FadeIn(blind), run_time=2.0)
        self.cue(47.0)
        self.play(Indicate(blind, color=WHITE), run_time=1.5)
        self.finish_to_audio()
