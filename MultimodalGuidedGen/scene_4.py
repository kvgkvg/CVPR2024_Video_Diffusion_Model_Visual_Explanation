from section_common import *


class Scene4(MultimodalScene):
    scene_number = 4

    def construct(self):
        heading = title("MotionCtrl: separate camera and object motion")
        model = model_block("pretrained\nvideo model", PRIMARY, 2.6, 1.35)
        camera = simple_camera(PURPLE).move_to(LEFT * 4.7 + UP * 1.35)
        camera_path = VMobject(color=PURPLE, stroke_width=4).set_points_smoothly([
            LEFT * 5.7 + UP * 1.9, LEFT * 4.7 + UP * 2.45, LEFT * 3.5 + UP * 1.85
        ])
        object_dot = Dot(LEFT * 4.7 + DOWN * 1.25, color=SECONDARY, radius=0.16)
        object_path = VMobject(color=SECONDARY, stroke_width=4).set_points_smoothly([
            LEFT * 5.7 + DOWN * 1.25, LEFT * 4.6 + DOWN * 0.65, LEFT * 3.5 + DOWN * 1.35
        ])
        camera_module = panel("camera control", PURPLE, 2.35, 0.85).move_to(RIGHT * 3.9 + UP * 1.35)
        object_module = panel("object adapter", SECONDARY, 2.35, 0.85).move_to(RIGHT * 3.9 + DOWN * 1.25)
        camera_links = VGroup(
            edge_arrow(camera, camera_module, RIGHT, LEFT, PURPLE),
            edge_arrow(camera_module, model, LEFT, RIGHT, PURPLE),
        )
        object_links = VGroup(
            edge_arrow(object_dot, object_module, RIGHT, LEFT, SECONDARY),
            edge_arrow(object_module, model, LEFT, RIGHT, SECONDARY),
        )
        self.play(Write(heading), FadeIn(model), run_time=1.8)
        self.play(Create(camera_path), FadeIn(camera), run_time=2)
        self.play(Create(object_path), FadeIn(object_dot), run_time=2)
        self.wait(1.2)
        self.play(FadeIn(camera_module), Create(camera_links), run_time=2.5)
        self.play(FadeIn(object_module), Create(object_links), run_time=2.5)
        self.wait(1.2)
        self.play(FadeOut(camera_links, object_links), run_time=0.8)
        self.play(MoveAlongPath(camera, camera_path), MoveAlongPath(object_dot, object_path), run_time=4)
        result = framed_image(asset("motionctrl_results.png", width=9.4), SECONDARY).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(camera_path, camera, object_path, object_dot, camera_module, object_module, model), FadeIn(result), run_time=2.5)
        self.finish_to_audio()
