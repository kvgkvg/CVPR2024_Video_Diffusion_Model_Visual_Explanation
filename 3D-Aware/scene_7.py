from section_common import *


class Scene7(AwareScene):
    scene_number = 7

    def construct(self):
        heading = title("The payoff: free viewpoints")
        volume = pseudo_volume(SECONDARY, 3.4, 2.45, 0.65).move_to(UP * 0.45)
        person = subject_icon(ACCENT, 0.8).move_to(volume)
        scene = Group(volume, person)
        camera = camera_icon(PURPLE).move_to(LEFT * 5.0 + UP * 1.2)
        path = ArcBetweenPoints(LEFT * 5.0 + UP * 1.2, RIGHT * 5.0 + UP * 1.2, angle=-PI / 3, color=PURPLE, stroke_width=3)
        rays = always_redraw(lambda: VGroup(
            Line(camera.get_right(), volume.get_corner(UL), color=PURPLE, stroke_opacity=0.5),
            Line(camera.get_right(), volume.get_corner(DL), color=PURPLE, stroke_opacity=0.5),
        )
        )
        self.play(Write(heading), FadeIn(scene), run_time=2.0)
        self.cue(3.6)
        self.play(FadeIn(camera), Create(rays), run_time=1.7)
        self.play(Create(path), run_time=1.5)
        self.cue(9.0)
        self.play(MoveAlongPath(camera, path), run_time=4.0, rate_func=smooth)
        self.play(Indicate(scene, color=WHITE), run_time=1.5)
        free = label("new camera path, same coherent edit", SECONDARY, BODY_SIZE).next_to(scene, DOWN, buff=0.35)
        self.play(Write(free), run_time=1.7)
        rays_label = label("camera rays query the same edited field", PURPLE, SMALL_SIZE).to_edge(DOWN, buff=0.28)
        self.cue(18.7)
        self.play(Write(rays_label), Indicate(scene, color=WHITE), run_time=2.2)
        self.play(MoveAlongPath(camera, path.copy().reverse_points()), run_time=4.0, rate_func=smooth)
        editable = label("an editable scene, not a stack of pictures", ACCENT, BODY_SIZE).to_edge(DOWN, buff=0.28)
        self.cue(25.7)
        self.play(ReplacementTransform(rays_label, editable), run_time=1.8)
        self.finish_to_audio()
