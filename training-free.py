# === PRODUCTION PLAN ===
# Core insight (one sentence): Training-free video editing does not retrain a
# model; it makes image-model edits behave like video by building temporal
# bridges between frames.
#
# Color encoding:
#   PRIMARY   = temporal bridges / cross-frame correspondences / connection
#   SECONDARY = consistent edited output / success
#   WARM      = flicker / per-frame failure / inconsistency
#   ACCENT    = attention maps / DDIM blueprint / preserved layout
#   MUTED     = original content / neutral frames / inactive
#
# Scene list:
#   Scene01_Opening_Flipbook — flipbook flicker vs connected stable pages
#   Scene02_EditingLandscape — method families as tool shelves
#   Scene03_TokenFlow_PerFrameFails — independent paint sheets vs traced flow
#   Scene04_TokenFlow_Correspondences — feature GPS trackers across frames
#   Scene05_TokenFlow_Pipeline — inversion, tokens, nearest-neighbor field
#   Scene06_TokenFlow_Denoising — current frame borrows from temporal neighbors
#   Scene07_TokenFlow_Results — three projectors: original, flicker, TokenFlow
#   Scene08_FateZero_Intro — transparent attention sheets blended together
#   Scene09_FateZero_DDIMScan — inversion scanner saves attention blueprints
#   Scene10_FateZero_Blending — locked stage set, edited foreground actor
#   Scene11_FateZero_Results — big brush failure vs surgical FateZero edits
#   Scene12_MoreMethods_Bridges — frame islands joined by bridge mechanisms
#   Scene13_STDF_VidToMe — space-time cube and token merging
#   Scene14_FinalSummary — all bridges converge to stable edited video
#
# Key transforms (moments where one thing morphs INTO another):
#   - flickering flipbook pages -> connected stable pages in Scene01
#   - video strip -> latent/tokens/correspondence map in Scene05
#   - jeep attention layer + target layer -> fused Porsche output in Scene08/10
#   - many method bridges -> one stable edited video in Scene14
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
A32 = os.path.join(ROOT, "images", "3.2")


def T(text, size=22, color=WHITE_ISH, max_width=11.5):
    mob = Text(text, font_size=size, color=color)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def box(w, h, color=MUTED, fill=None, opacity=0.07, radius=0.1, stroke=2):
    return RoundedRectangle(
        width=w,
        height=h,
        corner_radius=radius,
        color=color,
        stroke_width=stroke,
        fill_color=fill or color,
        fill_opacity=opacity,
    )


def img(name, w=None, h=None):
    mob = ImageMobject(os.path.join(A32, name))
    if w is not None:
        mob.scale_to_fit_width(w)
    if h is not None and mob.height > h:
        mob.scale_to_fit_height(h)
    return mob


def image_card(name, w=1.2, h=1.4, color=MUTED):
    frame = box(w, h, color, BG, 0.05, 0.08, 2)
    picture = img(name, w - 0.12, h - 0.12).move_to(frame)
    return Group(frame, picture)


def arrow(start, end, color=MUTED, width=3):
    return Arrow(start, end, buff=0.08, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.14)


def lock_icon(color=ACCENT, scale=1.0):
    shackle = Arc(radius=0.14, start_angle=0, angle=PI, color=color, stroke_width=3).shift(UP * 0.08)
    body = box(0.34, 0.24, color, color, 0.18, 0.03, 1).shift(DOWN * 0.07)
    return VGroup(shackle, body).scale(scale)


def filmstrip(names, color=MUTED, w=1.18, h=1.42, buff=0.18):
    cards = Group(*[image_card(n, w, h, color) for n in names]).arrange(RIGHT, buff=buff)
    return cards


def tiny_film(color=MUTED):
    frames = VGroup(*[box(0.28, 0.42, color, BG, 0.08, 0.03, 1) for _ in range(3)]).arrange(RIGHT, buff=0.05)
    rail = Line(frames.get_left() + DOWN * 0.3, frames.get_right() + DOWN * 0.3, color=color, stroke_width=1.5)
    return VGroup(frames, rail)


def token_grid(rows=3, cols=3, size=0.18, colors=None):
    if colors is None:
        colors = [PRIMARY] * (rows * cols)
    squares = VGroup()
    for i in range(rows * cols):
        c = colors[i % len(colors)]
        squares.add(Square(size, color=c, fill_color=c, fill_opacity=0.28, stroke_width=1.2))
    squares.arrange_in_grid(rows, cols, buff=0.035)
    return squares


def dog_keypoints(card, dx=0.0):
    center = card[0].get_center() + RIGHT * dx
    head = Dot(center + RIGHT * 0.42 + UP * 0.23, radius=0.07, color=PRIMARY)
    body = Dot(center + LEFT * 0.02 + UP * 0.04, radius=0.07, color=SECONDARY)
    tail = Dot(center + LEFT * 0.48 + UP * 0.24, radius=0.07, color=ACCENT)
    return VGroup(head, body, tail)


def feature_map(color=MUTED, highlight=WARM):
    shell = box(1.9, 2.45, color, BG, 0.06, 0.1, 2)
    cells = VGroup()
    for r in range(4):
        for c in range(4):
            fill = highlight if (r, c) == (1, 2) else color
            op = 0.55 if (r, c) == (1, 2) else 0.12
            cells.add(Square(0.28, color=fill, fill_color=fill, fill_opacity=op, stroke_width=1.0))
    cells.arrange_in_grid(4, 4, buff=0.08).move_to(shell)
    return VGroup(shell, cells)


class Scene01_Opening_Flipbook(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: bad editing is a flipbook whose pages mutate; the fix is visible strings connecting matching dog parts.
        divider = DashedLine([0, 3.35, 0], [0, -1.5, 0], color=MUTED, dash_length=0.12)
        left_h = T("Per-frame editing", 16, WARM).move_to([-3.2, 3.0, 0])
        right_h = T("Training-free video editing", 16, SECONDARY).move_to([3.1, 3.0, 0])
        left_names = ["dog_beach_flickering_A.png", "dog_beach_flickering_B.png", "dog_beach_flickering_A.png", "dog_beach_flickering_B.png", "dog_beach_flickering_A.png"]
        right_names = ["dog_beach_colorful.png"] * 5
        left = filmstrip(left_names, WARM, 0.92, 1.18, 0.08).move_to([-3.1, 0.95, 0])
        right = filmstrip(right_names, SECONDARY, 0.92, 1.18, 0.08).move_to([3.1, 0.95, 0])
        bolts = VGroup(*[T("!", 14, WARM).move_to((left[i].get_right() + left[i + 1].get_left()) / 2 + UP * 0.1) for i in range(4)])

        self.play(Write(left_h), LaggedStart(*[GrowFromCenter(c[0]) for c in left], lag_ratio=0.12), LaggedStart(*[FadeIn(c[1]) for c in left], lag_ratio=0.12))
        self.wait(BEAT)
        self.play(LaggedStart(*[Flash(b, color=WARM, flash_radius=0.18) for b in bolts], lag_ratio=0.14), LaggedStart(*[FadeIn(b) for b in bolts], lag_ratio=0.12))
        self.wait(BEAT)
        self.play(Create(divider), Write(right_h), LaggedStart(*[GrowFromCenter(c[0]) for c in right], lag_ratio=0.12), LaggedStart(*[FadeIn(c[1]) for c in right], lag_ratio=0.12))
        self.wait(BEAT)
        head_arcs = VGroup(*[ArcBetweenPoints(right[i][0].get_center() + UP * 0.35, right[i + 1][0].get_center() + UP * 0.35, angle=-0.45, color=PRIMARY, stroke_width=2) for i in range(4)])
        tail_arcs = VGroup(*[ArcBetweenPoints(right[i][0].get_center() + DOWN * 0.25, right[i + 1][0].get_center() + DOWN * 0.25, angle=0.45, color=PRIMARY, stroke_width=2) for i in range(4)])
        self.play(LaggedStart(*[Create(a) for a in head_arcs], lag_ratio=0.16)); self.wait(BEAT)
        self.play(LaggedStart(*[Create(a) for a in tail_arcs], lag_ratio=0.16)); self.wait(BEAT)
        self.play(FadeIn(T("flickering identity", 12, WARM).move_to([-3.1, -0.55, 0])), FadeIn(T("stable identity", 12, SECONDARY).move_to([3.1, -0.55, 0])))
        self.wait(BEAT)
        q1 = T('"How do we edit video with T2I models', 15).move_to([0, -2.35, 0])
        q2 = T('without training a new model?"', 15).move_to([0, -2.8, 0])
        self.play(Write(q1), Write(q2)); self.wait(LONG)


class Scene02_EditingLandscape(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the field is a toolbox; different shelves push toward the same stable edited video.
        center = VGroup(box(2.25, 0.9, MUTED, BG, 0.08), T("Input Video", 16, MUTED)).move_to([0, 0.3, 0])
        shelves = [
            ("Training-Free", ["no fine-tuning", "fast adaptation", "reuse image diffusion"], PRIMARY, [-4.3, 1.75, 0]),
            ("Tuning-Based", ["optimize on video", "strong personalization", "slower"], MUTED, [-4.3, -1.75, 0]),
            ("Controlled Editing", ["mask / pose / depth", "motion trajectory", "more user control"], ACCENT, [4.3, 0.0, 0]),
        ]
        shelf_mobs = VGroup()
        arrows = VGroup()
        for title, lines, color, pos in shelves:
            shell = box(3.05, 1.8, color, BG, 0.07, 0.14, 2)
            header = T(title, 14, color).next_to(shell, UP, buff=-0.28)
            body = VGroup(*[T("- " + line, 11, WHITE_ISH, 2.65) for line in lines]).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(shell).shift(DOWN * 0.12)
            mob = VGroup(shell, header, body).move_to(pos)
            shelf_mobs.add(mob)
            arrows.add(arrow(mob[0].get_edge_center(RIGHT if pos[0] < 0 else LEFT), center[0].get_edge_center(LEFT if pos[0] < 0 else RIGHT), color, 3))
        out = VGroup(box(3.9, 0.7, SECONDARY, BG, 0.08), T("Edited Video - temporally consistent", 13, SECONDARY, 3.5)).move_to([0, -2.8, 0])

        self.play(GrowFromCenter(center)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.3 if s.get_center()[0] < 0 else LEFT * 0.3) for s in shelf_mobs], lag_ratio=0.22)); self.wait(BEAT)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.18)); self.wait(BEAT)
        self.play(GrowArrow(arrow(center[0].get_bottom(), out[0].get_top(), SECONDARY, 3)), GrowFromCenter(out)); self.wait(BEAT)
        self.play(Indicate(shelf_mobs[0][0], color=PRIMARY)); self.wait(BEAT)
        self.play(FadeIn(T("Same goal: change content, preserve stability.", 17).move_to(DOWN * 3.35))); self.wait(LONG)


class Scene03_TokenFlow_PerFrameFails(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: independent painting creates moving color patches; traced feature flow keeps patches attached.
        top_h = T("Per-frame editing", 15, WARM).move_to([0, 3.0, 0])
        bot_h = T("TokenFlow", 15, SECONDARY).move_to([0, -0.35, 0])
        top = filmstrip(["dog_beach_flickering_A.png", "dog_beach_flickering_B.png", "dog_beach_flickering_A.png", "dog_beach_flickering_B.png"], WARM, 1.35, 1.45, 0.38).move_to([0, 1.75, 0])
        bottom = filmstrip(["dog_beach_colorful.png"] * 4, SECONDARY, 1.35, 1.45, 0.38).move_to([0, -1.35, 0])
        crosses = VGroup(*[Cross(top[i][0], stroke_color=WARM, stroke_width=3).scale(0.18).move_to((top[i].get_right() + top[i + 1].get_left()) / 2) for i in range(3)])
        divider = DashedLine([-5.8, 0.05, 0], [5.8, 0.05, 0], color=MUTED, dash_length=0.15)

        self.play(Write(top_h), LaggedStart(*[FadeIn(c) for c in top], lag_ratio=0.12)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(c) for c in crosses], lag_ratio=0.1)); self.wait(BEAT)
        self.play(FadeIn(T("Same prompt, different behavior.", 16).move_to([0, 0.55, 0]))); self.wait(BEAT)
        self.play(Create(divider)); self.wait(BEAT)
        self.play(Write(bot_h), LaggedStart(*[FadeIn(c) for c in bottom], lag_ratio=0.12)); self.wait(BEAT)
        head = VGroup(*[ArcBetweenPoints(bottom[i][0].get_center() + UP * 0.35, bottom[i + 1][0].get_center() + UP * 0.35, angle=-0.35, color=PRIMARY, stroke_width=2) for i in range(3)])
        tail = VGroup(*[ArcBetweenPoints(bottom[i][0].get_center() + DOWN * 0.22, bottom[i + 1][0].get_center() + DOWN * 0.22, angle=0.35, color=PRIMARY, stroke_width=2) for i in range(3)])
        self.play(LaggedStart(*[Create(a) for a in head], lag_ratio=0.15), LaggedStart(*[Create(a) for a in tail], lag_ratio=0.15)); self.wait(BEAT)
        self.play(FadeIn(T("Per-frame editing changes each page independently.", 14, WARM).move_to([0, -2.75, 0])))
        self.play(FadeIn(T("TokenFlow lets visual features flow through time.", 14, PRIMARY).move_to([0, -3.2, 0]))); self.wait(LONG)


class Scene04_TokenFlow_Correspondences(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the original video carries GPS-like feature trackers that reveal same physical parts over time.
        xs = [-3.5, 0, 3.5]
        shifts = [-0.13, 0, 0.13]
        cards = Group()
        dots = VGroup()
        for i, (x, dx) in enumerate(zip(xs, shifts)):
            c = image_card("dog_beach_original.png", 2.1, 2.35, MUTED).move_to([x, 0.55, 0])
            c[1].shift(RIGHT * dx)
            label = T(["Previous", "Current", "Next"][i], 11, WHITE_ISH if i == 1 else MUTED).next_to(c[0], DOWN, buff=0.12)
            cards.add(Group(c, label))
            dots.add(dog_keypoints(c, dx))
        self.play(LaggedStart(*[GrowFromCenter(c[0][0]) for c in cards], lag_ratio=0.2), LaggedStart(*[FadeIn(c[0][1]) for c in cards], lag_ratio=0.2), LaggedStart(*[Write(c[1]) for c in cards], lag_ratio=0.2))
        self.wait(BEAT)
        for idx, col in [(0, PRIMARY), (1, SECONDARY), (2, ACCENT)]:
            this = VGroup(*[d[idx] for d in dots])
            arcs = VGroup(*[ArcBetweenPoints(this[i].get_center(), this[i + 1].get_center(), angle=-0.38, color=col, stroke_width=2) for i in range(2)])
            self.play(LaggedStart(*[GrowFromCenter(d) for d in this], lag_ratio=0.2)); self.wait(BEAT)
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2)); self.wait(BEAT)
            gps = VGroup(*[T("GPS", 9, col).next_to(d, UP, buff=0.03) for d in this])
            self.play(FadeIn(gps)); self.wait(BEAT)
        self.play(FadeIn(T("Original video provides correspondences.", 17).move_to([0, -2.55, 0]))); self.wait(BEAT)
        self.play(FadeIn(T("Edited video should respect those correspondences.", 17, SECONDARY).move_to([0, -3.05, 0]))); self.wait(LONG)


class Scene05_TokenFlow_Pipeline(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: TokenFlow turns a video into latent puzzle pieces, then records which pieces match across time.
        labels = [
            ("Input\nVideo Strip", MUTED),
            ("DDIM\nInversion", ACCENT),
            ("Diffusion\nModel Blocks", PRIMARY),
            ("Extract\nTokens", PRIMARY),
            ("Nearest-\nNeighbor Field", SECONDARY),
        ]
        xs = [-5.2, -2.6, 0, 2.6, 5.2]
        stages = VGroup()
        for i, ((lab, col), x) in enumerate(zip(labels, xs)):
            shell = box(1.65, 1.05, col, BG, 0.07, 0.1, 2)
            title = T(lab, 10, col, 1.35).move_to(shell).shift(UP * 0.17)
            if i == 0:
                icon = tiny_film(col).scale(0.65).move_to(shell).shift(DOWN * 0.24)
            elif i == 1:
                icon = Arrow(RIGHT * 0.25, LEFT * 0.25, color=col, buff=0.02, stroke_width=2).move_to(shell).shift(DOWN * 0.24)
            elif i == 2:
                icon = VGroup(*[Rectangle(width=0.82, height=0.08, color=col, fill_color=col, fill_opacity=0.25) for _ in range(4)]).arrange(DOWN, buff=0.06).move_to(shell).shift(DOWN * 0.24)
            elif i == 3:
                icon = token_grid(3, 3, 0.13, [col, MUTED]).move_to(shell).shift(DOWN * 0.24)
            else:
                icon = VGroup(Dot(LEFT * 0.18, color=ACCENT), Dot(RIGHT * 0.18, color=SECONDARY), arrow(LEFT * 0.05, RIGHT * 0.05, PRIMARY, 1.6)).move_to(shell).shift(DOWN * 0.24)
            stages.add(VGroup(shell, title, icon).move_to([x, 0.75, 0]))
        self.play(GrowFromCenter(stages[0])); self.wait(BEAT)
        for i in range(4):
            self.play(GrowArrow(arrow(stages[i][0].get_right(), stages[i + 1][0].get_left(), MUTED, 2)), FadeIn(stages[i + 1]))
            self.wait(BEAT)
        frames = VGroup()
        for x in [-2.0, 0, 2.0]:
            shell = box(1.15, 1.0, MUTED, BG, 0.05, 0.08, 1.5)
            grid = token_grid(2, 2, 0.22, [PRIMARY, ACCENT, SECONDARY, MUTED]).move_to(shell)
            frames.add(VGroup(shell, grid).move_to([x, -1.75, 0]))
        self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.2)); self.wait(BEAT)
        match_arrows = VGroup(
            arrow(frames[0][1][1].get_center(), frames[1][1][1].get_center(), ACCENT, 2),
            arrow(frames[1][1][1].get_center(), frames[2][1][1].get_center(), ACCENT, 2),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in match_arrows], lag_ratio=0.2)); self.wait(BEAT)
        self.play(FadeIn(T("Pixels are not matched directly.", 13, MUTED).move_to([0, -3.05, 0])))
        self.play(FadeIn(T("Internal diffusion features are matched.", 13, PRIMARY).move_to([0, -3.45, 0]))); self.wait(LONG)


class Scene06_TokenFlow_Denoising(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the current frame is not allowed to decide alone; aligned neighbors vote its feature into place.
        maps = VGroup(feature_map(MUTED, MUTED), feature_map(WARM, WARM), feature_map(MUTED, MUTED))
        for m, x in zip(maps, [-3.5, 0, 3.5]):
            m.move_to([x, 0.55, 0])
        headers = VGroup(
            T("Previous frame", 13, MUTED).next_to(maps[0], UP, buff=0.12),
            T("Current frame", 13, WARM).next_to(maps[1], UP, buff=0.12),
            T("Next frame", 13, MUTED).next_to(maps[2], UP, buff=0.12),
        )
        self.play(LaggedStart(*[GrowFromCenter(m[0]) for m in maps], lag_ratio=0.2), LaggedStart(*[FadeIn(m[1]) for m in maps], lag_ratio=0.2)); self.wait(BEAT)
        self.play(Write(headers)); self.wait(BEAT)
        output = Square(0.45, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.55).move_to([0, -1.75, 0])
        out_label = T("Output feature", 12, SECONDARY).next_to(output, DOWN, buff=0.08)
        prev_a = arrow(maps[0][1][6].get_center(), output.get_left(), MUTED, 3)
        next_a = arrow(maps[2][1][6].get_center(), output.get_right(), MUTED, 3)
        cur_a = arrow(maps[1][1][6].get_center(), output.get_top(), WARM, 3)
        self.play(Indicate(maps[0][1][6], color=MUTED), Indicate(maps[1][1][6], color=WARM), Indicate(maps[2][1][6], color=MUTED)); self.wait(BEAT)
        self.play(GrowArrow(prev_a), FadeIn(T("x (1 - w_i)", 12, MUTED).next_to(prev_a, UP, buff=0.04))); self.wait(BEAT)
        self.play(GrowArrow(next_a), FadeIn(T("x w_i", 12, MUTED).next_to(next_a, UP, buff=0.04))); self.wait(BEAT)
        self.play(GrowFromCenter(output), FadeIn(out_label)); self.wait(BEAT)
        self.play(GrowArrow(cur_a), FadeIn(T("x 0", 14, WARM).next_to(cur_a, RIGHT, buff=0.05)), Create(Line(cur_a.get_center() + LEFT * 0.18 + DOWN * 0.18, cur_a.get_center() + RIGHT * 0.18 + UP * 0.18, color=WARM, stroke_width=3))); self.wait(BEAT)
        self.play(FadeIn(T("Current frame does not hallucinate alone.", 16, WARM).move_to([0, -2.85, 0])))
        self.play(FadeIn(T("It borrows temporally aligned features.", 16, PRIMARY).move_to([0, -3.3, 0]))); self.wait(LONG)


class Scene07_TokenFlow_Results(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: one projector is unedited, one flickers, and TokenFlow keeps the edit coherent.
        cols = [
            ("Original", MUTED, ["dog_beach_original.png"] * 4),
            ("Per-frame editing", WARM, ["dog_beach_flickering_A.png", "dog_beach_flickering_B.png", "dog_beach_flickering_A.png", "dog_beach_flickering_B.png"]),
            ("TokenFlow", SECONDARY, ["dog_beach_colorful.png"] * 4),
        ]
        groups = []
        for x, (title, col, names) in zip([-4, 0, 4], cols):
            h = T(title, 15, col).move_to([x, 3.05, 0])
            cards = Group(*[image_card(n, 1.25, 0.9, col).move_to([x, 1.85 - i * 0.85, 0]) for i, n in enumerate(names)])
            groups.append(Group(h, cards))
        self.play(FadeIn(groups[0][0]), LaggedStart(*[FadeIn(c) for c in groups[0][1]], lag_ratio=0.1)); self.wait(BEAT)
        self.play(FadeIn(groups[1][0]), LaggedStart(*[FadeIn(c) for c in groups[1][1]], lag_ratio=0.1)); self.wait(BEAT)
        self.play(Indicate(groups[1][1][1][0], color=WARM), Indicate(groups[1][1][3][0], color=WARM)); self.wait(BEAT)
        self.play(FadeIn(groups[2][0]), LaggedStart(*[FadeIn(c) for c in groups[2][1]], lag_ratio=0.1)); self.wait(BEAT)
        arcs = VGroup(*[ArcBetweenPoints(groups[2][1][i][0].get_bottom(), groups[2][1][i + 1][0].get_top(), angle=0.25, color=PRIMARY, stroke_width=1.5) for i in range(3)])
        self.play(Create(arcs)); self.wait(BEAT)
        self.play(FadeIn(T("style shakes", 12, WARM).move_to([0, -2.2, 0])), FadeIn(T("style holds", 12, SECONDARY).move_to([4, -2.2, 0]))); self.wait(BEAT)
        self.play(FadeIn(T("Frame quality is not enough.", 18, WARM).move_to([0, -2.9, 0])))
        self.play(FadeIn(T("Temporal identity matters.", 18, SECONDARY).move_to([0, -3.35, 0]))); self.wait(LONG)


class Scene08_FateZero_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: FateZero overlays a source attention sheet and a target attention sheet instead of discarding the source layout.
        sheet1 = Group(box(4.2, 2.45, ACCENT, ACCENT, 0.12, 0.15, 2), img("jeep_road.png", 3.45, 2.0)).move_to([-1.6, 0.95, 0])
        lab1 = VGroup(T("Source attention layer", 12, ACCENT), T("road - background - original mask", 10, ACCENT)).arrange(DOWN, buff=0.08).next_to(sheet1[0], DOWN, buff=0.08)
        sheet2 = Group(box(4.2, 2.45, SECONDARY, SECONDARY, 0.12, 0.15, 2), img("porsche_road.png", 3.45, 2.0)).move_to([1.6, 0.2, 0])
        lab2 = VGroup(T("Target attention layer", 12, SECONDARY), T("new car identity", 10, SECONDARY)).arrange(DOWN, buff=0.08).next_to(sheet2[0], DOWN, buff=0.08)
        self.play(FadeIn(sheet1, shift=RIGHT * 0.5), Write(lab1)); self.wait(BEAT)
        self.play(FadeIn(T("Stable road, background, original layout", 13, ACCENT).move_to([-3.5, 2.65, 0]))); self.wait(BEAT)
        self.play(FadeIn(sheet2, shift=LEFT * 0.5), Write(lab2)); self.wait(BEAT)
        self.play(sheet1.animate.move_to([0, 0.95, 0]), sheet2.animate.move_to([0, 0.2, 0]), FadeOut(lab1), FadeOut(lab2)); self.wait(BEAT)
        blend = VGroup(box(4.55, 0.65, WHITE_ISH, BG, 0.05, 0.1, 2), T("Inverted maps + generated maps = fused attention", 12, WHITE_ISH, 4.2)).move_to([0, -2.05, 0])
        self.play(GrowArrow(arrow(sheet1[0].get_bottom(), blend[0].get_top(), ACCENT, 3)), GrowArrow(arrow(sheet2[0].get_bottom(), blend[0].get_top(), SECONDARY, 3)), GrowFromCenter(blend)); self.wait(BEAT)
        out = VGroup(box(2.9, 0.6, SECONDARY, BG, 0.08), T("Porsche on same road", 12, SECONDARY)).move_to([0, -3.1, 0])
        self.play(GrowArrow(arrow(blend[0].get_bottom(), out[0].get_top(), SECONDARY, 3)), GrowFromCenter(out)); self.wait(LONG)


class Scene09_FateZero_DDIMScan(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: DDIM inversion is a scanner that saves latent blocks and attention-map blueprints before editing.
        input_box = Group(box(2.25, 1.4, MUTED, BG, 0.08), img("jeep_road.png", 1.95, 1.15)).move_to([-4.15, 0.65, 0])
        input_lab = T("Input video", 12, MUTED).next_to(input_box[0], DOWN, buff=0.1)
        scanner = VGroup(box(2.05, 2.35, ACCENT, BG, 0.08, 0.15, 2), T("DDIM Inversion\nScanner", 13, ACCENT)).move_to([0, 0.65, 0])
        scanline = Line(LEFT * 0.72, RIGHT * 0.72, color=ACCENT, stroke_width=3).move_to(scanner[0].get_top() + DOWN * 0.35)
        outs = VGroup(
            VGroup(box(2.85, 0.55, MUTED, BG, 0.08), T("Inverted latents  [z0, z1...]", 10, MUTED)).move_to([4.0, 1.8, 0]),
            VGroup(box(2.85, 0.55, ACCENT, BG, 0.08), T("Self-attention maps", 11, ACCENT)).move_to([4.0, 1.0, 0]),
            VGroup(box(2.85, 0.55, ACCENT, BG, 0.08), T("Cross-attention maps", 11, ACCENT)).move_to([4.0, 0.2, 0]),
        )
        self.play(FadeIn(input_box), FadeIn(input_lab)); self.wait(BEAT)
        self.play(GrowArrow(arrow(input_box[0].get_right(), scanner[0].get_left(), ACCENT, 3)), GrowFromCenter(scanner)); self.wait(BEAT)
        self.play(Create(scanline)); self.play(scanline.animate.move_to(scanner[0].get_bottom() + UP * 0.35), run_time=SLOW); self.wait(BEAT)
        self.play(LaggedStart(*[GrowArrow(arrow(scanner[0].get_right(), o[0].get_left(), ACCENT, 2)) for o in outs], lag_ratio=0.2), LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.2)); self.wait(BEAT)
        words = VGroup(T("jeep -> car region", 10, ACCENT), T("road -> road region", 10, ACCENT), T("countryside -> bg region", 10, ACCENT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([4.0, -0.85, 0])
        self.play(LaggedStart(*[FadeIn(w) for w in words], lag_ratio=0.2)); self.wait(BEAT)
        self.play(Write(T("Before editing, save the video's internal attention blueprint.", 15, ACCENT).move_to([0, -2.65, 0]))); self.wait(LONG)


class Scene10_FateZero_Blending(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the stage set is locked while the foreground actor changes costume from jeep to red sports car.
        frame = box(5.0, 3.0, MUTED, BG, 0.08, 0.12, 2).move_to([0, 0.45, 0])
        jeep = img("jeep_road.png", 4.35, 2.55).move_to(frame)
        bg_mask = Rectangle(width=4.8, height=1.2, color=ACCENT, fill_color=ACCENT, fill_opacity=0.18, stroke_width=2).move_to(frame.get_center() + DOWN * 0.55)
        fg_mask = Rectangle(width=2.0, height=1.25, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.18, stroke_width=2).move_to(frame.get_center() + LEFT * 0.35 + DOWN * 0.05)
        self.play(FadeIn(frame), FadeIn(jeep)); self.wait(BEAT)
        self.play(FadeIn(bg_mask), FadeIn(lock_icon(ACCENT, 0.9).move_to(bg_mask.get_left() + RIGHT * 0.45 + UP * 0.2)), FadeIn(T("Inverted maps\npreserve source", 12, ACCENT).move_to([-4.0, -0.4, 0]))); self.wait(BEAT)
        self.play(FadeIn(T("Stage set: preserve from inverted maps.", 14, ACCENT).move_to([0, -1.55, 0]))); self.wait(BEAT)
        brush = VGroup(Line(LEFT * 0.25, RIGHT * 0.25, color=SECONDARY, stroke_width=4), Triangle(color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.4).scale(0.12).next_to(RIGHT * 0.25, RIGHT, buff=0.0)).move_to(fg_mask.get_top() + DOWN * 0.25)
        self.play(FadeIn(fg_mask), FadeIn(brush), FadeIn(T("Generated maps\nintroduce target", 12, SECONDARY).move_to([4.0, -0.4, 0]))); self.wait(BEAT)
        self.play(FadeIn(T("Actor: edit with generated maps.", 14, SECONDARY).move_to([0, -2.0, 0]))); self.wait(BEAT)
        porsche = img("porsche_road.png", 4.35, 2.55).move_to(frame)
        self.play(FadeOut(jeep, scale=0.99), FadeIn(porsche, scale=1.01)); self.wait(BEAT)
        out = Group(box(3.5, 0.9, SECONDARY, BG, 0.08), img("porsche_road.png", 1.45, 0.75), T("Red Porsche - same road, same trees", 10, SECONDARY, 1.75))
        out[1].move_to(out[0]).shift(LEFT * 0.82); out[2].move_to(out[0]).shift(RIGHT * 0.65)
        out.move_to([0, -3.0, 0])
        self.play(GrowFromCenter(out)); self.wait(LONG)


class Scene11_FateZero_Results(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: bad methods use a big brush that damages the whole frame; FateZero behaves like a scalpel.
        headers = VGroup(T("Per-frame method", 13, WARM), T("Fine-tuned method", 13, MUTED), T("FateZero", 13, SECONDARY))
        for h, x in zip(headers, [-3.6, 0.2, 4.0]):
            h.move_to([x, 3.0, 0])
        row_labs = VGroup(T("Car -> Porsche", 11, MUTED), T("+ Watercolor", 11, MUTED), T("Swan -> Crystal", 11, MUTED))
        for lab, y in zip(row_labs, [1.55, 0.0, -1.55]):
            lab.move_to([-5.4, y, 0])
        cells = VGroup()
        for x, col, words in [(-3.6, WARM, "X bg changes"), (0.2, MUTED, "~ unstable"), (4.0, SECONDARY, "OK stable bg")]:
            for y in [1.55, 0.0, -1.55]:
                cell = VGroup(box(2.05, 0.9, col, col, 0.10 if col != MUTED else 0.05, 0.08, 2), T(words, 9, col, 1.7)).move_to([x, y, 0])
                cells.add(cell)
        self.play(LaggedStart(*[Write(h) for h in headers], lag_ratio=0.1), LaggedStart(*[Write(r) for r in row_labs], lag_ratio=0.1)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(c) for c in cells[:3]], lag_ratio=0.15)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(c) for c in cells[3:6]], lag_ratio=0.15)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(c) for c in cells[6:]], lag_ratio=0.15)); self.wait(BEAT)
        brush = Circle(0.28, color=WARM, fill_color=WARM, fill_opacity=0.18).next_to(headers[0], UP, buff=0.18)
        scalpel = VGroup(Line(LEFT * 0.35, RIGHT * 0.35, color=SECONDARY, stroke_width=4), Triangle(color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.3).scale(0.12).next_to(RIGHT * 0.35, RIGHT, buff=0)).next_to(headers[2], UP, buff=0.18)
        self.play(GrowFromCenter(brush), GrowFromCenter(scalpel)); self.wait(BEAT)
        self.play(FadeIn(T("Edit target region.", 18, SECONDARY).move_to([0, -2.75, 0])))
        self.play(FadeIn(T("Preserve everything else.", 18, SECONDARY).move_to([0, -3.25, 0]))); self.wait(LONG)


class Scene12_MoreMethods_Bridges(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: every training-free method is a different bridge that stops frame islands from drifting apart.
        xs = [-5.0, -2.5, 0, 2.5, 5.0]
        islands = VGroup()
        for i, x in enumerate(xs):
            shell = box(1.25, 1.45, MUTED, BG, 0.06, 0.1, 2).move_to([x, 0.65, 0])
            lab = T(f"Frame\n{i+1}", 11, MUTED).move_to(shell)
            islands.add(VGroup(shell, lab, T(f"F{i+1}", 10, MUTED).next_to(shell, DOWN, buff=0.1)))
        self.play(LaggedStart(*[GrowFromCenter(i) for i in islands], lag_ratio=0.15)); self.wait(BEAT)
        bridges = [
            (ArcBetweenPoints(islands[0][0].get_right(), islands[1][0].get_left(), angle=-0.5, color=PRIMARY, stroke_width=3), "feature\ncorrespondence", PRIMARY),
            (DashedLine(islands[1][0].get_right(), islands[2][0].get_left(), color=ACCENT, stroke_width=3), "attention\nfusion", ACCENT),
            (ParametricFunction(lambda t: np.array([-0.62 + t * 1.24, 0.23 * np.sin(4 * PI * t), 0]), t_range=[0, 1], color=SECONDARY, stroke_width=3).move_to((islands[2][0].get_right() + islands[3][0].get_left()) / 2), "optical\nflow", SECONDARY),
            (ArcBetweenPoints(islands[3][0].get_right(), islands[4][0].get_left(), angle=0.5, color=WARM, stroke_width=4), "latent\nfusion", WARM),
        ]
        for mob, label, col in bridges:
            txt = T(label, 9, col).next_to(mob, UP, buff=0.12)
            self.play(Create(mob), FadeIn(txt)); self.wait(BEAT)
        baseline = Line(islands[0][0].get_bottom() + DOWN * 0.62, islands[-1][0].get_bottom() + DOWN * 0.62, color=MUTED, stroke_width=3)
        blocks = VGroup(*[Square(0.16, color=MUTED, fill_color=MUTED, fill_opacity=0.25).move_to(baseline.point_from_proportion(p)) for p in np.linspace(0.1, 0.9, 7)])
        self.play(Create(baseline), FadeIn(blocks), FadeIn(T("token merging", 9, MUTED).next_to(baseline, DOWN, buff=0.08))); self.wait(BEAT)
        self.play(FadeIn(T("Training-free video editing =", 17).move_to([0, -2.85, 0])))
        self.play(FadeIn(T("reuse image diffusion  +  add temporal bridges.", 17, PRIMARY).move_to([0, -3.3, 0]))); self.wait(LONG)


class Scene13_STDF_VidToMe(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: STDF reads a video as a space-time volume, while VidToMe clusters repeated tokens before editing them.
        divider = DashedLine([0, 3.35, 0], [0, -3.2, 0], color=MUTED, dash_length=0.14)
        self.play(Create(divider), FadeIn(T("STDF", 20, PRIMARY).move_to([-3.25, 2.95, 0])), FadeIn(T("VidToMe", 20, SECONDARY).move_to([3.25, 2.95, 0]))); self.wait(BEAT)
        self.play(FadeIn(T("Space-Time Diffusion Features", 12, MUTED).move_to([-3.25, 2.45, 0])), FadeIn(T("Video Token Merging", 12, MUTED).move_to([3.25, 2.45, 0]))); self.wait(BEAT)
        front = Rectangle(width=2.1, height=2.1, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.08).move_to([-3.45, 0.5, 0])
        right_face = Polygon(front.get_corner(UR), front.get_corner(UR) + RIGHT * 0.75 + UP * 0.55, front.get_corner(DR) + RIGHT * 0.75 + UP * 0.55, front.get_corner(DR), color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.04)
        top_face = Polygon(front.get_corner(UL), front.get_corner(UR), front.get_corner(UR) + RIGHT * 0.75 + UP * 0.55, front.get_corner(UL) + RIGHT * 0.75 + UP * 0.55, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.04)
        grid = token_grid(3, 3, 0.22, [MUTED]).move_to(front)
        self.play(Create(front), Create(right_face), Create(top_face), FadeIn(grid)); self.wait(BEAT)
        traj = DashedVMobject(Line(front.get_corner(DL) + RIGHT * 0.35 + UP * 0.25, front.get_corner(UR) + RIGHT * 0.9 + UP * 0.45, color=PRIMARY, stroke_width=3), num_dashes=8)
        self.play(Create(traj), FadeIn(T("space-time\nfeature path", 10, PRIMARY).next_to(traj, RIGHT, buff=0.08)), FadeIn(T("T (time)", 10, PRIMARY).next_to(right_face, RIGHT, buff=0.1))); self.wait(BEAT)

        frames = VGroup(box(1.7, 1.05, MUTED, BG, 0.05), box(1.7, 1.05, MUTED, BG, 0.05)).arrange(RIGHT, buff=0.25).move_to([3.25, 0.95, 0])
        toks = VGroup()
        colors = [PRIMARY, SECONDARY, ACCENT, MUTED, PRIMARY, SECONDARY, ACCENT, MUTED]
        for i, f in enumerate(frames):
            toks.add(token_grid(2, 4, 0.16, colors).move_to(f))
        self.play(FadeIn(frames), LaggedStart(*[FadeIn(t) for t in toks], lag_ratio=0.05)); self.wait(BEAT)
        merged = VGroup(
            Square(0.42, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.35),
            Square(0.42, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.35),
            Square(0.42, color=ACCENT, fill_color=ACCENT, fill_opacity=0.35),
        ).arrange(RIGHT, buff=0.18).move_to([3.25, -0.35, 0])
        self.play(Indicate(toks, color=WHITE_ISH)); self.wait(BEAT)
        self.play(TransformFromCopy(toks, merged), FadeIn(T("Merged tokens", 10, MUTED).next_to(merged, DOWN, buff=0.06))); self.wait(BEAT)
        denoise = VGroup(box(2.0, 0.5, PRIMARY, BG, 0.08), T("denoise once", 10, PRIMARY)).move_to([3.25, -1.25, 0])
        self.play(GrowArrow(arrow(merged.get_bottom(), denoise[0].get_top(), PRIMARY, 2)), GrowFromCenter(denoise)); self.wait(BEAT)
        split = toks.copy().scale(0.8).move_to([3.25, -2.15, 0])
        self.play(GrowArrow(arrow(denoise[0].get_bottom(), split.get_top(), SECONDARY, 2)), FadeIn(split), FadeIn(T("Unmerge -> frame tokens", 10, MUTED).next_to(split, DOWN, buff=0.04))); self.wait(BEAT)
        self.play(FadeIn(T("Instead of training, reorganize information already inside the diffusion model.", 14, WHITE_ISH, 11).move_to([0, -3.25, 0]))); self.wait(LONG)


class Scene14_FinalSummary(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: flickering independent frames disappear; all bridge mechanisms converge to one stable edited filmstrip.
        bad1 = VGroup(box(2.0, 1.25, WARM, WARM, 0.12), token_grid(2, 3, 0.22, [WARM, PRIMARY, ACCENT])).move_to([-2.45, 1.25, 0])
        bad2 = VGroup(box(2.0, 1.25, WARM, WARM, 0.12), token_grid(2, 3, 0.22, [ACCENT, WARM, SECONDARY])).move_to([2.45, 1.25, 0])
        bad1[1].move_to(bad1[0]); bad2[1].move_to(bad2[0])
        self.play(GrowFromCenter(bad1), GrowFromCenter(bad2)); self.wait(BEAT)
        flick = T("X  flickering", 13, WARM).move_to([0, 0.15, 0])
        self.play(FadeIn(flick)); self.wait(BEAT)
        self.play(FadeOut(bad1, shift=UP * 0.4), FadeOut(bad2, shift=UP * 0.4), FadeOut(flick)); self.wait(BEAT)
        rows = [
            ("TokenFlow", "feature correspondences", PRIMARY),
            ("FateZero", "attention map fusion", ACCENT),
            ("MeDM / FLATTEN", "optical flow guidance", SECONDARY),
            ("InFusion", "latent fusion", MUTED),
            ("STDF / VidToMe", "space-time features / token merging", MUTED),
        ]
        row_mobs = VGroup()
        for i, (name, detail, col) in enumerate(rows):
            row_mobs.add(VGroup(T(name, 12, col), T(detail, 11, WHITE_ISH)).arrange(RIGHT, buff=0.18).move_to([-3.3, 0.5 - i * 0.48, 0]))
        output = VGroup(box(2.8, 2.0, SECONDARY, BG, 0.08, 0.15, 2), T("Edited Video\ntemporally consistent", 13, SECONDARY, 2.2)).move_to([3.45, -0.45, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in row_mobs], lag_ratio=0.15)); self.wait(BEAT)
        arrs = VGroup(*[arrow(r.get_right(), output[0].get_left(), rows[i][2], 3) for i, r in enumerate(row_mobs)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.12), GrowFromCenter(output)); self.wait(BEAT)
        self.play(Indicate(output[0], color=SECONDARY)); self.wait(BEAT)
        self.play(Write(T("An image model edits one frame beautifully.", 17, MUTED).move_to([0, -2.95, 0])))
        self.play(Write(T("A video method makes all frames agree.", 17, PRIMARY).move_to([0, -3.4, 0]))); self.wait(LONG)
