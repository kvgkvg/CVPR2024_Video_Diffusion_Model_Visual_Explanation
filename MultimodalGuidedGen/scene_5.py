from section_common import *


class Scene5(MultimodalScene):
    scene_number = 5

    def construct(self):
        heading = title("CameraCtrl: represent the rays, not just the pose")
        camera = simple_camera(PURPLE).move_to(LEFT * 4.8 + UP * 0.8)
        image_plane = Rectangle(width=2.4, height=2.0, color=PRIMARY).move_to(LEFT * 1.8 + UP * 0.8)
        rays = VGroup()
        for y in [-0.75, -0.25, 0.25, 0.75]:
            endpoint = image_plane.get_center() + UP * y + RIGHT * 1.2
            rays.add(Line(camera.get_right(), endpoint, color=PURPLE, stroke_width=2))
        self.play(Write(heading), FadeIn(camera), FadeIn(image_plane), run_time=2)
        self.play(LaggedStart(*[Create(ray) for ray in rays], lag_ratio=0.2), run_time=2.5)
        self.wait(1.2)

        pose = pill("raw pose: R, T", GREY).move_to(RIGHT * 2.1 + UP * 1.65)
        plucker = panel("6D Plucker\nray embedding", ACCENT, 2.8, 1.2).move_to(RIGHT * 2.1 + UP * 0.25)
        temporal = panel("temporal layers", PRIMARY, 2.8, 1.0).move_to(RIGHT * 5.0 + UP * 0.25)
        ray_link = edge_arrow(image_plane, plucker, RIGHT, LEFT, ACCENT)
        temporal_link = edge_arrow(plucker, temporal, RIGHT, LEFT, PRIMARY)
        self.play(FadeIn(pose), run_time=1.5)
        self.play(Create(ray_link), FadeIn(plucker), FadeOut(pose), run_time=2.4)
        self.play(Create(temporal_link), FadeIn(temporal), run_time=2)
        self.wait(1.2)

        path = VMobject(color=ACCENT, stroke_width=4).set_points_smoothly([
            LEFT * 5.5 + DOWN * 1.5, LEFT * 2.5 + DOWN * 2.3, RIGHT * 0.7 + DOWN * 1.6
        ])
        self.play(
            FadeOut(image_plane, rays, plucker, temporal, ray_link, temporal_link),
            Create(path),
            camera.animate.move_to(path.get_start()).scale(0.7),
            run_time=2,
        )
        self.play(MoveAlongPath(camera, path), run_time=3)
        result = framed_image(asset("cameractrl_results.png", width=9.3), PRIMARY).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(path, camera), FadeIn(result), run_time=2.5)
        self.finish_to_audio()
