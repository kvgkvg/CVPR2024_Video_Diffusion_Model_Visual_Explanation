from section_common import *


class Scene6(GuidedScene):
    scene_number = 6

    def construct(self):
        heading = title("MagicAnimate: three cooperating pathways")
        self.play(Write(heading), run_time=1.4)
        appearance = panel("appearance encoder\nidentity + background", APPEARANCE, 3.25, 1.25).move_to(LEFT * 4.5 + UP * 1.4)
        pose = panel("Pose ControlNet\nDensePose sequence", MOTION, 3.25, 1.25).move_to(LEFT * 4.5 + DOWN * 0.25)
        temporal = panel("temporal attention\ncross-frame links", TIME, 3.25, 1.25).move_to(LEFT * 4.5 + DOWN * 1.9)
        model = panel("video diffusion", PRIMARY, 3.0, 1.55, BODY_SIZE).move_to(RIGHT * 0.25 + DOWN * 0.25)
        targets = (model.get_edge_center(LEFT) + UP * 0.48, model.get_edge_center(LEFT), model.get_edge_center(LEFT) + DOWN * 0.48)
        arrows = VGroup(*[
            anchored_arrow(source.get_edge_center(RIGHT), target, color)
            for source, target, color in zip((appearance, pose, temporal), targets, (APPEARANCE, MOTION, TIME))
        ])
        self.cue(5.8)
        self.play(FadeIn(appearance), Create(arrows[0]), run_time=1.6)
        self.cue(11.8)
        self.play(FadeIn(pose), Create(arrows[1]), run_time=1.6)
        self.cue(19.7)
        self.play(FadeIn(temporal), Create(arrows[2]), run_time=1.6)
        self.cue(23.5)
        self.play(FadeIn(model), run_time=1.3)

        output = frame_strip(6, SECONDARY, 3.7, 2.0).move_to(RIGHT * 4.35 + DOWN * 0.25)
        output_people = VGroup(*[
            person_icon(APPEARANCE, 0.28, angle).move_to(frame)
            for frame, angle in zip(output, (-0.4, -0.2, 0.0, 0.25, 0.45, 0.15))
        ])
        out_arrow = edge_arrow(model, output, RIGHT, LEFT, SECONDARY)
        self.cue(27.5)
        self.play(Create(out_arrow), FadeIn(output), run_time=1.6)
        self.cue(31.3)
        self.play(LaggedStart(*[FadeIn(person) for person in output_people], lag_ratio=0.16), run_time=2.0)

        stable = VGroup(
            pill("what stays stable", APPEARANCE),
            pill("what changes", MOTION),
            pill("how it stays coherent", TIME),
        ).arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.25)
        self.cue(28.9)
        self.play(FadeIn(stable[0]), run_time=1.0)
        self.cue(31.4)
        self.play(FadeIn(stable[1]), run_time=1.0)
        self.cue(34.2)
        self.play(FadeIn(stable[2]), run_time=1.0)
        self.cue(39.7)
        self.play(Indicate(output_people, color=WHITE), run_time=1.8)
        self.cue(44.2)
        self.play(Indicate(model, color=ACCENT), run_time=2.0)
        self.finish_to_audio()
