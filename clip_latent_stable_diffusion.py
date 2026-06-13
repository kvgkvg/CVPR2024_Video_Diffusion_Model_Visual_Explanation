from pathlib import Path
import random

from manim import *


BG = "#1C1C1C"
BLUE_C = "#58C4DD"
TEAL_E = "#49A88F"
GREEN_C = "#83C167"
YELLOW_C = "#FFFF00"
RED_C = "#FC6255"
PURPLE_C = "#9A72AC"
GREY_C = "#888888"

PRIMARY = BLUE_C
SECONDARY = GREEN_C
ACCENT = YELLOW_C
MONO = "Consolas"

TITLE_SIZE = 44
SECTION_SIZE = 32
BODY_SIZE = 24
SMALL_SIZE = 19
MIN_SIZE = 16

ASSET_DIR = Path(__file__).parent / "assets" / "clip_latent_sd"
EXAMPLE_IMAGE = ASSET_DIR / "robot_bicycle_park.png"


def label(text, size=BODY_SIZE, color=WHITE, weight=NORMAL):
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)


def title_label(text):
    title = label(text, TITLE_SIZE, ACCENT, BOLD)
    if title.width > 12.0:
        title.set_width(12.0)
    return title


def box_label(text, color=PRIMARY, width=2.35, height=0.74, size=SMALL_SIZE):
    body = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.08,
    )
    txt = label(text, size, color, BOLD).move_to(body)
    return VGroup(body, txt)


def image_panel(path, width=3.2, color=PRIMARY):
    image = ImageMobject(str(path)).set_width(width)
    frame = SurroundingRectangle(image, color=color, buff=0.035, stroke_width=2)
    return Group(image, frame)


def vector_bar(color=PRIMARY, n=8):
    cells = VGroup()
    for i in range(n):
        opacity = 0.25 + 0.65 * ((i * 37) % 7) / 6
        cell = Square(
            side_length=0.28,
            stroke_color=color,
            stroke_width=1.2,
            fill_color=color,
            fill_opacity=opacity,
        )
        cells.add(cell)
    cells.arrange(RIGHT, buff=0.035)
    return cells


def latent_grid(rows=4, cols=6, side=0.27, color=TEAL_E):
    rng = random.Random(7)
    cells = VGroup()
    start_color = ManimColor(PURPLE_C)
    end_color = ManimColor(color)
    for _ in range(rows * cols):
        value = rng.random()
        cell = Square(
            side_length=side,
            stroke_color=color,
            stroke_width=0.8,
            fill_color=interpolate_color(start_color, end_color, value),
            fill_opacity=0.72,
        )
        cells.add(cell)
    cells.arrange_in_grid(rows=rows, cols=cols, buff=0.025)
    return cells


def noise_grid(rows=4, cols=6, side=0.27):
    rng = random.Random(21)
    cells = VGroup()
    palette = [GREY_C, BLUE_C, PURPLE_C, WHITE]
    for _ in range(rows * cols):
        cell = Square(
            side_length=side,
            stroke_color=GREY_C,
            stroke_width=0.6,
            fill_color=rng.choice(palette),
            fill_opacity=0.35 + 0.5 * rng.random(),
        )
        cells.add(cell)
    cells.arrange_in_grid(rows=rows, cols=cols, buff=0.025)
    return cells


def flow_arrow(left, right, color=PRIMARY):
    return Arrow(left.get_right(), right.get_left(), buff=0.1, color=color, stroke_width=3)


def vertical_arrow(top, bottom, color=GREY_C):
    return Arrow(top.get_bottom(), bottom.get_top(), buff=0.08, color=color, stroke_width=3)


class ClipLatentStableDiffusionExplainer(Scene):
    """Pages 21-24: CLIP, latent diffusion, and Stable Diffusion."""

    def construct(self):
        self.camera.background_color = BG
        scenes = [
            self.scene_1_clip_bridge,
            self.scene_2_latent_diffusion,
            self.scene_3_stable_diffusion,
            self.scene_4_why_it_matters,
        ]
        for i, scene in enumerate(scenes):
            scene()
            if i < len(scenes) - 1:
                self.play(FadeOut(*self.mobjects), run_time=0.75)
                self.wait(0.2)

    def scene_1_clip_bridge(self):
        title = title_label("CLIP: put words and images on the same map")
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.1)

        image = image_panel(EXAMPLE_IMAGE, width=3.55, color=PRIMARY).shift(LEFT * 4.05 + UP * 0.2)
        prompt = box_label('"a blue robot with a red bicycle"', GREEN_C, 3.95, 0.82, SMALL_SIZE)
        prompt.shift(RIGHT * 4.05 + UP * 0.2)
        img_encoder = box_label("image encoder", PRIMARY, 2.55, 0.72).next_to(image, DOWN, buff=0.55)
        txt_encoder = box_label("text encoder", GREEN_C, 2.55, 0.72).next_to(prompt, DOWN, buff=0.55)
        img_vec = vector_bar(PRIMARY).next_to(img_encoder, DOWN, buff=0.42)
        txt_vec = vector_bar(GREEN_C).next_to(txt_encoder, DOWN, buff=0.42)

        shared = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=3.2,
            y_length=2.1,
            background_line_style={"stroke_color": GREY_C, "stroke_width": 1, "stroke_opacity": 0.35},
            axis_config={"stroke_color": GREY_C, "stroke_opacity": 0.45},
        ).shift(DOWN * 2.0)
        map_label = label("shared embedding space", SMALL_SIZE, GREY_C).next_to(shared, DOWN, buff=0.16)
        dot_i = Dot(shared.c2p(-0.32, 0.28), color=PRIMARY, radius=0.07)
        dot_t = Dot(shared.c2p(-0.12, 0.18), color=GREEN_C, radius=0.07)
        close = DoubleArrow(dot_i.get_center(), dot_t.get_center(), buff=0.05, color=ACCENT, stroke_width=3)

        self.play(FadeIn(image, scale=0.98), FadeIn(prompt, shift=LEFT * 0.1), run_time=1.0)
        self.play(
            GrowArrow(Arrow(image.get_bottom(), img_encoder.get_top(), buff=0.1, color=PRIMARY)),
            GrowArrow(Arrow(prompt.get_bottom(), txt_encoder.get_top(), buff=0.1, color=GREEN_C)),
            FadeIn(img_encoder),
            FadeIn(txt_encoder),
            run_time=1.0,
        )
        self.play(Create(img_vec), Create(txt_vec), run_time=0.8)
        self.play(FadeIn(shared), FadeIn(map_label), run_time=0.8)
        self.play(
            img_vec.animate.copy().scale(0.45).move_to(dot_i),
            txt_vec.animate.copy().scale(0.45).move_to(dot_t),
            run_time=1.0,
        )
        self.play(FadeIn(dot_i), FadeIn(dot_t), Create(close), run_time=0.8)
        self.wait(2.2)

    def scene_2_latent_diffusion(self):
        title = title_label("Latent diffusion: denoise the small code")
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.0)

        pixels = image_panel(EXAMPLE_IMAGE, width=2.05, color=PRIMARY).shift(LEFT * 4.9 + UP * 0.95)
        encoder = box_label("encoder", PRIMARY, 1.35, 0.62).shift(LEFT * 2.85 + UP * 0.95)
        latent = latent_grid(rows=3, cols=5, side=0.24).scale(1.18).shift(LEFT * 1.25 + UP * 0.95)
        latent_caption = label("compact latent = cheaper than pixels", MIN_SIZE, TEAL_E, BOLD)
        latent_caption.next_to(latent, UP, buff=0.18)

        add_noise = box_label("add noise", GREY_C, 1.45, 0.62, MIN_SIZE).shift(LEFT * 1.25 + DOWN * 0.2)
        noisy = noise_grid(rows=3, cols=5, side=0.24).scale(1.18).shift(LEFT * 1.25 + DOWN * 1.5)
        denoise = box_label("denoise", TEAL_E, 1.45, 0.62, MIN_SIZE).shift(RIGHT * 0.55 + DOWN * 1.5)
        clean = latent_grid(rows=3, cols=5, side=0.24).scale(1.18).shift(RIGHT * 2.2 + DOWN * 1.5)
        decoder = box_label("decoder", PRIMARY, 1.35, 0.62).shift(RIGHT * 3.75 + DOWN * 1.5)
        output = image_panel(EXAMPLE_IMAGE, width=1.75, color=SECONDARY).shift(RIGHT * 5.55 + DOWN * 1.5)
        arrows = VGroup(
            flow_arrow(pixels, encoder, PRIMARY),
            flow_arrow(encoder, latent, PRIMARY),
            vertical_arrow(latent, add_noise, GREY_C),
            vertical_arrow(add_noise, noisy, GREY_C),
            flow_arrow(noisy, denoise, TEAL_E),
            flow_arrow(denoise, clean, TEAL_E),
            flow_arrow(clean, decoder, PRIMARY),
            flow_arrow(decoder, output, SECONDARY),
        )

        self.play(FadeIn(pixels), run_time=0.8)
        self.play(FadeIn(encoder), GrowArrow(arrows[0]), run_time=0.9)
        self.play(FadeIn(latent), GrowArrow(arrows[1]), FadeIn(latent_caption), run_time=1.1)
        self.wait(1.4)
        self.play(FadeIn(add_noise), GrowArrow(arrows[2]), run_time=0.8)
        self.play(FadeIn(noisy), GrowArrow(arrows[3]), run_time=0.9)
        self.play(FadeIn(denoise), GrowArrow(arrows[4]), run_time=0.8)
        self.play(FadeIn(clean), GrowArrow(arrows[5]), run_time=0.9)
        self.play(FadeIn(decoder), GrowArrow(arrows[6]), run_time=0.8)
        self.play(FadeIn(output), GrowArrow(arrows[7]), run_time=0.9)
        self.wait(3.2)

    def scene_3_stable_diffusion(self):
        title = title_label("Stable Diffusion: text steers latent denoising")
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.0)

        prompt = box_label("CLIP text embedding", GREEN_C, 3.1, 0.72).shift(LEFT * 4.55 + UP * 1.65)
        unet = RoundedRectangle(
            corner_radius=0.1,
            width=4.7,
            height=2.4,
            stroke_color=TEAL_E,
            stroke_width=2.5,
            fill_color=TEAL_E,
            fill_opacity=0.08,
        ).shift(LEFT * 0.45 + UP * 0.25)
        unet_label = label("denoising U-Net", SECTION_SIZE, TEAL_E, BOLD).move_to(unet.get_top() + DOWN * 0.42)
        attention = VGroup(*[box_label("Q K V", ACCENT, 0.9, 0.55, MIN_SIZE) for _ in range(4)]).arrange(RIGHT, buff=0.22)
        attention.move_to(unet.get_center() + DOWN * 0.34)
        zt = noise_grid(rows=3, cols=5, side=0.25).scale(1.25).shift(LEFT * 4.7 + DOWN * 1.45)
        z = latent_grid(rows=3, cols=5, side=0.25).scale(1.25).shift(RIGHT * 2.25 + DOWN * 1.45)
        decoder = box_label("decoder", PRIMARY, 1.5, 0.68).shift(RIGHT * 3.55 + DOWN * 1.45)
        image = image_panel(EXAMPLE_IMAGE, width=2.1, color=SECONDARY).shift(RIGHT * 5.55 + DOWN * 1.45)

        self.play(FadeIn(prompt), FadeIn(zt), run_time=0.8)
        self.play(FadeIn(unet), Write(unet_label), FadeIn(attention), run_time=1.0)
        self.play(
            GrowArrow(Arrow(prompt.get_right(), attention.get_top(), buff=0.15, color=GREEN_C)),
            run_time=0.7,
        )
        self.play(
            GrowArrow(Arrow(zt.get_right(), unet.get_left(), buff=0.15, color=GREY_C)),
            run_time=0.6,
        )
        self.play(TransformFromCopy(zt, z), run_time=1.0)
        self.play(
            GrowArrow(Arrow(unet.get_right(), z.get_left(), buff=0.15, color=TEAL_E)),
            FadeIn(decoder),
            GrowArrow(Arrow(z.get_right(), decoder.get_left(), buff=0.1, color=PRIMARY)),
            FadeIn(image),
            GrowArrow(Arrow(decoder.get_right(), image.get_left(), buff=0.1, color=SECONDARY)),
            run_time=1.2,
        )
        note = label("Conditioning makes generation controllable.", BODY_SIZE, ACCENT, BOLD).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.7)
        self.wait(2.4)

    def scene_4_why_it_matters(self):
        title = title_label("Why this backbone matters").to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.0)

        center = box_label("Stable Diffusion", ACCENT, 3.0, 0.88, BODY_SIZE).shift(UP * 0.2)
        clip = box_label("CLIP\nlanguage handle", GREEN_C, 2.45, 1.0, SMALL_SIZE).shift(LEFT * 4.35 + UP * 1.45)
        latent = box_label("latent space\nspeed handle", TEAL_E, 2.45, 1.0, SMALL_SIZE).shift(LEFT * 4.35 + DOWN * 1.1)
        control = box_label("controls\nimage, depth, video", PRIMARY, 2.9, 1.0, SMALL_SIZE).shift(RIGHT * 4.25 + UP * 1.45)
        video = box_label("video diffusion\nreuse the backbone", PURPLE_C, 2.9, 1.0, SMALL_SIZE).shift(RIGHT * 4.25 + DOWN * 1.1)

        spokes = VGroup(
            Arrow(clip.get_right(), center.get_left(), buff=0.1, color=GREEN_C),
            Arrow(latent.get_right(), center.get_left(), buff=0.1, color=TEAL_E),
            Arrow(center.get_right(), control.get_left(), buff=0.1, color=PRIMARY),
            Arrow(center.get_right(), video.get_left(), buff=0.1, color=PURPLE_C),
        )
        self.play(FadeIn(center, scale=0.98), run_time=0.6)
        self.play(FadeIn(clip), FadeIn(latent), GrowArrow(spokes[0]), GrowArrow(spokes[1]), run_time=1.1)
        self.play(FadeIn(control), FadeIn(video), GrowArrow(spokes[2]), GrowArrow(spokes[3]), run_time=1.1)

        summary = label(
            "The key idea: generate in a compact space,\nthen steer it with language and other conditions.",
            BODY_SIZE,
            WHITE,
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(summary, shift=UP * 0.15), run_time=0.8)
        self.wait(4.0)
