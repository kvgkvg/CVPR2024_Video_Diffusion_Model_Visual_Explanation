from section_common import *


class Scene5(AwareScene):
    scene_number = 5

    def construct(self):
        heading = title("Lift image tools into video")
        tools = VGroup(
            panel("ControlNet", ACCENT, 2.0, 0.8, MIN_SIZE),
            panel("Real-ESRGAN", PRIMARY, 2.0, 0.8, MIN_SIZE),
            panel("SAM", PURPLE, 2.0, 0.8, MIN_SIZE),
        ).arrange(DOWN, buff=0.38).move_to(LEFT * 5.0)
        canonical = panel("canonical\nimage", PRIMARY, 2.0, 1.4).move_to(LEFT * 1.8)
        deformation = panel("learned\ndeformation", PURPLE, 2.0, 1.4).move_to(RIGHT * 1.25)
        frames = frame_strip(4, SECONDARY, 2.8, 1.25).move_to(RIGHT * 4.8)

        tool_targets = np.linspace(0.35, -0.35, len(tools))
        tool_arrows = VGroup(*[
            anchored_arrow(
                tool.get_edge_center(RIGHT),
                canonical.get_edge_center(LEFT) + UP * y,
                tool[0].get_stroke_color(),
            )
            for tool, y in zip(tools, tool_targets)
        ])
        canonical_arrow = edge_arrow(canonical, deformation, RIGHT, LEFT, PURPLE)
        output_arrow = edge_arrow(deformation, frames, RIGHT, LEFT, SECONDARY)

        self.play(Write(heading), run_time=1.3)
        self.cue(7.1)
        self.play(FadeIn(tools[0]), run_time=1.0)
        self.play(FadeIn(tools[1]), run_time=1.0)
        self.cue(12.0)
        self.play(FadeIn(tools[2]), run_time=1.0)
        self.play(FadeIn(canonical), LaggedStart(*[Create(arrow) for arrow in tool_arrows], lag_ratio=0.22), run_time=2.5)
        self.cue(16.0)
        self.play(Create(canonical_arrow), FadeIn(deformation), run_time=2.0)
        self.cue(18.4)
        self.play(Create(output_arrow), LaggedStart(*[FadeIn(frame) for frame in frames], lag_ratio=0.16), run_time=2.4)

        once = label("change semantics once", ACCENT, SMALL_SIZE).next_to(canonical, DOWN, buff=0.28)
        across = label("preserve location over time", SECONDARY, SMALL_SIZE).next_to(frames, DOWN, buff=0.28)
        self.cue(26.8)
        self.play(Indicate(deformation, color=WHITE), run_time=1.6)
        self.cue(32.5)
        self.play(Write(once), Indicate(canonical, color=WHITE), run_time=1.8)
        self.play(Write(across), Indicate(deformation, color=WHITE), run_time=1.8)
        self.play(LaggedStart(*[Indicate(frame, color=SECONDARY) for frame in frames], lag_ratio=0.15), run_time=2.2)
        principle = label("appearance and motion are separated", WHITE, BODY_SIZE).to_edge(DOWN, buff=0.25)
        self.play(Write(principle), run_time=1.5)
        self.finish_to_audio()
