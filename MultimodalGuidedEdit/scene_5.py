from section_common import *


class Scene5(GuidedScene):
    scene_number = 5

    def construct(self):
        heading = title("Separate appearance from motion")
        self.play(Write(heading), run_time=1.4)

        reference_box = RoundedRectangle(
            width=3.0, height=1.75, corner_radius=0.16,
            color=APPEARANCE, fill_color=APPEARANCE, fill_opacity=0.08,
        ).move_to(LEFT * 4.2 + UP * 0.75)
        reference_person = person_icon(APPEARANCE, 0.67).move_to(reference_box)
        reference_label = label("reference image", APPEARANCE, SMALL_SIZE).next_to(reference_box, UP, buff=0.15)
        identity_note = label("identity + clothing + texture", APPEARANCE, MIN_SIZE).next_to(reference_box, DOWN, buff=0.15)
        reference = VGroup(reference_box, reference_person, reference_label, identity_note)

        poses = VGroup(*[
            person_icon(MOTION, 0.36, angle)
            for angle in (-0.5, -0.2, 0.15, 0.45, 0.1)
        ]).arrange(RIGHT, buff=0.18)
        pose_box = RoundedRectangle(
            width=3.5, height=1.75, corner_radius=0.16,
            color=MOTION, fill_color=MOTION, fill_opacity=0.08,
        ).move_to(RIGHT * 4.0 + UP * 0.75)
        poses.move_to(pose_box)
        pose_label = label("pose sequence", MOTION, SMALL_SIZE).next_to(pose_box, UP, buff=0.15)
        motion_note = label("changing skeletal structure", MOTION, MIN_SIZE).next_to(pose_box, DOWN, buff=0.15)
        pose_group = VGroup(pose_box, poses, pose_label, motion_note)

        model = panel("DreamPose", PRIMARY, 2.7, 1.05, BODY_SIZE).move_to(DOWN * 0.75)
        arrows = VGroup(
            anchored_arrow(reference_box.get_edge_center(RIGHT), model.get_edge_center(LEFT), APPEARANCE),
            anchored_arrow(pose_box.get_edge_center(LEFT), model.get_edge_center(RIGHT), MOTION),
        )
        self.cue(3.5)
        self.play(FadeIn(reference_box), FadeIn(reference_person), Write(reference_label), run_time=1.5)
        self.cue(7.9)
        self.play(FadeIn(pose_box), FadeIn(poses), Write(pose_label), run_time=1.8)
        self.cue(11.6)
        self.play(FadeIn(model), Create(arrows), run_time=1.8)
        self.cue(15.0)
        self.play(Write(identity_note), Write(motion_note), run_time=1.5)

        output = frame_strip(6, SECONDARY, 6.4, 1.0).to_edge(DOWN, buff=0.25)
        out_arrow = edge_arrow(model, output, DOWN, UP, SECONDARY)
        stable_people = VGroup(*[
            person_icon(APPEARANCE, 0.29, angle).move_to(frame)
            for frame, angle in zip(output, (-0.45, -0.2, 0.05, 0.3, 0.48, 0.15))
        ])
        self.cue(17.0)
        self.play(Create(out_arrow), FadeIn(output), run_time=1.5)
        self.cue(21.0)
        self.play(LaggedStart(*[FadeIn(person) for person in stable_people], lag_ratio=0.14), run_time=1.8)

        analysis_label = label("naive frame-by-frame generation", ERROR, BODY_SIZE).move_to(UP * 1.55)
        bad_people = VGroup(*[
            person_icon(ERROR if i % 2 else APPEARANCE, 0.25 + 0.025 * (i % 3), -0.4 + i * 0.18).move_to(frame)
            for i, frame in enumerate(output)
        ])
        self.cue(24.7)
        self.play(
            FadeOut(reference), FadeOut(pose_group), FadeOut(model), FadeOut(arrows), FadeOut(out_arrow),
            FadeOut(stable_people), output.animate.move_to(UP * 0.25), Write(analysis_label),
            run_time=2.0,
        )
        bad_people.move_to(output)
        self.play(FadeIn(bad_people), run_time=1.0)

        problems = VGroup(
            pill("flicker", ERROR),
            pill("background drift", ERROR),
            pill("identity drift", ERROR),
        ).arrange(RIGHT, buff=0.65).move_to(DOWN * 1.25)
        self.cue(28.6)
        self.play(LaggedStart(*[FadeIn(problem) for problem in problems], lag_ratio=0.25), run_time=1.8)

        links = attention_links(output, SECONDARY)
        consistent = VGroup(*[
            person_icon(APPEARANCE, 0.28, angle).move_to(frame)
            for frame, angle in zip(output, (-0.45, -0.2, 0.05, 0.3, 0.48, 0.15))
        ])
        consistency_label = label("same appearance, changing pose", SECONDARY, SECTION_SIZE).move_to(DOWN * 1.25)
        self.cue(34.4)
        self.play(FadeOut(bad_people), FadeOut(problems), FadeIn(consistent), Create(links), ReplacementTransform(analysis_label, consistency_label), run_time=2.2)
        self.cue(38.6)
        self.play(Indicate(VGroup(output, consistent, links), color=WHITE), run_time=2.0)
        self.finish_to_audio()
