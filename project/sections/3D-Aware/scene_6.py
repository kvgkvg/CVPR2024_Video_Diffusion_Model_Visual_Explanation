from section_common import *


class Scene6(AwareScene):
    scene_number = 6

    def construct(self):
        heading = title("DynVideo-E: move the representation into 3D")
        flat = atlas_grid(PRIMARY, 3.0, 2.0).move_to(LEFT * 3.8 + UP * 0.8)
        flat_label = label("2D canonical image", PRIMARY, SMALL_SIZE).next_to(flat, DOWN, buff=0.2)
        hidden = DashedLine(flat.get_right(), flat.get_right() + RIGHT * 1.2, color=ERROR)
        hidden_label = label("no hidden surface", ERROR, SMALL_SIZE).next_to(hidden, DOWN, buff=0.15)
        self.play(Write(heading), run_time=1.4)
        self.cue(2.3)
        self.play(FadeIn(flat), Write(flat_label), run_time=1.8)
        self.cue(5.6)
        self.play(flat.animate.stretch(0.2, 0), run_time=2.2)
        self.cue(8.8)
        self.play(Create(hidden), Write(hidden_label), run_time=1.8)

        volume = pseudo_volume(SECONDARY, 2.8, 2.0, 0.55).move_to(RIGHT * 3.45 + UP * 0.8)
        volume_label = label("dynamic NeRF", SECONDARY, BODY_SIZE).next_to(volume, DOWN, buff=0.25)
        pivot_arrow = anchored_arrow(flat.get_edge_center(RIGHT), volume.get_edge_center(LEFT), ACCENT)
        self.cue(14.0)
        self.play(Create(pivot_arrow), FadeIn(volume), Write(volume_label), run_time=2.5)

        top_volume = volume.copy().move_to(UP * 1.2)
        top_label = label("dynamic NeRF", SECONDARY, BODY_SIZE).next_to(top_volume, UP, buff=0.22)
        self.cue(16.1)
        self.play(
            FadeOut(flat), FadeOut(flat_label), FadeOut(hidden), FadeOut(hidden_label), FadeOut(pivot_arrow),
            Transform(volume, top_volume), ReplacementTransform(volume_label, top_label),
            run_time=2.0,
        )
        background = panel("background\nNeRF", PRIMARY, 2.3, 1.15).move_to(LEFT * 4.2 + DOWN * 1.55)
        human = panel("human\nNeRF", ACCENT, 2.3, 1.15).move_to(DOWN * 1.55)
        deform = panel("deformation\nfield", PURPLE, 2.3, 1.15).move_to(RIGHT * 4.2 + DOWN * 1.55)
        components = VGroup(background, human, deform)
        target_x = np.linspace(-0.75, 0.75, 3)
        arrows = VGroup(*[
            anchored_arrow(component.get_edge_center(UP), top_volume.get_edge_center(DOWN) + RIGHT * x, component[0].get_stroke_color())
            for component, x in zip(components, target_x)
        ])
        self.cue(21.5)
        self.play(LaggedStart(*[FadeIn(component) for component in components], lag_ratio=0.25), run_time=2.4)
        self.play(LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.2), run_time=2.2)
        self.cue(28.0)
        self.play(Indicate(background, color=WHITE), Indicate(human, color=WHITE), run_time=2.0)
        self.cue(33.8)
        self.play(Indicate(deform, color=WHITE), Indicate(volume, color=WHITE), run_time=2.0)
        note = label("independent edits, coherent 3D rendering", SECONDARY, BODY_SIZE).to_edge(DOWN, buff=0.2)
        self.cue(40.6)
        self.play(Write(note), run_time=1.6)
        self.finish_to_audio()
