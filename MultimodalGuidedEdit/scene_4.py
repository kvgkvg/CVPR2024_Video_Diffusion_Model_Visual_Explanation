from section_common import *


class Scene4(GuidedScene):
    scene_number = 4

    def construct(self):
        heading = title("Audio is a temporal control signal")
        self.play(Write(heading), run_time=1.4)
        wave = waveform(9.0, 1.0, AUDIO).move_to(UP * 1.45)
        clock = timeline(9, TIME, 9.0).move_to(UP * 0.55)
        self.cue(3.0)
        self.play(Create(wave), run_time=2.0)
        self.cue(4.9)
        self.play(Create(clock), run_time=1.5)

        identity = panel("identity frame", APPEARANCE, 2.5, 1.1).move_to(LEFT * 4.5 + DOWN * 1.0)
        noisy = panel("noisy frame", PRIMARY, 2.5, 1.1).move_to(LEFT * 1.5 + DOWN * 1.0)
        model = panel("audio-conditioned\ndiffusion", AUDIO, 2.8, 1.3).move_to(RIGHT * 1.65 + DOWN * 1.0)
        face = Circle(radius=0.6, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.08).move_to(RIGHT * 4.8 + DOWN * 1.0)
        mouth = Arc(radius=0.22, start_angle=PI, angle=PI, color=ERROR, stroke_width=5).move_to(face.get_center() + DOWN * 0.18)
        face_group = VGroup(face, mouth)
        flow = VGroup(
            edge_arrow(identity, noisy, RIGHT, LEFT, APPEARANCE),
            edge_arrow(noisy, model, RIGHT, LEFT, PRIMARY),
            edge_arrow(model, face_group, RIGHT, LEFT, SECONDARY),
        )
        self.cue(7.4)
        self.play(FadeIn(identity), run_time=1.2)
        self.cue(13.9)
        self.play(FadeIn(noisy), FadeIn(model), Create(flow[0]), Create(flow[1]), run_time=1.8)
        self.cue(20.4)
        self.play(Create(flow[2]), FadeIn(face_group), run_time=1.5)
        self.cue(22.4)
        self.play(mouth.animate.stretch(1.8, 1), run_time=0.7)
        self.play(mouth.animate.stretch(0.55, 1), run_time=0.7)

        events = VGroup(
            pill("step", AUDIO),
            pill("impact", AUDIO),
            pill("water", AUDIO),
            pill("fire", AUDIO),
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 2.45)
        self.cue(26.6)
        self.play(FadeOut(identity), FadeOut(noisy), FadeOut(model), FadeOut(face_group), FadeOut(flow), FadeIn(events), run_time=2.0)
        event_marks = VGroup(*[
            DashedLine(event.get_edge_center(UP), clock[0].point_from_proportion(p), color=AUDIO, dash_length=0.08)
            for event, p in zip(events, (0.18, 0.42, 0.66, 0.86))
        ])
        self.cue(31.2)
        self.play(LaggedStart(*[Create(mark) for mark in event_marks], lag_ratio=0.2), run_time=2.0)
        self.cue(38.7)
        pulse = Dot(clock[0].get_start(), color=ACCENT, radius=0.1)
        self.add(pulse)
        self.play(MoveAlongPath(pulse, clock[0]), run_time=3.2, rate_func=linear)
        self.finish_to_audio()
