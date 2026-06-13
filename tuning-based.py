# === PRODUCTION PLAN ===
# Core insight (one sentence): The same body of motion can wear any costume:
# one-shot tuned editing preserves a reference video's motion and structure
# while text and pretrained image knowledge repaint the appearance.
#
# Color encoding:
#   PRIMARY   = motion / skeleton layer / temporal connections / what moves
#   SECONDARY = appearance / visual identity / successful stable edited output
#   WARM      = failure / flicker / cost / instability / what breaks
#   ACCENT    = structural blueprint / DDIM guide / attention gates
#   MUTED     = frozen pretrained model / inactive background / unchanged parts
#
# Scene list:
#   Scene01_OneShot_Intro — filmstrip splits into motion and appearance layers
#   Scene02_EditingLandscape — city map of editing families, zoom to tuning
#   Scene03_TuneAVideo_Motivation — appearance library + motion video feed machine
#   Scene04_WhyNotScratch — GPU factory vs adapter bolted onto existing machine
#   Scene05_Observation1_FrameLevel — good still frames become flickering video
#   Scene06_Observation2_STAttention — isolated rooms vs cross-frame wires
#   Scene07_NetworkInflation — flat image sheet inflates into a time flipbook
#   Scene08_AttentionCostExplosion — clean token links become a tangled web
#   Scene09_WhyNotFullFineTune — disassembled robot vs Q/K/V gate tuning
#   Scene10_FrozenCastle — frozen castle with only warm Q/K/V gates
#   Scene11_DDIMInversion — photo traced into blueprint, then repainted
#   Scene12_SameMotionDifferentCharacters — same dashed choreography, new actors
#   Scene13_ActorPropBackground — actor, prop, and background swap; motion locked
#   Scene14_Ablation_Table — Tune-A-Video rests on three supports
#   Scene15_Ablation_NoSTAttn — removing ST attention makes frames disagree
#   Scene16_Ablation_NoDDIM — removing inversion makes structure drift
#   Scene17_Ablation_NoFineTune — prompt content passes, reference motion fails
#   Scene18_Dreamix_Training — movie and photo teachers train one student
#   Scene19_Dreamix_Inference — corrupt original, regenerate with prompt
#   Scene20_EI2_Stabilizer — flickering strip enters anti-flicker stabilizer
#   Scene21_VideoP2P_CrossAttention — token spotlights land on image regions
#   Scene22_Comparison_OneShot_TrainingFree — speed vs shape-change sliders
#   Scene23_OneShot_to_MultipleShot — many golf strips funnel to common skeleton
#   Scene24_MotionDirector — nouns pass, verb fails, coach teaches motion
#   Scene25_DecouplingAppearanceMotion — appearance fades, skeleton transfers
#   Scene26_FinalSummary — appearance, structure, and motion merge into editing
#
# Key transforms (moments where one thing morphs INTO another):
#   - man dribbling filmstrip -> separate skeleton/costume layers in Scene01
#   - single image square -> video flipbook stack in Scene07
#   - exploded full fine-tune machine -> intact selective Q/K/V machine in Scene09
#   - original video frame -> structural blueprint -> edited frame in Scene11
#   - Man -> Bond -> Lego -> Astronaut -> Iron Man on a fixed path in Scene12
#   - three layer plates -> Edited Video in Scene26
# ======================

from manim import *
import os
import itertools
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
A31 = os.path.join(ROOT, "images", "3.1")
A22 = os.path.join(ROOT, "images", "2.2")
A24 = os.path.join(ROOT, "images", "2.4")


def T(s, size=22, color=WHITE_ISH, max_width=11.4):
    mob = Text(s, font_size=size, color=color)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def box(w, h, color=MUTED, fill=None, opacity=0.08, radius=0.1, stroke=2):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, color=color, stroke_width=stroke,
        fill_color=fill or color, fill_opacity=opacity
    )


def line_arrow(start, end, color=MUTED, width=3):
    return Arrow(start, end, color=color, buff=0.08, stroke_width=width, max_tip_length_to_length_ratio=0.14)


def img(path, w=None, h=None):
    mob = ImageMobject(path)
    if w is not None:
        mob.scale_to_fit_width(w)
    if h is not None and mob.height > h:
        mob.scale_to_fit_height(h)
    return mob


def image_frame(path, w=1.4, h=1.4, color=SECONDARY, opacity=0.08):
    b = box(w, h, color, BG, opacity, 0.08, 2)
    im = img(path, w - 0.12, h - 0.12).move_to(b)
    return Group(b, im)


def frame_slot(w=1.25, h=1.45, color=MUTED):
    return box(w, h, color, BG, 0.08, 0.08, 2)


def filmstrip_from_image(path, n=4, w=1.1, h=1.25, color=SECONDARY, buff=0.13):
    frames = Group(*[image_frame(path, w, h, color) for _ in range(n)]).arrange(RIGHT, buff=buff)
    rail = Line(frames.get_left() + DOWN * (h / 2 + 0.18), frames.get_right() + DOWN * (h / 2 + 0.18), color=color, stroke_width=2)
    arrows = VGroup(*[
        line_arrow(frames[i].get_right(), frames[i + 1].get_left(), color, 2)
        for i in range(n - 1)
    ])
    return Group(frames, rail, arrows)


def stick_figure(color=PRIMARY, scale=1, pose=0):
    head = Circle(0.12, color=color, stroke_width=3).shift(UP * 0.48)
    spine = Line(UP * 0.35, DOWN * 0.25, color=color, stroke_width=3)
    arms = VGroup(
        Line(UP * 0.15, LEFT * (0.35 + 0.05 * pose) + DOWN * 0.08, color=color, stroke_width=3),
        Line(UP * 0.12, RIGHT * (0.34 - 0.03 * pose) + DOWN * 0.16, color=color, stroke_width=3),
    )
    legs = VGroup(
        Line(DOWN * 0.25, LEFT * (0.28 - 0.04 * pose) + DOWN * 0.7, color=color, stroke_width=3),
        Line(DOWN * 0.25, RIGHT * (0.34 + 0.05 * pose) + DOWN * 0.65, color=color, stroke_width=3),
    )
    ball = Circle(0.09, color=color, fill_color=color, fill_opacity=0.35).shift(RIGHT * 0.42 + DOWN * (0.52 + 0.08 * pose))
    return VGroup(head, spine, arms, legs, ball).scale(scale)


def ski_skeleton(color=PRIMARY, scale=1):
    body = VGroup(
        Circle(0.12, color=color, stroke_width=3).shift(UP * 0.5),
        Line(UP * 0.38, DOWN * 0.1, color=color, stroke_width=3),
        Line(DOWN * 0.08, LEFT * 0.5 + DOWN * 0.55, color=color, stroke_width=3),
        Line(DOWN * 0.08, RIGHT * 0.55 + DOWN * 0.55, color=color, stroke_width=3),
        Line(LEFT * 0.75 + DOWN * 0.65, RIGHT * 0.8 + DOWN * 0.65, color=color, stroke_width=3),
        Line(UP * 0.15, LEFT * 0.55 + DOWN * 0.05, color=color, stroke_width=3),
        Line(UP * 0.12, RIGHT * 0.55 + DOWN * 0.02, color=color, stroke_width=3),
    )
    return body.scale(scale)


def golf_skeleton(color=PRIMARY, scale=1):
    body = VGroup(
        Circle(0.12, color=color, stroke_width=3).shift(UP * 0.48),
        Line(UP * 0.35, DOWN * 0.05, color=color, stroke_width=3),
        Line(DOWN * 0.05, LEFT * 0.35 + DOWN * 0.65, color=color, stroke_width=3),
        Line(DOWN * 0.05, RIGHT * 0.35 + DOWN * 0.65, color=color, stroke_width=3),
        Line(UP * 0.18, RIGHT * 0.72 + UP * 0.35, color=color, stroke_width=3),
        Line(RIGHT * 0.72 + UP * 0.35, RIGHT * 1.12 + UP * 0.75, color=ACCENT, stroke_width=3),
        ArcBetweenPoints(LEFT * 0.65 + UP * 0.35, RIGHT * 1.0 + DOWN * 0.48, angle=-TAU / 3, color=color, stroke_width=3),
    )
    return body.scale(scale)


def lock_icon(color=WHITE_ISH, scale=1):
    shackle = Arc(radius=0.15, start_angle=0, angle=PI, color=color, stroke_width=3).shift(UP * 0.08)
    body = box(0.34, 0.24, color, color, 0.18, 0.03, 1).shift(DOWN * 0.07)
    return VGroup(shackle, body).scale(scale)


def gpu_chip(scale=1):
    b = box(0.58, 0.36, WARM, WARM, 0.16, 0.05, 2)
    label = T("GPU", 8, WHITE_ISH).move_to(b)
    pins = VGroup()
    for y in [-0.12, 0, 0.12]:
        pins.add(Line(b.get_left() + UP * y, b.get_left() + LEFT * 0.09 + UP * y, color=WARM, stroke_width=1))
        pins.add(Line(b.get_right() + UP * y, b.get_right() + RIGHT * 0.09 + UP * y, color=WARM, stroke_width=1))
    return VGroup(pins, b, label).scale(scale)


def card_text(label, w=1.2, h=0.55, color=SECONDARY, size=14):
    b = box(w, h, color, color, 0.12, 0.06, 2)
    t = T(label, size, WHITE_ISH, w - 0.12).move_to(b)
    return VGroup(b, t)


def costume(label, color=SECONDARY):
    torso = box(0.55, 0.75, color, color, 0.25, 0.08, 2)
    head = Circle(0.14, color=color, fill_color=color, fill_opacity=0.18).next_to(torso, UP, buff=0.04)
    lab = T(label, 11, color, 0.9).next_to(torso, DOWN, buff=0.04)
    return VGroup(torso, head, lab)


def pulse_lines_between(frames, color=PRIMARY):
    lines = VGroup()
    for i in range(len(frames) - 1):
        a = frames[i].get_center()
        b = frames[i + 1].get_center()
        for dy in [0.36, 0.05, -0.38]:
            lines.add(Line(a + UP * dy, b + UP * dy, color=color, stroke_width=2))
    return lines


def simple_table():
    top = Rectangle(width=5.0, height=0.34, color=MUTED, fill_color=MUTED, fill_opacity=0.35).move_to(UP * 0.45)
    title = T("Tune-A-Video", 20).move_to(top)
    legs = VGroup(
        Rectangle(width=0.32, height=2.15, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.25).move_to(LEFT * 1.85 + DOWN * 0.75),
        Rectangle(width=0.32, height=2.15, color=ACCENT, fill_color=ACCENT, fill_opacity=0.25).move_to(DOWN * 0.75),
        Rectangle(width=0.32, height=2.15, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.25).move_to(RIGHT * 1.85 + DOWN * 0.75),
    )
    labels = VGroup(
        T("ST-Attn", 14, SECONDARY).next_to(legs[0], DOWN, buff=0.1),
        T("DDIM Inv.", 14, ACCENT).next_to(legs[1], DOWN, buff=0.1),
        T("Fine-Tuning", 14, PRIMARY).next_to(legs[2], DOWN, buff=0.1),
    )
    strip = Group(*[image_frame(os.path.join(A31, "cat_cheeseburger_beach.png"), 0.82, 0.62, SECONDARY) for _ in range(4)]).arrange(RIGHT, buff=0.08).next_to(top, UP, buff=0.1)
    return Group(top, title, legs, labels, strip)


def checklist(items, colors, w=3.1, h=2.4):
    b = box(w, h, WHITE_ISH, BG, 0.08, 0.12, 2)
    rows = VGroup(*[T(s, 16, c, w - 0.3) for s, c in zip(items, colors)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    rows.move_to(b)
    return VGroup(b, rows)


def clean_up(scene):
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=FAST)


class Scene01_OneShot_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the video splits into a motion skeleton layer and a costume layer; only costumes change.
        rail = Line([-6, -2.5, 0], [6, -2.5, 0], color=MUTED)
        xs = [-4.5, -1.5, 1.5, 4.5]
        frames = Group(*[image_frame(os.path.join(A31, "man_dribbling.png"), 1.6, 2.0, MUTED) for _ in xs])
        for f, x in zip(frames, xs):
            f.move_to([x, 0.2, 0])
        prompt = T('"A man dribbling a basketball"', 16, MUTED).move_to(UP * 2.7)
        arrows = VGroup(*[line_arrow(frames[i].get_right(), frames[i + 1].get_left(), MUTED, 2) for i in range(3)])
        self.play(Create(rail), LaggedStart(*[GrowFromCenter(f[0]) for f in frames], lag_ratio=0.18), LaggedStart(*[FadeIn(f[1]) for f in frames], lag_ratio=0.18))
        self.wait(BEAT)
        self.play(Write(prompt)); self.wait(BEAT)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2)); self.wait(BEAT)

        split = DashedLine([0, 3.5, 0], [0, -3.5, 0], color=MUTED)
        self.play(FadeOut(rail), FadeOut(prompt), FadeOut(arrows), frames.animate.scale(0.42).shift(UP * 2.55), Create(split))
        self.wait(BEAT)
        left_header = T("Motion layer", 17, PRIMARY).move_to([-3.35, 2.8, 0])
        right_header = T("Appearance layer", 17, SECONDARY).move_to([3.35, 2.8, 0])
        left_frames = VGroup()
        for i, x in enumerate([-5.15, -3.95, -2.75, -1.55]):
            slot = frame_slot(1.02, 1.36, PRIMARY).move_to([x, 0.25, 0])
            sk = stick_figure(PRIMARY, 0.65, i - 1.5).move_to(slot)
            lab = T(f"F{i+1}", 11, PRIMARY).next_to(slot, DOWN, buff=0.07)
            left_frames.add(VGroup(slot, sk, lab))
        right_frames = VGroup()
        for x in [1.55, 2.75, 3.95, 5.15]:
            slot = frame_slot(1.02, 1.36, SECONDARY).move_to([x, 0.25, 0])
            c = costume("Man", MUTED).scale(0.72).move_to(slot)
            right_frames.add(VGroup(slot, c))
        self.play(FadeIn(left_header), FadeIn(right_header)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(g[0]) for g in left_frames], lag_ratio=0.15), LaggedStart(*[Create(g[1]) for g in left_frames], lag_ratio=0.15), LaggedStart(*[FadeIn(g[2]) for g in left_frames], lag_ratio=0.15))
        self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(g) for g in right_frames], lag_ratio=0.15)); self.wait(BEAT)
        for name, col in [("James Bond", SECONDARY), ("Astronaut", ACCENT), ("Iron Man", WARM)]:
            new = VGroup(*[costume(name, col).scale(0.68).move_to(g[0]) for g in right_frames])
            self.play(*[ReplacementTransform(right_frames[i][1], new[i]) for i in range(4)], Wiggle(left_frames, rotation_angle=0.05), run_time=NORMAL)
            for i in range(4):
                right_frames[i][1] = new[i]
            self.wait(BEAT)
        msg = T("Same motion. Different identity.", 32).move_to(DOWN * 3.0)
        self.play(FadeIn(msg, shift=UP * 0.2)); self.wait(LONG)


class Scene02_EditingLandscape(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: video editing is a city map; the story drives into the tuning workshop district.
        hub = VGroup(box(2.4, 1.0, ACCENT, ACCENT, 0.12, 0.15, 2), T("Video Editing", 18)).move_to(ORIGIN)
        districts = [
            ("Training-Free Street", [-4.2, 2.2, 0], MUTED),
            ("Tuning-Based Workshop", [4.2, 2.2, 0], PRIMARY),
            ("Controlled Editing Room", [-5.0, 0, 0], MUTED),
            ("Multimodal Hub", [-4.2, -2.2, 0], MUTED),
            ("3D Studio", [4.2, -2.2, 0], MUTED),
        ]
        boxes = VGroup()
        roads = VGroup()
        for label, pos, col in districts:
            b = VGroup(box(2.2, 0.85, col, BG, 0.08, 0.1, 2), T(label, 13, WHITE_ISH, 2.0)).move_to(pos)
            boxes.add(b)
            roads.add(Line(hub.get_center(), b.get_center(), color=MUTED, stroke_width=2.5))
        self.play(GrowFromCenter(hub[0]), Write(hub[1])); self.wait(BEAT)
        self.play(LaggedStart(*[Create(r) for r in roads], lag_ratio=0.2)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.18)); self.wait(BEAT)
        note = T("Several families of methods", 17, MUTED).move_to(DOWN * 3.1)
        self.play(FadeIn(note)); self.wait(BEAT)
        self.play(*[boxes[i][0].animate.set_stroke(MUTED, opacity=0.2) for i in [0, 2, 3, 4]], *[roads[i].animate.set_opacity(0.15) for i in [0, 2, 3, 4]], boxes[1][0].animate.set_stroke(PRIMARY, width=3))
        self.wait(BEAT)
        self.play(self.camera.frame.animate.move_to([4.2, 2.2, 0]).scale(0.55), run_time=SLOW)
        self.wait(BEAT)
        focus = T("methods that adapt the model to the video", 15, PRIMARY, 3.0).next_to(boxes[1], DOWN, buff=0.18)
        self.play(FadeIn(focus)); self.wait(LONG)


class Scene03_TuneAVideo_Motivation(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: appearance cards and one reference motion strip enter the same machine and leave as one edited video.
        machine = VGroup(box(2.8, 1.8, MUTED, BG, 0.12, 0.2, 2), T("Tune-A-Video", 18)).move_to([0, 0.2, 0])
        self.play(GrowFromCenter(machine[0]), Write(machine[1])); self.wait(BEAT)
        library = Group(box(2.8, 2.2, SECONDARY, BG, 0.08, 0.15, 2), T("Appearance Library", 14, SECONDARY))
        cards = Group(
            card_text("Spider-Man", 0.78, 0.42, SECONDARY, 9),
            card_text("Astronaut", 0.78, 0.42, SECONDARY, 9),
            card_text("James Bond", 0.78, 0.42, SECONDARY, 9),
            image_frame(os.path.join(A24, "cartoon_card.png"), 0.78, 0.48, SECONDARY),
            image_frame(os.path.join(A24, "anime_card.png"), 0.78, 0.48, SECONDARY),
            image_frame(os.path.join(A24, "cyberpunk_card.png"), 0.78, 0.48, SECONDARY),
        ).arrange_in_grid(2, 3, buff=(0.08, 0.1))
        cards.move_to(library[0].get_center() + DOWN * 0.12)
        library[1].next_to(library[0], UP, buff=0.08)
        library.add(cards).move_to([-4.5, 1.35, 0])
        self.play(FadeIn(library, shift=RIGHT * 1.2)); self.wait(BEAT)
        self.play(Indicate(library[0], color=SECONDARY)); self.wait(BEAT)
        arr1 = line_arrow(library[0].get_right(), machine[0].get_left(), SECONDARY, 4)
        self.play(GrowArrow(arr1), Flash(machine[0].get_left(), color=SECONDARY)); self.wait(BEAT)
        strip = filmstrip_from_image(os.path.join(A31, "man_skiing.png"), 3, 1.08, 1.16, PRIMARY, 0.1).move_to([-1.0, -2.0, 0])
        lab = T("Reference Video", 14, PRIMARY).next_to(strip, DOWN, buff=0.08)
        self.play(FadeIn(strip, shift=UP * 1.0), FadeIn(lab)); self.wait(BEAT)
        sk = ski_skeleton(PRIMARY, 0.38).move_to(strip[0][1])
        self.play(Create(sk)); self.wait(BEAT)
        arr2 = line_arrow(strip.get_top(), machine[0].get_bottom(), PRIMARY, 4)
        self.play(GrowArrow(arr2), Flash(machine[0].get_bottom(), color=PRIMARY)); self.wait(BEAT)
        out = image_frame(os.path.join(A31, "redblue_skiing.png"), 1.9, 1.9, SECONDARY).move_to([4.55, 0.2, 0])
        out_lab = T("new appearance,\nsame ski motion", 13, SECONDARY).next_to(out, DOWN, buff=0.08)
        arr3 = line_arrow(machine[0].get_right(), out[0].get_left(), MUTED, 3)
        self.play(GrowArrow(arr3), GrowFromCenter(out), FadeIn(out_lab)); self.wait(BEAT)
        msg = T("Appearance from T2I.  Motion from reference video.", 18).move_to(DOWN * 3.2)
        self.play(Write(msg)); self.wait(LONG)


class Scene04_WhyNotScratch(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: building a GPU factory is different from docking a small video adapter onto a frozen machine.
        div = DashedLine([0, 3.5, 0], [0, -3.5, 0], color=MUTED)
        left_h = T("Train from scratch", 18, WARM).move_to([-3.2, 3.0, 0])
        right_h = T("One-shot tuning", 18, SECONDARY).move_to([3.2, 3.0, 0])
        self.play(Create(div), FadeIn(left_h), FadeIn(right_h)); self.wait(BEAT)
        gpus = VGroup(*[gpu_chip(0.88).move_to([-4.25 + j * 0.95, 1.65 - i * 0.48, 0]) for i in range(4) for j in range(3)])
        cables = VGroup(*[Line(gpus[i].get_right(), gpus[i + 1].get_left(), color=WARM, stroke_width=1) for i in range(len(gpus) - 1) if (i + 1) % 3])
        self.play(LaggedStart(*[GrowFromCenter(g) for g in gpus], lag_ratio=0.04), Create(cables)); self.wait(BEAT)
        tri = Triangle(color=WARM, fill_color=WARM, fill_opacity=0.12).scale(0.5)
        warn = VGroup(tri, T("!", 28, WARM).move_to(tri)).move_to([-5.35, 1.05, 0])
        self.play(GrowFromCenter(warn)); self.wait(BEAT)
        expensive = VGroup(box(2.25, 0.58, WARM, BG, 0.08), T("Too expensive", 22, WARM)).move_to([-3.25, -0.65, 0])
        clock = VGroup(Circle(0.25, color=WARM), Line(ORIGIN, UP * 0.16, color=WARM), Line(ORIGIN, RIGHT * 0.12, color=WARM), T("Years", 12, WARM).shift(DOWN * 0.45)).move_to([-3.25, -1.75, 0])
        self.play(FadeIn(expensive), GrowFromCenter(clock)); self.wait(BEAT)
        model = VGroup(box(2.6, 1.6, MUTED, BG, 0.08, 0.15), T("Pretrained T2I Model", 14, MUTED), lock_icon().scale(0.7).shift(RIGHT * 0.95 + UP * 0.45)).move_to([3.0, 1.0, 0])
        self.play(GrowFromCenter(model)); self.wait(BEAT)
        adapter = VGroup(box(1.6, 0.6, PRIMARY, PRIMARY, 0.22, 0.1), T("Video Adapter", 13)).move_to([3.0, -0.4, 0])
        plug = Line(model[0].get_bottom(), adapter[0].get_top(), color=ACCENT, stroke_width=4)
        self.play(FadeIn(adapter, shift=UP * 0.8), Create(plug), Flash(plug, color=ACCENT)); self.wait(BEAT)
        wins = VGroup(*[T(s, 14, SECONDARY) for s in ["Fast  ✓", "Stable  ✓", "Preserves knowledge  ✓"]]).arrange(DOWN, buff=0.22).move_to([3.0, -1.9, 0])
        self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.3) for w in wins], lag_ratio=0.3)); self.wait(LONG)


class Scene05_Observation1_FrameLevel(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: each still frame passes by itself; as a timeline, the same frames visibly disagree.
        prompt = T('"A man is running on the beach"', 16, MUTED).move_to(UP * 2.7)
        cards = Group(*[image_frame(os.path.join(A31, "man_running_beach.png"), 1.68, 1.9, WHITE_ISH) for _ in range(4)])
        cards.arrange(RIGHT, buff=1.0).move_to(UP * 0.8)
        cards[1][1].set_opacity(0.75)
        cards[2][1].shift(RIGHT * 0.08)
        cards[3][1].scale(0.88)
        checks = VGroup(*[T("✓", 30, SECONDARY).next_to(c, UP, buff=0.08) for c in cards])
        self.play(Write(prompt)); self.wait(BEAT)
        self.play(LaggedStart(*[GrowFromCenter(c[0]) for c in cards], lag_ratio=0.2), LaggedStart(*[FadeIn(c[1]) for c in cards], lag_ratio=0.2)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.15)); self.wait(BEAT)
        good = T("Each image can show the action.", 18, SECONDARY).move_to(UP * 3.18)
        self.play(FadeIn(good)); self.wait(BEAT)
        small = cards.copy().scale(0.7).move_to(DOWN * 1.25)
        rail = Line([-5.5, -2.25, 0], [5.5, -2.25, 0], color=MUTED)
        self.play(Create(rail), LaggedStart(*[FadeIn(s) for s in small], lag_ratio=0.12)); self.wait(BEAT)
        around = SurroundingRectangle(small, color=WARM)
        self.play(Create(around), Wiggle(small, rotation_angle=0.1, n_wiggles=5)); self.wait(BEAT)
        bad = T("But the images do not agree with each other.", 18, WARM).move_to(DOWN * 2.75)
        self.play(FadeIn(bad)); self.wait(BEAT)
        verdict = T("Good frames  ≠  good video", 34, WARM).move_to(DOWN * 3.32)
        self.play(FadeIn(verdict, shift=UP * 0.2)); self.wait(LONG)


class Scene06_Observation2_STAttention(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: isolated rooms produce unrelated frames; glowing wires let frame tokens remember each other.
        top_h = T("Spatial attention only", 17, WARM).move_to(UP * 2.85)
        top = VGroup()
        for i, x in enumerate([-4.5, -1.5, 1.5, 4.5]):
            slot = frame_slot(1.3, 1.5, MUTED).move_to([x, 1.45, 0])
            sk = stick_figure(MUTED, 0.7, i - 1.5).move_to(slot)
            top.add(VGroup(slot, sk))
        self.play(Write(top_h), LaggedStart(*[GrowFromCenter(g[0]) for g in top], lag_ratio=0.2), LaggedStart(*[Create(g[1]) for g in top], lag_ratio=0.2)); self.wait(BEAT)
        self.play(LaggedStart(*[Indicate(g[0], color=WARM) for g in top], lag_ratio=0.15)); self.wait(BEAT)
        isolated = T("isolated rooms", 13, WARM).move_to(UP * 0.43)
        self.play(FadeIn(isolated)); self.wait(BEAT)
        div = DashedLine([-6, 0, 0], [6, 0, 0], color=MUTED)
        self.play(Create(div)); self.wait(BEAT)
        bot_h = T("Spatio-temporal attention", 17, PRIMARY).move_to(DOWN * 2.85)
        bot = VGroup()
        for x in [-4.5, -1.5, 1.5, 4.5]:
            slot = frame_slot(1.3, 1.5, PRIMARY).move_to([x, -1.35, 0])
            sk = stick_figure(PRIMARY, 0.7, 0).move_to(slot)
            bot.add(VGroup(slot, sk))
        self.play(Write(bot_h), LaggedStart(*[GrowFromCenter(g[0]) for g in bot], lag_ratio=0.2), LaggedStart(*[Create(g[1]) for g in bot], lag_ratio=0.2)); self.wait(BEAT)
        wires = pulse_lines_between([b[0] for b in bot], PRIMARY)
        self.play(LaggedStart(*[Create(w) for w in wires[:3]], lag_ratio=0.25)); self.wait(BEAT)
        self.play(LaggedStart(*[Create(w) for w in wires[3:]], lag_ratio=0.16)); self.wait(BEAT)
        memory = T("frames share memory", 13, SECONDARY).move_to(DOWN * 2.55)
        self.play(FadeIn(memory)); self.wait(BEAT)
        self.play(Indicate(wires, color=PRIMARY)); self.wait(BEAT)
        msg = T("Temporal consistency comes from communication between frames.", 17).move_to(DOWN * 3.2)
        self.play(Write(msg)); self.wait(LONG)


class Scene07_NetworkInflation(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: a flat spatial sheet gains a new time depth and the kernel sweeps through the stack.
        img_square = Square(2.0, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.12).move_to([-3.5, 0.45, 0])
        axes = VGroup(Arrow(img_square.get_corner(DL), img_square.get_corner(DR) + RIGHT * 0.25, color=MUTED, buff=0.02), Arrow(img_square.get_corner(DL), img_square.get_corner(UL) + UP * 0.25, color=MUTED, buff=0.02))
        labels = VGroup(T("W", 14, MUTED).next_to(axes[0], RIGHT, buff=0.04), T("H", 14, MUTED).next_to(axes[1], UP, buff=0.04), T("H × W\n(single image)", 14).next_to(img_square, DOWN, buff=0.2))
        kernel = VGroup(*[Square(0.22, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.35) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.02).move_to(img_square.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.45)
        self.play(Create(axes), GrowFromCenter(img_square), FadeIn(kernel), Write(labels)); self.wait(BEAT)
        self.play(kernel.animate.shift(RIGHT * 0.7)); self.play(kernel.animate.shift(DOWN * 0.7)); self.wait(BEAT)
        arr = line_arrow([-1.5, 0.45, 0], [0.8, 0.45, 0], PRIMARY, 4)
        inf = T("inflation", 13, PRIMARY).next_to(arr, UP, buff=0.08)
        self.play(GrowArrow(arr), Write(inf)); self.wait(BEAT)
        front = Square(1.8, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.12).move_to([2.1, 0.35, 0])
        t_axis = Arrow([1.25, -1.15, 0], [4.9, 1.75, 0], color=PRIMARY, buff=0.02, stroke_width=4)
        self.play(GrowFromCenter(front), Create(t_axis), FadeIn(T("T  (time)", 14, PRIMARY).next_to(t_axis.get_end(), RIGHT, buff=0.04))); self.wait(BEAT)
        stack = VGroup(*[front.copy().shift(RIGHT * 0.25 * i + UP * 0.22 * i) for i in range(1, 6)])
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.25 + UP * 0.22) for s in stack], lag_ratio=0.22)); self.wait(BEAT)
        k3d = VGroup(*[Rectangle(width=0.24, height=0.08, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.4).shift(RIGHT * 0.05 * i + UP * 0.05 * i) for i in range(3)]).move_to(front)
        self.play(FadeIn(k3d)); self.play(k3d.animate.shift(RIGHT * 0.5 + UP * 0.45), run_time=SLOW); self.wait(BEAT)
        bar = VGroup(card_text("2D conv: space only", 2.4, 0.45, MUTED, 13), T("→", 24, PRIMARY), card_text("pseudo-3D conv: space + time", 3.0, 0.45, PRIMARY, 13)).arrange(RIGHT, buff=0.18).move_to(DOWN * 2.75)
        self.play(GrowFromEdge(bar, LEFT)); self.wait(BEAT)
        msg = T("Image model: space only.  Video model: space + time.", 18).move_to(DOWN * 3.25)
        self.play(FadeIn(msg)); self.wait(LONG)


class Scene08_AttentionCostExplosion(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: a tiny attention graph is clean; video full attention becomes a tangled web until sparse links remain.
        single = box(1.2, 1.2, WHITE_ISH, BG, 0.05).move_to([-4.0, 0.6, 0])
        dots = VGroup(*[Dot(single.get_center() + np.array([x, y, 0]), radius=0.08, color=PRIMARY) for x, y in [(-0.35, -0.35), (-0.35, 0.35), (0.35, -0.35), (0.35, 0.35)]])
        links = VGroup(*[Line(a.get_center(), b.get_center(), color=MUTED, stroke_width=1.3) for a, b in itertools.combinations(dots, 2)])
        self.play(GrowFromCenter(single), FadeIn(dots)); self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.15)); self.wait(BEAT)
        self.play(Write(T("Single image\n4 tokens", 13).next_to(single, DOWN, buff=0.18))); self.wait(BEAT)
        arrow = line_arrow([-2.9, 0.6, 0], [-1.55, 0.6, 0], PRIMARY, 3)
        self.play(GrowArrow(arrow), Write(T("video", 13, PRIMARY).next_to(arrow, UP, buff=0.04))); self.wait(BEAT)
        frames = VGroup(*[frame_slot(0.88, 1.2, MUTED) for _ in range(4)]).arrange(RIGHT, buff=0.1).move_to([0.8, 0.6, 0])
        tokens = VGroup()
        for f in frames:
            for x in [-0.22, 0, 0.22]:
                for y in [-0.28, 0.28]:
                    tokens.add(Dot(f.get_center() + RIGHT * x + UP * y, radius=0.045, color=PRIMARY))
        self.play(LaggedStart(*[GrowFromCenter(f) for f in frames], lag_ratio=0.18), LaggedStart(*[FadeIn(d) for d in tokens], lag_ratio=0.02)); self.wait(BEAT)
        all_lines = VGroup()
        for i in range(0, len(tokens), 3):
            for j in range(i + 1, len(tokens), 4):
                all_lines.add(Line(tokens[i].get_center(), tokens[j].get_center(), color=WARM, stroke_width=0.55, stroke_opacity=0.55))
        self.play(LaggedStart(*[Create(l) for l in all_lines], lag_ratio=0.004), run_time=2.5); self.wait(BEAT)
        self.play(FadeIn(T("24 × 24 = 576 pairs", 11, WARM).next_to(frames, DOWN, buff=0.18)))
        self.wait(BEAT)
        warn = T("Full attention: explodes.", 18, WARM).move_to(DOWN * 2.0)
        self.play(FadeIn(warn), Wiggle(frames, rotation_angle=0.05)); self.wait(BEAT)
        sparse = VGroup(*[Line(tokens[i].get_center(), tokens[i + 6].get_center(), color=PRIMARY, stroke_width=2) for i in range(6)])
        self.play(FadeOut(all_lines), Create(sparse)); self.wait(BEAT)
        self.play(FadeIn(T("Sparse attention", 13, PRIMARY).next_to(frames, DOWN, buff=0.45)))
        self.wait(BEAT)
        ok = T("Use sparse connections to make it manageable.", 17, SECONDARY).move_to(DOWN * 2.55)
        self.play(FadeIn(ok)); self.wait(LONG)


class Scene09_WhyNotFullFineTune(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: full fine-tuning scatters the model; selective tuning keeps it intact and adjusts only three gates.
        div = DashedLine([0, 3.5, 0], [0, -3.5, 0], color=MUTED)
        self.play(Create(div), FadeIn(T("Full fine-tuning", 18, WARM).move_to([-3.1, 3, 0])), FadeIn(T("Selective tuning", 18, SECONDARY).move_to([3.1, 3, 0]))); self.wait(BEAT)
        core = box(2.0, 1.35, WARM, BG, 0.1).move_to([-3.25, 0.95, 0])
        blocks = VGroup(*[box(0.42, 0.28, WARM, WARM, 0.18, 0.04).move_to(core).shift(v) for v in [LEFT * 0.62 + UP * 0.42, RIGHT * 0.6 + UP * 0.38, LEFT * 0.62 + DOWN * 0.38, RIGHT * 0.58 + DOWN * 0.34, UP * 0.68]])
        self.play(GrowFromCenter(core), FadeIn(blocks)); self.wait(BEAT)
        self.play(LaggedStart(*[b.animate.shift((b.get_center() - core.get_center()) * 0.9) for b in blocks], lag_ratio=0.1)); self.wait(BEAT)
        trap = DashedVMobject(SurroundingRectangle(VGroup(core, blocks), color=WARM, buff=0.18))
        self.play(Create(trap)); self.wait(BEAT)
        left_notes = VGroup(T("slow", 16, WARM), T("expensive", 16, WARM), T("overfits one clip", 16, WARM)).arrange(DOWN, buff=0.18).move_to([-3.25, -1.35, 0])
        self.play(LaggedStart(*[FadeIn(n) for n in left_notes], lag_ratio=0.18)); self.wait(BEAT)

        tower = box(2.65, 2.45, MUTED, BG, 0.08).move_to([3.05, 0.6, 0])
        rows = VGroup(*[box(1.55, 0.3, MUTED, MUTED, 0.14, 0.04).move_to([2.75, 1.45 - i * 0.48, 0]) for i in range(4)])
        snow = VGroup(*[Star(n=6, outer_radius=0.08, inner_radius=0.035, color=MUTED, fill_color=MUTED, fill_opacity=0.45).move_to(r.get_left() + RIGHT * 0.18) for r in rows])
        self.play(GrowFromCenter(tower), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08), FadeIn(snow)); self.wait(BEAT)
        gates = VGroup(*[card_text(s, 0.5, 0.32, ACCENT, 13).move_to([4.12, 1.22 - i * 0.48, 0]) for i, s in enumerate(["Q", "K", "V"])])
        gate_arrows = VGroup(*[line_arrow(rows[i].get_right(), gates[i].get_left(), ACCENT, 2) for i in range(3)])
        self.play(LaggedStart(*[GrowArrow(a) for a in gate_arrows], lag_ratio=0.16), LaggedStart(*[FadeIn(g) for g in gates], lag_ratio=0.16)); self.wait(BEAT)
        tuned_note = VGroup(T("frozen backbone", 15, MUTED), T("only Q/K/V tuned", 15, ACCENT), T("knowledge preserved", 15, SECONDARY)).arrange(DOWN, buff=0.18).move_to([3.05, -1.6, 0])
        self.play(LaggedStart(*[FadeIn(n) for n in tuned_note], lag_ratio=0.18)); self.wait(LONG)


class Scene10_FrozenCastle(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the pretrained model is a frozen castle; only Q/K/V gates accept warm updates.
        castle = box(4.0, 3.65, MUTED, BG, 0.08, 0.25, 3).move_to(UP * 0.45)
        rows = VGroup(*[box(3.0, 0.34, MUTED, MUTED, 0.16, 0.04).move_to([0, 1.55 - i * 0.55, 0]) for i in range(5)])
        row_labels = VGroup(*[T("Pretrained Layer", 12, MUTED).move_to(r) for r in rows])
        self.play(GrowFromEdge(castle, DOWN), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08), LaggedStart(*[FadeIn(l) for l in row_labels], lag_ratio=0.08)); self.wait(BEAT)
        snow = VGroup(*[Star(n=6, outer_radius=0.12, inner_radius=0.05, color=MUTED, fill_color=MUTED, fill_opacity=0.5).move_to(r.get_left() + RIGHT * 0.25) for r in rows])
        self.play(LaggedStart(*[FadeIn(s) for s in snow], lag_ratio=0.08), Write(T("Frozen", 22, MUTED).move_to([-1.15, 2.0, 0]))); self.wait(BEAT)
        tray = box(2.25, 0.78, MUTED, BG, 0.08, 0.08, 2).move_to([0, -2.0, 0])
        icons = VGroup(*[Square(0.18, color=c, fill_color=c, fill_opacity=0.35) for c in [PRIMARY, SECONDARY, ACCENT, WARM, WHITE_ISH, MUTED, PRIMARY, SECONDARY]]).arrange_in_grid(2, 4, buff=0.08).move_to(tray).shift(UP * 0.1)
        knowledge = T("Rich visual knowledge", 12, MUTED).next_to(tray, DOWN, buff=0.08)
        self.play(GrowFromCenter(tray), LaggedStart(*[FadeIn(i) for i in icons], lag_ratio=0.04)); self.wait(BEAT)
        self.play(FadeIn(knowledge)); self.wait(BEAT)
        bad_arrow = line_arrow([-5.2, 0.2, 0], castle.get_left(), WARM, 5)
        self.play(GrowArrow(bad_arrow), Wiggle(castle, rotation_angle=0.03), FadeIn(T("Full gradient ✗", 14, WARM).next_to(bad_arrow, DOWN, buff=0.08))); self.wait(BEAT)
        gates = VGroup(*[card_text(s, 0.55, 0.38, ACCENT, 14).move_to([2.25, 0.95 - i * 0.55, 0]) for i, s in enumerate(["Q", "K", "V"])])
        self.play(LaggedStart(*[GrowFromCenter(g) for g in gates], lag_ratio=0.3), LaggedStart(*[Flash(g, color=ACCENT) for g in gates], lag_ratio=0.3)); self.wait(BEAT)
        key = VGroup(Line(LEFT * 0.22, RIGHT * 0.22, color=ACCENT, stroke_width=4), Circle(0.11, color=ACCENT, stroke_width=3).shift(LEFT * 0.32), Line(RIGHT * 0.1, RIGHT * 0.1 + DOWN * 0.12, color=ACCENT, stroke_width=3)).move_to([3.35, 0.2, 0])
        grad = VGroup(*[line_arrow([5.0, 0.95 - i * 0.55, 0], gates[i].get_right(), PRIMARY, 3) for i in range(3)])
        self.play(FadeIn(key), Wiggle(key)); self.wait(BEAT)
        self.play(LaggedStart(*[GrowArrow(a) for a in grad], lag_ratio=0.2), LaggedStart(*[Indicate(g, color=ACCENT) for g in gates], lag_ratio=0.2)); self.wait(BEAT)
        self.play(Write(T("Most knowledge stays frozen.  Only motion-sensitive gates are tuned.", 16).move_to(DOWN * 2.85))); self.wait(LONG)


class Scene11_DDIMInversion(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: DDIM strips the original down to a reusable structural blueprint, then the prompt repaints that structure.
        original_box = box(2.45, 2.05, MUTED, BG, 0.08).move_to([-4.15, 0.65, 0])
        blueprint_box = box(2.65, 2.05, ACCENT, BG, 0.08).move_to([0, 0.65, 0])
        edited_box = box(2.45, 2.05, SECONDARY, BG, 0.08).move_to([4.15, 0.65, 0])
        labels = VGroup(
            T("Original frame", 15, WHITE_ISH).next_to(original_box, UP, buff=0.12),
            T("Structural blueprint", 15, ACCENT).next_to(blueprint_box, UP, buff=0.12),
            T("Edited frame", 15, SECONDARY).next_to(edited_box, UP, buff=0.12),
        )
        original_img = img(os.path.join(A31, "man_skiing.png"), 1.85, 1.5).move_to(original_box)
        self.play(GrowFromCenter(original_box), Write(labels[0]), FadeIn(original_img)); self.wait(BEAT)

        blueprint = ski_skeleton(ACCENT, 0.78).move_to(blueprint_box).shift(UP * 0.08)
        ground = Line(LEFT * 1.05, RIGHT * 1.05, color=ACCENT, stroke_width=3).move_to(blueprint_box.get_center() + DOWN * 0.56)
        dd_arrow = line_arrow(original_box.get_right(), blueprint_box.get_left(), ACCENT, 4)
        dd_label = T("DDIM inversion", 13, ACCENT).next_to(dd_arrow, UP, buff=0.12)
        self.play(GrowArrow(dd_arrow), FadeIn(dd_label)); self.wait(BEAT)
        self.play(GrowFromCenter(blueprint_box), Write(labels[1]), Create(blueprint), Create(ground)); self.wait(BEAT)

        kept = VGroup(
            T("pose", 13, ACCENT),
            T("layout", 13, ACCENT),
            T("motion path", 13, ACCENT),
        ).arrange(RIGHT, buff=0.35).next_to(blueprint_box, DOWN, buff=0.14)
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in kept], lag_ratio=0.18)); self.wait(BEAT)

        denoise_arrow = line_arrow(blueprint_box.get_right(), edited_box.get_left(), PRIMARY, 4)
        denoise_label = VGroup(
            T("denoise", 13, PRIMARY),
            T('+"red-blue skier"', 12, SECONDARY),
        ).arrange(DOWN, buff=0.05).next_to(denoise_arrow, UP, buff=0.08)
        self.play(GrowArrow(denoise_arrow), FadeIn(denoise_label)); self.wait(BEAT)
        edited_img = img(os.path.join(A31, "redblue_skiing.png"), 1.85, 1.5).move_to(edited_box)
        self.play(GrowFromCenter(edited_box), Write(labels[2]), FadeIn(edited_img)); self.wait(BEAT)

        path_overlay = ski_skeleton(ACCENT, 0.55).move_to(edited_box).set_opacity(0.45)
        self.play(TransformFromCopy(blueprint, path_overlay)); self.wait(BEAT)
        self.play(FadeOut(path_overlay), Circumscribe(VGroup(blueprint_box, edited_box), color=ACCENT)); self.wait(BEAT)
        self.play(Write(T("The blueprint keeps the layout.  The prompt changes the appearance.", 18).move_to(DOWN * 3.1))); self.wait(LONG)


class Scene12_SameMotionDifferentCharacters(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: actors swap in the center, but the dashed dribble choreography never moves.
        stage = Rectangle(width=11, height=5, color=MUTED, fill_color=MUTED, fill_opacity=0.05)
        path = DashedVMobject(ArcBetweenPoints([-5.0, -0.25, 0], [5.0, -0.25, 0], angle=-0.36, color=PRIMARY, stroke_width=3))
        ghosts = VGroup(*[stick_figure(PRIMARY, 0.42, i - 1).move_to([x, -0.35 + 0.25 * (i == 1), 0]).set_opacity(0.42) for i, x in enumerate([-3.4, 0, 3.4])])
        self.play(FadeIn(stage)); self.wait(BEAT)
        self.play(Create(path), LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.35)); self.wait(BEAT)
        self.play(FadeIn(T("Motion path stays fixed.", 16, PRIMARY).move_to(UP * 2.55))); self.wait(BEAT)
        slot = frame_slot(1.8, 2.15, WHITE_ISH).move_to([0, 0.35, 0])

        def actor_image(filename, label, color):
            picture = img(os.path.join(A31, filename), 1.62, 1.78).move_to(slot).shift(UP * 0.08)
            caption = T(label, 12, color).next_to(slot, DOWN, buff=0.08)
            return Group(picture, caption)

        def actor_glyph(label, color):
            return Group(costume(label, color).scale(1.08).move_to(slot).shift(UP * 0.05), T(label, 12, color).next_to(slot, DOWN, buff=0.08))

        current = actor_image("man_dribbling.png", "Man", WHITE_ISH)
        self.play(GrowFromCenter(slot), FadeIn(current)); self.wait(BEAT)
        swaps = [
            actor_glyph("James Bond", SECONDARY),
            actor_image("lego_dribbling.png", "Lego Man", PRIMARY),
            actor_image("astronaut_dribbling.png", "Astronaut", ACCENT),
            actor_glyph("Iron Man", WARM),
        ]
        for new in swaps:
            self.play(FadeOut(current, scale=0.98), FadeIn(new, scale=1.02)); current = new
            self.wait(BEAT)
        self.play(Indicate(path, color=PRIMARY)); self.wait(BEAT)
        left = T("The actor changes.", 22, SECONDARY).move_to([-3.2, -2.55, 0])
        right = T("The choreography remains.", 22, PRIMARY).move_to([3.0, -2.55, 0])
        self.play(LaggedStart(FadeIn(left), FadeIn(right), lag_ratio=0.5)); self.wait(LONG)


class Scene13_ActorPropBackground(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the input card splits into four controls; three repaint, the motion control remains locked.
        source = image_frame(os.path.join(A31, "rabbit_watermelon.png"), 2.1, 2.1, SECONDARY).move_to([-4.6, 0.45, 0])
        src_lab = T("reference action", 15, PRIMARY).next_to(source, DOWN, buff=0.12)
        self.play(GrowFromCenter(source), FadeIn(src_lab)); self.wait(BEAT)
        slots = VGroup()
        labels = [("Actor", SECONDARY), ("Prop", SECONDARY), ("Background", SECONDARY), ("Motion", PRIMARY)]
        xs = [-1.75, 0.15, 2.05, 3.95]
        for (lab, col), x in zip(labels, xs):
            shell = box(1.55, 1.55, col, BG, 0.08, 0.12, 2).move_to([x, 0.55, 0])
            title = T(lab, 14, col).next_to(shell, UP, buff=0.08)
            slots.add(VGroup(shell, title))
        self.play(LaggedStart(*[GrowFromCenter(s[0]) for s in slots], lag_ratio=0.18), LaggedStart(*[Write(s[1]) for s in slots], lag_ratio=0.18)); self.wait(BEAT)
        contents = [
            image_frame(os.path.join(A31, "rabbit_watermelon.png"), 1.25, 1.25, SECONDARY).move_to(slots[0][0]),
            image_frame(os.path.join(A31, "rabbit_watermelon.png"), 1.25, 1.25, SECONDARY).move_to(slots[1][0]),
            card_text("wood table", 1.18, 0.52, SECONDARY, 11).move_to(slots[2][0]),
            VGroup(stick_figure(PRIMARY, 0.5, 0), lock_icon(PRIMARY, 0.6).shift(UP * 0.55)).move_to(slots[3][0]),
        ]
        self.play(LaggedStart(*[FadeIn(c) for c in contents], lag_ratio=0.18)); self.wait(BEAT)
        lock = lock_icon(PRIMARY, 0.75).move_to(slots[3][0].get_corner(UR) + LEFT * 0.18 + DOWN * 0.18)
        self.play(FadeIn(lock), Circumscribe(slots[3][0], color=PRIMARY)); self.wait(BEAT)
        new_contents = [
            image_frame(os.path.join(A31, "cat_sunglasses.png"), 1.35, 1.35, SECONDARY).move_to(slots[0][0]),
            image_frame(os.path.join(A31, "puppy_cheeseburger.png"), 1.35, 1.35, SECONDARY).move_to(slots[1][0]),
            card_text("beach", 1.18, 0.52, SECONDARY, 12).move_to(slots[2][0]),
        ]
        for i, new in enumerate(new_contents):
            self.play(FadeOut(contents[i], scale=0.96), FadeIn(new, scale=1.04)); contents[i] = new
            self.wait(BEAT)
        out = image_frame(os.path.join(A31, "cat_cheeseburger_beach.png"), 1.65, 1.65, SECONDARY).move_to([0.9, -1.85, 0])
        keep = T("same eating motion", 14, PRIMARY).next_to(out, RIGHT, buff=0.22)
        self.play(LaggedStart(*[GrowArrow(line_arrow(slots[i][0].get_bottom(), out[0].get_top(), labels[i][1], 2)) for i in range(4)], lag_ratio=0.15), GrowFromCenter(out), FadeIn(keep)); self.wait(BEAT)
        self.play(Write(T("Appearance controls change.  Motion stays locked.", 18).move_to(DOWN * 3.1))); self.wait(LONG)


class Scene14_Ablation_Table(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the clean edited video rests on three different supports.
        table = simple_table()
        self.play(LaggedStart(*[GrowFromEdge(l, DOWN) for l in table[2]], lag_ratio=0.35)); self.wait(BEAT)
        self.play(GrowFromEdge(table[0], LEFT), Write(table[1])); self.wait(BEAT)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in table[4]], lag_ratio=0.2)); self.wait(BEAT)
        desc = VGroup(T("Keeps frames consistent", 13, SECONDARY), T("Keeps structure of input", 13, ACCENT), T("Adapts to reference motion", 13, PRIMARY)).arrange(DOWN, buff=0.18).move_to([4.0, 1.2, 0])
        self.play(LaggedStart(*[Write(l) for l in table[3]], lag_ratio=0.35), LaggedStart(*[FadeIn(d) for d in desc], lag_ratio=0.35)); self.wait(BEAT)
        self.play(FadeIn(T("A good edit needs three supports.", 22).move_to(DOWN * 3.2))); self.wait(LONG)


class Scene15_Ablation_NoSTAttn(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: pull the ST-attention leg and the filmstrip starts flickering.
        table = simple_table()
        self.play(FadeIn(table)); self.wait(BEAT)
        self.play(Circumscribe(table[2][0], color=SECONDARY)); self.wait(BEAT)
        wires = pulse_lines_between([f for f in table[4]], SECONDARY)
        self.play(Create(wires)); self.wait(BEAT)
        self.play(FadeOut(table[2][0]), FadeOut(wires), table[3][0].animate.set_color(WARM)); self.wait(BEAT)
        self.play(Wiggle(table[4], rotation_angle=0.12, n_wiggles=6), Create(SurroundingRectangle(table[4], color=WARM))); self.wait(BEAT)
        fails = VGroup(*[card_text(s, 1.28, 0.72, WARM if i else SECONDARY, 9) for i, s in enumerate(["F1 ok", "F2 identity shifts", "F3 prop jumps", "F4 pose changes"])]).arrange(RIGHT, buff=0.08).move_to([0.9, 2.25, 0])
        self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.3) for f in fails], lag_ratio=0.25)); self.wait(BEAT)
        self.play(FadeIn(T("Without ST-Attn: frames stop agreeing.", 18, WARM).move_to(DOWN * 3.0))); self.wait(LONG)


class Scene16_Ablation_NoDDIM(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: when the blueprint vanishes, output elements drift out of alignment.
        table = simple_table()
        guide = VGroup(Line(table[4].get_left() + DOWN * 0.4, table[4].get_right() + DOWN * 0.4, color=ACCENT, stroke_width=2), *[Line(f.get_center() + DOWN * 0.65, f.get_center() + UP * 0.45, color=ACCENT, stroke_width=1.5) for f in table[4]])
        dots = VGroup(*[Dot(f.get_center(), radius=0.045, color=ACCENT) for f in table[4]])
        self.play(FadeIn(table), Create(guide), FadeIn(dots)); self.wait(BEAT)
        self.play(Circumscribe(table[2][1], color=ACCENT)); self.wait(BEAT)
        self.play(FadeOut(table[2][1]), FadeOut(guide), table[3][1].animate.set_color(WARM)); self.wait(BEAT)
        self.play(FadeIn(T("Gold structure guide removed", 15, ACCENT).move_to(UP * 2.65))); self.wait(BEAT)
        drift = [UP * 0.35, RIGHT * 0.3, DOWN * 0.32, RIGHT * 0.44 + UP * 0.16]
        arrows = VGroup(*[Arrow(dots[i].get_center(), dots[i].get_center() + drift[i], color=WARM, buff=0.03, stroke_width=2) for i in range(4)])
        self.play(*[dots[i].animate.shift(drift[i]) for i in range(4)], LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12)); self.wait(BEAT)
        self.play(FadeIn(T("Without inversion: the structure drifts.", 18, WARM).move_to(DOWN * 3.0))); self.wait(LONG)


class Scene17_Ablation_NoFineTune(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the prompt nouns pass the checklist, but the reference action fails.
        table = simple_table().shift(LEFT * 2.0)
        self.play(FadeIn(table)); self.wait(BEAT)
        self.play(Circumscribe(table[2][2], color=PRIMARY)); self.wait(BEAT)
        self.play(FadeOut(table[2][2]), table[3][2].animate.set_color(WARM)); self.wait(BEAT)
        boxlist = checklist(["Puppy  ✓", "Cheeseburger  ✓", "Comic style  ✓", "Reference motion  ✗"], [SECONDARY, SECONDARY, SECONDARY, WARM], 3.4, 2.7).move_to([3.25, 0.25, 0])
        self.play(GrowFromCenter(boxlist[0])); self.wait(BEAT)
        for row in boxlist[1]:
            self.play(Write(row)); self.wait(BEAT)
        puppy = image_frame(os.path.join(A31, "puppy_cheeseburger.png"), 1.25, 1.05, SECONDARY).next_to(boxlist, UP, buff=0.12)
        wrong_path = DashedVMobject(Line(puppy.get_left() + DOWN * 0.7, puppy.get_right() + DOWN * 0.7, color=WARM, stroke_width=2))
        self.play(FadeIn(puppy), Create(wrong_path), FadeIn(T("flat motion", 11, WARM).next_to(wrong_path, DOWN, buff=0.04))); self.wait(BEAT)
        self.play(Flash(boxlist[1][-1], color=WARM)); self.wait(BEAT)
        self.play(FadeIn(T("Without fine-tuning:\nthe model misses the reference motion.", 17, WARM).move_to(DOWN * 3.0))); self.wait(LONG)


class Scene18_Dreamix_Training(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: a student model learns motion from a movie teacher and detail from a photo teacher.
        dreamix = VGroup(Circle(1.05, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.05), box(2.4, 1.6, PRIMARY, BG, 0.1, 0.2), T("Dreamix", 24)).move_to([0, 0.2, 0])
        self.play(GrowFromCenter(dreamix[1]), FadeIn(dreamix[0]), Write(dreamix[2])); self.wait(BEAT)
        movie = Group(box(2.75, 1.75, MUTED, BG, 0.08, 0.15), T("Movie Teacher", 17), filmstrip_from_image(os.path.join(A31, "man_skiing.png"), 3, 0.78, 0.82, SECONDARY, 0.06).scale(0.9)).move_to([-4.0, 0.8, 0])
        movie[1].next_to(movie[0], UP, buff=0.08); movie[2].move_to(movie[0])
        self.play(FadeIn(movie, shift=RIGHT * 1.5)); self.wait(BEAT)
        arr1 = line_arrow(movie[0].get_right(), dreamix[1].get_left(), PRIMARY, 4)
        self.play(GrowArrow(arr1), movie[2].animate.shift(RIGHT * 0.1)); self.wait(BEAT)
        photo = VGroup(box(2.75, 1.75, MUTED, BG, 0.08, 0.15), T("Photo Teacher", 17)).move_to([4.0, 0.8, 0])
        photo[1].next_to(photo[0], UP, buff=0.08)
        cards = Group(*[image_frame(os.path.join(A31, f), 0.72, 0.78, SECONDARY).rotate(a) for f, a in zip(["rabbit_watermelon.png", "cat_sunglasses.png", "puppy_cheeseburger.png", "redblue_skiing.png"], [-0.18, -0.05, 0.08, 0.19])]).arrange(RIGHT, buff=-0.18).move_to(photo[0])
        self.play(FadeIn(photo, shift=LEFT * 1.5), LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.15)); self.wait(BEAT)
        arr2 = line_arrow(photo[0].get_left(), dreamix[1].get_right(), SECONDARY, 4)
        self.play(GrowArrow(arr2), cards.animate.scale(1.15)); self.wait(BEAT)
        self.play(dreamix[1].animate.set_stroke(SECONDARY, width=3)); self.play(dreamix[1].animate.set_stroke(PRIMARY, width=3)); self.wait(BEAT)
        out = filmstrip_from_image(os.path.join(A31, "cat_sunglasses.png"), 4, 0.78, 0.86, SECONDARY, 0.06).move_to([0, -1.9, 0])
        self.play(GrowArrow(line_arrow(dreamix[1].get_bottom(), out.get_top(), PRIMARY, 3)), GrowFromEdge(out, LEFT)); self.wait(BEAT)
        self.play(Write(T("Video teaches motion.  Images teach detail.  Dreamix learns both.", 17).move_to(DOWN * 3.0))); self.wait(LONG)


class Scene19_Dreamix_Inference(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the original is deliberately degraded, then regenerated cleanly under a new prompt.
        xs = [-5.0, -2.5, 0, 2.5, 5.0]
        labels = ["Input video", "Downsample", "Add noise", "Denoise + upscale", "Edited video"]
        cols = [MUTED, MUTED, WARM, PRIMARY, SECONDARY]
        stages = VGroup()
        for i, x in enumerate(xs):
            b = frame_slot(1.35, 1.65, cols[i]).move_to([x, 0.55, 0])
            lab = T(labels[i], 11, cols[i], 1.7).next_to(b, DOWN, buff=0.1)
            stages.add(VGroup(b, lab))
        self.play(GrowFromCenter(stages[0]), FadeIn(img(os.path.join(A31, "man_skiing.png"), 1.1, 1.35).move_to(stages[0][0]))); self.wait(BEAT)
        pix = VGroup(*[Square(0.18, color=c, fill_color=c, fill_opacity=0.75) for c in [MUTED, PRIMARY, SECONDARY, MUTED, ACCENT] * 4]).arrange_in_grid(4, 5, buff=0.015).move_to(stages[1][0])
        self.play(GrowArrow(line_arrow(stages[0][0].get_right(), stages[1][0].get_left(), MUTED, 3)), GrowFromCenter(stages[1]), FadeIn(pix)); self.wait(BEAT)
        noise = Rectangle(width=1.12, height=1.42, fill_color=WARM, fill_opacity=0.35, stroke_width=0).move_to(stages[2][0])
        self.play(GrowArrow(line_arrow(stages[1][0].get_right(), stages[2][0].get_left(), WARM, 3)), GrowFromCenter(stages[2]), FadeIn(pix.copy().move_to(stages[2][0])), FadeIn(noise)); self.wait(BEAT)
        self.play(FadeIn(T("Corrupt the original.", 17, WARM).move_to(DOWN * 1.8))); self.wait(BEAT)
        clear = noise.copy().move_to(stages[3][0])
        self.play(GrowArrow(line_arrow(stages[2][0].get_right(), stages[3][0].get_left(), PRIMARY, 3)), GrowFromCenter(stages[3]), FadeIn(clear), FadeIn(T('"red-blue skier"', 10, SECONDARY).next_to(stages[3], UP, buff=0.08)))
        self.play(clear.animate.set_fill(opacity=0), run_time=SLOW); self.wait(BEAT)
        self.play(GrowArrow(line_arrow(stages[3][0].get_right(), stages[4][0].get_left(), SECONDARY, 3)), GrowFromCenter(stages[4]), FadeIn(img(os.path.join(A31, "redblue_skiing.png"), 1.12, 1.35).move_to(stages[4][0]))); self.wait(BEAT)
        self.play(FadeIn(T("Regenerate it with the new prompt.", 17, PRIMARY).move_to(DOWN * 2.25))); self.wait(LONG)


class Scene20_EI2_Stabilizer(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: an unstable strip passes through EI² and exits with matching frames.
        left = VGroup(box(3.2, 1.75, WARM, BG, 0.08), T("Before EI²", 14, WARM)).move_to([-4.2, 0.55, 0])
        left[1].next_to(left[0], UP, buff=0.08)
        lframes = Group(*[image_frame(os.path.join(A31, "rabbit_watermelon.png"), 0.68, 0.9, c) for c in [WARM, MUTED, WARM, MUTED]]).arrange(RIGHT, buff=0.08).move_to(left[0])
        lframes[1][1].shift(UP * 0.08); lframes[2][1].set_opacity(0.55); lframes[3][1].shift(RIGHT * 0.1)
        self.play(FadeIn(left), LaggedStart(*[GrowFromCenter(f) for f in lframes], lag_ratio=0.18)); self.play(Wiggle(lframes, rotation_angle=0.09, n_wiggles=5)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(T(s, 11, WARM).move_to([-4.2, -0.6 - i * 0.25, 0])) for i, s in enumerate(["identity flicker", "style flicker", "background flicker"])], lag_ratio=0.2)); self.wait(BEAT)
        box_e = VGroup(box(2.0, 1.4, PRIMARY, BG, 0.12, 0.2), T("EI²", 28), T("self-attention\nstabilizer", 12, PRIMARY)).move_to([0, 0.55, 0])
        box_e[2].next_to(box_e[1], DOWN, buff=0.1)
        self.play(GrowArrow(line_arrow(left[0].get_right(), box_e[0].get_left(), PRIMARY, 4)), GrowFromCenter(box_e)); self.wait(BEAT)
        right = VGroup(box(3.2, 1.75, SECONDARY, BG, 0.08), T("After EI²", 14, SECONDARY)).move_to([4.2, 0.55, 0])
        right[1].next_to(right[0], UP, buff=0.08)
        rframes = Group(*[image_frame(os.path.join(A31, "rabbit_watermelon.png"), 0.68, 0.9, SECONDARY) for _ in range(4)]).arrange(RIGHT, buff=0.08).move_to(right[0])
        self.play(GrowArrow(line_arrow(box_e[0].get_right(), right[0].get_left(), PRIMARY, 4)), FadeIn(right), LaggedStart(*[FadeIn(f) for f in rframes], lag_ratio=0.18)); self.wait(BEAT)
        self.play(Circumscribe(right, color=SECONDARY)); self.wait(BEAT)
        self.play(Write(T("EI² acts like an anti-flicker stabilizer.", 20).move_to(DOWN * 2.8))); self.wait(LONG)


class Scene21_VideoP2P_CrossAttention(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: each prompt word casts a spotlight onto the region it controls.
        words = ["cat", "sunglasses", "watermelon", "beach"]
        tokens = VGroup(*[card_text(w, 1.45, 0.58, ACCENT if i != 2 else SECONDARY, 15) for i, w in enumerate(words)]).arrange(RIGHT, buff=0.45).move_to(UP * 2.55)
        frame = box(5.0, 2.75, MUTED, BG, 0.08, 0.15).move_to(ORIGIN)
        regions = VGroup(
            Circle(0.5, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.08).move_to([-1.65, 0.25, 0]),
            Circle(0.3, color=ACCENT, fill_color=ACCENT, fill_opacity=0.08).move_to([-1.15, 0.68, 0]),
            Circle(0.5, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.08).move_to([0.85, 0.0, 0]),
            Rectangle(width=4.4, height=0.95, color=MUTED, fill_color=MUTED, fill_opacity=0.05).move_to([0.0, -0.65, 0]),
        )
        labels = VGroup(T("animal", 10, PRIMARY).move_to(regions[0]), T("eyes", 10, ACCENT).move_to(regions[1]), T("object", 10, SECONDARY).move_to(regions[2]), T("background", 10, MUTED).move_to(regions[3]))
        self.play(GrowFromCenter(frame), FadeIn(regions), FadeIn(labels)); self.wait(BEAT)
        self.play(LaggedStart(*[GrowFromCenter(t) for t in tokens], lag_ratio=0.25)); self.wait(BEAT)
        spotlights = VGroup()
        for i in range(4):
            cone = Polygon(tokens[i].get_bottom() + LEFT * 0.12, tokens[i].get_bottom() + RIGHT * 0.12, regions[i].get_center() + RIGHT * 0.5, regions[i].get_center() + LEFT * 0.5, color=tokens[i][0].get_color(), fill_color=tokens[i][0].get_color(), fill_opacity=0.13, stroke_opacity=0.25)
            spotlights.add(cone)
            self.play(Indicate(tokens[i], color=tokens[i][0].get_color()), FadeIn(cone), Indicate(regions[i], color=tokens[i][0].get_color()))
            self.wait(BEAT)
        self.play(Indicate(spotlights, color=ACCENT)); self.wait(BEAT)
        self.play(Write(T("Cross-attention decides where each word edits the video.", 17).move_to(DOWN * 2.85))); self.wait(LONG)


class Scene22_Comparison_OneShot_TrainingFree(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: training-free wins on speed, one-shot tuned wins on large shape changes.
        div = DashedLine([0, 3.5, 0], [0, -2.0, 0], color=MUTED)
        self.play(Create(div), FadeIn(T("Training-Free", 20, SECONDARY).move_to([-3.0, 2.65, 0])), FadeIn(T("One-Shot Tuned", 20, PRIMARY).move_to([3.0, 2.65, 0]))); self.wait(BEAT)
        left_box = box(2.45, 1.45, MUTED, BG, 0.1).move_to([-3.0, 0.9, 0])
        left_strip = filmstrip_from_image(os.path.join(A31, "rabbit_watermelon.png"), 3, 0.68, 0.75, SECONDARY, 0.05).move_to(left_box)
        left_lab = T("Instant", 14, SECONDARY).next_to(left_box, DOWN, buff=0.12)
        self.play(FadeIn(left_box), FadeIn(left_strip), FadeIn(left_lab)); self.wait(BEAT)
        right_box = box(2.45, 1.45, PRIMARY, BG, 0.1).move_to([3.0, 0.9, 0])
        right_strip = filmstrip_from_image(os.path.join(A31, "puppy_cheeseburger.png"), 3, 0.68, 0.75, PRIMARY, 0.05).move_to(right_box)
        right_lab = T("Requires training", 14, WARM).next_to(right_box, DOWN, buff=0.12)
        self.play(FadeIn(right_box), FadeIn(right_strip), FadeIn(right_lab)); self.wait(BEAT)
        speed = Line([-4.3, -1.0, 0], [4.3, -1.0, 0], color=MUTED)
        shape = Line([-4.3, -1.8, 0], [4.3, -1.8, 0], color=MUTED)
        self.play(Create(speed), Create(shape), FadeIn(T("Speed", 14).next_to(speed, LEFT, buff=0.2)), FadeIn(T("Shape Change", 14).next_to(shape, LEFT, buff=0.2))); self.wait(BEAT)
        d1 = Dot([2.5, -1.0, 0], radius=0.14, color=SECONDARY)
        d2 = Dot([2.5, -1.8, 0], radius=0.14, color=PRIMARY)
        self.play(GrowFromCenter(d1), FadeIn(T("Training-Free ▲", 11, SECONDARY).next_to(d1, UP, buff=0.08))); self.wait(BEAT)
        self.play(GrowFromCenter(d2), FadeIn(T("One-Shot Tuned ▲", 11, PRIMARY).next_to(d2, UP, buff=0.08))); self.wait(BEAT)
        self.play(FadeIn(T("Training-free is faster.", 18, SECONDARY).move_to([-3.0, -2.75, 0])), FadeIn(T("Tuned editing changes shape more.", 18, PRIMARY).move_to([3.0, -2.75, 0]))); self.wait(LONG)


class Scene23_OneShot_to_MultipleShot(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: many golf references enter a funnel; accidental details fade, leaving the shared swing skeleton.
        strips = Group()
        for i in range(4):
            s = filmstrip_from_image(os.path.join(A31, "golf_swing.png"), 3, 0.68, 0.76, MUTED, 0.05)
            s.move_to([-4.55 + (i % 2) * 2.05, 1.45 - (i // 2) * 1.35, 0])
            strips.add(s)
        self.play(LaggedStart(*[FadeIn(s) for s in strips], lag_ratio=0.12)); self.wait(BEAT)
        detail_labels = VGroup(*[T(s, 10, WARM).next_to(strips[i], DOWN, buff=0.05) for i, s in enumerate(["clothes", "camera", "background", "person"][:4])])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in detail_labels], lag_ratio=0.1)); self.wait(BEAT)
        self.play(FadeIn(T("One video: person + clothes + background + camera", 14, WARM).move_to(UP * 2.8))); self.wait(BEAT)
        funnel = Polygon([-1.0, 1.85, 0], [-1.0, -1.65, 0], [1.25, -0.25, 0], [1.25, 0.25, 0], color=MUTED, fill_opacity=0)
        self.play(Create(funnel)); self.wait(BEAT)
        self.play(strips.animate.move_to([-0.8, 0, 0]).scale(0.45)); self.wait(BEAT)
        self.play(FadeOut(detail_labels)); self.wait(BEAT)
        skbox = box(2.25, 1.9, PRIMARY, PRIMARY, 0.08, 0.15).move_to([3.45, 0.85, 0])
        sk = golf_skeleton(PRIMARY, 0.95).move_to(skbox)
        outputs = Group(
            image_frame(os.path.join(A31, "monkey_golf.png"), 1.05, 1.05, SECONDARY),
            image_frame(os.path.join(A31, "robot_golf.png"), 1.05, 1.05, SECONDARY),
            image_frame(os.path.join(A31, "panda_golf.png"), 1.05, 1.05, SECONDARY),
        ).arrange(RIGHT, buff=0.14).move_to([3.45, -1.55, 0])
        self.play(GrowFromCenter(skbox), Create(sk)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(o) for o in outputs], lag_ratio=0.16)); self.wait(BEAT)
        self.play(FadeIn(T("Many videos reveal the motion concept.", 20).move_to(DOWN * 3.0))); self.wait(LONG)


class Scene24_MotionDirector(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: text supplies nouns, the verb fails, then reference videos coach the missing motion.
        prompt = VGroup(box(2.8, 0.7, MUTED, BG, 0.08), T('"A monkey is playing golf."', 14)).move_to([-3.7, 2.4, 0])
        self.play(GrowFromCenter(prompt)); self.wait(BEAT)
        items = checklist(["Monkey  ✓", "Golf club  ✓", "Golf course  ✓", "Golf swing  ✗"], [SECONDARY, SECONDARY, SECONDARY, WARM], 3.4, 2.55).move_to([3.0, 0.6, 0])
        self.play(GrowFromCenter(items[0])); self.wait(BEAT)
        for row in items[1][:3]:
            self.play(Write(row)); self.wait(BEAT)
        self.play(Write(items[1][3]), Flash(items[1][3], color=WARM)); self.wait(BEAT)
        what = T("Text says what.", 16, MUTED).move_to([-3.7, 1.75, 0])
        self.play(FadeIn(what)); self.wait(BEAT)
        coach = Group(box(2.8, 1.55, ACCENT, BG, 0.08, 0.15), T("MotionDirector\ncoach", 14, ACCENT), filmstrip_from_image(os.path.join(A31, "golf_swing.png"), 3, 0.62, 0.7, ACCENT, 0.05)).move_to([-3.6, -0.9, 0])
        coach[2].move_to(coach[0]).shift(DOWN * 0.23)
        self.play(FadeIn(coach, shift=RIGHT * 1.2)); self.wait(BEAT)
        arrs = VGroup(*[line_arrow(coach[0].get_right() + DOWN * y, items[0].get_left() + DOWN * y, ACCENT, 3) for y in [-0.25, 0.25]])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.3)); self.wait(BEAT)
        fixed = T("Golf swing  ✓", 16, SECONDARY).move_to(items[1][3])
        self.play(ReplacementTransform(items[1][3], fixed), Flash(fixed, color=ACCENT)); self.wait(BEAT)
        monkey = image_frame(os.path.join(A31, "monkey_golf.png"), 1.95, 1.72, SECONDARY).move_to([3.0, -1.55, 0])
        self.play(GrowFromCenter(monkey)); self.wait(BEAT)
        self.play(Write(T("Text says what to generate.\nReference videos show how it should move.", 17).move_to(DOWN * 2.95))); self.wait(LONG)


class Scene25_DecouplingAppearanceMotion(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: human appearance fades away, leaving a skeleton that transfers to monkey, robot, and panda.
        human = image_frame(os.path.join(A31, "golf_swing.png"), 2.05, 2.5, SECONDARY).move_to([-3.75, 0.25, 0])
        self.play(GrowFromCenter(human)); self.wait(BEAT)
        app = T("Appearance:\nbody, clothes, face, bg", 14, SECONDARY, 2.2).move_to([-3.7, 2.65, 0])
        self.play(FadeIn(app), Circumscribe(human, color=SECONDARY)); self.wait(BEAT)
        motion = T("Motion:\ngolf swing skeleton", 14, PRIMARY, 2.2).move_to([-1.3, 2.65, 0])
        sk = golf_skeleton(PRIMARY, 0.85).move_to(human)
        self.play(FadeIn(motion), Create(sk)); self.wait(BEAT)
        self.play(human[1].animate.set_opacity(0.1)); self.wait(BEAT)
        self.play(FadeIn(T("Appearance fades.  Motion stays.", 18).move_to(DOWN * 2.45))); self.wait(BEAT)
        targets = [(-1.0, os.path.join(A31, "monkey_golf.png"), "Monkey"), (1.65, os.path.join(A31, "robot_golf.png"), "Robot"), (4.25, os.path.join(A31, "panda_golf.png"), "Panda")]
        for x, path, _name in targets:
            subject = image_frame(path, 1.7, 1.85, SECONDARY).move_to([x, 0.25, 0])
            skcopy = golf_skeleton(PRIMARY, 0.68).move_to(subject)
            self.play(TransformFromCopy(sk, skcopy), FadeIn(subject)); self.wait(BEAT)
        self.play(FadeIn(T("Learn the motion, not the actor.", 26, PRIMARY).move_to(DOWN * 3.05))); self.wait(LONG)


class Scene26_FinalSummary(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: appearance, structure, and motion stack into an edited video, then the whole recipe flows to a stable filmstrip.
        plates = VGroup(
            VGroup(box(5.5, 1.0, SECONDARY, SECONDARY, 0.18), T("Appearance  →  T2I pretrained model + text prompt", 14, SECONDARY)).move_to([0, 2.0, 0]),
            VGroup(box(5.5, 1.0, ACCENT, ACCENT, 0.18), T("Structure  →  DDIM inversion blueprint", 14, ACCENT)).move_to([0, 0.5, 0]),
            VGroup(box(5.5, 1.0, PRIMARY, PRIMARY, 0.18), T("Motion  →  reference video skeleton", 14, PRIMARY)).move_to([0, -1.0, 0]),
        )
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 1.5) for p in plates], lag_ratio=0.4)); self.wait(BEAT)
        for p, c in zip(plates, [SECONDARY, ACCENT, PRIMARY]):
            self.play(Indicate(p, color=c)); self.wait(BEAT)
        edited = T("Edited Video", 32)
        self.play(ReplacementTransform(plates, edited)); self.wait(LONG)
        self.play(FadeOut(edited))
        items = VGroup(
            T("Reference video → motion skeleton", 14, PRIMARY),
            T("Text prompt → new appearance", 14, SECONDARY),
            T("DDIM inversion → structure blueprint", 14, ACCENT),
            T("Spatio-temporal attention → frame consistency", 14, PRIMARY),
            T("Fine-tuning → video-specific adaptation", 14, MUTED),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.6, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.3) for i in items], lag_ratio=0.25)); self.wait(BEAT)
        output = VGroup(box(2.0, 3.0, SECONDARY, BG, 0.1), T("Stable edited\nfilmstrip", 16, SECONDARY)).move_to([4.0, 0.2, 0])
        arrow_colors = [PRIMARY, SECONDARY, ACCENT, PRIMARY, MUTED]
        arrows = VGroup(*[line_arrow(i.get_right(), output[0].get_left(), arrow_colors[n], 6) for n, i in enumerate(items)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), GrowFromEdge(output, LEFT)); self.wait(BEAT)
        self.play(LaggedStart(*[Indicate(a, color=arrow_colors[n], scale_factor=1.03) for n, a in enumerate(arrows)], lag_ratio=0.12)); self.wait(BEAT)
        self.play(Circumscribe(output, color=SECONDARY, run_time=1.2)); self.wait(BEAT)
        self.play(Write(T("Video editing = repaint appearance\nwhile preserving structure and motion.", 20).move_to(DOWN * 3.2))); self.wait(LONG)
