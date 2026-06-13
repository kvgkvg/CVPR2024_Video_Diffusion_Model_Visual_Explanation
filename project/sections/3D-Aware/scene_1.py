from section_common import *


class Scene1(AwareScene):
    scene_number = 1

    def construct(self):
        heading = title("Why should an edit understand geometry?")
        frames = frame_strip(5, PRIMARY, 8.6, 1.8).move_to(UP * 0.55)
        subjects = VGroup()
        for index, frame in enumerate(frames):
            person = subject_icon(ACCENT, 0.55 + 0.08 * (index % 3))
            person.move_to(frame)
            person.rotate((-0.12 + 0.06 * index))
            subjects.add(person)

        self.play(Write(heading), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(frame) for frame in frames], lag_ratio=0.15), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(person) for person in subjects], lag_ratio=0.16), run_time=1.8)

        per_frame = label("five convincing images", WHITE, SMALL_SIZE).next_to(frames, DOWN, buff=0.3)
        self.play(Write(per_frame), run_time=1.0)

        drift_colors = [ACCENT, ERROR, SECONDARY, PURPLE, PRIMARY]
        self.cue(6.2)
        self.play(
            *[person.animate.set_color(color) for person, color in zip(subjects, drift_colors)],
            run_time=1.8,
        )
        warnings = VGroup(
            label("identity drift", ERROR, SMALL_SIZE),
            label("flicker", ERROR, SMALL_SIZE),
            label("viewpoint failure", ERROR, SMALL_SIZE),
        ).arrange(RIGHT, buff=0.75).next_to(frames, DOWN, buff=0.3)
        self.play(ReplacementTransform(per_frame, warnings), run_time=1.5)
        self.cue(14.2)
        self.play(LaggedStart(*[Indicate(person, color=ERROR) for person in subjects], lag_ratio=0.12), run_time=2.2)

        shared = panel("shared scene\nrepresentation", SECONDARY, 3.0, 1.25).move_to(DOWN * 2.05)
        target_x = np.linspace(-1.0, 1.0, len(frames))
        arrows = VGroup(*[
            anchored_arrow(
                shared.get_edge_center(UP) + RIGHT * x,
                frame.get_edge_center(DOWN),
                SECONDARY,
            )
            for frame, x in zip(frames, target_x)
        ])
        self.cue(23.0)
        self.play(FadeOut(warnings), FadeIn(shared), run_time=1.4)
        self.play(LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.13), run_time=2.5)
        self.play(*[person.animate.set_color(SECONDARY) for person in subjects], run_time=2.0)
        question = label("one object, across time and viewpoint", ACCENT, BODY_SIZE).to_edge(DOWN, buff=0.25)
        self.cue(31.0)
        self.play(Write(question), Indicate(shared, color=WHITE), run_time=2.0)
        self.finish_to_audio()
