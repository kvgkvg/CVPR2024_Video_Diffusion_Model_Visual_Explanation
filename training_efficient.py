# === PRODUCTION PLAN ===
# Core insight (one sentence): Do not rebuild the painter; keep the frozen image
# model and add the cheapest temporal discipline that makes frames remember each
# other.
#
# Color encoding:
#   PRIMARY   = trainable / new / motion
#   SECONDARY = consistency / success / stable identity
#   WARM      = flicker / failure / cost
#   ACCENT    = attention / memory / reference
#   MUTED     = frozen / pretrained / locked
#
# Scene list:
#   Scene01_PainterForgets - independent image generations become different cats
#   Scene02_CubeOfCost - a flat image plate extrudes into an expensive time cube
#   Scene03_TwoRoads - full video training versus reuse plus a motion module
#   Scene04_MarketplaceWall - many image painters cannot each get a video model
#   Scene05_OneEngineManyPainters - one motion module plugs into many styles
#   Scene06_FrozenBodyTrainableEngine - locked gray body, blue trainable modules
#   Scene07_GradientsBounceOffGray - training updates only the blue modules
#   Scene08_FourBeforeAfters - identity, motion, background, and style stabilize
#   Scene09_IslandsToConversation - frame islands become a temporal conversation
#   Scene10_TrainSmallDeployBig - low-res motion transfers to high-res painters
#   Scene11_AnimateDiffOneBreath - freeze, train motion, reuse everywhere
#   Scene12_StillNeedsTraining - AnimateDiff works but still needs video data
#   Scene13_ZeroNewWeights - an unchanged model is steered at inference time
#   Scene14_StrangersVsSiblings - unrelated noise makes strangers; shifted noise
#       makes related frames
#   Scene15_NoiseDragsContent - shifted noise drags the object through time
#   Scene16_FirstFrameMemoryCard - frame one becomes a shared reference card
#   Scene17_QueryChangesKVDont - changing queries move pose while K/V anchors look
#   Scene18_TwoRiversOneCalm - moving foreground recombines with a stable plate
#   Scene19_Text2VideoZeroOneBreath - three controls orbit an unchanged model
#   Scene20_TheScale - learned motion versus zero-training control
#   Scene21_LookingOverYourShoulder - later frames attend to earlier frames
#   Scene22_SmallPatchesGiantBuilding - adapters absorb gradients on a huge model
#   Scene23_TwoRiversMerge - content and motion streams braid into one video
#   Scene24_BigPictureTree - five mechanisms are branches of one idea
#   Scene25_ShortClipsToWholeMovies - short clips shrink beside the movie problem
#
# Key transforms (moments where one thing morphs INTO another):
#   - single image -> five-frame strip in Scene01
#   - flat image square -> time cube in Scene02
#   - still output -> video strip when blue module clicks in Scene03
#   - frame 1 -> yellow memory card in Scene16
#   - content stream + motion stream -> finished strip in Scene23
# ======================

from manim import *
import os
import numpy as np


BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#E8C468"
WARM = "#E86B5F"
MUTED = "#888888"
WHITE_ISH = "#F0EDE6"

FAST = 0.4
NORMAL = 0.8
SLOW = 1.5
BEAT = 1.2
LONG = 2.5

ROOT = os.path.dirname(__file__)
A22 = os.path.join(ROOT, "images", "2.2")
A24 = os.path.join(ROOT, "images", "2.4")
NOISE = MUTED


def txt(s, color=WHITE_ISH, size=24, max_width=11.4):
    mob = Text(s, color=color, font_size=size)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def footer(s, color=WHITE_ISH, size=23):
    mob = txt(s, color, size, 11.5)
    return mob.to_edge(DOWN, buff=0.22)


def add_backdrop(scene):
    # Reference chapters use open dark space, not a persistent grid or frame.
    return VGroup()


def box(w=1.6, h=0.9, color=MUTED, fill=None, opacity=0.12, radius=0.1, stroke=3):
    return RoundedRectangle(
        width=w,
        height=h,
        corner_radius=radius,
        color=color,
        stroke_width=stroke,
        fill_color=fill or color,
        fill_opacity=opacity,
    )


def label_box(label, w=1.6, h=0.5, color=ACCENT, size=15):
    b = box(w, h, color, BG, 0.08, 0.08)
    t = txt(label, WHITE_ISH, size, w - 0.18).move_to(b)
    return VGroup(b, t)


def machine(label="T2I Model", w=2.05, h=1.05, color=MUTED, socket=True):
    body = box(w, h, color, BG, 0.1, 0.14)
    slot_l = Rectangle(width=0.15, height=0.45, color=color, fill_color=BG, fill_opacity=1).next_to(body, LEFT, buff=-0.06)
    slot_r = slot_l.copy().next_to(body, RIGHT, buff=-0.06)
    vents = VGroup(*[Line(LEFT * 0.16, RIGHT * 0.16, color=color, stroke_width=1) for _ in range(3)]).arrange(DOWN, buff=0.035)
    vents.move_to(body.get_bottom() + UP * 0.22)
    t = txt(label, WHITE_ISH, 17, w - 0.3).move_to(body)
    parts = [body, slot_l, slot_r, vents, t]
    if socket:
        s = box(0.46, 0.14, PRIMARY, BG, 0.4, 0.035, stroke=2).move_to(body.get_top() + DOWN * 0.14)
        parts.append(s)
    return VGroup(*parts)


def motion_module(scale=1):
    body = box(0.82, 0.6, PRIMARY, PRIMARY, 0.26, 0.1)
    halo = box(1.02, 0.8, PRIMARY, PRIMARY, 0.06, 0.14, stroke=1).move_to(body)
    gear = VGroup(Circle(0.15, color=WHITE_ISH, stroke_width=3), Dot(radius=0.035, color=WHITE_ISH))
    arrows = VGroup(
        Arrow(LEFT * 0.32, LEFT * 0.08, color=WHITE_ISH, buff=0.01, stroke_width=2, max_tip_length_to_length_ratio=0.35),
        Arrow(RIGHT * 0.08, RIGHT * 0.32, color=WHITE_ISH, buff=0.01, stroke_width=2, max_tip_length_to_length_ratio=0.35),
    ).move_to(body.get_bottom() + UP * 0.12)
    return VGroup(halo, body, gear.move_to(body.get_center() + UP * 0.06), arrows).scale(scale)


def lock_icon(scale=1):
    shackle = Arc(radius=0.13, start_angle=0, angle=PI, color=WHITE_ISH, stroke_width=3).shift(UP * 0.05)
    base = box(0.3, 0.22, WHITE_ISH, WHITE_ISH, 0.18, 0.03, stroke=1).shift(DOWN * 0.06)
    return VGroup(shackle, base).scale(scale)


def noise_square(seed=1, side=0.55, color=NOISE):
    rng = np.random.default_rng(seed)
    border = Square(side, color=color, stroke_width=2, fill_color=BG, fill_opacity=0.85)
    dots = VGroup()
    for _ in range(42):
        dots.add(Dot(
            [rng.uniform(-side / 2 + 0.04, side / 2 - 0.04), rng.uniform(-side / 2 + 0.04, side / 2 - 0.04), 0],
            radius=rng.uniform(0.01, 0.025),
            color=color if rng.random() > 0.45 else WHITE_ISH,
        ))
    dots.move_to(border)
    return VGroup(border, dots)


def image_card(path, w=1.0, h=0.74, color=SECONDARY):
    border = box(w, h, color, BG, 1, 0.06, stroke=3)
    img = ImageMobject(path)
    img.scale_to_fit_width(w - 0.08)
    if img.height > h - 0.08:
        img.scale_to_fit_height(h - 0.08)
    img.move_to(border)
    return Group(border, img)


def photo_strip(paths, *args, **kwargs):
    if isinstance(paths, str):
        if args and isinstance(args[0], int):
            n = args[0]
            w = args[1] if len(args) > 1 else kwargs.get("w", 1.0)
            if len(args) > 2 and isinstance(args[2], (int, float)):
                h = args[2]
                color = args[3] if len(args) > 3 else kwargs.get("color", SECONDARY)
                buff = args[4] if len(args) > 4 else kwargs.get("buff", 0.12)
            else:
                h = kwargs.get("h", w * 0.72)
                color = args[2] if len(args) > 2 else kwargs.get("color", SECONDARY)
                buff = args[3] if len(args) > 3 else kwargs.get("buff", 0.12)
            paths = [paths] * n
        else:
            w = args[0] if len(args) > 0 else kwargs.get("w", 1.0)
            h = args[1] if len(args) > 1 else kwargs.get("h", 0.75)
            color = args[2] if len(args) > 2 else kwargs.get("color", SECONDARY)
            buff = args[3] if len(args) > 3 else kwargs.get("buff", 0.12)
            paths = [paths] * kwargs.get("n", 4)
    else:
        w = args[0] if len(args) > 0 else kwargs.get("w", 1.0)
        h = args[1] if len(args) > 1 else kwargs.get("h", 0.75)
        color = args[2] if len(args) > 2 else kwargs.get("color", SECONDARY)
        buff = args[3] if len(args) > 3 else kwargs.get("buff", 0.12)
    return Group(*[image_card(p, w, h, color) for p in paths]).arrange(RIGHT, buff=buff)


def dog_paths(n=4):
    return [os.path.join(A22, f"dog_{i}.jpg") for i in range(n)]


def motion_photo_strip(paths, w=1.0, h=0.72, color=SECONDARY, buff=0.12, marker=ACCENT, direction=RIGHT):
    strip = photo_strip(paths, w, h, color, buff)
    n = len(strip)
    dots = VGroup()
    arrows = VGroup()
    for i, frame in enumerate(strip):
        alpha = 0 if n == 1 else i / (n - 1)
        local = direction * (0.34 - 0.68 * alpha) + DOWN * 0.18
        dots.add(Dot(frame.get_center() + local, radius=min(w, h) * 0.055, color=marker))
        if i > 0:
            arrows.add(Arrow(strip[i - 1].get_bottom() + DOWN * 0.12, frame.get_bottom() + DOWN * 0.12,
                             color=marker, buff=0.06, stroke_width=2.5, max_tip_length_to_length_ratio=0.16))
    return Group(strip, dots, arrows)


def cat_frame(pose=0, color=SECONDARY, bg=SECONDARY, scale=1):
    frame = box(0.95, 0.64, color, BG, 0.12, 0.06, stroke=2)
    ground = Line(frame.get_left() + RIGHT * 0.1 + DOWN * 0.2, frame.get_right() + LEFT * 0.1 + DOWN * 0.2, color=bg, stroke_width=2)
    body = Ellipse(width=0.38, height=0.18, color=color, fill_color=color, fill_opacity=0.7)
    head = Circle(0.1, color=color, fill_color=color, fill_opacity=0.7).next_to(body, RIGHT, buff=-0.04).shift(UP * 0.04)
    tail = ArcBetweenPoints(body.get_left(), body.get_left() + LEFT * 0.18 + UP * (0.08 + 0.03 * pose), angle=-0.8, color=color, stroke_width=3)
    legs = VGroup(
        Line(body.get_bottom() + LEFT * 0.08, body.get_bottom() + LEFT * (0.15 + 0.03 * pose) + DOWN * 0.12, color=color, stroke_width=3),
        Line(body.get_bottom() + RIGHT * 0.08, body.get_bottom() + RIGHT * (0.15 - 0.03 * pose) + DOWN * 0.12, color=color, stroke_width=3),
    )
    cat = VGroup(body, head, tail, legs).move_to(frame).shift(RIGHT * 0.08 * pose)
    return VGroup(frame, ground, cat).scale(scale)


def filmstrip(n=5, scale=0.7, color=SECONDARY):
    frames = VGroup(*[cat_frame(i - (n - 1) / 2, color=color, scale=1) for i in range(n)]).arrange(RIGHT, buff=0.08)
    line = Line(frames.get_left() + DOWN * 0.28, frames.get_right() + DOWN * 0.28, color=color, stroke_width=2)
    return VGroup(frames, line).scale(scale)


def unet_stack(include_modules=True):
    blocks = VGroup(*[box(1.5, 0.42, MUTED, MUTED, 0.14, 0.06) for _ in range(5)]).arrange(DOWN, buff=0.13)
    locks = VGroup(*[lock_icon(0.42).move_to(b.get_right() + LEFT * 0.22) for b in blocks])
    mods = VGroup()
    if include_modules:
        for i in range(4):
            m = box(1.0, 0.24, PRIMARY, PRIMARY, 0.28, 0.05)
            arrow = Arrow(LEFT * 0.34, RIGHT * 0.34, color=WHITE_ISH, buff=0.02, stroke_width=2, max_tip_length_to_length_ratio=0.25).move_to(m)
            mods.add(VGroup(m, arrow).move_to((blocks[i].get_bottom() + blocks[i + 1].get_top()) / 2))
    return VGroup(blocks, locks, mods)


def gpu_chip(w=0.58, h=0.36, color=MUTED, fill=None, label_size=9):
    body = box(w, h, color, fill or BG, 0.16, 0.06, stroke=2)
    pins = VGroup()
    for y in [-h * 0.24, 0, h * 0.24]:
        pins.add(Line(body.get_left() + RIGHT * 0.02 + UP * y, body.get_left() + LEFT * 0.1 + UP * y, color=color, stroke_width=1.4))
        pins.add(Line(body.get_right() + LEFT * 0.02 + UP * y, body.get_right() + RIGHT * 0.1 + UP * y, color=color, stroke_width=1.4))
    label = txt("GPU", color, label_size, w - 0.12).move_to(body)
    return VGroup(pins, body, label)


def gpu_stack(n=4, color=WARM):
    cards = VGroup(*[gpu_chip(0.62, 0.24, color, color, 7) for _ in range(n)]).arrange(UP, buff=0.04)
    return cards


def memory_card(scale=1):
    card = box(1.15, 0.78, ACCENT, ACCENT, 0.16, 0.08)
    icons = VGroup(Circle(0.08, color=WHITE_ISH), Square(0.15, color=SECONDARY), Circle(0.08, color=ACCENT), Line(LEFT * 0.08, RIGHT * 0.08 + UP * 0.04, color=WHITE_ISH)).arrange(RIGHT, buff=0.08)
    lab = txt("frame 1", WHITE_ISH, 11, 0.8).next_to(icons, DOWN, buff=0.04)
    return VGroup(card, VGroup(icons, lab).move_to(card)).scale(scale)


STYLE_ASSETS = [
    ("Anime", os.path.join(A24, "anime_card.png")),
    ("Realistic", os.path.join(A22, "director.jpg")),
    ("Cartoon", os.path.join(A24, "cartoon_card.png")),
    ("Fantasy", os.path.join(A24, "fantasy_castle_card.png")),
    ("Animal", os.path.join(A22, "panda.jpg")),
    ("Cyberpunk", os.path.join(A24, "cyberpunk_card.png")),
    ("3D", os.path.join(A22, "robot.jpg")),
    ("Ink", os.path.join(A24, "ink_style_card.png")),
]


def style_card(name, path):
    img = image_card(path, 1.18, 0.88, SECONDARY)
    lab = txt(name, WHITE_ISH, 13, 1.15).next_to(img, DOWN, buff=0.05)
    return Group(img, lab)


def fade_all(scene, *keep):
    keep_set = set(keep)
    mobs = [m for m in scene.mobjects if m not in keep_set]
    if mobs:
        scene.play(*[FadeOut(m) for m in mobs], run_time=FAST)


class Scene01_PainterForgets(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: one beautiful cat photo succeeds, but independent frames become a broken timeline.
        prompt = txt('"A cat on grass"', WHITE_ISH, 16).move_to(LEFT * 4.5 + UP * 2.15)
        t2i = machine().move_to(LEFT * 4.45 + UP * 0.55)
        noise = noise_square(3, 0.5, MUTED).move_to(LEFT * 5.55 + UP * 0.55)
        arrow_in = Arrow(noise.get_right(), t2i.get_left(), color=MUTED, buff=0.05, stroke_width=3)
        still = image_card(os.path.join(A22, "cat.jpg"), 1.55, 1.25, SECONDARY).move_to(LEFT * 1.55 + UP * 0.55)
        check = txt("✓", SECONDARY, 30).next_to(still, UP, buff=0.08)
        self.play(GrowFromCenter(t2i)); self.wait(BEAT)
        self.play(Write(prompt)); self.wait(BEAT)
        self.play(FadeIn(noise, shift=RIGHT * 0.25), GrowArrow(arrow_in), Indicate(t2i, color=ACCENT))
        self.play(GrowFromCenter(still), FadeIn(check))
        self.wait(BEAT)
        self.play(Write(txt("Beautiful single image", SECONDARY, 16).next_to(still, DOWN, buff=0.14)))
        self.wait(BEAT)

        divider = DashedLine(UP * 3.05, DOWN * 2.65, color=MUTED, dash_length=0.14)
        timeline = Line(RIGHT * 0.55 + DOWN * 1.85, RIGHT * 5.65 + DOWN * 1.85, color=MUTED)
        slots = Group(*[image_card(os.path.join(A22, "cat.jpg"), 0.92, 0.72, MUTED) for _ in range(5)]).arrange(RIGHT, buff=0.12)
        slots.move_to(RIGHT * 3.1 + DOWN * 0.35)
        slots[1].set_opacity(0.65)
        slots[2][1].scale(0.86)
        slots[3].rotate(0.08)
        slots[4].stretch(0.86, 0)
        frame_noise = VGroup(*[noise_square(20 + i, 0.28, WARM) for i in range(5)]).arrange(RIGHT, buff=0.18).next_to(timeline, UP, buff=0.22)
        self.play(Create(divider)); self.wait(BEAT)
        self.play(Create(timeline), LaggedStart(*[FadeIn(n, shift=RIGHT * 0.12) for n in frame_noise], lag_ratio=0.08))
        self.wait(BEAT)
        self.play(FadeOut(frame_noise), LaggedStart(*[GrowFromCenter(s) for s in slots], lag_ratio=0.12))
        self.wait(BEAT)
        defects = VGroup(*[Circle(0.18, color=WARM, stroke_width=3).move_to(slots[i]).shift(v)
                           for i, v in enumerate([UP * 0.06, RIGHT * 0.08, DOWN * 0.08, LEFT * 0.06, DOWN * 0.1])])
        broken = VMobject(color=WARM, stroke_width=4).set_points_as_corners(
            [s.get_center() + DOWN * 0.55 + UP * (0.12 if i % 2 else -0.08) for i, s in enumerate(slots)]
        )
        self.play(LaggedStart(*[Create(d) for d in defects], lag_ratio=0.08), Create(broken))
        verdict = VGroup(txt("Good images", WARM, 30), txt("≠", WARM, 30), txt("good video", WARM, 30))
        verdict.arrange(RIGHT, buff=0.22).to_edge(DOWN, buff=0.25)
        self.play(Wiggle(slots, rotation_angle=0.04), FadeIn(verdict, shift=UP * 0.12))
        self.wait(LONG)


class Scene02_CubeOfCost(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: video is an image square extruded through time, so every cost grows with the extra axis.
        flat = Square(1.8, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.12).move_to(LEFT * 3.15 + UP * 0.75)
        axes = VGroup(
            Arrow(flat.get_corner(DL), flat.get_corner(DR) + RIGHT * 0.25, color=WHITE_ISH, buff=0.02, stroke_width=4),
            Arrow(flat.get_corner(DL), flat.get_corner(UL) + UP * 0.25, color=WHITE_ISH, buff=0.02, stroke_width=4),
        )
        w_label = txt("W", WHITE_ISH, 14).next_to(axes[0].get_end(), RIGHT, buff=0.05)
        h_label = txt("H", WHITE_ISH, 14).next_to(axes[1].get_end(), UP, buff=0.05)
        hw_label = txt("H x W", WHITE_ISH, 16).next_to(flat, DOWN, buff=0.22)
        small_gpu = gpu_chip(0.58, 0.38, MUTED, BG, 10).next_to(flat, RIGHT, buff=0.42).shift(DOWN * 0.75)
        small_gpu_label = txt("1 GPU", MUTED, 11).next_to(small_gpu, DOWN, buff=0.04)

        self.play(Create(axes), GrowFromCenter(flat), Write(hw_label), FadeIn(small_gpu), FadeIn(small_gpu_label), Write(w_label), Write(h_label))
        self.wait(BEAT)

        plus_time = VGroup(
            Arrow(LEFT * 1.55 + UP * 0.75, LEFT * 0.1 + UP * 0.75, color=PRIMARY, stroke_width=4, buff=0.05),
            txt("+ time", PRIMARY, 18),
        )
        plus_time[1].next_to(plus_time[0], UP, buff=0.08)
        self.play(GrowArrow(plus_time[0]), Write(plus_time[1]))
        self.wait(BEAT)

        front = Square(1.8, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.1).move_to(RIGHT * 1.6 + UP * 0.75)
        t_axis = Arrow(front.get_corner(UR), front.get_corner(UR) + RIGHT * 1.65 + UP * 1.25, color=PRIMARY, stroke_width=4, buff=0.02)
        t_label = txt("T", PRIMARY, 14).next_to(t_axis.get_end(), RIGHT, buff=0.04)
        self.play(GrowFromCenter(front), GrowArrow(t_axis), Write(t_label))
        self.wait(BEAT)

        stack = VGroup(*[
            front.copy().shift(RIGHT * 0.28 * i + UP * 0.22 * i)
            for i in range(1, 6)
        ])
        thw_label = txt("T x H x W", WHITE_ISH, 16).next_to(front, DOWN, buff=0.22)
        big_gpu = gpu_stack(4, WARM).move_to(RIGHT * 5.0 + UP * 0.75)
        big_gpu_label = txt("many GPUs", WARM, 13).next_to(big_gpu, DOWN, buff=0.08)
        self.play(
            LaggedStart(*[FadeIn(s, shift=RIGHT * 0.28 + UP * 0.22) for s in stack], lag_ratio=0.18),
            FadeIn(thw_label),
            GrowFromEdge(big_gpu, DOWN),
            FadeIn(big_gpu_label),
        )
        self.wait(BEAT)

        self.play(
            LaggedStart(*[m.animate.shift(RIGHT * 0.08 + UP * 0.06) for m in VGroup(front, *stack)], lag_ratio=0.12),
            run_time=SLOW,
        )
        self.wait(BEAT)

        image_bar = Rectangle(width=0.65, height=1.0, color=MUTED, fill_color=MUTED, fill_opacity=0.28).move_to(LEFT * 1.65 + DOWN * 2.35)
        video_bar = Rectangle(width=0.65, height=0.05, color=WARM, fill_color=WARM, fill_opacity=0.3).move_to(RIGHT * 1.15 + DOWN * 3.02)
        image_model = txt("Image model", WHITE_ISH, 16).next_to(image_bar, UP, buff=0.12)
        final_video_bar = video_bar.copy().stretch_to_fit_height(2.25).move_to(RIGHT * 1.15 + DOWN * 1.9)
        video_model = txt("Video model", WARM, 16).next_to(final_video_bar, LEFT, buff=0.55)
        self.play(GrowFromEdge(image_bar, DOWN), FadeIn(image_model))
        self.play(FadeIn(video_bar), FadeIn(video_model))
        self.play(video_bar.animate.stretch_to_fit_height(2.25).move_to(RIGHT * 1.15 + DOWN * 1.9), run_time=SLOW)
        self.wait(BEAT)

        cost_labels = VGroup(*[
            txt(s, WARM, 18, 2.4)
            for s in ["More frames", "More memory", "More compute", "More training data"]
        ]).arrange(DOWN, buff=0.08).next_to(video_bar, RIGHT, buff=0.32)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in cost_labels], lag_ratio=0.2))
        self.wait(BEAT)

        progress_track = Rectangle(width=3.6, height=0.2, color=MUTED, fill_color=BG, fill_opacity=0.2).move_to(RIGHT * 1.55 + DOWN * 3.22)
        progress_fill = Rectangle(width=0.01, height=0.16, stroke_width=0, fill_color=WARM, fill_opacity=0.9)
        progress_fill.align_to(progress_track, LEFT).move_to(progress_track.get_left() + RIGHT * 0.005)
        progress_label = txt("Training from scratch...", WARM, 17).next_to(progress_track, LEFT, buff=0.18)
        self.play(Create(progress_track), FadeIn(progress_fill), Write(progress_label))
        self.play(progress_fill.animate.stretch_to_fit_width(1.8).move_to(progress_track.get_left() + RIGHT * 0.9), run_time=3.5)
        self.wait(LONG)


class Scene03_TwoRoads(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: the steep road means full video training; the gentle road means reuse the image model and add motion.
        divider = DashedLine(UP * 3.0, DOWN * 2.8, color=MUTED, dash_length=0.15)
        left_head = txt("Full training", WARM, 24).move_to(LEFT * 3.4 + UP * 2.55)
        right_head = txt("Reuse + extend", SECONDARY, 24).move_to(RIGHT * 3.15 + UP * 2.55)
        start = Dot(LEFT * 4.6 + DOWN * 1.8, color=WHITE_ISH)
        road_bad = VMobject(color=WARM, stroke_width=5).set_points_smoothly([start.get_center(), LEFT * 3.4 + DOWN * 0.5, LEFT * 2.4 + UP * 1.8])
        road_good = VMobject(color=SECONDARY, stroke_width=5).set_points_smoothly([RIGHT * 0.45 + DOWN * 1.8, RIGHT * 2.0 + DOWN * 1.35, RIGHT * 5.2 + DOWN * 1.35])
        self.play(Create(divider), Write(left_head), Write(right_head), FadeIn(start), Create(road_bad), Create(road_good))
        self.wait(BEAT)
        warnings = VGroup(*[Triangle(color=WARM, fill_color=WARM, fill_opacity=0.25).scale(0.2).move_to(p) for p in [LEFT * 3.4, LEFT * 2.9 + UP * 0.65, LEFT * 2.45 + UP * 1.35]])
        peak = label_box("Full Video Model", 2.1, 0.8, WARM, 18).move_to(LEFT * 1.9 + UP * 2.0)
        t2i = machine().move_to(RIGHT * 2.0 + DOWN * 0.35)
        still = image_card(os.path.join(A22, "cat.jpg"), 1.0, 0.72, SECONDARY).next_to(t2i, RIGHT, buff=0.32)
        self.play(LaggedStart(*[FadeIn(w) for w in warnings], lag_ratio=0.12), FadeIn(peak), FadeIn(t2i), FadeIn(still))
        self.wait(BEAT)
        mod = motion_module(0.95).next_to(t2i, DOWN, buff=0.14)
        plug = Line(mod.get_top(), t2i.get_bottom(), color=PRIMARY, stroke_width=4)
        strip = photo_strip(os.path.join(A22, "cat.jpg"), 4, 0.72, SECONDARY, 0.08).move_to(RIGHT * 3.95 + DOWN * 1.45)
        self.play(FadeIn(mod, shift=DOWN * 0.3), Indicate(mod, color=PRIMARY))
        self.play(Create(plug), FadeOut(still), FadeIn(strip, shift=RIGHT * 0.2))
        self.play(Write(txt("keep image ability", SECONDARY, 18).next_to(strip, UP, buff=0.14)), Write(txt("add temporal ability", PRIMARY, 18).next_to(strip, DOWN, buff=0.14)))
        self.wait(LONG)


class Scene04_MarketplaceWall(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: many style cards fit as still-image painters; giving each a video model crowds the screen.
        cards = Group(*[style_card(n, p).scale(0.86) for n, p in STYLE_ASSETS]).arrange_in_grid(2, 4, buff=(0.62, 0.48)).move_to(LEFT * 0.55 + UP * 0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.06))
        self.wait(BEAT)
        stamps = VGroup(*[VGroup(box(0.86, 0.28, WARM, WARM, 0.18, 0.04), txt("IMAGE", WHITE_ISH, 11, 0.74)).move_to(c[0]).rotate(0.15) for c in cards])
        self.play(LaggedStart(*[GrowFromCenter(s) for s in stamps], lag_ratio=0.05))
        self.wait(BEAT)
        self.play(FadeOut(stamps), run_time=FAST)
        self.play(cards.animate.scale(0.72).move_to(LEFT * 3.15 + UP * 0.5))
        video_boxes = VGroup(*[box(0.68, 0.46, MUTED, BG, 0.12, 0.04) for _ in range(8)]).arrange_in_grid(2, 4, buff=(0.45, 0.42)).move_to(RIGHT * 2.15 + UP * 0.55)
        gpus = VGroup(*[gpu_stack(3, WARM).scale(0.28).next_to(v, DOWN, buff=0.08) for v in video_boxes])
        self.play(LaggedStart(*[FadeIn(v, shift=RIGHT * 0.12) for v in video_boxes], lag_ratio=0.04), LaggedStart(*[FadeIn(g) for g in gpus], lag_ratio=0.04))
        shade = Rectangle(width=14, height=8, fill_color=BG, fill_opacity=0.55, stroke_width=0).set_z_index(20)
        warning = txt("Too expensive", WARM, 38).move_to(ORIGIN).set_z_index(21)
        self.play(FadeIn(shade), FadeIn(warning, scale=1.2))
        self.wait(LONG)


class Scene05_OneEngineManyPainters(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: one blue hub sends motion outward; each style keeps its own look while becoming a strip.
        mod = motion_module(1.35).move_to(ORIGIN)
        ring = Group(*[style_card(n, p) for n, p in STYLE_ASSETS[:6]]).scale(0.88)
        positions = [UP * 2.25 + LEFT * 1.7, UP * 2.25 + RIGHT * 1.7, LEFT * 4.15 + DOWN * 0.35,
                     RIGHT * 4.15 + DOWN * 0.35, LEFT * 1.7 + DOWN * 1.95, RIGHT * 1.7 + DOWN * 1.95]
        for c, p in zip(ring, positions):
            c.move_to(p)
        self.play(GrowFromCenter(mod), Write(txt("learn motion once", PRIMARY, 20).next_to(mod, DOWN, buff=0.18)))
        self.play(LaggedStart(*[FadeIn(c) for c in ring], lag_ratio=0.06))
        self.wait(BEAT)
        lines = VGroup(*[Line(mod.get_center(), c[0].get_center(), color=PRIMARY, stroke_width=2.5) for c in ring])
        strips = Group(*[motion_photo_strip([path, path, path], 0.54, 0.42, SECONDARY, 0.05, marker=PRIMARY).scale(0.85).next_to(c, DOWN, buff=0.08) for c, (_, path) in zip(ring, STYLE_ASSETS[:6])])
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.05), LaggedStart(*[FadeIn(s) for s in strips], lag_ratio=0.05))
        self.play(Write(txt("same motion knowledge, different visual styles", SECONDARY, 22).to_edge(DOWN, buff=0.18)))
        self.wait(LONG)


class Scene06_FrozenBodyTrainableEngine(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: gradient arrows hit blue modules and bounce away from locked gray layers.
        stack = unet_stack(include_modules=True).move_to(LEFT * 0.45 + UP * 0.2)
        self.play(LaggedStart(*[FadeIn(b) for b in stack[0]], lag_ratio=0.08))
        self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(l) for l in stack[1]], lag_ratio=0.08), Write(txt("Frozen", MUTED, 20).next_to(stack, LEFT, buff=0.55)))
        self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.6) for m in stack[2]], lag_ratio=0.08), Write(txt("trainable motion modules", PRIMARY, 18).next_to(stack, DOWN, buff=0.2)))
        self.wait(BEAT)
        warm_label = txt("WARM gradient hits locked layers", WARM, 18).move_to(LEFT * 3.6 + UP * 2.4)
        accent_label = txt("ACCENT update reaches blue modules", ACCENT, 18).move_to(RIGHT * 3.1 + UP * 2.4)
        into_blue = VGroup(*[Arrow(RIGHT * 4.4, m.get_right(), color=ACCENT, buff=0.05, stroke_width=4) for m in stack[2]])
        bounce_gray = VGroup(*[Arrow(LEFT * 4.2, b.get_left(), color=WARM, buff=0.05, stroke_width=3) for b in stack[0]])
        self.play(Write(warm_label), Write(accent_label))
        self.play(LaggedStart(*[GrowArrow(a) for a in bounce_gray], lag_ratio=0.05), LaggedStart(*[GrowArrow(a) for a in into_blue], lag_ratio=0.05))
        self.play(Write(txt("Only motion modules are trained", WHITE_ISH, 25).to_edge(DOWN, buff=0.25)))
        self.wait(LONG)


class Scene07_GradientsBounceOffGray(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: a video clip moves through a training factory, then the gradient returns only to blue modules.
        conveyor = Line(LEFT * 5.6 + DOWN * 0.75, RIGHT * 5.6 + DOWN * 0.75, color=MUTED, stroke_width=3)
        stations = Group(
            photo_strip([os.path.join(A22, f"dog_{i}.jpg") for i in range(4)], 0.78, 0.56, SECONDARY, 0.05),
            label_box("VAE", 0.9, 0.55, ACCENT, 17),
            VGroup(*[Square(0.22, color=ACCENT, fill_color=ACCENT, fill_opacity=0.2) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.05),
            noise_square(3, 0.75, WARM),
            unet_stack(True).scale(0.55),
            label_box("loss", 0.85, 0.55, WARM, 18),
        ).arrange(RIGHT, buff=0.42).move_to(UP * 0.75)
        labels = VGroup(*[txt(s, WHITE_ISH, 13, 1.0).next_to(stations[i], UP, buff=0.12) for i, s in enumerate(["video", "encode", "latent", "+ noise", "T2I + motion", "compare"])])
        self.play(Create(conveyor), LaggedStart(*[FadeIn(s) for s in stations], lag_ratio=0.08), LaggedStart(*[Write(l) for l in labels], lag_ratio=0.06))
        self.wait(BEAT)
        arrows = VGroup(*[Arrow(stations[i].get_right(), stations[i + 1].get_left(), color=PRIMARY, buff=0.08, stroke_width=3) for i in range(len(stations) - 1)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08))
        self.wait(BEAT)
        grad_start = stations[-1].get_bottom() + DOWN * 0.28
        grad_end = stations[4].get_bottom() + DOWN * 0.28
        grad = DashedLine(grad_start, grad_end, color=WARM, dash_length=0.14, stroke_width=4)
        grad_dots = VGroup(*[Dot(grad_start + (grad_end - grad_start) * t, radius=0.045, color=WARM) for t in np.linspace(0.12, 0.88, 5)])
        grad_label = txt("loss signal returns to the motion stack", WARM, 16).next_to(grad, DOWN, buff=0.08)
        self.play(Create(grad), LaggedStart(*[FadeIn(d) for d in grad_dots], lag_ratio=0.08), Write(grad_label))
        gray_hits = VGroup(*[SurroundingRectangle(b, color=WARM, buff=0.02) for b in stations[4][0]])
        blue_hits = VGroup(*[SurroundingRectangle(m, color=PRIMARY, buff=0.02) for m in stations[4][2]])
        self.play(LaggedStart(*[Create(h) for h in gray_hits], lag_ratio=0.04), run_time=NORMAL)
        self.play(FadeOut(gray_hits), LaggedStart(*[Create(h) for h in blue_hits], lag_ratio=0.04), FadeIn(footer("Gradient bounces off gray, updates blue motion modules", PRIMARY, 24)))
        self.wait(LONG)


class Scene08_FourBeforeAfters(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: four large before/after rows show what temporal modeling stabilizes.
        left_head = txt("Without motion module", WARM, 24).move_to(LEFT * 2.7 + UP * 2.78)
        right_head = txt("With motion module", SECONDARY, 24).move_to(RIGHT * 2.75 + UP * 2.78)
        divider = DashedLine(UP * 2.95, DOWN * 2.65, color=MUTED, dash_length=0.14)
        yvals = [1.78, 0.72, -0.34, -1.4]
        labels = ["identity", "motion", "background", "style"]
        rows = Group()

        bad_identity = photo_strip([os.path.join(A22, "cat.jpg"), os.path.join(A22, "panda.jpg"), os.path.join(A22, "robot.jpg")], 0.72, 0.54, WARM, 0.1).move_to(LEFT * 2.45 + UP * yvals[0])
        good_identity = motion_photo_strip([os.path.join(A22, "cat.jpg")] * 3, 0.72, 0.54, SECONDARY, 0.1, marker=SECONDARY).move_to(RIGHT * 2.55 + UP * yvals[0])
        rows.add(Group(txt(labels[0], WHITE_ISH, 20, 1.35).move_to(LEFT * 5.25 + UP * yvals[0]), bad_identity, good_identity))

        bad_motion = motion_photo_strip([os.path.join(A22, "dog_0.jpg"), os.path.join(A22, "dog_4.jpg"), os.path.join(A22, "dog_1.jpg")], 0.72, 0.54, WARM, 0.1, marker=WARM).move_to(LEFT * 2.45 + UP * yvals[1])
        good_motion = motion_photo_strip(dog_paths(3), 0.72, 0.54, SECONDARY, 0.1, marker=SECONDARY).move_to(RIGHT * 2.55 + UP * yvals[1])
        rows.add(Group(txt(labels[1], WHITE_ISH, 20, 1.35).move_to(LEFT * 5.25 + UP * yvals[1]), bad_motion, good_motion))

        bad_bg = photo_strip([os.path.join(A22, "cat.jpg")] * 3, 0.72, 0.54, WARM, 0.1).move_to(LEFT * 2.45 + UP * yvals[2])
        for j, f in enumerate(bad_bg):
            f.add(Rectangle(width=0.62, height=0.22, stroke_width=0, fill_color=[MUTED, WARM, PRIMARY][j], fill_opacity=0.45).move_to(f[0].get_bottom() + UP * 0.2))
        good_bg = photo_strip([os.path.join(A22, "cat.jpg")] * 3, 0.72, 0.54, SECONDARY, 0.1).move_to(RIGHT * 2.55 + UP * yvals[2])
        for f in good_bg:
            f.add(Rectangle(width=0.62, height=0.22, stroke_width=0, fill_color=MUTED, fill_opacity=0.35).move_to(f[0].get_bottom() + UP * 0.2))
        rows.add(Group(txt(labels[2], WHITE_ISH, 20, 1.35).move_to(LEFT * 5.25 + UP * yvals[2]), bad_bg, good_bg))

        bad_style = photo_strip([os.path.join(A24, "anime_card.png"), os.path.join(A24, "cyberpunk_card.png"), os.path.join(A24, "ink_style_card.png")], 0.72, 0.54, WARM, 0.1).move_to(LEFT * 2.45 + UP * yvals[3])
        good_style = motion_photo_strip([os.path.join(A24, "anime_card.png")] * 3, 0.72, 0.54, SECONDARY, 0.1, marker=SECONDARY).move_to(RIGHT * 2.55 + UP * yvals[3])
        rows.add(Group(txt(labels[3], WHITE_ISH, 20, 1.35).move_to(LEFT * 5.25 + UP * yvals[3]), bad_style, good_style))

        self.play(Create(divider), Write(left_head), Write(right_head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08))
        self.wait(BEAT)
        for row in rows:
            self.play(Wiggle(row[1], rotation_angle=0.025), Indicate(row[2], color=SECONDARY), run_time=FAST)
        self.play(FadeIn(footer("More than movement: identity, style, layout, background", WHITE_ISH, 24)))
        self.wait(LONG)


class Scene09_IslandsToConversation(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: four isolated frame features project into temporal space, talk, then project back out updated.
        left = VGroup(*[box(0.78, 0.58, MUTED, BG, 0.08, 0.06) for _ in range(4)]).arrange(DOWN, buff=0.22).move_to(LEFT * 4.5)
        left_labels = VGroup(*[txt(f"F{i+1}", WHITE_ISH, 16).move_to(left[i]) for i in range(4)])
        funnel_in = Polygon(LEFT * 0.45 + UP * 1.15, RIGHT * 0.15 + UP * 0.45, RIGHT * 0.15 + DOWN * 0.45, LEFT * 0.45 + DOWN * 1.15, color=ACCENT).move_to(LEFT * 2.7)
        nodes = VGroup(*[Circle(0.25, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.25) for _ in range(4)]).arrange(DOWN, buff=0.28).move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.08), LaggedStart(*[Write(l) for l in left_labels], lag_ratio=0.08))
        self.wait(BEAT)
        self.play(Create(funnel_in), ReplacementTransform(VGroup(left.copy(), left_labels.copy()), nodes))
        links = VGroup()
        for i in range(4):
            for j in range(i + 1, 4):
                links.add(ArcBetweenPoints(nodes[i].get_right(), nodes[j].get_right(), angle=-0.45, color=PRIMARY, stroke_width=3))
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.06), FadeIn(txt("temporal attention", PRIMARY, 24).move_to(UP * 2.35)))
        self.wait(BEAT)
        funnel_out = funnel_in.copy().rotate(PI).move_to(RIGHT * 2.7)
        right = VGroup(*[box(0.78, 0.58, SECONDARY, BG, 0.1, 0.06) for _ in range(4)]).arrange(DOWN, buff=0.22).move_to(RIGHT * 4.5)
        right_labels = VGroup(*[txt(f"F{i+1}'", SECONDARY, 16).move_to(right[i]) for i in range(4)])
        self.play(Create(funnel_out))
        self.play(LaggedStart(*[TransformFromCopy(nodes[i], right[i]) for i in range(4)], lag_ratio=0.08), FadeIn(right_labels))
        self.play(FadeIn(footer("Frames communicate before returning to the model", PRIMARY, 25)))
        self.wait(LONG)


class Scene10_TrainSmallDeployBig(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: coarse low-res motion is learned once, then reused inside a sharper appearance model.
        coarse = VGroup(*[box(0.76, 0.76, PRIMARY, PRIMARY, 0.12, 0.06) for _ in range(4)]).arrange(RIGHT, buff=0.16).move_to(LEFT * 3.45 + UP * 0.85)
        coarse_arrows = VGroup(*[
            Arrow(c.get_center() + LEFT * 0.19 + DOWN * 0.05, c.get_center() + RIGHT * 0.2 + UP * 0.12,
                  color=PRIMARY, buff=0.02, stroke_width=3, max_tip_length_to_length_ratio=0.22)
            for c in coarse
        ])
        mod = motion_module(1.05).next_to(coarse, DOWN, buff=0.22)
        title_l = txt("256 x 256 motion blueprint", PRIMARY, 22).next_to(coarse, UP, buff=0.22)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in coarse], lag_ratio=0.07), LaggedStart(*[GrowArrow(a) for a in coarse_arrows], lag_ratio=0.07), Write(title_l))
        self.wait(BEAT)
        self.play(GrowFromCenter(mod), Write(txt("train motion here", PRIMARY, 18).next_to(mod, DOWN, buff=0.12)))
        self.wait(BEAT)
        big = machine("personalized model", 2.25, 1.0).move_to(RIGHT * 1.0 + DOWN * 0.15)
        plug = Arrow(mod.get_right(), big.get_left(), color=PRIMARY, stroke_width=4, buff=0.08)
        out = motion_photo_strip([os.path.join(A24, "anime_card.png"), os.path.join(A24, "cartoon_card.png"), os.path.join(A24, "cyberpunk_card.png"), os.path.join(A24, "fantasy_castle_card.png")], 0.88, 0.68, SECONDARY, 0.09, marker=PRIMARY).move_to(RIGHT * 3.75 + UP * 0.95)
        title_r = txt("larger image model paints detail", SECONDARY, 22).next_to(out, UP, buff=0.24)
        self.play(GrowArrow(plug), FadeIn(big))
        self.play(FadeIn(out, shift=RIGHT * 0.2), Write(title_r))
        self.wait(BEAT)
        bar = VGroup(
            box(4.3, 0.45, PRIMARY, PRIMARY, 0.16, 0.05),
            box(4.3, 0.45, SECONDARY, SECONDARY, 0.16, 0.05),
        ).arrange(RIGHT, buff=0.05).move_to(DOWN * 2.25)
        self.play(FadeIn(bar), Write(txt("motion layer", PRIMARY, 18).move_to(bar[0])), Write(txt("appearance layer", SECONDARY, 18).move_to(bar[1])))
        self.wait(LONG)


class Scene11_AnimateDiffOneBreath(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: AnimateDiff compresses into three trusted icons: locked body, trained module, reused styles.
        col = unet_stack(True).scale(0.85).move_to(LEFT * 4.0 + UP * 0.35)
        mod = motion_module(1.15).move_to(ORIGIN + UP * 0.35)
        painters = Group(*[style_card(n, p) for n, p in STYLE_ASSETS[:4]]).scale(0.48).arrange(RIGHT, buff=0.15).move_to(RIGHT * 3.65 + UP * 0.35)
        a1 = Arrow(col.get_right(), mod.get_left(), color=PRIMARY, buff=0.15, stroke_width=4)
        a2 = Arrow(mod.get_right(), painters.get_left(), color=PRIMARY, buff=0.15, stroke_width=4)
        self.play(FadeIn(col), Write(txt("1 freeze image layers", MUTED, 18).next_to(col, DOWN, buff=0.15)))
        self.wait(BEAT)
        self.play(GrowArrow(a1), GrowFromCenter(mod), Write(txt("2 train one motion module", PRIMARY, 18).next_to(mod, DOWN, buff=0.15)))
        self.wait(BEAT)
        self.play(GrowArrow(a2), FadeIn(painters), Write(txt("3 reuse across styles", SECONDARY, 18).next_to(painters, DOWN, buff=0.15)))
        self.wait(BEAT)
        fade_all(self)
        self.play(FadeIn(txt("AnimateDiff = reusable motion module for personalized T2I models", WHITE_ISH, 28).move_to(ORIGIN)))
        self.wait(LONG)


class Scene12_StillNeedsTraining(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: a good moving strip casts a dataset-and-GPU shadow, then only the zero-training question remains.
        strip = photo_strip([os.path.join(A22, f"dog_{i}.jpg") for i in range(5)], 0.92, 0.66, SECONDARY, 0.1).move_to(UP * 0.9)
        self.play(FadeIn(strip), Write(txt("works well", SECONDARY, 24).next_to(strip, DOWN, buff=0.18)))
        self.wait(BEAT)
        data = label_box("WebVid-10M", 1.8, 0.82, WARM, 19).move_to(LEFT * 2.0 + DOWN * 1.2)
        gpus = gpu_stack(6, WARM).move_to(RIGHT * 1.8 + DOWN * 1.05)
        self.play(FadeIn(data, scale=1.1), FadeIn(gpus), Write(txt("still requires motion training", WARM, 24).to_edge(DOWN, buff=0.3)))
        self.wait(BEAT)
        fade_all(self)
        add_backdrop(self)
        q = txt("Can we generate video with zero training?", ACCENT, 32).move_to(ORIGIN)
        self.play(Write(q))
        self.play(Indicate(q, color=ACCENT))
        self.wait(LONG)


class Scene13_ZeroNewWeights(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: Stable Diffusion stays locked while external inference tools steer the frames.
        sd = machine("Stable Diffusion", 3.0, 1.45, socket=False).move_to(RIGHT * 0.15 + UP * 0.05)
        lock = VGroup(
            Arc(radius=0.1, start_angle=0, angle=PI, color=MUTED, stroke_width=2),
            Rectangle(width=0.28, height=0.22, color=MUTED, stroke_width=2),
        ).arrange(DOWN, buff=-0.02).move_to(sd.get_corner(UR) + LEFT * 0.28 + DOWN * 0.22)
        unchanged = txt("weights unchanged", MUTED, 15).next_to(sd, DOWN, buff=0.14)
        stamp = txt("NO TRAINING", WARM, 28).next_to(sd, UP, buff=0.18)

        noise_tool = box(2.3, 0.72, PRIMARY, BG, 0.08, 0.1).move_to(LEFT * 4.35 + UP * 1.35)
        n1 = noise_square(20, 0.24, PRIMARY).move_to(noise_tool.get_center() + LEFT * 0.38)
        n2 = n1.copy().shift(RIGHT * 0.58 + LEFT * 0.06)
        noise_arrow = Arrow(n1.get_right(), n2.get_left(), color=PRIMARY, stroke_width=3, buff=0.02, max_tip_length_to_length_ratio=0.18)
        noise_label = txt("Tool 1: shifted noise", PRIMARY, 16).next_to(noise_tool, DOWN, buff=0.08)
        noise_icon = Group(noise_tool, n1, n2, noise_arrow, noise_label)

        anchor_tool = box(2.3, 0.72, ACCENT, BG, 0.08, 0.1).move_to(LEFT * 4.35 + DOWN * 1.15)
        mem = memory_card(0.45).move_to(anchor_tool.get_center() + LEFT * 0.48)
        rays = VGroup(*[
            Line(mem.get_right(), anchor_tool.get_right() + LEFT * 0.52 + v, color=ACCENT, stroke_width=2)
            for v in [UP * 0.2, ORIGIN, DOWN * 0.2]
        ])
        anchor_label = txt("Tool 2: attention anchor", ACCENT, 16).next_to(anchor_tool, DOWN, buff=0.08)
        anchor_icon = Group(anchor_tool, mem, rays, anchor_label)

        conn1 = Arrow(noise_icon.get_right(), sd.get_left() + UP * 0.32, color=PRIMARY, stroke_width=4, buff=0.08, max_tip_length_to_length_ratio=0.08)
        conn2 = Arrow(anchor_icon.get_right(), sd.get_left() + DOWN * 0.32, color=ACCENT, stroke_width=4, buff=0.08, max_tip_length_to_length_ratio=0.08)
        strip = motion_photo_strip(dog_paths(4), 0.72, 0.54, SECONDARY, 0.09, marker=PRIMARY).move_to(RIGHT * 4.25 + DOWN * 0.05)
        out_arrow = Arrow(sd.get_right(), strip.get_left(), color=SECONDARY, stroke_width=4, buff=0.08, max_tip_length_to_length_ratio=0.1)

        self.play(Create(sd), FadeIn(lock), FadeIn(unchanged))
        self.wait(BEAT)
        self.play(FadeIn(stamp), Indicate(sd, color=WARM))
        self.wait(BEAT)
        self.play(FadeIn(noise_icon, shift=RIGHT * 0.7), GrowArrow(conn1))
        self.wait(BEAT)
        self.play(FadeIn(anchor_icon, shift=RIGHT * 0.7), GrowArrow(conn2))
        self.wait(BEAT)
        self.play(Indicate(conn1, color=PRIMARY), Indicate(conn2, color=ACCENT))
        self.wait(BEAT)
        self.play(GrowArrow(out_arrow), FadeIn(strip, shift=RIGHT * 0.2))
        self.wait(BEAT)
        self.play(Write(footer("Text2Video-Zero = no training, only inference control", WHITE_ISH, 24)))
        self.wait(LONG)


class Scene14_StrangersVsSiblings(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: different noise squares make unrelated cats; copied-shifted noise makes a family of frames.
        top_noise = VGroup(*[noise_square(10 + i, 0.56, WARM) for i in range(4)]).arrange(RIGHT, buff=0.34).move_to(RIGHT * 1.4 + UP * 1.95)
        top = photo_strip([os.path.join(A22, "cat.jpg"), os.path.join(A22, "panda.jpg"), os.path.join(A22, "robot.jpg"), os.path.join(A22, "city.jpg")], 0.76, 0.56, WARM, 0.18).next_to(top_noise, DOWN, buff=0.34)
        bottom_parent = noise_square(30, 0.64, PRIMARY)
        bottom_noise = VGroup(*[bottom_parent.copy().shift(LEFT * 0.06 * i).scale(0.88) for i in range(4)]).arrange(RIGHT, buff=0.34).move_to(RIGHT * 1.4 + DOWN * 0.5)
        bottom_strip = VGroup(*[cat_frame(i - 1.5, SECONDARY, SECONDARY, 0.88) for i in range(4)]).arrange(RIGHT, buff=0.18).move_to(RIGHT * 1.4 + DOWN * 1.7)
        bottom_markers = VGroup(*[
            Dot(bottom_strip[i].get_center() + LEFT * (0.24 - 0.13 * i) + DOWN * 0.17, radius=0.04, color=ACCENT)
            for i in range(4)
        ])
        bottom_motion = VGroup(*[
            Arrow(bottom_strip[i].get_bottom() + DOWN * 0.12, bottom_strip[i + 1].get_bottom() + DOWN * 0.12,
                  color=PRIMARY, buff=0.07, stroke_width=2.2, max_tip_length_to_length_ratio=0.16)
            for i in range(3)
        ])
        bottom = Group(bottom_strip, bottom_markers, bottom_motion)
        bad_arrows = VGroup(*[Arrow(top_noise[i].get_bottom(), top[i].get_top(), color=WARM, buff=0.08, stroke_width=2.5) for i in range(4)])
        good_arrows = VGroup(*[Arrow(bottom_noise[i].get_bottom(), bottom_strip[i].get_top(), color=PRIMARY, buff=0.08, stroke_width=2.5) for i in range(4)])
        self.play(Write(txt("independent noise", WARM, 22).move_to(LEFT * 4.25 + UP * 1.95)), LaggedStart(*[FadeIn(n) for n in top_noise], lag_ratio=0.06))
        self.play(LaggedStart(*[GrowArrow(a) for a in bad_arrows], lag_ratio=0.04), FadeIn(top), Wiggle(top, rotation_angle=0.025))
        self.wait(BEAT)
        self.play(Write(txt("shifted copies of one noise", PRIMARY, 22).move_to(LEFT * 3.7 + DOWN * 0.5)), LaggedStart(*[FadeIn(n) for n in bottom_noise], lag_ratio=0.06))
        self.play(LaggedStart(*[GrowArrow(a) for a in good_arrows], lag_ratio=0.04))
        self.play(FadeIn(bottom_strip), FadeIn(bottom_markers), FadeIn(bottom_motion))
        self.play(Indicate(bottom_strip, color=SECONDARY), run_time=FAST)
        self.wait(LONG)


class Scene15_NoiseDragsContent(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: the noise texture shifts left, and the visible object in each output frame follows it.
        title = txt("Global motion: LEFT", PRIMARY, 24).move_to(LEFT * 4.0 + UP * 2.58)
        direction = Arrow(RIGHT * 2.25 + UP * 2.45, LEFT * 0.85 + UP * 2.45, color=PRIMARY, stroke_width=5)
        self.play(Write(title), GrowArrow(direction))
        self.wait(BEAT)
        parent = noise_square(44, 0.78, PRIMARY)
        noises = VGroup(*[parent.copy().shift(LEFT * 0.09 * i) for i in range(4)]).arrange(RIGHT, buff=0.72).move_to(UP * 1.35)
        shifts = VGroup(*[Arrow(noises[i].get_right(), noises[i + 1].get_left(), color=PRIMARY, buff=0.08, stroke_width=3) for i in range(3)])
        self.play(FadeIn(noises[0]))
        self.wait(BEAT)
        self.play(LaggedStart(*[GrowArrow(a) for a in shifts], lag_ratio=0.15), LaggedStart(*[FadeIn(n) for n in noises[1:]], lag_ratio=0.15))
        self.wait(BEAT)
        sd = machine("SD", 1.2, 0.58, socket=False).move_to(ORIGIN + DOWN * 0.05)
        guides = VGroup(*[Arrow(noises[i].get_bottom(), sd.get_top() + RIGHT * (-0.36 + i * 0.24), color=ACCENT, buff=0.06, stroke_width=2.5) for i in range(4)])
        frames = motion_photo_strip(dog_paths(4), 1.05, 0.76, SECONDARY, 0.26, marker=ACCENT, direction=RIGHT).move_to(DOWN * 1.65)
        down = VGroup(*[Arrow(sd.get_bottom() + RIGHT * (-0.36 + i * 0.24), frames[0][i].get_top(), color=ACCENT, buff=0.06, stroke_width=2.5) for i in range(4)])
        self.play(FadeIn(sd), LaggedStart(*[GrowArrow(g) for g in guides], lag_ratio=0.04))
        self.wait(BEAT)
        self.play(LaggedStart(*[GrowArrow(a) for a in down], lag_ratio=0.04), FadeIn(frames))
        self.play(FadeIn(footer("Shifted noise -> shifted content", WHITE_ISH, 28)))
        self.wait(LONG)


class Scene16_FirstFrameMemoryCard(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: frame one lifts into a yellow reference card that later artists keep looking at.
        f1 = image_card(os.path.join(A22, "cat.jpg"), 1.9, 1.35, ACCENT).move_to(LEFT * 4.1 + UP * 0.65)
        mem = memory_card(1.45).move_to(LEFT * 1.1 + UP * 0.65)
        self.play(FadeIn(f1))
        self.wait(BEAT)
        self.play(FadeIn(mem, shift=RIGHT * 0.35), Write(txt("Reference Memory", ACCENT, 22).next_to(mem, DOWN, buff=0.12)), Indicate(f1, color=ACCENT))
        easels = photo_strip(os.path.join(A22, "cat.jpg"), 3, 0.95, 0.68, SECONDARY, 0.28).move_to(RIGHT * 2.7 + DOWN * 0.55)
        for i, e in enumerate(easels):
            e.shift(UP * (0.1 * (i - 1)))
        lines = VGroup(*[Arrow(e.get_top(), mem.get_right(), color=ACCENT, buff=0.08, stroke_width=3) for e in easels])
        self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(e) for e in easels], lag_ratio=0.08), LaggedStart(*[GrowArrow(l) for l in lines], lag_ratio=0.08))
        self.play(FadeIn(footer("Same reference, different frame", SECONDARY, 26)))
        self.wait(LONG)


class Scene17_QueryChangesKVDont(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: the yellow K/V card stays fixed while blue questions change the next pose.
        mem = memory_card(1.45).move_to(LEFT * 4.0 + UP * 0.75)
        fixed = txt("FIXED: K1 / V1", ACCENT, 23).next_to(mem, UP, buff=0.18)
        self.play(FadeIn(mem), Write(fixed))
        self.wait(BEAT)
        poses = photo_strip(os.path.join(A22, "cat.jpg"), 3, 1.0, 0.7, SECONDARY, 0.28).move_to(RIGHT * 2.2 + UP * 0.55)
        qs = VGroup(*[label_box(f"Q{i+2}", 0.62, 0.38, PRIMARY, 15).next_to(poses[i], UP, buff=0.18) for i in range(3)])
        lines = VGroup(*[Arrow(q.get_left(), mem.get_right(), color=ACCENT, buff=0.06, stroke_width=3) for q in qs])
        self.play(Write(txt("CHANGING: queries", PRIMARY, 23).next_to(poses, UP, buff=0.55)), LaggedStart(*[FadeIn(q) for q in qs], lag_ratio=0.08), LaggedStart(*[FadeIn(p) for p in poses], lag_ratio=0.08))
        self.play(LaggedStart(*[GrowArrow(l) for l in lines], lag_ratio=0.06))
        self.play(FadeIn(footer("Queries change. Appearance stays anchored.", WHITE_ISH, 25)))
        self.wait(LONG)


class Scene18_TwoRiversOneCalm(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: the moving object layer separates from flickering backgrounds, which collapse into one calm plate.
        horse = os.path.join(A24, "horse_running.png")
        bg_colors = [MUTED, WARM, PRIMARY, WARM]
        strip = Group(*[image_card(horse, 0.95, 0.68, WARM) for _ in range(4)]).arrange(RIGHT, buff=0.12).move_to(LEFT * 2.8 + UP * 1.6)
        for i, f in enumerate(strip):
            f.add_to_back(Rectangle(width=0.82, height=0.5, stroke_width=0, fill_color=bg_colors[i], fill_opacity=0.5).move_to(f[0]))
            f.add(Dot(f.get_center() + RIGHT * (-0.25 + i * 0.16) + DOWN * 0.12, radius=0.06, color=ACCENT))
        self.play(Write(txt("flickering video", WARM, 21).next_to(strip, UP, buff=0.16)), LaggedStart(*[FadeIn(f) for f in strip], lag_ratio=0.05))
        self.wait(BEAT)
        flashes = VGroup(*[SurroundingRectangle(f, color=WARM, buff=0.02) for f in strip])
        self.play(LaggedStart(*[Create(f) for f in flashes], lag_ratio=0.06), Write(txt("backgrounds are different", WARM, 21).next_to(strip, DOWN, buff=0.12)))
        self.wait(BEAT)
        mask = VGroup(box(1.25, 0.86, ACCENT, BG, 0.08, 0.06), Ellipse(width=0.72, height=0.34, color=WHITE_ISH, fill_color=WHITE_ISH, fill_opacity=0.7)).move_to(RIGHT * 1.15 + UP * 1.6)
        a1 = Arrow(strip.get_right(), mask.get_left(), color=ACCENT, buff=0.16, stroke_width=3)
        self.play(FadeOut(flashes), GrowArrow(a1), FadeIn(mask), Write(txt("object mask", ACCENT, 19).next_to(mask, UP, buff=0.14)))
        self.wait(BEAT)
        foregrounds = VGroup(*[Ellipse(width=0.62, height=0.28, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.28) for _ in range(4)]).arrange(RIGHT, buff=0.15).move_to(LEFT * 2.95 + DOWN * 0.35)
        backgrounds = VGroup(*[box(0.62, 0.42, MUTED, c, 0.42, 0.04) for c in bg_colors]).arrange(RIGHT, buff=0.1).move_to(RIGHT * 1.25 + DOWN * 0.35)
        split_arrow = Arrow(mask.get_bottom(), ORIGIN + DOWN * 0.05, color=ACCENT, buff=0.12, stroke_width=3)
        self.play(GrowArrow(split_arrow), FadeIn(foregrounds), FadeIn(backgrounds),
                  Write(txt("foreground moves", SECONDARY, 17).next_to(foregrounds, UP, buff=0.1)),
                  Write(txt("backgrounds average", MUTED, 17).next_to(backgrounds, UP, buff=0.1)))
        calm = box(2.7, 0.52, SECONDARY, MUTED, 0.32, 0.05).move_to(backgrounds)
        self.play(FadeOut(backgrounds), FadeIn(calm), Indicate(calm, color=SECONDARY))
        final = motion_photo_strip([horse] * 5, 0.84, 0.6, SECONDARY, 0.1, marker=ACCENT).to_edge(DOWN, buff=0.55)
        stable_plate = Rectangle(width=final[0].width, height=0.3, stroke_width=0, fill_color=MUTED, fill_opacity=0.34).move_to(final[0].get_center()).set_z_index(-1)
        self.play(FadeOut(foregrounds), FadeOut(calm), FadeIn(final), FadeIn(stable_plate), Write(txt("moving object + stable background", SECONDARY, 22).next_to(final, UP, buff=0.1)))
        self.wait(LONG)


class Scene19_Text2VideoZeroOneBreath(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: shifted noise, memory, and mask orbit the unchanged model as controls.
        sd = machine("Stable Diffusion", 2.85, 1.22, socket=False).move_to(ORIGIN + UP * 0.2)
        unchanged = txt("unchanged weights", MUTED, 15).next_to(sd, DOWN, buff=0.1)
        self.play(Create(sd), FadeIn(unchanged))
        self.wait(BEAT)

        shifted_box = box(2.0, 0.72, PRIMARY, BG, 0.08, 0.08).move_to(LEFT * 3.95 + UP * 1.65)
        n1 = noise_square(5, 0.28, PRIMARY).move_to(shifted_box.get_center() + LEFT * 0.35)
        n2 = n1.copy().shift(RIGHT * 0.62)
        shifted = Group(shifted_box, n1, n2, Arrow(n1.get_right(), n2.get_left(), color=PRIMARY, buff=0.03, stroke_width=3),
                        txt("shifted noise", PRIMARY, 16).next_to(shifted_box, DOWN, buff=0.08))

        memory_box = box(2.0, 0.72, ACCENT, BG, 0.08, 0.08).move_to(RIGHT * 3.75 + UP * 1.65)
        memory = Group(memory_box, memory_card(0.48).move_to(memory_box), txt("first-frame K/V", ACCENT, 16).next_to(memory_box, DOWN, buff=0.08))

        mask_box = box(2.0, 0.72, SECONDARY, BG, 0.08, 0.08).move_to(DOWN * 1.45)
        mask = Group(mask_box, Ellipse(width=0.58, height=0.3, color=SECONDARY).move_to(mask_box),
                     txt("smooth background", SECONDARY, 16).next_to(mask_box, DOWN, buff=0.08))
        a1 = Arrow(shifted_box.get_right(), sd.get_corner(UL), color=PRIMARY, buff=0.12, stroke_width=3)
        a2 = Arrow(memory_box.get_left(), sd.get_corner(UR), color=ACCENT, buff=0.12, stroke_width=3)
        a3 = Arrow(mask_box.get_top(), sd.get_bottom(), color=SECONDARY, buff=0.12, stroke_width=3)
        self.play(FadeIn(shifted, shift=RIGHT * 0.25), GrowArrow(a1))
        self.wait(BEAT)
        self.play(FadeIn(memory, shift=LEFT * 0.25), GrowArrow(a2))
        self.wait(BEAT)
        self.play(FadeIn(mask, shift=UP * 0.25), GrowArrow(a3))
        self.wait(BEAT)
        strip = motion_photo_strip(dog_paths(5), 0.68, 0.5, SECONDARY, 0.08, marker=PRIMARY).move_to(RIGHT * 4.0 + DOWN * 0.35)
        out = Arrow(sd.get_right(), strip.get_left(), color=SECONDARY, buff=0.08, stroke_width=3)
        self.play(GrowArrow(out), FadeIn(strip))
        self.play(FadeIn(footer("Text2Video-Zero = no training, only inference control", WHITE_ISH, 25)))
        self.wait(LONG)


class Scene20_TheScale(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: the scale is heavier on trained motion and lighter on zero-training controls.
        beam = Line(LEFT * 4.0, RIGHT * 4.0, color=MUTED, stroke_width=5).move_to(DOWN * 0.15)
        fulcrum = Triangle(color=MUTED, fill_color=MUTED, fill_opacity=0.18).scale(0.45).move_to(DOWN * 0.8)
        self.play(Create(beam), FadeIn(fulcrum))
        self.wait(BEAT)
        left = VGroup(unet_stack(True).scale(0.38), motion_module(0.45), gpu_stack(3, WARM).scale(0.35)).arrange(RIGHT, buff=0.08).move_to(LEFT * 3.1 + UP * 0.8)
        right = VGroup(machine("SD", 0.85, 0.45, socket=False).scale(0.75), noise_square(1, 0.3), memory_card(0.34)).arrange(RIGHT, buff=0.08).move_to(RIGHT * 3.1 + UP * 0.8)
        self.play(FadeIn(left), Rotate(beam, angle=-0.08, about_point=ORIGIN), Write(txt("AnimateDiff", PRIMARY, 17).move_to(LEFT * 3.1 + DOWN * 1.35)))
        self.play(FadeIn(right), Rotate(beam, angle=0.035, about_point=ORIGIN), Write(txt("Text2Video-Zero", ACCENT, 17).move_to(RIGHT * 3.1 + DOWN * 1.35)))
        self.play(Write(txt("more training cost", PRIMARY, 17).move_to(LEFT * 3.1 + UP * 2.05)), Write(txt("no training cost", ACCENT, 17).move_to(RIGHT * 3.1 + UP * 2.05)))
        self.wait(LONG)


class Scene21_LookingOverYourShoulder(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: each later frame receives arrows from all prior frames, forming a growing causal triangle.
        isolated = motion_photo_strip(dog_paths(4), 0.88, 0.64, WARM, 0.22, marker=WARM).move_to(UP * 1.55)
        no_mem = txt("No temporal memory", WARM, 22).next_to(isolated, DOWN, buff=0.18)
        self.play(LaggedStart(*[FadeIn(b) for b in isolated], lag_ratio=0.06), Write(no_mem))
        self.wait(BEAT)
        self.play(FadeOut(isolated), FadeOut(no_mem))
        boxes = motion_photo_strip(dog_paths(4), 1.05, 0.76, PRIMARY, 0.58, marker=ACCENT).move_to(DOWN * 0.15)
        frame_strip = boxes[0]
        self.play(FadeIn(frame_strip[0]), FadeIn(boxes[1][0]))
        arrows = VGroup()
        for j in range(1, 4):
            self.play(FadeIn(frame_strip[j]), FadeIn(boxes[1][j]), run_time=FAST)
            new = VGroup(*[ArcBetweenPoints(frame_strip[i].get_top(), frame_strip[j].get_top(), angle=-PI / 2, color=PRIMARY, stroke_width=3) for i in range(j)])
            arrows.add(new)
            self.play(LaggedStart(*[Create(a) for a in new], lag_ratio=0.04))
        self.play(FadeIn(boxes[2]))
        self.play(FadeIn(footer("Later frames look back at earlier frames", PRIMARY, 25)))
        self.wait(LONG)


class Scene22_SmallPatchesGiantBuilding(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: tiny blue adapters on a huge gray building absorb all incoming gradient arrows.
        building = VGroup(box(2.7, 3.25, MUTED, MUTED, 0.12, 0.1), VGroup(*[Line(LEFT * 1.08 + UP * y, RIGHT * 1.08 + UP * y, color=BG, stroke_width=2) for y in np.linspace(-1.15, 1.15, 6)])).move_to(LEFT * 1.35 + UP * 0.1)
        self.play(FadeIn(building), Wiggle(building, rotation_angle=0.018), FadeIn(footer("training the whole model is costly", WARM, 22)))
        self.wait(BEAT)
        patches = VGroup(*[Square(0.34, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.42).move_to(building.get_center() + p) for p in [LEFT * 0.75 + UP * 0.95, RIGHT * 0.75 + UP * 0.3, LEFT * 0.45 + DOWN * 0.75]])
        self.play(LaggedStart(*[FadeIn(p, scale=1.2) for p in patches], lag_ratio=0.08), Write(txt("lightweight adapters", PRIMARY, 22).next_to(building, UP, buff=0.18)))
        arrows = VGroup(*[Arrow(RIGHT * 5.1 + UP * (1.35 - i * 0.55), p.get_center(), color=ACCENT, buff=0.08, stroke_width=4) for i, p in enumerate(patches)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06))
        latents = VGroup(*[Square(0.32, color=MUTED, fill_color=MUTED, fill_opacity=0.18) for _ in range(7)]).arrange(RIGHT, buff=0.06).move_to(RIGHT * 2.7 + DOWN * 1.45)
        self.play(FadeIn(latents))
        self.play(latents.animate.shift(RIGHT * 0.18), Write(txt("shift latents to create temporal change", PRIMARY, 17).next_to(latents, DOWN, buff=0.1)))
        self.wait(LONG)


class Scene23_TwoRiversMerge(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: a calm content river and restless motion river bend together into one finished strip.
        merge_point = RIGHT * 1.25 + UP * 0.2
        content = VMobject(color=SECONDARY, stroke_width=6).set_points_smoothly([LEFT * 5.2 + UP * 1.35, LEFT * 1.8 + UP * 1.35, merge_point])
        motion = VMobject(color=PRIMARY, stroke_width=6).set_points_smoothly([LEFT * 5.2 + DOWN * 1.35, LEFT * 1.8 + DOWN * 1.35, merge_point])
        self.play(Create(content), Write(txt("Content Stream", SECONDARY, 18).move_to(LEFT * 3.4 + UP * 1.65)))
        self.wait(BEAT)
        self.play(Create(motion), Write(txt("Motion Stream", PRIMARY, 18).move_to(LEFT * 3.4 + DOWN * 1.65)))
        icons = VGroup(Circle(0.17, color=SECONDARY), Square(0.24, color=SECONDARY), Triangle(color=SECONDARY).scale(0.18)).arrange(RIGHT, buff=0.18).move_to(LEFT * 2.7 + UP * 1.35)
        arrows = VGroup(*[Arrow(LEFT * 0.15, RIGHT * 0.15, color=PRIMARY, buff=0.01) for _ in range(3)]).arrange(RIGHT, buff=0.18).move_to(LEFT * 2.7 + DOWN * 1.35)
        self.play(FadeIn(icons), FadeIn(arrows))
        out = motion_photo_strip(dog_paths(5), 0.82, 0.6, SECONDARY, 0.08, marker=ACCENT).move_to(RIGHT * 3.75 + UP * 0.2)
        connector = Arrow(merge_point + RIGHT * 0.15, out.get_left(), color=ACCENT, buff=0.08, stroke_width=4)
        self.play(GrowArrow(connector), FadeOut(Group(icons, arrows)), FadeIn(out), FadeIn(footer("Combine content and motion", WHITE_ISH, 24)))
        self.wait(LONG)


class Scene24_BigPictureTree(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: the five mechanisms reassemble as branches of one training-efficient tree.
        root = txt("Training-Efficient Video Generation", WHITE_ISH, 24).move_to(DOWN * 2.45)
        trunk = Line(DOWN * 2.2, DOWN * 1.35, color=ACCENT, stroke_width=5)
        self.play(Write(root), Create(trunk))
        self.wait(BEAT)
        names = ["motion module", "zero-shot", "temporal attention", "adapters", "dual streams"]
        xs = [-4.3, -2.15, 0, 2.15, 4.3]
        branches = VGroup()
        nodes = VGroup()
        for x, name in zip(xs, names):
            center = np.array([x, 0.95, 0])
            node = label_box(name, 1.55, 0.58, MUTED, 13).move_to(center)
            nodes.add(node)
            branch_end = node.get_bottom() + DOWN * 0.02
            branches.add(ArcBetweenPoints(DOWN * 1.35, branch_end, angle=0.35 * (1 if x >= 0 else -1), color=ACCENT, stroke_width=3))
        self.play(LaggedStart(*[Create(b) for b in branches], lag_ratio=0.07), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.07))
        icons = VGroup(
            motion_module(0.36).next_to(nodes[0], UP, buff=0.12),
            noise_square(1, 0.34).next_to(nodes[1], UP, buff=0.12),
            VGroup(*[ArcBetweenPoints(LEFT * 0.15 * i, RIGHT * 0.15 * (i + 1), angle=-PI / 2, color=PRIMARY) for i in range(3)]).next_to(nodes[2], UP, buff=0.12),
            VGroup(*[Square(0.14, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.3) for _ in range(3)]).arrange(RIGHT, buff=0.04).next_to(nodes[3], UP, buff=0.12),
            VGroup(Line(LEFT * 0.32 + UP * 0.1, RIGHT * 0.08, color=SECONDARY), Line(LEFT * 0.32 + DOWN * 0.1, RIGHT * 0.08, color=PRIMARY)).next_to(nodes[4], UP, buff=0.12),
        )
        self.play(LaggedStart(*[FadeIn(i) for i in icons], lag_ratio=0.07))
        self.play(FadeIn(footer("Reuse image models. Add temporal consistency. Avoid full video training.", WHITE_ISH, 22)))
        self.wait(LONG)


class Scene25_ShortClipsToWholeMovies(Scene):
    def construct(self):
        self.camera.background_color = BG
        add_backdrop(self)
        # Visual answer: impressive short object clips shrink into a corner of a much larger story screen.
        paths = [os.path.join(A22, "cat.jpg"), os.path.join(A24, "horse_running.png"), os.path.join(A24, "astronaut_ski.png"), os.path.join(A24, "panda_guitar.png")]
        clips = Group(*[image_card(p, 1.22, 0.88, SECONDARY) for p in paths]).arrange(RIGHT, buff=0.18).move_to(UP * 1.55)
        short_label = txt("short object-centric videos", SECONDARY, 23).next_to(clips, DOWN, buff=0.14)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in clips], lag_ratio=0.06), Write(short_label))
        self.wait(BEAT)
        screen = box(7.0, 3.25, MUTED, BG, 0.08, 0.1).move_to(DOWN * 0.1)
        self.play(FadeOut(short_label), Create(screen), clips.animate.scale(0.5).move_to(screen.get_corner(UL) + RIGHT * 1.1 + DOWN * 0.48))
        story = VGroup(*[box(0.9, 0.6, ACCENT, BG, 0.1, 0.06) for _ in range(5)]).arrange(RIGHT, buff=0.24).move_to(screen.get_center() + UP * 0.25)
        timeline = Line(story.get_left() + DOWN * 0.5, story.get_right() + DOWN * 0.5, color=ACCENT, stroke_width=3)
        labels = VGroup(*[txt(s, WHITE_ISH, 15, 1.9) for s in ["long duration", "multiple subjects", "complex events", "story consistency", "character identity"]]).arrange(DOWN, buff=0.08).next_to(screen, RIGHT, buff=0.22)
        self.play(LaggedStart(*[FadeIn(s) for s in story], lag_ratio=0.07), Create(timeline), LaggedStart(*[Write(l) for l in labels], lag_ratio=0.05))
        self.wait(BEAT)
        self.play(FadeOut(Group(clips, screen, story, timeline, labels)), run_time=FAST)
        question = txt("Can we generate long, complex videos?", ACCENT, 32).move_to(ORIGIN)
        self.play(Write(question))
        self.play(Indicate(question, color=ACCENT))
        self.wait(LONG)
