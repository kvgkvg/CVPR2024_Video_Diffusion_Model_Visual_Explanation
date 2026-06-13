from section_common import *


class Scene8(MultimodalScene):
    scene_number = 8

    def construct(self):
        heading = title("Cinematic Mindscapes: video from fMRI")
        watched = video_strip(4, PRIMARY, 3.8, 1.2).move_to(LEFT * 5.1 + UP * 0.75)
        brain = brain_icon(PURPLE).move_to(LEFT * 1.3 + UP * 0.75)
        fmri = panel("fMRI\nsignal", PURPLE, 1.8, 1.2).move_to(RIGHT * 1.3 + UP * 0.75)
        latent = panel("visual + motion\nrepresentations", ACCENT, 2.7, 1.2).move_to(RIGHT * 4.5 + UP * 0.75)
        top_links = VGroup(
            edge_arrow(watched, brain, RIGHT, LEFT, WHITE),
            edge_arrow(brain, fmri, RIGHT, LEFT, PURPLE),
            edge_arrow(fmri, latent, RIGHT, LEFT, ACCENT),
        )
        self.play(Write(heading), LaggedStart(*[FadeIn(f) for f in watched], lag_ratio=0.2), run_time=2)
        self.play(Create(top_links[0]), FadeIn(brain), run_time=2)
        self.play(Create(top_links[1]), FadeIn(fmri), run_time=2)
        self.wait(1.2)

        noisy = waveform(2.0, 0.55, PURPLE, 18).move_to(fmri)
        self.play(Create(noisy), run_time=1.8)
        self.play(Create(top_links[2]), FadeIn(latent), run_time=2.2)
        self.wait(1.2)

        diffusion = model_block("video diffusion", PRIMARY, 2.5, 1.2).move_to(RIGHT * 1.0 + DOWN * 1.65)
        reconstruction = video_strip(4, SECONDARY, 3.8, 1.2).move_to(LEFT * 3.0 + DOWN * 1.65)
        latent_link = edge_arrow(latent, diffusion, DOWN, UP, PRIMARY)
        reconstruction_link = edge_arrow(diffusion, reconstruction, LEFT, RIGHT, SECONDARY)
        self.play(Create(latent_link), FadeIn(diffusion), run_time=2)
        self.play(Create(reconstruction_link), LaggedStart(*[FadeIn(f) for f in reconstruction], lag_ratio=0.18), run_time=2.7)
        caution = label("reconstruction from a weak biological measurement", GREY, SMALL_SIZE).to_edge(DOWN, buff=0.2)
        self.play(Write(caution), run_time=2)
        self.finish_to_audio()
