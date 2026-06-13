# === PRODUCTION PLAN ===
# Core insight (one sentence): A video model is pretrained image knowledge plus
# a way to handle time plus clean, aligned data.
#
# Color encoding:
#   PRIMARY   = time / temporal dimension / motion / connections between frames
#   SECONDARY = spatial content / single-frame quality / what things look like
#   WARM      = problems / artifacts / cost / rejected or bad data
#   ACCENT    = active model / mechanism currently under the microscope
#   MUTED     = closed systems / raw data / inactive states
#   WHITE_ISH = all text labels
#
# Scene list:
#   Scene01_LockedStudio — visible results behind a locked studio vs an open lab
#   Scene02_FiveModelsOneQuestion — five approaches orbit one shared question
#   Scene03_PainterToAnimator — one-image painter stretches across time
#   Scene04_InflateTo3D — a 2D image extrudes into a time stack
#   Scene05_FlipbookAndWindows — spatial scan within pages, temporal scan across pages
#   Scene06_SameDogEveryFrame — attention binds parts and identity
#   Scene07_AccordionAndCollapse — variable length collapses back to one image
#   Scene08_WatermarkGhost — an artifact seeps from training data into output
#   Scene09_CleaningTheLens — cleaner fine-tuning removes the inherited habit
#   Scene10_PandaSignChecklist — prompt alignment becomes a visible checklist
#   Scene11_TwoArtistsCanvasVsSketch — pixel directness vs latent efficiency
#   Scene12_DirectorAndCinematographer — pixel directs, latent polishes
#   Scene13_AnimationProductionLine — Show-1's four generation stages
#   Scene14_VideoCrafterUNetAndGuidance — temporal blocks slot into a latent U-Net
#   Scene15_TwoQuestionsRevisited — spatial and temporal transformers work together
#   Scene16_TwoPilesOfData — messy and clean datasets teach different habits
#   Scene17_TwoStreamsAndStaircase — joint tuning plus curriculum learning
#   Scene18_LaVieGallery — four real LaVie worlds from one model
#   Scene19_DataPipelineAndCutDetection — raw timelines split into clean clips
#   Scene20_CaptionMergeAndFilterGate — captions merge and samples are filtered
#   Scene21_FlowArrowsAndOCRBox — motion and text filters expose bad clips
#   Scene22_FunnelToCuratedSet — a huge raw set compresses to a bright core
#   Scene23_ThreeStageRail — SVD learns looks, motion, then general capability
#   Scene24_PainterBecomesFilmmaker — all lessons converge into filmmaking
#
# Key transforms:
#   - locked wall -> open door in Scene01
#   - painter's canvas -> film strip in Scene03
#   - square -> time stack in Scene04
#   - accordion -> one image in Scene07
#   - dirty lens -> clean lens in Scene09
#   - compressed sketch -> decoded image in Scene11
#   - low-res pixel scene -> high-res latent scene in Scene12
#   - raw timeline -> separated clips in Scene19
#   - painter's canvas -> film reel in Scene24
# ======================

from manim import *
import numpy as np
import os

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

ASSET_DIR = os.path.join(os.path.dirname(__file__), "images", "2.2")


def txt(s, color=WHITE_ISH, size=24):
    return Text(s, color=color, font_size=size)


def frame(w=1.5, h=1.1, color=WHITE_ISH, fill=BG, opacity=0.0):
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.08, color=color, stroke_width=3,
        fill_color=fill, fill_opacity=opacity,
    )


def film_strip(n=5, w=0.75, h=0.62, color=PRIMARY):
    fs = VGroup(*[frame(w, h, color) for _ in range(n)]).arrange(RIGHT, buff=0.09)
    return fs


def dog(color=SECONDARY, scale=1):
    body = Ellipse(width=0.9, height=0.42, color=color, fill_color=color, fill_opacity=0.5)
    head = Circle(0.22, color=color, fill_color=color, fill_opacity=0.5).next_to(body, RIGHT, buff=-0.07).shift(UP * 0.1)
    legs = VGroup(*[
        Line(body.get_center() + x + DOWN * 0.1, body.get_center() + x + DOWN * 0.42, color=color, stroke_width=4)
        for x in (LEFT * 0.25, RIGHT * 0.25)
    ])
    tail = ArcBetweenPoints(body.get_left(), body.get_left() + LEFT * 0.35 + UP * 0.25, angle=-0.7, color=color, stroke_width=4)
    return VGroup(body, head, legs, tail).scale(scale)


def person(color=WHITE_ISH, scale=1):
    p = VGroup(
        Circle(0.15, color=color, fill_color=color, fill_opacity=0.35).shift(UP * 0.48),
        Line(UP * 0.32, DOWN * 0.3, color=color, stroke_width=4),
        Line(UP * 0.12, LEFT * 0.36 + DOWN * 0.05, color=color, stroke_width=4),
        Line(UP * 0.12, RIGHT * 0.36 + DOWN * 0.05, color=color, stroke_width=4),
        Line(DOWN * 0.3, LEFT * 0.28 + DOWN * 0.7, color=color, stroke_width=4),
        Line(DOWN * 0.3, RIGHT * 0.28 + DOWN * 0.7, color=color, stroke_width=4),
    )
    return p.scale(scale)


def gear(color=ACCENT, r=0.3):
    return VGroup(
        Circle(r, color=color, stroke_width=4),
        Circle(r * 0.22, color=color, fill_color=color, fill_opacity=1),
        *[Line(rotate_vector(RIGHT * r * 0.3, a), rotate_vector(RIGHT * r, a), color=color, stroke_width=3)
          for a in np.linspace(0, TAU, 8, endpoint=False)]
    )


def watermark(w=1.7):
    return VGroup(
        Line(LEFT * w / 2 + DOWN * 0.48, RIGHT * w / 2 + UP * 0.48, color=WARM, stroke_width=18).set_opacity(0.38),
        Line(LEFT * w / 2 + UP * 0.48, RIGHT * w / 2 + DOWN * 0.48, color=WARM, stroke_width=8).set_opacity(0.22),
        txt("WATERMARK", WHITE_ISH, max(16, int(w * 8))).rotate(0.3),
    )


def mini_scene(w=2.2, h=1.5, crisp=True):
    box = frame(w, h, SECONDARY if crisp else MUTED, PRIMARY, 0.08)
    ground = Line(box.get_left() + RIGHT * 0.12 + DOWN * 0.4, box.get_right() + LEFT * 0.12 + DOWN * 0.4, color=SECONDARY)
    sun = Circle(0.13, color=ACCENT, fill_color=ACCENT, fill_opacity=0.7).move_to(box.get_corner(UR) + LEFT * 0.35 + DOWN * 0.3)
    subject = dog(SECONDARY, 0.65).move_to(box.get_center() + DOWN * 0.15)
    g = VGroup(box, ground, sun, subject)
    if not crisp:
        g.set_opacity(0.42)
    return g


def model_emblems():
    strip = film_strip(3, 0.3, 0.25, PRIMARY)
    split = VGroup(Arc(radius=0.34, start_angle=PI / 2, angle=PI, color=SECONDARY),
                   Arc(radius=0.34, start_angle=-PI / 2, angle=PI, color=PRIMARY),
                   Line(UP * 0.34, DOWN * 0.34, color=WHITE_ISH))
    ushape = VGroup(Line(LEFT * 0.35 + UP * 0.3, LEFT * 0.35 + DOWN * 0.25, color=SECONDARY),
                    ArcBetweenPoints(LEFT * 0.35 + DOWN * 0.25, RIGHT * 0.35 + DOWN * 0.25, angle=PI, color=SECONDARY),
                    Line(RIGHT * 0.35 + DOWN * 0.25, RIGHT * 0.35 + UP * 0.3, color=SECONDARY))
    stairs = VGroup(*[Square(0.18, color=ACCENT, fill_color=ACCENT, fill_opacity=0.25).shift(RIGHT * i * 0.18 + UP * i * 0.18) for i in range(3)])
    funnel = Polygon(LEFT * 0.45 + UP * 0.3, RIGHT * 0.45 + UP * 0.3, RIGHT * 0.12 + DOWN * 0.1,
                     RIGHT * 0.12 + DOWN * 0.42, LEFT * 0.12 + DOWN * 0.42, LEFT * 0.12 + DOWN * 0.1,
                     color=ACCENT)
    return VGroup(strip, split, ushape, stairs, funnel)


def image_panel(path, w=3.0, h=1.8):
    border = frame(w, h, PRIMARY)
    img = ImageMobject(path)
    img.set_height(h - 0.12)
    if img.width > w - 0.12:
        img.set_width(w - 0.12)
    return Group(border, img.move_to(border))


def photo(name, w=2.0, h=1.4, opacity=1.0):
    img = ImageMobject(os.path.join(ASSET_DIR, name))
    img.set_opacity(opacity)
    if img.width / img.height > w / h:
        img.set_width(w)
    else:
        img.set_height(h)
    return img


def photo_panel(name, w=2.0, h=1.4, color=WHITE_ISH, opacity=1.0):
    border = frame(w, h, color, BG, 1)
    img = photo(name, w - 0.12, h - 0.12, opacity).move_to(border)
    return Group(border, img)


def dog_photo(index, w=1.8, h=1.25, color=SECONDARY, opacity=1.0):
    return photo_panel(f"dog_{index % 6}.jpg", w, h, color, opacity)


def photo_card(name, caption, w=1.7, h=1.1, color=SECONDARY, opacity=1.0):
    panel = photo_panel(name, w, h, color, opacity)
    label = txt(caption, WHITE_ISH, 13).next_to(panel, DOWN, buff=0.08)
    return Group(panel, label)


class Scene01_LockedStudio(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A viewer can see glowing results through windows, but only the open lab exposes the mechanism.
        studio = RoundedRectangle(width=7, height=3.4, corner_radius=0.15, color=MUTED).shift(LEFT * 2)
        windows = VGroup(*[frame(1, 0.65, SECONDARY, SECONDARY, 0.1) for _ in range(5)]).arrange(RIGHT, buff=0.22).move_to(studio.get_center() + UP * 0.55)
        inner = VGroup(*[Circle(0.11 + i * 0.015, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.5).move_to(w) for i, w in enumerate(windows)])
        wall = Rectangle(width=1.0, height=1.45, color=MUTED, fill_color=MUTED, fill_opacity=0.35).move_to(studio.get_bottom() + UP * 0.75)
        lock = VGroup(Rectangle(width=0.45, height=0.42, color=WARM), Arc(radius=0.22, start_angle=0, angle=PI, color=WARM).shift(UP * 0.22)).move_to(wall)
        self.play(Create(studio)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(w) for w in windows], *[GrowFromCenter(x) for x in inner], lag_ratio=0.1)); self.wait(BEAT)
        self.play(FadeIn(wall), GrowFromCenter(lock), FadeIn(txt("machinery hidden", WARM, 20).next_to(wall, DOWN))); self.wait(BEAT)
        lab = RoundedRectangle(width=3, height=3, corner_radius=0.15, color=ACCENT).shift(RIGHT * 4.5)
        door = Rectangle(width=0.75, height=1.3, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.12).move_to(lab.get_bottom() + UP * 0.68)
        core = gear(ACCENT, 0.35).move_to(lab.get_center() + UP * 0.55)
        label = txt("open-source foundation models", WHITE_ISH, 18).next_to(lab, UP)
        self.play(GrowFromEdge(lab, DOWN), Create(door), GrowFromCenter(core), FadeIn(label)); self.wait(BEAT)
        people = VGroup(*[person(PRIMARY, 0.42) for _ in range(3)]).arrange(RIGHT, buff=0.18).move_to(lab.get_center() + DOWN * 0.45)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT) for p in people], lag_ratio=0.2), Indicate(core)); self.wait(LONG)


class Scene02_FiveModelsOneQuestion(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Five distinct mechanisms are arranged as answers to one central transformation.
        q = MathTex("?", color=ACCENT).scale(2)
        ring = Circle(1.0, color=ACCENT).move_to(q)
        prompt = txt("image diffusion  →  video diffusion?", WHITE_ISH, 24).next_to(ring, DOWN, buff=0.35)
        self.play(Write(q), Create(ring), FadeIn(prompt)); self.wait(BEAT)
        names = ["ModelScopeT2V", "Show-1", "VideoCrafter", "LaVie", "SVD"]
        emblems = model_emblems()
        positions = [UP * 2.65 + LEFT * 3.4, UP * 2.65 + RIGHT * 3.4, LEFT * 4.5 + DOWN * 1.2, RIGHT * 4.5 + DOWN * 1.2, DOWN * 2.6]
        groups = VGroup(*[VGroup(e, txt(n, WHITE_ISH, 17).next_to(e, DOWN, buff=0.15)).move_to(p) for e, n, p in zip(emblems, names, positions)])
        self.play(LaggedStart(*[GrowFromCenter(g) for g in groups], lag_ratio=0.18)); self.wait(BEAT)
        links = VGroup()
        for g in groups:
            direction = ring.get_center() - g[0].get_center()
            links.add(Line(
                g[0].get_boundary_point(direction),
                ring.get_boundary_point(-direction),
                color=PRIMARY, stroke_width=2,
            ).set_opacity(0.55))
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.15)); self.wait(BEAT)
        self.play(LaggedStart(*[Indicate(g[0], color=ACCENT) for g in groups], lag_ratio=0.3)); self.wait(LONG)


class Scene03_PainterToAnimator(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A real painter cycles through real subjects, then the canvas frame multiplies across time.
        painter = photo_panel("painter.jpg", 2.7, 3.4, SECONDARY).shift(LEFT * 4.7)
        canvas = frame(2.35, 1.65, SECONDARY).shift(LEFT * 2.0 + UP * 0.35)
        subjects = [photo(n, 2.35, 1.65).move_to(canvas) for n in
                    ["dog_0.jpg", "robot.jpg", "city.jpg", "sunset.jpg", "panda.jpg", "waterfall.jpg"]]
        self.play(FadeIn(painter), Create(canvas), FadeIn(subjects[0])); self.wait(BEAT)
        current = subjects[0]
        for target in subjects[1:]:
            self.play(FadeTransform(current, target), run_time=FAST)
            current = target
        self.wait(BEAT)
        ghost = frame(1.8, 1.3, MUTED).next_to(canvas, RIGHT, buff=0.35)
        clock = VGroup(Circle(0.3, color=WARM), Line(ORIGIN, UP * 0.18, color=WARM), Line(ORIGIN, RIGHT * 0.13, color=WARM)).next_to(canvas, UP)
        self.play(Create(clock), Wiggle(current)); self.wait(BEAT)
        self.play(FadeIn(ghost), Wiggle(ghost), FadeOut(ghost)); self.wait(BEAT)
        question = txt("...can it become an animator?", ACCENT, 26).to_edge(UP)
        self.play(FadeIn(question)); self.wait(BEAT)
        self.play(FadeOut(current), FadeOut(clock))
        strip = film_strip(6, 0.95, 0.82, SECONDARY).move_to(RIGHT * 3.0 + UP * 0.25)
        motion = Line(strip.get_left() + DOWN * 0.75, strip.get_right() + DOWN * 0.75, color=PRIMARY, stroke_width=5)
        copies = Group(*[photo(f"dog_{i}.jpg", 0.95, 0.8).move_to(f) for i, f in enumerate(strip)])
        self.play(ReplacementTransform(canvas.copy(), strip), LaggedStart(*[FadeIn(d) for d in copies], lag_ratio=0.12), Create(motion), run_time=SLOW)
        self.wait(LONG)


class Scene04_InflateTo3D(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The original image face stays bright while new temporal faces grow behind it.
        image = Square(2.5, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.12)
        grid = VGroup(*[Dot(color=SECONDARY, radius=0.045) for _ in range(16)]).arrange_in_grid(4, 4, buff=0.35).move_to(image)
        axes = VGroup(MathTex("H", color=SECONDARY).next_to(image, LEFT), MathTex("W", color=SECONDARY).next_to(image, DOWN))
        self.play(Create(image), LaggedStart(*[FadeIn(d) for d in grid], lag_ratio=0.05), Write(axes)); self.wait(BEAT)
        t_dir = normalize(RIGHT * 2 + UP * 1.2)
        t = Arrow(image.get_right(), image.get_right() + t_dir * 2.4, color=PRIMARY, buff=0.05)
        tl = MathTex("t", color=PRIMARY).next_to(t, UP)
        self.play(GrowArrow(t), Write(tl)); self.wait(BEAT)
        faces = VGroup(*[Square(2.5, color=PRIMARY, fill_opacity=0).shift(t_dir * i * 0.42) for i in range(5, 0, -1)])
        stack = VGroup(faces, image, grid)
        self.play(LaggedStart(*[Create(f) for f in faces], lag_ratio=0.12), run_time=SLOW); self.wait(BEAT)
        labels = VGroup(txt("pretrained weights — kept", SECONDARY, 18).next_to(image, DOWN, buff=0.8).shift(LEFT * 0.5),
                        txt("temporal layers — added", PRIMARY, 18).move_to(RIGHT * 4.0 + UP * 1.4))
        self.play(FadeIn(labels)); self.wait(BEAT)
        self.play(Indicate(image, color=SECONDARY), Indicate(faces, color=PRIMARY)); self.wait(LONG)


class Scene05_FlipbookAndWindows(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A real photographic flipbook is read within a page for appearance and through pages for motion.
        pages = VGroup(*[frame(2.5, 1.7, WHITE_ISH).shift(RIGHT * i * 0.16 + UP * i * 0.11) for i in range(6, -1, -1)]).shift(LEFT * 2)
        dogs = Group(*[photo(f"dog_{i % 6}.jpg", 2.3, 1.5).move_to(p) for i, p in enumerate(pages)])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.12) for p in pages], lag_ratio=0.1), LaggedStart(*[FadeIn(d) for d in dogs], lag_ratio=0.1)); self.wait(BEAT)
        scan = Square(0.55, color=SECONDARY, stroke_width=4).move_to(pages[-1].get_left() + RIGHT * 0.5)
        self.play(Create(scan), scan.animate.shift(RIGHT * 1.45), run_time=SLOW); self.wait(BEAT)
        self.play(LaggedStart(*[Indicate(d, color=PRIMARY) for d in dogs], lag_ratio=0.1)); self.wait(BEAT)
        label = VGroup(txt("2D spatial", SECONDARY, 24), MathTex("+", color=WHITE_ISH), txt("1D temporal", PRIMARY, 24)).arrange(RIGHT).to_edge(UP)
        self.play(FadeIn(label)); self.wait(BEAT)
        left = photo_panel("dog_2.jpg", 3.1, 2.1, SECONDARY).shift(LEFT * 3.3 + DOWN * 1.5)
        right = Group(*[dog_photo(i, 2.2, 1.45, PRIMARY).shift(RIGHT * i * 0.13 + UP * i * 0.09) for i in range(4, -1, -1)]).shift(RIGHT * 3.2 + DOWN * 1.5)
        sw = Square(0.48, color=SECONDARY).move_to(left.get_left() + RIGHT * 0.4)
        tw = Square(0.48, color=PRIMARY).move_to(right.get_left() + RIGHT * 0.4)
        self.play(FadeIn(left), FadeIn(right), Create(sw), Create(tw))
        self.play(sw.animate.shift(RIGHT * 2.3), tw.animate.shift(RIGHT * 1.2 + UP * 0.8), run_time=SLOW)
        self.play(FadeIn(txt("spatial window: moves across one photo", SECONDARY, 18).next_to(left, DOWN)),
                  FadeIn(txt("temporal window: follows one paw through frames", PRIMARY, 18).next_to(right, DOWN))); self.wait(LONG)


class Scene06_SameDogEveryFrame(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Temporal attention binds the same real dog across widely separated frames.
        dogs = Group(*[dog_photo(i, 2.3, 1.55, MUTED, 0.45) for i in [0, 2, 3, 5]]).arrange(RIGHT, buff=0.35).shift(DOWN * 0.15)
        nums = VGroup(*[txt(str(n), WHITE_ISH, 18).next_to(d, DOWN) for n, d in zip([1, 4, 8, 12], dogs)])
        self.play(LaggedStart(*[FadeIn(d) for d in dogs], lag_ratio=0.2), FadeIn(nums)); self.wait(BEAT)
        self.play(LaggedStart(*[d[1].animate.set_opacity(1) for d in dogs], lag_ratio=0.15)); self.wait(BEAT)
        arcs = VGroup(*[ArcBetweenPoints(dogs[i].get_top(), dogs[i + 1].get_top(), angle=-0.6, color=PRIMARY, stroke_width=4) for i in range(3)])
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2)); self.wait(BEAT)
        caption = txt("temporal attention — still the same dog", WHITE_ISH, 23).to_edge(DOWN)
        self.play(FadeIn(caption)); self.wait(LONG)


class Scene07_AccordionAndCollapse(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Frame count and attention-map size visibly expand together, then collapse to image mode.
        title = txt("the temporal dimension can change length", WHITE_ISH, 26).to_edge(UP)
        row8 = Group(*[dog_photo(i, 1.15, 0.75, PRIMARY) for i in range(8)]).arrange(RIGHT, buff=0.08).shift(DOWN * 0.1)
        map8 = VGroup(*[Square(0.07, color=PRIMARY, stroke_width=1) for _ in range(64)]).arrange_in_grid(8, 8, buff=0.01).shift(UP * 1.75)
        n8 = txt("8 frames  ↔  8×8 temporal attention", PRIMARY, 21).to_edge(DOWN)
        self.play(FadeIn(title), LaggedStart(*[FadeIn(f) for f in row8], lag_ratio=0.08), FadeIn(map8), FadeIn(n8)); self.wait(BEAT)
        row16 = Group(*[dog_photo(i % 6, 0.58, 0.42, PRIMARY) for i in range(16)]).arrange(RIGHT, buff=0.035).move_to(row8)
        map16 = VGroup(*[Square(0.035, color=PRIMARY, stroke_width=0.5) for _ in range(256)]).arrange_in_grid(16, 16, buff=0.004).move_to(map8)
        n16 = txt("16 frames  ↔  larger 16×16 attention", PRIMARY, 21).move_to(n8)
        self.play(FadeOut(row8), FadeIn(row16), ReplacementTransform(map8, map16), Transform(n8, n16), run_time=SLOW); self.wait(BEAT)
        one = dog_photo(0, 3.0, 2.0, SECONDARY).move_to(DOWN * 0.1)
        one_cell = Square(0.5, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.2).move_to(map16)
        self.play(FadeOut(row16), FadeIn(one), ReplacementTransform(map16, one_cell),
                  Transform(n8, txt("1 frame  ↔  image generation mode", SECONDARY, 24).move_to(n8)), run_time=SLOW); self.wait(BEAT)
        self.play(Indicate(one, color=SECONDARY)); self.wait(LONG)


class Scene08_WatermarkGhost(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The exact same generated shot inherits a visible watermark from its examples.
        clean = photo_panel("dog_grass.png", 4.4, 2.8, SECONDARY).shift(LEFT * 1.6)
        clips = VGroup(*[VGroup(frame(1.5, 0.9, MUTED), watermark(1.2)).shift(RIGHT * i * 0.13 + UP * i * 0.1) for i in range(3, -1, -1)]).shift(RIGHT * 4.2)
        self.play(GrowFromCenter(clean)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(c) for c in clips], lag_ratio=0.15)); self.wait(BEAT)
        lineage = DashedLine(clips.get_left(), clean.get_right(), color=WARM)
        self.play(Create(lineage)); self.wait(BEAT)
        inherited = watermark(3.5).move_to(clean)
        self.play(FadeIn(inherited), run_time=SLOW); self.wait(BEAT)
        self.play(FadeIn(txt("not added on purpose — copied from the data", WHITE_ISH, 24).to_edge(DOWN)), Indicate(inherited, color=WARM)); self.wait(LONG)


class Scene09_CleaningTheLens(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same shot is cleaned; only the inherited watermark and softness disappear.
        scene = photo_panel("dog_grass.png", 4.2, 2.8, WARM, 0.65)
        mark = watermark(3.4).move_to(scene)
        lens = Circle(2.0, color=MUTED, fill_color=MUTED, fill_opacity=0.12)
        smudges = VGroup(*[Arc(radius=0.65 + i * 0.16, start_angle=0.3, angle=1.8, color=MUTED).rotate(i * 0.45) for i in range(5)])
        cloth = Polygon(LEFT * 0.3, RIGHT * 0.4, UP * 0.25, color=WHITE_ISH, fill_color=WHITE_ISH, fill_opacity=0.8).move_to(lens.get_left())
        self.play(FadeIn(scene), FadeIn(mark), FadeIn(lens), Create(smudges)); self.wait(BEAT)
        self.play(cloth.animate.move_to(lens.get_right()), LaggedStart(*[Uncreate(s) for s in smudges], lag_ratio=0.15), run_time=SLOW); self.wait(BEAT)
        crisp = photo_panel("dog_grass.png", 4.2, 2.8, SECONDARY)
        self.play(FadeOut(scene), FadeOut(mark), FadeIn(crisp), FadeOut(lens), FadeOut(cloth)); self.wait(BEAT)
        before = Group(photo_panel("dog_grass.png", 2.2, 1.4, WARM), watermark(1.8)).shift(LEFT * 3.5 + DOWN * 1.8)
        after = photo_panel("dog_grass.png", 2.2, 1.4, SECONDARY).shift(RIGHT * 3.5 + DOWN * 1.8)
        self.play(FadeIn(before), FadeIn(after), FadeIn(txt("same ability — cleaner textbook", WHITE_ISH, 23).to_edge(DOWN))); self.wait(LONG)


class Scene10_PandaSignChecklist(Scene):
    def construct(self):
        self.camera.background_color = BG
        # One coherent generated frame contains the panda and waterfall, but no sign or text.
        prompt = txt("\"A panda beside a waterfall holding a sign that says 'Show Lab'\"", WHITE_ISH, 20).to_edge(UP)
        self.play(Write(prompt)); self.wait(BEAT)
        rows = VGroup(*[VGroup(Square(0.28, color=MUTED), txt(s, WHITE_ISH, 19)).arrange(RIGHT, buff=0.18) for s in ["panda", "waterfall", "sign", "text \"Show Lab\""]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(LEFT * 4 + DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.15)); self.wait(BEAT)
        panel = photo_panel("panda_waterfall_no_sign.png", 5.4, 3.2, PRIMARY).shift(RIGHT * 2.5 + DOWN * 0.2)
        self.play(FadeIn(panel)); self.wait(BEAT)
        checks = VGroup(*[txt("✓", SECONDARY, 28).move_to(rows[i][0]) for i in range(2)],
                        *[txt("✗", WARM, 28).move_to(rows[i][0]) for i in range(2, 4)])
        self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.25)); self.wait(BEAT)
        cap = txt("2 of 4 — looks good, does not fully listen", WHITE_ISH, 24).to_edge(DOWN)
        self.play(FadeIn(cap), Circumscribe(VGroup(rows[2], rows[3]), color=WARM)); self.wait(LONG)


class Scene11_TwoArtistsCanvasVsSketch(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same real image goes through a direct pipeline and a compressed lossy pipeline.
        left = photo_panel("dog_grass.png", 4.6, 2.8, SECONDARY).shift(LEFT * 3.5 + UP * 0.25)
        right = photo_panel("dog_grass.png", 4.6, 2.8, PRIMARY).shift(RIGHT * 3.5 + UP * 0.25)
        title = txt("the same image — two ways to work on it", WHITE_ISH, 24).to_edge(UP)
        self.play(FadeIn(title), FadeIn(left), FadeIn(right)); self.wait(BEAT)
        cursor = Dot(color=ACCENT, radius=0.09).move_to(left.get_corner(UL) + RIGHT * 0.7 + DOWN * 0.5)
        detail_points = [left.get_center() + RIGHT * 1.1 + UP * 0.35, left.get_center() + RIGHT * 0.55 + UP * 0.7,
                         left.get_center() + RIGHT * 1.3 + DOWN * 0.5, left.get_center() + LEFT * 1.2]
        self.play(FadeIn(cursor))
        for p in detail_points:
            self.play(cursor.animate.move_to(p), Flash(p, color=SECONDARY), run_time=FAST)
        self.play(FadeIn(txt("pixel-space: every detail reachable", SECONDARY, 19).next_to(left, DOWN))); self.wait(BEAT)
        tiny = photo_panel("dog_grass_pixelated.png", 1.1, 0.7, PRIMARY).move_to(right)
        self.play(FadeOut(right), FadeIn(tiny), FadeIn(txt("latent-space: compress first", PRIMARY, 19).next_to(right, DOWN))); self.wait(BEAT)
        decoded = photo_panel("dog_grass_pixelated.png", 4.6, 2.8, WARM).move_to(right)
        self.play(FadeOut(tiny), FadeIn(decoded), run_time=SLOW); self.wait(BEAT)
        scores = VGroup(txt("direct · faithful · expensive", SECONDARY, 18).move_to(LEFT * 3.5 + DOWN * 2.6),
                        txt("cheap · fast · lossy", WARM, 18).move_to(RIGHT * 3.5 + DOWN * 2.6))
        self.play(FadeIn(scores)); self.wait(LONG)


class Scene12_DirectorAndCinematographer(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A carefully directed low-resolution video becomes a larger, sharper video.
        low = Group(*[photo_panel("dog_grass_pixelated.png", 0.82, 0.56, SECONDARY) for _ in range(5)]).arrange(RIGHT, buff=0.05).shift(LEFT * 3.8 + UP * 0.3)
        chair = VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=ACCENT), Line(LEFT * 0.25, LEFT * 0.4 + DOWN * 0.5, color=ACCENT), Line(RIGHT * 0.25, RIGHT * 0.4 + DOWN * 0.5, color=ACCENT)).next_to(low, LEFT)
        self.play(LaggedStart(*[FadeIn(f) for f in low], lag_ratio=0.12), Create(chair), run_time=SLOW); self.wait(BEAT)
        director = txt("pixel stage — directs a small, controlled video", WHITE_ISH, 19).next_to(low, DOWN)
        self.play(FadeIn(director)); self.wait(BEAT)
        tiny = low.copy().scale(0.28).move_to(ORIGIN)
        self.play(ReplacementTransform(low.copy(), tiny)); self.wait(BEAT)
        high = Group(*[dog_photo(i, 1.05, 0.72, PRIMARY) for i in range(5)]).arrange(RIGHT, buff=0.06).shift(RIGHT * 2.8 + UP * 0.3)
        camera = VGroup(Rectangle(width=0.65, height=0.42, color=ACCENT), Triangle(color=ACCENT).scale(0.18).rotate(-PI / 2).next_to(ORIGIN, RIGHT, buff=0)).next_to(high, RIGHT)
        path = Arrow(low.get_right(), high.get_left(), color=PRIMARY)
        self.play(FadeOut(tiny), GrowArrow(path), LaggedStart(*[FadeIn(f) for f in high], lag_ratio=0.1), GrowFromCenter(camera), run_time=SLOW); self.wait(BEAT)
        self.play(FadeIn(txt("latent stage — makes every frame large and sharp", WHITE_ISH, 19).next_to(high, DOWN))); self.wait(BEAT)
        self.play(FadeIn(txt("small pixel video  →  high-resolution latent video", PRIMARY, 24).to_edge(UP))); self.wait(LONG)


class Scene13_AnimationProductionLine(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same real motion-study photos gain density and detail station by station.
        rail = Line(LEFT * 5.5 + DOWN * 1.8, RIGHT * 5.5 + DOWN * 1.8, color=MUTED, stroke_width=5)
        xs = [-4.5, -1.5, 1.5, 4.5]
        stations = VGroup(*[Dot(np.array([x, -1.8, 0]), color=ACCENT, radius=0.1) for x in xs])
        names = ["keyframes", "interpolation", "super-resolution", "final render"]
        labels = VGroup(*[txt(n, WHITE_ISH, 17).next_to(s, DOWN) for n, s in zip(names, stations)])
        self.play(Create(rail), LaggedStart(*[FadeIn(s) for s in stations], *[FadeIn(l) for l in labels], lag_ratio=0.1)); self.wait(BEAT)
        sparse = Group(dog_photo(0, 2.6, 1.75, MUTED, 0.45), dog_photo(5, 2.6, 1.75, MUTED, 0.45)).arrange(RIGHT, buff=1.1).move_to(UP * 0.45)
        self.play(FadeIn(sparse), Flash(stations[0], color=ACCENT), Indicate(labels[0], color=ACCENT)); self.wait(BEAT)
        interp = Group(*[dog_photo(i, 1.65, 1.1, MUTED, 0.45) for i in range(5)]).arrange(RIGHT, buff=0.18).move_to(UP * 0.45)
        self.play(FadeOut(sparse), LaggedStart(*[FadeIn(d) for d in interp], lag_ratio=0.12),
                  Flash(stations[1], color=ACCENT), Indicate(labels[1], color=ACCENT)); self.wait(BEAT)
        clean = Group(*[dog_photo(i, 1.65, 1.1, SECONDARY) for i in range(5)]).arrange(RIGHT, buff=0.18).move_to(UP * 0.45)
        self.play(FadeOut(interp), FadeIn(clean), Flash(stations[2], color=ACCENT), Indicate(labels[2], color=ACCENT)); self.wait(BEAT)
        final = Group(*[dog_photo(i, 1.8, 1.2, SECONDARY) for i in range(5)]).arrange(RIGHT, buff=0.18).move_to(UP * 0.45)
        self.play(FadeOut(clean), LaggedStart(*[FadeIn(f) for f in final], lag_ratio=0.1),
                  Flash(stations[3], color=ACCENT), Indicate(labels[3], color=ACCENT)); self.wait(LONG)


class Scene14_VideoCrafterUNetAndGuidance(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Temporal blocks slot into the U-Net, then text and image guidance visibly produce the promised result.
        coords = [(-2.4, 1.2), (-1.3, 0.2), (0, -0.7), (1.3, 0.2), (2.4, 1.2)]
        blocks = VGroup(*[RoundedRectangle(width=1.0, height=0.7, corner_radius=0.1, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.14).move_to([x, y, 0]) for x, y in coords])
        links = VGroup(*[Line(blocks[i].get_center(), blocks[i + 1].get_center(), color=MUTED) for i in range(4)])
        image_label = txt("green blocks: image model understands each frame", SECONDARY, 18).to_edge(UP)
        self.play(LaggedStart(*[Create(b) for b in blocks], lag_ratio=0.15), Create(links), FadeIn(image_label)); self.wait(BEAT)
        slots = VGroup(*[Rectangle(width=0.42, height=0.42, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.4).move_to((blocks[i].get_center() + blocks[i + 1].get_center()) / 2) for i in range(4)])
        starts = [UP * 3 + LEFT * 3, UP * 3 + LEFT, UP * 3 + RIGHT, UP * 3 + RIGHT * 3]
        for slot, start in zip(slots, starts):
            slot.move_to(start)
        temporal_label = txt("blue blocks: added between them to connect time", PRIMARY, 18).move_to(image_label)
        self.play(LaggedStart(*[slot.animate.move_to((blocks[i].get_center() + blocks[i + 1].get_center()) / 2) for i, slot in enumerate(slots)], lag_ratio=0.2),
                  Transform(image_label, temporal_label)); self.wait(BEAT)
        self.play(LaggedStart(*[Indicate(s, color=PRIMARY) for s in slots], lag_ratio=0.15)); self.wait(BEAT)
        text_in = VGroup(frame(2.5, 0.8, WHITE_ISH), txt("text: run on the grass", WHITE_ISH, 18)).shift(LEFT * 5 + UP * 2.2)
        image_in = Group(photo_panel("dog_2.jpg", 2.5, 1.25, SECONDARY), txt("image: how it looks", SECONDARY, 16)).arrange(DOWN, buff=0.1).shift(LEFT * 5 + DOWN * 1.3)
        arrows = VGroup(Arrow(text_in.get_right(), blocks[0].get_left(), color=WHITE_ISH), Arrow(image_in.get_right(), blocks[0].get_left(), color=SECONDARY))
        self.play(FadeIn(text_in), FadeIn(image_in), GrowArrow(arrows[0]), GrowArrow(arrows[1])); self.wait(BEAT)
        self.play(FadeOut(text_in), FadeOut(image_in), FadeOut(arrows), Flash(blocks[0], color=ACCENT)); self.wait(BEAT)
        output = photo_panel("dog_grass.png", 3.3, 2.0, ACCENT).shift(RIGHT * 4.15 + DOWN * 0.2)
        out_arrow = Arrow(blocks[-1].get_right(), output.get_left(), color=ACCENT, buff=0.12)
        self.play(GrowArrow(out_arrow), FadeIn(output))
        self.play(Circumscribe(output, color=ACCENT),
                  FadeIn(txt("same dog + run on the grass", WHITE_ISH, 20).next_to(output, DOWN))); self.wait(LONG)


class Scene15_TwoQuestionsRevisited(Scene):
    def construct(self):
        self.camera.background_color = BG
        # VideoCrafter asks the same two questions over the same real dog photos.
        output = Group(*[dog_photo(i, 2.25, 1.5, SECONDARY) for i in [0, 2, 3, 5]]).arrange(RIGHT, buff=0.35).shift(DOWN * 0.4)
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in output], lag_ratio=0.15)); self.wait(BEAT)
        q1 = txt("what is inside this frame?", SECONDARY, 24).shift(UP * 2.5 + LEFT * 3)
        tri = Polygon(output[0].get_center() + RIGHT * 0.45 + UP * 0.25, output[0].get_center(), output[0].get_center() + LEFT * 0.3 + DOWN * 0.35, color=SECONDARY)
        self.play(Write(q1), Create(tri)); self.wait(BEAT)
        q2 = txt("how does it relate to the others?", PRIMARY, 24).shift(UP * 2.5 + RIGHT * 3)
        arcs = VGroup(*[ArcBetweenPoints(output[i].get_top(), output[i + 1].get_top(), angle=-0.6, color=PRIMARY) for i in range(3)])
        self.play(Write(q2), LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.2)); self.wait(BEAT)
        no_spatial = txt("NO SPATIAL: one frame breaks", WARM, 22).to_edge(DOWN)
        broken = photo_panel("dog_grass_pixelated.png", 2.25, 1.5, WARM).move_to(output[1])
        self.play(FadeOut(tri), FadeOut(output[1]), FadeIn(broken), FadeIn(no_spatial)); self.wait(BEAT)
        no_temporal = txt("NO TEMPORAL: the same dog jumps through impossible motion", WARM, 20).move_to(no_spatial)
        jumpy = Group(dog_photo(5, 2.25, 1.5, WARM).move_to(output[2]),
                      dog_photo(1, 2.25, 1.5, WARM).move_to(output[3]))
        jump_arrows = VGroup(*[Arrow(output[i].get_bottom() + DOWN * 0.15, output[i + 1].get_bottom() + DOWN * 0.15,
                                     color=WARM, stroke_width=3, buff=0.15) for i in range(3)])
        self.play(FadeOut(broken), FadeIn(output[1]), FadeOut(arcs), FadeOut(output[2]), FadeOut(output[3]), FadeIn(jumpy), FadeIn(jump_arrows),
                  Transform(no_spatial, no_temporal)); self.wait(BEAT)
        self.play(FadeOut(jumpy), FadeOut(jump_arrows), FadeIn(output[2]), FadeIn(output[3]), FadeIn(tri), FadeIn(arcs),
                  Transform(no_spatial, txt("both restored: good frames + coherent video", WHITE_ISH, 22).move_to(no_spatial))); self.wait(LONG)


class Scene16_TwoPilesOfData(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Two piles of real photo cards teach visibly different output habits.
        names = ["ocean.jpg", "forest.jpg", "mountain.jpg", "street.jpg", "city.jpg", "waterfall.jpg"]
        messy = Group(*[photo_panel(n, 1.4, 0.9, MUTED, 0.42).rotate((i - 3) * 0.13).shift(RIGHT * (i % 3) * 0.25 + UP * (i // 3) * 0.35) for i, n in enumerate(names)]).move_to(LEFT * 3.7 + UP * 0.7)
        clean = Group(*[photo_panel(n, 1.4, 0.9, SECONDARY if i % 2 else PRIMARY).shift(UP * i * 0.16 + RIGHT * i * 0.08) for i, n in enumerate(names)]).move_to(RIGHT * 3.7 + UP * 0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN) for c in messy], lag_ratio=0.1)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(c, shift=UP) for c in clean], lag_ratio=0.1)); self.wait(BEAT)
        labels = VGroup(txt("messy: blur · bad captions · watermark", WARM, 18).next_to(messy, DOWN),
                        txt("Vimeo25M: ~25M curated pairs", SECONDARY, 18).next_to(clean, DOWN))
        self.play(FadeIn(labels)); self.wait(BEAT)
        models = VGroup(gear(WARM, 0.3).move_to(LEFT * 3.7 + DOWN * 1.5), gear(ACCENT, 0.3).move_to(RIGHT * 3.7 + DOWN * 1.5))
        bad = photo_panel("mountain.jpg", 1.8, 1.15, WARM, 0.35).next_to(models[0], RIGHT)
        good = photo_panel("ocean.jpg", 1.8, 1.15, SECONDARY).next_to(models[1], RIGHT)
        self.play(GrowFromCenter(models), FadeIn(bad), FadeIn(good)); self.wait(BEAT)
        self.play(FadeIn(txt("architecture matters — data matters just as much", WHITE_ISH, 23).to_edge(DOWN))); self.wait(LONG)


class Scene17_TwoStreamsAndStaircase(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Still images and film strips flow together, then the model climbs difficulty one step at a time.
        core = gear(ACCENT, 0.5).shift(RIGHT * 4.6)
        image_path = Arrow(LEFT * 1.0 + UP * 1.35, core.get_left() + UP * 0.18, color=SECONDARY, buff=0.15)
        video_path = Arrow(LEFT * 1.0 + DOWN * 1.35, core.get_left() + DOWN * 0.18, color=PRIMARY, buff=0.15)
        stills = Group(*[photo_panel(n, 0.85, 0.55, SECONDARY) for n in ["ocean.jpg", "forest.jpg", "mountain.jpg", "street.jpg"]]).arrange(RIGHT, buff=0.15).move_to(LEFT * 3.3 + UP * 1.35)
        videos = Group(*[dog_photo(i, 0.85, 0.55, PRIMARY) for i in range(4)]).arrange(RIGHT, buff=0.15).move_to(LEFT * 3.3 + DOWN * 1.35)
        self.play(GrowArrow(image_path), GrowArrow(video_path), FadeIn(core), LaggedStart(*[FadeIn(s) for s in stills], *[FadeIn(v) for v in videos], lag_ratio=0.1)); self.wait(BEAT)
        image_label = txt("images teach looks", SECONDARY, 20).next_to(stills, UP)
        video_label = txt("videos teach motion", PRIMARY, 20).next_to(videos, DOWN)
        self.play(FadeIn(image_label), FadeIn(video_label)); self.wait(BEAT)
        self.play(FadeOut(Group(image_path, video_path, stills, videos, image_label, video_label)))
        steps = VGroup(*[Rectangle(width=2.0, height=0.65, color=ACCENT, fill_color=ACCENT, fill_opacity=0.08).shift(RIGHT * i * 1.45 + UP * i * 0.72) for i in range(4)]).move_to(ORIGIN + DOWN * 0.65)
        labels = ["low-res", "short clips", "rich scenes", "full curriculum"]
        labs = VGroup(*[txt(s, WHITE_ISH, 15).move_to(st) for s, st in zip(labels, steps)])
        self.play(LaggedStart(*[Create(s) for s in steps], *[FadeIn(l) for l in labs], lag_ratio=0.12)); self.wait(BEAT)
        climber = core.copy().scale(0.7).move_to(steps[0].get_top() + UP * 0.4)
        self.play(FadeOut(core), FadeIn(climber))
        for st in steps[1:]:
            self.play(climber.animate.move_to(st.get_top() + UP * 0.4).scale(1.08), run_time=NORMAL)
            self.wait(BEAT)
        self.play(FadeIn(txt("climbs — instead of jumping to the top", WHITE_ISH, 23).to_edge(DOWN))); self.wait(LONG)


class Scene18_LaVieGallery(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Four real LaVie outputs reveal one model preserving four different visual worlds.
        paths = ["lavie_iron.jpg", "lavie_jelly.jpg", "lavie_mars.jpg", "lavie_bund.jpg"]
        labels = ["identity", "quality", "environment", "style"]
        panels = Group(*[image_panel(os.path.join(ASSET_DIR, p), 3.7, 2.15) for p in paths])
        panels.arrange_in_grid(2, 2, buff=(0.45, 0.45)).shift(UP * 0.2)
        borders = VGroup(*[p[0] for p in panels])
        images = Group(*[p[1] for p in panels])
        self.play(LaggedStart(*[Create(b) for b in borders], lag_ratio=0.15)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(im) for im in images], lag_ratio=0.3), run_time=SLOW)
        for im in images:
            self.wait(BEAT)
        core = gear(ACCENT, 0.42)
        corners = [DR, DL, UR, UL]
        links = VGroup(*[
            Line(core.get_boundary_point(p.get_corner(corner) - core.get_center()), p.get_corner(corner),
                 color=WHITE_ISH, stroke_width=1.5)
            for p, corner in zip(panels, corners)
        ])
        self.play(GrowFromCenter(core), Create(links), run_time=SLOW); self.wait(BEAT)
        cap = txt("not just motion — style, identity, environment, quality", WHITE_ISH, 21).to_edge(DOWN)
        self.play(FadeIn(cap), LaggedStart(*[Indicate(p, color=ACCENT) for p in panels], lag_ratio=0.25)); self.wait(LONG)


class Scene19_DataPipelineAndCutDetection(Scene):
    def construct(self):
        self.camera.background_color = BG
        # One literal continuous filmstrip contains three incompatible realities, then splits at the visible seams.
        photos = Group(photo("dog_2.jpg", 3.7, 2.0), photo("car.jpg", 3.7, 2.0), photo("building.jpg", 3.7, 2.0)).arrange(RIGHT, buff=0)
        border = Rectangle(width=11.1, height=2.35, color=MUTED).move_to(photos)
        ticks = VGroup(*[
            Square(0.1, color=MUTED, fill_color=MUTED, fill_opacity=0.5).move_to([x, y, 0])
            for x in np.linspace(-5.35, 5.35, 24) for y in (-1.12, 1.12)
        ])
        filename = txt("raw_clip_0042 — one continuous strip", WHITE_ISH, 21).next_to(border, UP)
        caption = txt("one caption: a dog", SECONDARY, 21).next_to(border, DOWN)
        seams = [photos[0].get_right(), photos[1].get_right()]
        self.play(Create(border), LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.02), FadeIn(filename)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(p) for p in photos], lag_ratio=0.35), FadeIn(caption)); self.wait(BEAT)
        seam_lines = VGroup(*[Line(p + UP, p + DOWN, color=WARM, stroke_width=5) for p in seams])
        self.play(Create(seam_lines[0]), Flash(seams[0], color=WARM),
                  Transform(caption, txt("one caption: a dog... a car?", WARM, 21).move_to(caption))); self.wait(BEAT)
        self.play(Create(seam_lines[1]), Flash(seams[1], color=WARM),
                  Transform(caption, txt("one caption cannot describe all three", WARM, 21).move_to(caption))); self.wait(BEAT)
        scissors = VGroup(*[VGroup(Line(LEFT * 0.2, RIGHT * 0.2 + UP * 0.28, color=ACCENT),
                                  Line(LEFT * 0.2, RIGHT * 0.2 + DOWN * 0.28, color=ACCENT)).move_to(p + UP * 1.7) for p in seams])
        self.play(FadeIn(scissors)); self.wait(BEAT)
        self.play(LaggedStart(*[sc.animate.move_to(seams[i]) for i, sc in enumerate(scissors)], lag_ratio=0.3)); self.wait(BEAT)
        self.play(FadeOut(Group(border, ticks, filename, caption, seam_lines, scissors)),
                  photos[0].animate.shift(LEFT * 0.7), photos[2].animate.shift(RIGHT * 0.7)); self.wait(BEAT)
        clean_frames = VGroup(*[SurroundingRectangle(p, color=SECONDARY, buff=0.08) for p in photos])
        stable = VGroup(*[txt(s, WHITE_ISH, 18).next_to(p, DOWN) for s, p in zip(["a dog", "a car", "a building"], photos)])
        self.play(Create(clean_frames), FadeIn(stable)); self.wait(LONG)


class Scene20_CaptionMergeAndFilterGate(Scene):
    def construct(self):
        self.camera.background_color = BG
        # One caption identifies appearance; the other adds visible motion from a real sequence.
        still = Group(dog_photo(2, 2.3, 1.45, SECONDARY), txt("a white dog", SECONDARY, 18)).arrange(DOWN, buff=0.08).shift(LEFT * 4 + UP * 1.6)
        motion_frames = Group(*[dog_photo(i, 0.82, 0.55, PRIMARY) for i in [0, 1, 2, 3]]).arrange(RIGHT, buff=0.05)
        motion = Group(motion_frames, txt("running left to right", PRIMARY, 17)).arrange(DOWN, buff=0.08).shift(LEFT * 4 + DOWN * 0.5)
        llm = gear(ACCENT, 0.4).shift(RIGHT * 0.4 + UP * 0.7)
        arrows = VGroup(Arrow(still.get_right(), llm.get_left(), color=SECONDARY), Arrow(motion.get_right(), llm.get_left(), color=PRIMARY))
        merged_frames = Group(*[dog_photo(i, 0.82, 0.55, ACCENT) for i in [0, 1, 2, 3]]).arrange(RIGHT, buff=0.05)
        merged = Group(merged_frames, txt("a white dog running left to right", WHITE_ISH, 18)).arrange(DOWN, buff=0.12).shift(RIGHT * 4 + UP * 0.7)
        self.play(FadeIn(still), FadeIn(motion), GrowArrow(arrows[0]), GrowArrow(arrows[1]), GrowFromCenter(llm)); self.wait(BEAT)
        self.play(FadeIn(merged, shift=RIGHT)); self.wait(BEAT)
        self.play(Circumscribe(merged, color=ACCENT)); self.wait(BEAT)
        self.play(FadeOut(Group(still, motion, arrows, llm, merged)))
        gate = VGroup(Line(UP * 1.2, DOWN * 1.2, color=MUTED, stroke_width=8), Line(ORIGIN, RIGHT * 1.4, color=MUTED, stroke_width=6)).move_to(ORIGIN)
        cards = [
            photo_card("cat.jpg", "a cat", color=SECONDARY),
            photo_card("car.jpg", "a cat", color=WARM),
            photo_card("mountain.jpg", "a mountain", color=WARM, opacity=0.3),
            photo_card("ocean.jpg", "ocean waves", color=SECONDARY),
        ]
        source = LEFT * 4
        accepted = [RIGHT * 2.4 + UP * 1.2, RIGHT * 4.4 + UP * 1.2]
        rejected = [RIGHT * 2.4 + DOWN * 1.8, RIGHT * 4.2 + DOWN * 1.8]
        self.play(Create(gate)); self.wait(BEAT)
        for i, card in enumerate(cards):
            card.move_to(source)
            self.play(FadeIn(card, shift=RIGHT * 0.2)); self.wait(BEAT)
            if i in (0, 3):
                target = accepted[0 if i == 0 else 1]
                self.play(Rotate(gate[1], PI / 2, about_point=gate[1].get_start()), card.animate.move_to(target)); self.wait(BEAT)
                self.play(Rotate(gate[1], -PI / 2, about_point=gate[1].get_start()))
            else:
                target = rejected[0 if i == 1 else 1]
                self.play(Wiggle(card), card.animate.move_to(target)); self.wait(BEAT)
        self.play(FadeIn(txt("matching + clear pass; mismatched or poor-quality clips are rejected", WHITE_ISH, 19).to_edge(DOWN))); self.wait(LONG)


class Scene21_FlowArrowsAndOCRBox(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Arrows overlay genuinely changing dog photos and a genuinely static building photo.
        left = Group(dog_photo(0, 2.0, 1.45, SECONDARY), dog_photo(4, 2.0, 1.45, SECONDARY)).arrange(RIGHT, buff=0.15).shift(LEFT * 3.5 + UP * 0.7)
        right = Group(photo_panel("building.jpg", 2.0, 1.45, MUTED), photo_panel("building.jpg", 2.0, 1.45, MUTED)).arrange(RIGHT, buff=0.15).shift(RIGHT * 3.5 + UP * 0.7)
        right[1].shift(RIGHT * 0.03)
        self.play(FadeIn(left), FadeIn(right))
        arrows = VGroup(*[Arrow(LEFT * 0.2, RIGHT * 0.55, color=PRIMARY, buff=0, stroke_width=4).move_to(left.get_center() + UP * y) for y in [-0.55, 0, 0.55]])
        tiny = VGroup(*[Arrow(LEFT * 0.02, RIGHT * 0.06, color=MUTED, buff=0).move_to(right.get_center() + UP * y) for y in [-0.45, 0, 0.45]])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), FadeIn(tiny)); self.wait(BEAT)
        self.play(FadeIn(txt("strong motion → keep", SECONDARY, 19).next_to(left, DOWN)), FadeIn(txt("almost static → filter out", WARM, 19).next_to(right, DOWN))); self.wait(BEAT)
        old_labels = Group(*[m for m in self.mobjects if isinstance(m, Text)])
        self.play(FadeOut(Group(left, right, arrows, tiny, old_labels)))
        clip = photo_panel("subtitle.jpg", 6, 3.2, WHITE_ISH)
        glyph_bg = Rectangle(width=3.2, height=0.55, fill_color=BLACK, fill_opacity=0.8, stroke_width=0).move_to(clip.get_bottom() + UP * 0.45)
        glyphs = txt("SUBTITLE  LOGO  123", WHITE_ISH, 22).move_to(glyph_bg)
        scanner = Rectangle(width=1.8, height=0.6, color=ACCENT).move_to(clip.get_left() + RIGHT * 1.0)
        self.play(FadeIn(clip), FadeIn(glyph_bg), FadeIn(glyphs), Create(scanner))
        self.play(scanner.animate.move_to(glyphs), run_time=SLOW)
        lock = SurroundingRectangle(glyphs, color=WARM, buff=0.08)
        self.play(ReplacementTransform(scanner, lock), Flash(glyphs, color=WARM)); self.wait(BEAT)
        self.play(FadeIn(txt("OCR detects subtitles, watermarks, logos", WHITE_ISH, 22).to_edge(DOWN))); self.wait(LONG)


class Scene22_FunnelToCuratedSet(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A vast dull cloud visibly loses most of its mass while a small bright core emerges.
        rng = np.random.default_rng(7)
        cloud = VGroup(*[Dot([rng.uniform(-5, 5), rng.uniform(0.5, 3.0), 0], color=MUTED, radius=0.035) for _ in range(180)])
        title = txt("hundreds of millions of raw clips", MUTED, 21).to_edge(UP)
        self.play(FadeIn(cloud), FadeIn(title)); self.wait(BEAT)
        funnel = Polygon(LEFT * 3 + UP * 0.4, RIGHT * 3 + UP * 0.4, RIGHT * 0.7 + DOWN * 1.4, RIGHT * 0.7 + DOWN * 2,
                         LEFT * 0.7 + DOWN * 2, LEFT * 0.7 + DOWN * 1.4, color=ACCENT)
        self.play(Create(funnel)); self.wait(BEAT)
        keep = VGroup(*[
            Dot(color=SECONDARY if i % 2 else PRIMARY, radius=0.06)
            for i in range(24)
        ]).arrange_in_grid(4, 6, buff=0.1).move_to(DOWN * 2.85 + RIGHT * 1.5)
        reject = VGroup(*[
            Dot(color=WARM, radius=0.045) for _ in range(60)
        ]).arrange_in_grid(4, 15, buff=0.09).move_to(DOWN * 2.85 + LEFT * 2.4)
        self.play(TransformFromCopy(VGroup(*cloud[:24]), keep), TransformFromCopy(VGroup(*cloud[24:84]), reject), cloud.animate.set_opacity(0.18), run_time=SLOW); self.wait(BEAT)
        subset_label = txt("curated subset", SECONDARY, 19).next_to(keep, DOWN, buff=0.12)
        reject_label = txt("rejected", WARM, 17).next_to(reject, DOWN, buff=0.12)
        self.play(FadeIn(subset_label), FadeIn(reject_label)); self.wait(BEAT)
        self.play(FadeOut(cloud), FadeOut(reject), FadeOut(reject_label), FadeOut(title), funnel.animate.set_opacity(0.25)); self.wait(BEAT)
        formula = MathTex(r"\text{more data}\ne\text{better}\qquad \text{better data}=\text{better results}", color=WHITE_ISH).scale(0.65).move_to(UP * 2.65)
        self.play(Write(formula)); self.wait(BEAT)
        self.play(Indicate(formula[0], color=ACCENT)); self.wait(LONG)


class Scene23_ThreeStageRail(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same input enters the same model at three stations; only its visible capabilities grow.
        rail = Line(LEFT * 5.4 + DOWN * 1.8, RIGHT * 5.4 + DOWN * 1.8, color=MUTED, stroke_width=5)
        stations = VGroup(*[Dot([x, -1.8, 0], color=ACCENT, radius=0.12) for x in [-4, 0, 4]])
        self.play(Create(rail), LaggedStart(*[FadeIn(s) for s in stations], lag_ratio=0.2)); self.wait(BEAT)
        model = VGroup(*[Square(0.8, color=PRIMARY).shift(RIGHT * i * 0.12 + UP * i * 0.08) for i in range(3, -1, -1)]).move_to(LEFT * 4 + UP * 0.3)
        test = photo_panel("dog_grass.png", 1.75, 1.1, SECONDARY).next_to(model, LEFT, buff=0.35)
        still = photo_panel("dog_grass.png", 1.75, 1.1, SECONDARY).next_to(model, RIGHT, buff=0.35)
        stage_label = txt("Stage I — image pretraining: one picture", SECONDARY, 20).move_to(DOWN * 2.45)
        self.play(FadeIn(test), Create(model), FadeIn(stage_label)); self.wait(BEAT)
        self.play(TransformFromCopy(test, still)); self.wait(BEAT)

        self.play(FadeOut(test), FadeOut(still), model.animate.move_to(UP * 0.3),
                  Transform(stage_label, txt("Stage II — video pretraining: now it moves", PRIMARY, 20).move_to(stage_label))); self.wait(BEAT)
        test2 = photo_panel("dog_grass.png", 1.75, 1.1, SECONDARY).next_to(model, LEFT, buff=0.35)
        running = Group(*[dog_photo(i, 0.95, 0.62, PRIMARY) for i in range(5)]).arrange(RIGHT, buff=0.04).next_to(model, RIGHT, buff=0.35)
        temporal_arcs = VGroup(*[ArcBetweenPoints(model.get_left() + UP * y, model.get_right() + UP * y, angle=-0.5, color=PRIMARY) for y in [-0.25, 0, 0.25]])
        self.play(FadeIn(test2), Create(temporal_arcs)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(f) for f in running], lag_ratio=0.12)); self.wait(BEAT)

        self.play(FadeOut(test2), FadeOut(running), FadeOut(temporal_arcs), model.animate.move_to(RIGHT * 4 + UP * 0.3),
                  Transform(stage_label, txt("Stage III — one backbone, many video tasks", ACCENT, 20).move_to(stage_label))); self.wait(BEAT)
        test3 = photo_panel("dog_grass.png", 1.55, 0.95, SECONDARY).next_to(model, LEFT, buff=0.28)
        self.play(FadeIn(test3), Indicate(model, color=ACCENT)); self.wait(BEAT)
        outputs = Group(
            Group(*[dog_photo(i, 0.55, 0.38, SECONDARY) for i in range(3)]).arrange(RIGHT, buff=0.03),
            Group(*[dog_photo(i, 0.42, 0.3, PRIMARY) for i in [0, 2, 4]]).arrange(RIGHT, buff=0.02),
            Group(*[dog_photo(i, 0.42, 0.3, PRIMARY) for i in range(5)]).arrange(RIGHT, buff=0.02),
            Group(photo_panel("dog_0.jpg", 1.0, 0.68, ACCENT), photo_panel("dog_5.jpg", 1.0, 0.68, ACCENT)).arrange(RIGHT, buff=0.04),
        ).arrange(RIGHT, buff=0.45).move_to(UP * 2.25)
        output_labels = VGroup(*[
            txt(s, WHITE_ISH, 12).next_to(o, DOWN, buff=0.06)
            for s, o in zip(["better quality", "image → video", "frame interpolation", "multi-view"], outputs)
        ])
        self.play(LaggedStart(*[FadeIn(o) for o in outputs], lag_ratio=0.15), FadeIn(output_labels)); self.wait(LONG)
        self.play(ShowPassingFlash(rail.copy().set_stroke(color=PRIMARY, width=10), time_width=0.2), run_time=SLOW); self.wait(LONG)


class Scene24_PainterBecomesFilmmaker(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Every lesson converges into a real painter, then dissolves into a real filmmaker.
        emblems = model_emblems().scale(1.5).arrange(RIGHT, buff=1.35).move_to(UP * 0.6)
        recaps = ["inflate + time", "pixel + latent", "temporal U-Net", "curriculum", "curated data"]
        self.play(LaggedStart(*[GrowFromCenter(e) for e in emblems], lag_ratio=0.15))
        for e, recap in zip(emblems, recaps):
            label = txt(recap, WHITE_ISH, 16).next_to(e, DOWN)
            self.play(Indicate(e, color=ACCENT), FadeIn(label), run_time=FAST)
            self.play(FadeOut(label), run_time=FAST)
        self.wait(BEAT)
        painter = photo_panel("painter.jpg", 4.2, 3.5, SECONDARY).shift(DOWN * 0.35)
        canvas = frame(1.6, 1.25, SECONDARY).next_to(painter, RIGHT, buff=0.7)
        self.play(FadeIn(painter), Create(canvas),
                  *[e.animate.move_to(painter).scale(0.2).set_opacity(0) for e in emblems], run_time=SLOW); self.wait(BEAT)
        words = VGroup(txt("images", SECONDARY, 27), txt("time", PRIMARY, 27), txt("clean data", ACCENT, 27)).arrange(RIGHT, buff=1).to_edge(UP)
        for word in words:
            self.play(FadeIn(word, shift=UP * 0.2), Flash(word, color=word.get_color())); self.wait(BEAT)
        director = photo_panel("director_set.png", 5.8, 3.5, ACCENT).move_to(painter)
        reel = VGroup(Circle(0.55, color=PRIMARY, stroke_width=4), *[Circle(0.1, color=PRIMARY).shift(rotate_vector(RIGHT * 0.28, a)) for a in np.linspace(0, TAU, 5, endpoint=False)]).move_to(canvas)
        self.play(FadeOut(painter), FadeIn(director), ReplacementTransform(canvas, reel), run_time=SLOW); self.wait(BEAT)
        final = txt("teaching an image model to become a filmmaker", WHITE_ISH, 27).to_edge(DOWN)
        self.play(FadeIn(final), Indicate(reel, color=PRIMARY)); self.wait(LONG)
