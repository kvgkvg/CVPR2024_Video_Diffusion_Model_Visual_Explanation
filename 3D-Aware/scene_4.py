from section_common import *


class Scene4(AwareScene):
    scene_number = 4

    def construct(self):
        heading = title("CoDeF: appearance + deformation")
        video_coord = pill("(x, y, t)", WHITE, BODY_SIZE).move_to(LEFT * 5.2 + UP * 1.0)
        deformation = panel("deformation\nfield", PURPLE, 2.3, 1.25).move_to(LEFT * 2.15 + UP * 1.0)
        canonical_coord = pill("(x′, y′)", ACCENT, BODY_SIZE).move_to(RIGHT * 0.75 + UP * 1.0)
        canonical = panel("canonical\nfield", PRIMARY, 2.3, 1.25).move_to(RIGHT * 3.4 + UP * 1.0)
        rgb = pill("(r, g, b)", SECONDARY, BODY_SIZE).move_to(RIGHT * 5.7 + UP * 1.0)
        chain = VGroup(video_coord, deformation, canonical_coord, canonical, rgb)
        arrows = VGroup(*[
            edge_arrow(chain[i], chain[i + 1], RIGHT, LEFT, chain[i + 1][0].get_stroke_color())
            for i in range(4)
        ])

        self.play(Write(heading), run_time=1.5)
        self.cue(5.5)
        self.play(FadeIn(video_coord), run_time=1.0)
        self.play(Create(arrows[0]), FadeIn(deformation), run_time=2.0)
        self.cue(11.5)
        self.play(Create(arrows[1]), FadeIn(canonical_coord), run_time=1.8)
        self.cue(15.5)
        self.play(Create(arrows[2]), FadeIn(canonical), run_time=2.0)
        self.cue(19.0)
        self.play(Create(arrows[3]), FadeIn(rgb), run_time=1.8)

        motion = panel("motion over time", PURPLE, 3.0, 0.75, MIN_SIZE).move_to(LEFT * 2.2 + DOWN * 0.55)
        appearance = panel("shared appearance", PRIMARY, 3.0, 0.75, MIN_SIZE).move_to(RIGHT * 3.35 + DOWN * 0.55)
        motion_arrow = edge_arrow(deformation, motion, DOWN, UP, PURPLE)
        appearance_arrow = edge_arrow(canonical, appearance, DOWN, UP, PRIMARY)
        self.cue(22.0)
        self.play(Create(motion_arrow), FadeIn(motion), run_time=1.7)
        self.play(Create(appearance_arrow), FadeIn(appearance), run_time=1.7)

        canonical_image = atlas_grid(PRIMARY, 2.4, 1.35).move_to(LEFT * 0.35 + DOWN * 2.15)
        edit = subject_icon(ERROR, 0.5).move_to(canonical_image)
        frames = frame_strip(4, SECONDARY, 4.4, 1.25).move_to(DOWN * 2.15 + RIGHT * 4.0)
        propagate = edge_arrow(canonical_image, frames, RIGHT, LEFT, SECONDARY)
        self.cue(27.1)
        self.play(FadeOut(motion), FadeOut(appearance), FadeOut(motion_arrow), FadeOut(appearance_arrow), FadeIn(canonical_image), FadeIn(edit), run_time=2.0)
        self.cue(36.6)
        self.play(Create(propagate), LaggedStart(*[FadeIn(frame) for frame in frames], lag_ratio=0.15), run_time=2.8)
        subtle = label("subtle motion survives", ACCENT, SMALL_SIZE).next_to(frames, DOWN, buff=0.18)
        self.cue(40.0)
        self.play(Write(subtle), LaggedStart(*[Indicate(frame, color=ACCENT) for frame in frames], lag_ratio=0.15), run_time=2.4)
        self.finish_to_audio()
