from section_common import *


class Scene6(MultimodalScene):
    scene_number = 6

    def construct(self):
        heading = title("Sound guidance: control what happens when")
        prompt = pill('"a beautiful beach under a blue sky"', PRIMARY, SMALL_SIZE).move_to(UP * 1.65)
        wave = waveform(8.0, 0.7, ACCENT).move_to(UP * 0.2)
        wave_label = label("audio over time", ACCENT, SMALL_SIZE).next_to(wave, UP, buff=0.2)
        self.play(Write(heading), FadeIn(prompt), run_time=1.8)
        self.play(Create(wave), Write(wave_label), run_time=2.5)
        self.wait(1.2)

        frames = video_strip(7, SECONDARY, 9.0, 1.35).move_to(DOWN * 1.65)
        frame_labels = VGroup()
        for i, frame in enumerate(frames):
            text = "waves" if i < 4 else "fire"
            color = PRIMARY if i < 4 else ERROR
            frame_labels.add(label(text, color, MIN_SIZE).move_to(frame))
        self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.12), run_time=2.2)
        cursor = Line(UP * 0.7, DOWN * 2.4, color=WHITE, stroke_width=3).move_to(frames[0].get_center() + UP * 0.55)
        self.play(FadeIn(cursor), run_time=0.8)
        for i, text in enumerate(frame_labels):
            self.play(cursor.animate.set_x(frames[i].get_x()), FadeIn(text), run_time=1.0)
        self.wait(1.2)

        alignment = label("audio event  <->  visual event", ACCENT, BODY_SIZE).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(cursor), Write(alignment), run_time=2)
        self.play(Indicate(wave, color=WHITE), Indicate(frames, color=WHITE), run_time=2)
        self.finish_to_audio()
