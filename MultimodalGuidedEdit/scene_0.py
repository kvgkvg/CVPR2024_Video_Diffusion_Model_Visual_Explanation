from section_common import *


class Scene0(GuidedScene):
    scene_number = 0
    intro_pause = 0.8

    def construct(self):
        self.start_scene()
        heading = label("Multimodal-Guided Video Editing", PRIMARY, 54, weight=BOLD).to_edge(UP, buff=0.35)
        question = label("How should we specify an edit?", ACCENT, BODY_SIZE).next_to(heading, DOWN, buff=0.35)
        self.play(Write(heading), run_time=1.5)
        self.cue(2.2)
        self.play(Write(question), run_time=1.2)

        model = panel("video diffusion", PRIMARY, 3.0, 1.35, BODY_SIZE).move_to(DOWN * 0.15)
        self.cue(12.1)
        self.play(FadeIn(model), run_time=1.2)

        instruction = panel("instruction\nsemantic intent", INSTRUCTION, 2.45, 1.15).move_to(LEFT * 4.6 + UP * 1.15)
        audio = panel("audio\ntiming + events", AUDIO, 2.45, 1.15).move_to(LEFT * 4.6 + DOWN * 1.55)
        image = panel("reference image\nappearance", APPEARANCE, 2.55, 1.15).move_to(RIGHT * 4.55 + UP * 1.15)
        pose = panel("pose sequence\nmotion", MOTION, 2.55, 1.15).move_to(RIGHT * 4.55 + DOWN * 1.55)
        controls = VGroup(instruction, audio, image, pose)
        arrows = VGroup(
            edge_arrow(instruction, model, RIGHT, LEFT, INSTRUCTION),
            edge_arrow(audio, model, RIGHT, LEFT, AUDIO),
            edge_arrow(image, model, LEFT, RIGHT, APPEARANCE),
            edge_arrow(pose, model, LEFT, RIGHT, MOTION),
        )
        self.cue(19.9)
        self.play(FadeIn(instruction), Create(arrows[0]), run_time=1.5)
        self.cue(22.8)
        self.play(FadeIn(audio), Create(arrows[1]), run_time=1.5)
        self.cue(25.7)
        self.play(FadeIn(image), Create(arrows[2]), run_time=1.5)
        self.cue(28.5)
        self.play(FadeIn(pose), Create(arrows[3]), run_time=1.5)

        output = frame_strip(5, SECONDARY, 5.2, 1.0).to_edge(DOWN, buff=0.25)
        out_arrow = edge_arrow(model, output, DOWN, UP, SECONDARY)
        self.cue(31.2)
        self.play(Create(out_arrow), FadeIn(output), run_time=1.6)
        self.cue(35.5)
        self.play(
            Indicate(controls, color=WHITE),
            Indicate(output, color=WHITE),
            run_time=2.0,
        )
        self.finish_to_audio()
