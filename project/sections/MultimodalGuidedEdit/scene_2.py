from section_common import *


class Scene2(GuidedScene):
    scene_number = 2

    def construct(self):
        heading = title("Instruction editing begins with data")
        self.play(Write(heading), run_time=1.4)
        triplet = VGroup(
            panel("source video", PRIMARY, 2.4, 1.0),
            panel("instruction", INSTRUCTION, 2.4, 1.0),
            panel("target video", SECONDARY, 2.4, 1.0),
        ).arrange(RIGHT, buff=1.0).move_to(UP * 1.1)
        arrows = VGroup(
            edge_arrow(triplet[0], triplet[1], RIGHT, LEFT, WHITE),
            edge_arrow(triplet[1], triplet[2], RIGHT, LEFT, WHITE),
        )
        self.cue(4.8)
        self.play(FadeIn(triplet), Create(arrows), run_time=2.0)
        rare = label("expensive + rare", ERROR, BODY_SIZE).next_to(triplet, DOWN, buff=0.28)
        self.cue(11.9)
        self.play(Write(rare), run_time=1.3)

        synth = VGroup(
            panel("language model\nrewrite + instruction", INSTRUCTION, 3.0, 1.2),
            panel("image / video\nsynthesis", APPEARANCE, 3.0, 1.2),
            panel("synthetic pairs", SECONDARY, 2.7, 1.2),
        ).arrange(RIGHT, buff=0.75).move_to(DOWN * 1.35)
        synth_arrows = VGroup(
            edge_arrow(synth[0], synth[1], RIGHT, LEFT, WHITE),
            edge_arrow(synth[1], synth[2], RIGHT, LEFT, WHITE),
        )
        self.cue(14.0)
        self.play(FadeOut(rare), FadeIn(synth[0]), run_time=1.5)
        self.cue(19.0)
        self.play(Create(synth_arrows[0]), FadeIn(synth[1]), run_time=1.5)
        self.cue(24.2)
        self.play(Create(synth_arrows[1]), FadeIn(synth[2]), run_time=1.5)

        names = VGroup(
            pill("ChatGPT", INSTRUCTION),
            pill("BLIP", APPEARANCE),
            pill("Tune-A-Video", SECONDARY),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.7)
        self.cue(29.1)
        self.play(FadeIn(names), run_time=1.8)

        model = panel("inflated Stable Diffusion", PRIMARY, 3.6, 1.2).move_to(DOWN * 0.1)
        inputs = VGroup(triplet[0].copy(), triplet[1].copy()).arrange(DOWN, buff=0.28).move_to(LEFT * 4.5 + DOWN * 0.1)
        output = triplet[2].copy().move_to(RIGHT * 4.5 + DOWN * 0.1)
        in_arrow = edge_arrow(inputs, model, RIGHT, LEFT, PRIMARY)
        out_arrow = edge_arrow(model, output, RIGHT, LEFT, SECONDARY)
        self.cue(37.9)
        self.play(FadeOut(synth), FadeOut(synth_arrows), FadeOut(names), FadeOut(triplet), FadeOut(arrows), FadeIn(inputs), FadeIn(model), run_time=2.2)
        self.cue(41.4)
        self.play(Create(in_arrow), Create(out_arrow), FadeIn(output), run_time=1.8)
        motion = label("semantic edit, recognizable motion", SECONDARY, BODY_SIZE).to_edge(DOWN, buff=0.35)
        self.cue(44.8)
        self.play(Write(motion), run_time=1.6)
        self.finish_to_audio()
