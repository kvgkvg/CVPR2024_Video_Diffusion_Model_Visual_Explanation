# === PRODUCTION PLAN ===
# Core insight (one sentence): Image diffusion already knows how to draw; video
# generation turns that painter into a filmmaker by adding time and memory.
#
# Color encoding:
#   PRIMARY   = time / temporal dimension / motion / connections between frames
#   SECONDARY = spatial content / image quality / what one frame looks like
#   WARM      = noise / computational cost / inconsistency / failure
#   ACCENT    = active model / key mechanism / newly introduced insight
#   MUTED     = inactive state / rough draft / background static
#
# Scene list:
#   Scene01_ImageVsVideo — one photograph fans into a time-linked sequence
#   Scene02_VideoLandscape — one research path lights up in a branching forest
#   Scene03_KarateToadChallenge — a frozen subject becomes a consistent actor
#   Scene04_FlipbookDimensions — a flat sheet grows into a time-stacked flipbook
#   Scene05_TemporalMemory — a broken transition contrasts with a remembered one
#   Scene06_Convolution2Dto3D — a window slides on an image; a cube moves in time
#   Scene07_ArtistDirector — expensive 3D work splits into artist and director
#   Scene08_FireworksFromNoise — static organizes into a complete firework event
#   Scene09_SpatialTemporalDivision — frame quality and continuity divide the work
#   Scene10_CascadedPipeline — a rough moving sketch travels through a production line
#   Scene11_IdentityInit — a silent temporal observer awakens during fine-tuning
#   Scene12_BeadNecklace — beautiful frames are threaded into one coherent video
#   Scene13_TwoPhaseLearning — image school teaches seeing; video school teaches motion
#   Scene14_VerbsToMotion — a static noun scene becomes a lived action
#   Scene15_LatentBlueprint — a huge pixel volume compresses into a compact blueprint
#   Scene16_TemporalInjection — time-aware machinery is installed throughout a factory
#   Scene17_PainterToFilmmaker — painter transforms into filmmaker
#
# Key transforms (moments where one thing morphs INTO another):
#   - photograph -> fan of frames in Scene01
#   - flat image plane -> time-stacked flipbook in Scene04
#   - 3D convolution cube -> spatial pass + temporal pass in Scene07
#   - rough video product -> polished video product in Scene10
#   - silent observer -> active temporal layer in Scene11
#   - scattered beads -> coherent necklace in Scene12
#   - pixel volume -> latent blueprint in Scene15
#   - painter tools -> filmmaker tools in Scene17
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
DOG_ASSET = os.path.join(os.path.dirname(__file__), "assets", "flying_dog.png")

FAST = 0.4
NORMAL = 0.8
SLOW = 1.5
BEAT = 1.2
LONG = 2.5


def txt(text, color=WHITE_ISH, size=24):
    return Text(text, color=color, font_size=size)


def photo_frame(width=2.0, height=2.5, color=WHITE_ISH):
    return RoundedRectangle(width=width, height=height, corner_radius=0.08, color=color, stroke_width=3)


def subject(radius=0.34, color=SECONDARY):
    return Circle(radius=radius, color=color, fill_color=color, fill_opacity=0.8, stroke_width=3)


def arrow_between(a, b, color=PRIMARY, buff=0.12):
    return Arrow(a.get_right(), b.get_left(), color=color, buff=buff, stroke_width=4, max_tip_length_to_length_ratio=0.2)


def stick_actor(pose=0, scale=1.0, color=SECONDARY):
    head = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=0.35).shift(UP * 0.55)
    body = Line(UP * 0.35, DOWN * 0.4, color=color, stroke_width=5)
    arm_l = Line(UP * 0.15, LEFT * 0.55 + UP * (0.2 + 0.2 * pose), color=color, stroke_width=5)
    arm_r = Line(UP * 0.15, RIGHT * 0.55 + UP * (0.45 - 0.3 * pose), color=color, stroke_width=5)
    leg_l = Line(DOWN * 0.4, LEFT * 0.42 + DOWN * (0.75 - 0.1 * pose), color=color, stroke_width=5)
    leg_r = Line(DOWN * 0.4, RIGHT * 0.42 + DOWN * (0.6 + 0.12 * pose), color=color, stroke_width=5)
    belt = Line(LEFT * 0.28 + DOWN * 0.2, RIGHT * 0.28 + DOWN * 0.2, color=WHITE_ISH, stroke_width=4)
    return VGroup(head, body, arm_l, arm_r, leg_l, leg_r, belt).scale(scale)


def actor_frame(pose=0, width=1.65, height=2.0, color=WHITE_ISH):
    frame = photo_frame(width, height, color)
    floor = Line(LEFT * width * 0.38, RIGHT * width * 0.38, color=MUTED, stroke_width=2).shift(DOWN * height * 0.35)
    actor = stick_actor(pose, 0.65).move_to(frame.get_center())
    return VGroup(frame, floor, actor)


def firework(stage, radius=0.7):
    if stage <= 0.15:
        return Dot(radius=0.05, color=ACCENT)
    rays = VGroup()
    ray_count = 10
    length = radius * min(1, stage * 1.3)
    opacity = max(0.15, 1.25 - stage)
    for i in range(ray_count):
        angle = TAU * i / ray_count
        start = rotate_vector(RIGHT * length * 0.25, angle)
        end = rotate_vector(RIGHT * length, angle)
        rays.add(Line(start, end, color=PRIMARY, stroke_width=3).set_opacity(opacity))
    rays.add(Dot(radius=0.06, color=ACCENT).set_opacity(opacity))
    return rays


def film_strip(count=5, frame_width=0.7, frame_height=0.55, color=MUTED):
    frames = VGroup(*[Rectangle(width=frame_width, height=frame_height, color=color, stroke_width=2) for _ in range(count)])
    frames.arrange(RIGHT, buff=0.08)
    holes_top = VGroup(*[Square(0.08, color=color, fill_opacity=1, stroke_width=0) for _ in range(count * 2)])
    holes_bottom = holes_top.copy()
    holes_top.arrange(RIGHT, buff=0.27).next_to(frames, UP, buff=0.04)
    holes_bottom.arrange(RIGHT, buff=0.27).next_to(frames, DOWN, buff=0.04)
    return VGroup(frames, holes_top, holes_bottom)


def grid_panel(rows=6, cols=6, side=2.5, color=MUTED, cell_fill=0.25):
    cells = VGroup()
    step = side / max(rows, cols)
    for r in range(rows):
        for c in range(cols):
            cell = Square(step * 0.62, color=color, fill_color=color, fill_opacity=cell_fill, stroke_width=1)
            cell.move_to(LEFT * side / 2 + RIGHT * (c + 0.5) * side / cols + UP * side / 2 + DOWN * (r + 0.5) * side / rows)
            cells.add(cell)
    border = Square(side, color=WHITE_ISH, stroke_width=2)
    return VGroup(border, cells)


def gear(radius=0.35, color=PRIMARY):
    ring = Circle(radius=radius, color=color, stroke_width=4)
    hub = Circle(radius=radius * 0.22, color=color, fill_color=color, fill_opacity=1)
    spokes = VGroup(*[
        Line(rotate_vector(RIGHT * radius * 0.25, a), rotate_vector(RIGHT * radius * 0.9, a), color=color, stroke_width=3)
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    teeth = VGroup(*[
        Line(rotate_vector(RIGHT * radius, a), rotate_vector(RIGHT * radius * 1.22, a), color=color, stroke_width=4)
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    return VGroup(ring, hub, spokes, teeth)


def network_block(label, width=2.2):
    box = RoundedRectangle(width=width, height=1.25, corner_radius=0.15, color=ACCENT, stroke_width=3)
    name = txt(label, size=20).move_to(box)
    return VGroup(box, name)


def room_frame(pose=0, width=1.7, height=1.65, beach=False, missing_arm=False):
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.06, color=WHITE_ISH, stroke_width=2)
    wall_color = PRIMARY if beach else SECONDARY
    wall = Rectangle(width=width * 0.88, height=height * 0.82, stroke_width=0, fill_color=wall_color, fill_opacity=0.12).move_to(frame)
    floor = Line(frame.get_left() + RIGHT * 0.12 + UP * height * 0.18, frame.get_right() + LEFT * 0.12 + UP * height * 0.18, color=wall_color, stroke_width=3)
    if beach:
        sun = Circle(0.11, color=ACCENT, fill_color=ACCENT, fill_opacity=0.8).move_to(frame.get_corner(UR) + LEFT * 0.3 + DOWN * 0.3)
        wave = ArcBetweenPoints(frame.get_left() + RIGHT * 0.15 + DOWN * 0.25, frame.get_right() + LEFT * 0.15 + DOWN * 0.25, angle=-0.18, color=PRIMARY)
        background = VGroup(wall, floor, sun, wave)
    else:
        mat = Rectangle(width=width * 0.52, height=0.18, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.25).move_to(frame.get_bottom() + UP * 0.25)
        background = VGroup(wall, floor, mat)
    actor = stick_actor(pose, 0.48).move_to(frame.get_center() + DOWN * 0.05)
    if missing_arm:
        actor[3].set_opacity(0)
    return VGroup(frame, background, actor)


def dog_shape(scale=1.0, cape_flow=0.0, color=SECONDARY):
    body = Ellipse(width=1.05, height=0.52, color=color, fill_color=color, fill_opacity=0.55)
    head = Circle(0.27, color=color, fill_color=color, fill_opacity=0.55).next_to(body, RIGHT, buff=-0.08).shift(UP * 0.12)
    snout = Ellipse(width=0.3, height=0.16, color=color, fill_color=color, fill_opacity=0.55).next_to(head, RIGHT, buff=-0.08)
    ear = Triangle(color=color, fill_color=color, fill_opacity=0.7).scale(0.17).rotate(-0.3).move_to(head.get_top() + LEFT * 0.08)
    legs = VGroup(
        Line(body.get_center() + LEFT * 0.28 + DOWN * 0.15, body.get_center() + LEFT * 0.38 + DOWN * 0.48, color=color, stroke_width=5),
        Line(body.get_center() + RIGHT * 0.25 + DOWN * 0.15, body.get_center() + RIGHT * 0.38 + DOWN * 0.46, color=color, stroke_width=5),
    )
    tail = ArcBetweenPoints(body.get_left(), body.get_left() + LEFT * 0.42 + UP * 0.3, angle=-0.7, color=color, stroke_width=5)
    cape = Polygon(
        body.get_left() + UP * 0.18,
        body.get_left() + LEFT * (0.45 + cape_flow * 0.35) + UP * (0.1 + cape_flow * 0.18),
        body.get_left() + LEFT * (0.38 + cape_flow * 0.45) + DOWN * (0.35 + cape_flow * 0.08),
        color=WARM, fill_color=WARM, fill_opacity=0.75, stroke_width=2,
    )
    return VGroup(cape, body, head, snout, ear, legs, tail).scale(scale)


def dog_frame(position=0.0, cape_flow=0.0, width=1.7, height=1.35, crisp=True):
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.06, color=SECONDARY, stroke_width=2)
    sky = Rectangle(width=width * 0.9, height=height * 0.82, fill_color=PRIMARY, fill_opacity=0.06, stroke_width=0).move_to(frame)
    cloud = VGroup(*[Circle(0.08, color=WHITE_ISH, fill_color=WHITE_ISH, fill_opacity=0.35).shift(RIGHT * i * 0.1) for i in range(3)])
    cloud.move_to(frame.get_corner(UR) + LEFT * (0.35 + position * 0.12) + DOWN * 0.32)
    dog = dog_shape(0.42 if crisp else 0.38, cape_flow).move_to(frame.get_center() + RIGHT * position)
    if not crisp:
        dog.set_opacity(0.35)
    return VGroup(frame, sky, cloud, dog)


def dog_image_frame(position=0.0, width=1.7, height=1.35, opacity=1.0, cape_flow=0.0, show_cape=False):
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.06, color=SECONDARY, stroke_width=2)
    sky = Rectangle(width=width * 0.9, height=height * 0.82, fill_color=PRIMARY, fill_opacity=0.06, stroke_width=0).move_to(frame)
    dog = ImageMobject(DOG_ASSET).set_height(height * 0.72).set_opacity(opacity).move_to(frame.get_center() + RIGHT * position)
    cape = Polygon(
        dog.get_left() + RIGHT * 0.22 + UP * 0.14,
        dog.get_left() + LEFT * (0.28 + cape_flow * 0.32) + UP * (0.14 + cape_flow * 0.08),
        dog.get_left() + LEFT * (0.38 + cape_flow * 0.38) + DOWN * (0.12 + cape_flow * 0.05),
        dog.get_left() + RIGHT * 0.22 + DOWN * 0.05,
        color=WARM, fill_color=WARM, fill_opacity=0.75 if show_cape else 0, stroke_width=2 if show_cape else 0,
    )
    return Group(frame, sky, cape, dog)


def dog_image_stack(count, width, height, opacity=1.0, position_shift=0.0):
    stack = Group()
    offset = RIGHT * 0.1 + UP * 0.08
    for i in reversed(range(count)):
        if i == 0:
            page = dog_image_frame(position_shift * (count - 1), width, height, opacity)
        else:
            frame = RoundedRectangle(width=width, height=height, corner_radius=0.06, color=SECONDARY, stroke_width=2)
            sky = Rectangle(width=width * 0.9, height=height * 0.82, fill_color=PRIMARY, fill_opacity=0.04, stroke_width=0).move_to(frame)
            page = Group(frame, sky)
        page.shift(i * offset)
        stack.add(page)
    return stack


def video_stack(count, width, height, crispness=0, position_shift=0.0):
    stack = VGroup()
    offset = RIGHT * 0.1 + UP * 0.08
    for i in reversed(range(count)):
        page = dog_frame(
            position=position_shift * (count - i - 1),
            cape_flow=min(1, (count - i - 1) / max(1, count - 1)),
            width=width,
            height=height,
            crisp=crispness > 0,
        )
        page.shift(i * offset)
        if crispness == 0:
            page[3].set_opacity(0.18)
        elif crispness == 1:
            page[3].set_opacity(0.6)
        stack.add(page)
    return stack


def simple_video_strip(positions, width=0.75, height=0.62, border=PRIMARY, noise=False):
    strip = VGroup()
    rng = np.random.default_rng(77)
    for pos in positions:
        box = Rectangle(width=width, height=height, color=border, stroke_width=2)
        content = VGroup()
        if noise:
            content = VGroup(*[
                Dot(radius=0.012, color=WARM if j % 3 == 0 else MUTED).move_to(box.get_center() + [rng.uniform(-width * 0.38, width * 0.38), rng.uniform(-height * 0.35, height * 0.35), 0])
                for j in range(12)
            ])
        else:
            content = subject(0.1, SECONDARY).move_to(box.get_center() + RIGHT * pos)
        strip.add(VGroup(box, content))
    strip.arrange(RIGHT, buff=0.08)
    return strip


class Scene01_ImageVsVideo(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A frozen photograph physically multiplies and gains a depth direction,
        # making time visible before the word "video" appears.
        divider = Line(UP * 3.1, DOWN * 3.1, color=MUTED, stroke_width=2)
        left = VGroup(photo_frame(), subject()).move_to(LEFT * 3.3 + UP * 0.25)
        self.play(GrowFromCenter(left[0]), FadeIn(left[1]), run_time=NORMAL)
        self.wait(BEAT)
        image_label = txt("image").next_to(left, DOWN, buff=0.35)
        self.play(FadeIn(image_label, shift=UP * 0.15), Create(divider), run_time=NORMAL)
        self.wait(BEAT)

        cards = VGroup()
        for i in range(5):
            card = VGroup(photo_frame(), subject()).rotate((i - 2) * 1.8 * DEGREES)
            card.shift(RIGHT * i * 0.22 + UP * i * 0.08)
            cards.add(card)
        cards.move_to(RIGHT * 3.0 + UP * 0.3)
        self.play(LaggedStart(*[GrowFromCenter(card) for card in cards], lag_ratio=0.18), run_time=SLOW)
        self.wait(BEAT)
        video_label = txt("video").next_to(cards, DOWN, buff=0.25)
        self.play(FadeIn(video_label), run_time=NORMAL)
        self.wait(BEAT)
        time_arrow = Arrow(LEFT * 1.1, RIGHT * 1.1, color=PRIMARY, stroke_width=5).next_to(video_label, DOWN, buff=0.35)
        time_label = MathTex(r"t", color=PRIMARY).next_to(time_arrow, RIGHT, buff=0.12)
        dots = VGroup(*[Dot(cards[i].get_center(), color=PRIMARY, radius=0.035) for i in range(5)])
        self.play(Create(time_arrow), Write(time_label), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.12))
        self.wait(BEAT)
        question = MathTex(r"?", color=ACCENT, font_size=72).next_to(cards, UP, buff=0.25)
        self.play(GrowFromCenter(question), run_time=NORMAL)
        self.wait(LONG)


class Scene02_VideoLandscape(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A research forest grows from one trunk; every route recedes except the
        # bright path that adds time to image generation.
        trunk = Line(DOWN * 1.65, UP * 1.35, color=SECONDARY, stroke_width=12)
        crown = txt("Video Generation", size=30).next_to(trunk, UP, buff=0.22)
        self.play(Create(trunk), FadeIn(crown), run_time=SLOW)
        self.wait(BEAT)
        endpoints = [
            (-4.7, 2.6, "Efficient Training"), (4.7, 2.6, "Long Video"),
            (-5.0, 0.8, "Open-Source Models"), (4.8, 0.7, "Storyboards"),
            (-4.5, -2.3, "Multimodal-Guided"), (4.4, -2.35, "Other Directions"),
        ]
        muted = VGroup()
        for x, y, name in endpoints:
            branch = Line(trunk.get_center(), [x * 0.72, y * 0.75, 0], color=MUTED, stroke_width=4)
            label = txt(name, MUTED, 19).next_to(branch.get_end(), normalize([x, y, 0]), buff=0.12)
            muted.add(VGroup(branch, label))
        self.play(LaggedStart(*[AnimationGroup(Create(g[0]), FadeIn(g[1])) for g in muted], lag_ratio=0.14), run_time=SLOW * 1.5)
        self.wait(BEAT)
        focus_line = Line(trunk.get_center(), RIGHT * 4.1 + DOWN * 0.8, color=PRIMARY, stroke_width=9)
        focus = VGroup(
            txt("Pioneering Works", PRIMARY, 25),
            txt("VDM  •  Make-A-Video", WHITE_ISH, 17),
            txt("Imagen Video  •  Align Your Latents", WHITE_ISH, 17),
        ).arrange(DOWN, buff=0.12).next_to(focus_line.get_end(), RIGHT, buff=0.18)
        focus.scale_to_fit_width(2.65)
        self.play(Create(focus_line), FadeIn(focus, shift=RIGHT * 0.2), run_time=SLOW)
        self.wait(BEAT)
        self.play(Circumscribe(VGroup(focus_line, focus), color=ACCENT), run_time=NORMAL)
        self.wait(BEAT)
        self.play(muted.animate.set_opacity(0.25), run_time=NORMAL)
        self.wait(LONG)
        question = txt("How does an image model gain a sense of time?", size=24).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(question, shift=UP * 0.2))
        self.wait(BEAT)


class Scene03_KarateToadChallenge(Scene):
    def construct(self):
        self.camera.background_color = BG

        # The same simple actor is first frozen, then made to perform while its
        # room and identity stay fixed across frames.
        frozen = actor_frame(0, 2.2, 2.7).move_to(LEFT * 4.2 + UP * 0.4)
        prompt = txt('"Toad practicing karate"', size=19).next_to(frozen, DOWN, buff=0.22)
        self.play(GrowFromCenter(frozen), FadeIn(prompt), run_time=NORMAL)
        self.wait(BEAT)
        video_query = Arrow(frozen.get_right(), LEFT * 1.3, color=WARM, stroke_width=4)
        self.play(Create(video_query), Write(MathTex(r"?", color=WARM).next_to(video_query, UP)))
        self.wait(BEAT)
        sequence = VGroup(*[actor_frame(p, 1.45, 1.85) for p in [-1, 0, 1]])
        sequence.arrange(RIGHT, buff=0.42).move_to(RIGHT * 3.0 + UP * 1.15)
        arrows = VGroup(*[arrow_between(sequence[i], sequence[i + 1]) for i in range(2)])
        self.play(LaggedStart(*[GrowFromCenter(f) for f in sequence], lag_ratio=0.2), run_time=SLOW)
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=NORMAL)
        self.wait(BEAT)
        right_label = txt("text-to-video", PRIMARY, 23).next_to(sequence, UP, buff=0.25)
        self.play(FadeIn(right_label))
        self.wait(BEAT)
        constraints = VGroup(
            txt("✓ outfit stays recognizable", SECONDARY, 18),
            txt("✓ action unfolds", PRIMARY, 18),
            txt("✓ limbs move", PRIMARY, 18),
            txt("✓ background stays stable", SECONDARY, 18),
            txt("✓ identity persists", PRIMARY, 18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(RIGHT * 3.05 + DOWN * 1.7)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.15) for item in constraints], lag_ratio=0.22), run_time=SLOW * 1.3)
        self.wait(LONG)


class Scene04_FlipbookDimensions(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A posed character on one flat page becomes a flipbook whose pages show
        # successive poses; flipping the pages makes the third dimension tangible.
        origin = LEFT * 5.5 + DOWN * 1.35
        x_axis = Arrow(origin, origin + RIGHT * 3.6, color=WHITE_ISH, stroke_width=3)
        y_axis = Arrow(origin, origin + UP * 3.25, color=WHITE_ISH, stroke_width=3)
        axes_labels = VGroup(MathTex("x", color=WHITE_ISH, font_size=28).next_to(x_axis.get_end(), DOWN), MathTex("y", color=WHITE_ISH, font_size=28).next_to(y_axis.get_end(), LEFT))
        sheet = room_frame(-0.8, 2.3, 2.2).move_to(LEFT * 3.75 + UP * 0.05)
        self.play(Create(x_axis), Create(y_axis), FadeIn(axes_labels), GrowFromCenter(sheet), run_time=SLOW)
        self.wait(BEAT)
        dim2 = MathTex(r"\mathrm{image}: H \times W", color=WHITE_ISH, font_size=36).move_to(LEFT * 3.75 + DOWN * 2.55)
        self.play(Write(dim2))
        self.wait(BEAT)
        plus_time = VGroup(Arrow(LEFT, RIGHT, color=PRIMARY), txt("add time", PRIMARY, 20)).arrange(DOWN, buff=0.1).move_to(ORIGIN)
        self.play(Create(plus_time[0]), FadeIn(plus_time[1]))
        self.wait(BEAT)
        stack = VGroup(*[room_frame(p, 2.05, 1.85).shift(i * (RIGHT * 0.25 + UP * 0.16)) for i, p in enumerate([1, 0.6, 0.2, -0.2, -0.6, -1])])
        stack.move_to(RIGHT * 3.35 + UP * 0.25)
        t_axis = Arrow(stack[0].get_corner(DL) + LEFT * 0.12, stack[-1].get_corner(UL) + LEFT * 0.12, color=PRIMARY, stroke_width=4)
        t_label = MathTex(r"t", color=PRIMARY, font_size=34).next_to(t_axis.get_end(), UP, buff=0.08)
        self.play(Create(t_axis), Write(t_label))
        self.play(LaggedStart(*[GrowFromCenter(p) for p in stack], lag_ratio=0.15), run_time=SLOW)
        dim3 = MathTex(r"\mathrm{video}: T \times H \times W", color=WHITE_ISH, font_size=36).move_to(RIGHT * 3.5 + DOWN * 2.55)
        self.play(Write(dim3))
        self.wait(BEAT)
        for page in stack:
            self.play(page.animate.shift(LEFT * 0.32 + DOWN * 0.08), Indicate(page[2], color=PRIMARY), run_time=FAST)
        self.wait(BEAT)
        insight = txt("motion emerges from still frames", size=23).move_to(DOWN * 3.2)
        self.play(FadeIn(insight, shift=UP * 0.2))
        self.wait(LONG)


class Scene05_TemporalMemory(Scene):
    def construct(self):
        self.camera.background_color = BG

        # The broken transition changes both actor and room; the remembered
        # transition preserves the room and identity while only the pose moves.
        divider = Line(LEFT * 5.7, RIGHT * 5.7, color=MUTED, stroke_width=2)
        bad_a = room_frame(-1, 1.9, 1.7).move_to(LEFT * 2 + UP * 1.7)
        bad_b = room_frame(0, 1.9, 1.7, beach=True, missing_arm=True).move_to(RIGHT * 2 + UP * 1.7)
        bad_arrow = arrow_between(bad_a, bad_b, WARM)
        self.play(GrowFromCenter(bad_a), Create(bad_arrow), GrowFromCenter(bad_b), run_time=SLOW)
        self.wait(BEAT)
        bad_x = MathTex(r"\times", color=WARM, font_size=72).move_to(bad_b)
        self.play(GrowFromCenter(bad_x), Flash(bad_b, color=WARM), run_time=NORMAL)
        bad_notes = VGroup(txt("arm vanished", WARM, 18), txt("room became a beach", WARM, 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(bad_b, RIGHT, buff=0.25)
        self.play(FadeIn(bad_notes), Create(divider))
        self.wait(BEAT)
        good_a = room_frame(-1, 1.9, 1.7).move_to(LEFT * 2 + DOWN * 1.45)
        good_b = room_frame(0.2, 1.9, 1.7).move_to(RIGHT * 2 + DOWN * 1.45)
        good_arrow = arrow_between(good_a, good_b, PRIMARY)
        self.play(GrowFromCenter(good_a), Create(good_arrow), GrowFromCenter(good_b), run_time=SLOW)
        self.wait(BEAT)
        check = MathTex(r"\checkmark", color=PRIMARY, font_size=62).next_to(good_b, RIGHT, buff=0.3)
        stable_notes = VGroup(txt("same actor", SECONDARY, 18), txt("same training room", SECONDARY, 18)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(check, RIGHT, buff=0.2)
        self.play(GrowFromCenter(check), FadeIn(stable_notes))
        self.wait(BEAT)
        bracket = Brace(VGroup(good_a, good_b), DOWN, color=PRIMARY)
        memory = txt("temporal memory", PRIMARY, 24).next_to(bracket, DOWN, buff=0.12)
        self.play(GrowFromCenter(bracket), FadeIn(memory))
        self.wait(LONG)


class Scene06_Convolution2Dto3D(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A square window sweeps one visible grid, while a compact cube stays
        # inside a video volume and follows the moving hand across depth.
        left_plane = Rectangle(width=4.0, height=2.8, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.08).move_to(LEFT * 3.7 + UP * 0.2)
        left_grid = VGroup(
            *[Line(left_plane.get_corner(DL) + RIGHT * i, left_plane.get_corner(UL) + RIGHT * i, color=MUTED, stroke_width=1) for i in [1, 2, 3]],
            *[Line(left_plane.get_corner(DL) + UP * i, left_plane.get_corner(DR) + UP * i, color=MUTED, stroke_width=1) for i in [0.7, 1.4, 2.1]],
        )
        depth = RIGHT * 0.5 + UP * 0.34
        right_faces = VGroup(*[
            Rectangle(width=3.35, height=2.45, color=SECONDARY, fill_opacity=0.03).shift(i * depth * 0.34)
            for i in range(4)
        ]).move_to(RIGHT * 3.55 + UP * 0.05)
        hand_path = VGroup(*[Dot(f.get_center() + LEFT * 0.45 + RIGHT * i * 0.28, color=PRIMARY, radius=0.07) for i, f in enumerate(right_faces)])
        self.play(GrowFromCenter(left_plane), Create(left_grid), LaggedStart(*[GrowFromCenter(f) for f in right_faces], lag_ratio=0.15), FadeIn(hand_path), run_time=SLOW)
        self.wait(BEAT)
        labels = VGroup(txt("2D convolution", size=24).next_to(left_plane, UP), txt("3D convolution", size=24).next_to(right_faces, UP))
        self.play(FadeIn(labels))
        self.wait(BEAT)
        kernel2 = Square(0.68, color=ACCENT, fill_color=ACCENT, fill_opacity=0.45).move_to(left_plane.get_corner(UL) + RIGHT * 0.55 + DOWN * 0.55)
        kernel3 = VGroup(*[
            Square(0.52, color=ACCENT, fill_color=ACCENT, fill_opacity=0.28).shift(i * depth * 0.34)
            for i in range(3)
        ]).move_to(right_faces[0].get_center() + LEFT * 0.45)
        k2 = MathTex(r"k \times k", color=ACCENT, font_size=28).next_to(left_plane, LEFT, buff=0.12)
        k3 = MathTex(r"k \times k \times d", color=ACCENT, font_size=28).next_to(right_faces, LEFT, buff=0.15)
        k3.set_color_by_tex("d", PRIMARY)
        self.play(GrowFromCenter(kernel2), GrowFromCenter(kernel3), Write(k2), Write(k3))
        self.wait(BEAT)
        self.play(kernel2.animate.shift(RIGHT * 2.35), kernel3.animate.shift(RIGHT * 0.8 + depth * 0.45), run_time=SLOW)
        self.play(kernel2.animate.shift(DOWN * 1.35 + LEFT * 1.5), kernel3.animate.shift(DOWN * 0.75 + depth * 0.6), run_time=SLOW)
        self.play(kernel2.animate.shift(RIGHT * 1.25), kernel3.animate.shift(RIGHT * 0.55 + depth * 0.45), run_time=SLOW)
        self.wait(BEAT)
        sees = VGroup(txt("sees shape", SECONDARY, 21).next_to(left_plane, DOWN, buff=0.45), txt("sees a hand moving", PRIMARY, 21).next_to(right_faces, DOWN, buff=0.45))
        self.play(FadeIn(sees, shift=UP * 0.15))
        self.wait(LONG)


class Scene07_ArtistDirector(Scene):
    def construct(self):
        self.camera.background_color = BG

        # An expensive space-time block visibly factors into a broad spatial
        # brush and a narrow temporal baton: artist first, director second.
        cube = VGroup(*[Square(1.9, color=MUTED, fill_color=MUTED, fill_opacity=0.08).shift(i * (RIGHT + UP) * 0.13) for i in range(4)])
        cube.move_to(LEFT * 4.6 + UP * 0.55)
        formula = MathTex(r"t \times k \times k", color=MUTED).move_to(cube)
        cost = txt("expensive", WARM, 22).next_to(cube, DOWN, buff=0.35)
        self.play(GrowFromCenter(cube), Write(formula), FadeIn(cost))
        self.wait(BEAT)
        spatial = VGroup(Rectangle(width=2.15, height=1.75, color=SECONDARY), Square(0.5, color=ACCENT, fill_opacity=0.35), MathTex(r"1 \times k \times k", color=SECONDARY, font_size=29))
        spatial[1].move_to(spatial[0].get_corner(UL) + RIGHT * 0.45 + DOWN * 0.45)
        spatial[2].next_to(spatial[0], UP, buff=0.18)
        spatial.move_to(LEFT * 0.8 + UP * 0.7)
        frames = VGroup(*[room_frame(i - 1, 0.78, 0.75) for i in range(3)]).arrange(RIGHT, buff=0.18)
        temporal = VGroup(frames, MathTex(r"t \times 1 \times 1", color=PRIMARY, font_size=29).next_to(frames, UP, buff=0.22)).move_to(RIGHT * 4.05 + UP * 0.7)
        self.play(ReplacementTransform(cube.copy(), spatial[0]), ReplacementTransform(cube, frames), FadeOut(formula), FadeOut(cost), run_time=SLOW)
        self.play(FadeIn(spatial[1:]), FadeIn(temporal[1]))
        self.wait(BEAT)
        self.play(spatial[1].animate.shift(RIGHT * 1.25 + DOWN * 0.7), run_time=SLOW)
        palette = VGroup(Circle(0.3, color=SECONDARY), *[Dot(color=c, radius=0.04).shift(v) for c, v in [(SECONDARY, LEFT * 0.1), (ACCENT, RIGHT * 0.1), (PRIMARY, UP * 0.1)]])
        artist = VGroup(palette, txt("artist: appearance", SECONDARY, 19)).arrange(DOWN, buff=0.15).next_to(spatial, DOWN, buff=0.28)
        self.play(FadeIn(artist))
        self.wait(BEAT)
        t_arrows = VGroup(*[arrow_between(frames[i], frames[i + 1], PRIMARY, 0.05) for i in range(2)])
        baton = VGroup(Line(DOWN * 0.25, UP * 0.3 + RIGHT * 0.18, color=PRIMARY, stroke_width=5), Arc(radius=0.35, start_angle=0, angle=PI, color=PRIMARY))
        director = VGroup(baton, txt("director: continuity", PRIMARY, 19)).arrange(DOWN, buff=0.15).next_to(temporal, DOWN, buff=0.28)
        self.play(LaggedStart(*[Create(a) for a in t_arrows], lag_ratio=0.3), FadeIn(director))
        self.wait(BEAT)
        sequence_arrow = Arrow(spatial.get_right(), temporal.get_left(), color=ACCENT, buff=0.25, stroke_width=4)
        result = VGroup(MathTex(r"(2+1)\mathrm{D}", color=ACCENT), txt("artist, then director", ACCENT, 20)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.2)
        self.play(Create(sequence_arrow), Write(result[0]), FadeIn(result[1]))
        self.wait(LONG)


class Scene08_FireworksFromNoise(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A real film strip begins as synchronized static, then a ValueTracker
        # reveals one complete temporal arc without overlapping its explanations.
        frames = VGroup()
        rng = np.random.default_rng(8)
        for i in range(16):
            box = Rectangle(width=0.68, height=1.7, color=MUTED, stroke_width=1)
            dots = VGroup(*[
                Dot(radius=0.018, color=WARM if j % 3 == 0 else MUTED).move_to(box.get_center() + [rng.uniform(-0.29, 0.29), rng.uniform(-0.72, 0.72), 0])
                for j in range(16)
            ])
            frames.add(VGroup(box, dots))
        frames.arrange(RIGHT, buff=0.05).scale_to_fit_width(11.5).move_to(UP * 0.75)
        sprockets = VGroup(*[Square(0.055, color=MUTED, fill_color=MUTED, fill_opacity=1, stroke_width=0).move_to(frames.get_left() + RIGHT * i * frames.width / 31) for i in range(32)])
        sprockets_top = sprockets.copy().next_to(frames, UP, buff=0.06)
        sprockets_bottom = sprockets.copy().next_to(frames, DOWN, buff=0.06)
        self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.04), FadeIn(sprockets_top), FadeIn(sprockets_bottom), run_time=SLOW)
        frame_count = txt("16 frames / about 1 second", size=20).move_to(DOWN * 0.7)
        self.play(FadeIn(frame_count))
        self.wait(BEAT)
        noise_label = txt("noise", WARM, 20).next_to(frames[0], UP, buff=0.18)
        self.play(FadeIn(noise_label))
        self.wait(BEAT)
        contents = []
        for i, frame in enumerate(frames):
            if i < 3:
                contents.append(frame[1].copy())
            else:
                stage = min((i - 2) / 7, (16 - i) / 5)
                contents.append(firework(max(0.1, stage), 0.5).move_to(frame[0]))
        self.play(*[ReplacementTransform(frames[i][1], contents[i]) for i in range(16)], run_time=SLOW * 3)
        self.wait(BEAT)
        self.play(FadeOut(frame_count))
        peak = SurroundingRectangle(VGroup(*frames[5:12]), color=ACCENT, buff=0.08)
        arc_label = txt("spark grows → burst → fade", ACCENT, 22).next_to(frames, UP, buff=0.3)
        self.play(Create(peak), FadeIn(arc_label))
        self.wait(BEAT)
        single = VGroup(frames[8].copy().scale(1.35), txt("image diffusion: one moment", SECONDARY, 18)).arrange(DOWN, buff=0.12).move_to(LEFT * 2.8 + DOWN * 1.85)
        whole_label = txt("video diffusion: the whole event", PRIMARY, 20).move_to(RIGHT * 2.7 + DOWN * 1.85)
        whole_arrow = Arrow(whole_label.get_top(), frames.get_bottom() + RIGHT * 2.5, color=PRIMARY, buff=0.15)
        self.play(FadeIn(single), Create(whole_arrow), FadeIn(whole_label))
        self.wait(LONG)


class Scene09_SpatialTemporalDivision(Scene):
    def construct(self):
        self.camera.background_color = BG

        # One ACCENT tracking point stays fixed across three frames: green arrows
        # explain its frame-local burst, while a blue spine tracks it through time.
        frames = VGroup()
        for stage in [0.18, 0.85, 1.25]:
            box = Rectangle(width=2.65, height=2.15, color=MUTED, stroke_width=2)
            burst = firework(stage, 0.78).move_to(box.get_center() + UP * 0.15)
            frames.add(VGroup(box, burst))
        frames.arrange(RIGHT, buff=0.95).move_to(UP * 0.35)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in frames], lag_ratio=0.2), run_time=SLOW)
        self.wait(BEAT)
        tracking = VGroup(*[Dot(f[0].get_center() + UP * 0.15, color=ACCENT, radius=0.09) for f in frames])
        stage_labels = VGroup(*[txt(s, c, 18).next_to(f, DOWN, buff=0.18) for s, c, f in zip(["spark", "burst", "fade"], [ACCENT, ACCENT, MUTED], frames)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in tracking], lag_ratio=0.2), FadeIn(stage_labels))
        self.wait(BEAT)
        center = tracking[1].get_center()
        spatial = VGroup(*[
            CurvedArrow(center, center + rotate_vector(RIGHT * 0.78, a), angle=0.25, color=SECONDARY, stroke_width=3)
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ])
        spatial_label = txt("spatial: which pixels relate inside this frame?", SECONDARY, 22).to_edge(UP, buff=0.35)
        self.play(LaggedStart(*[Create(a) for a in spatial], lag_ratio=0.12), FadeIn(spatial_label))
        self.wait(BEAT)
        spine_y = frames.get_bottom()[1] - 0.65
        spine_points = [np.array([d.get_center()[0], spine_y, 0]) for d in tracking]
        line = VMobject(color=PRIMARY, stroke_width=5).set_points_smoothly([
            spine_points[0],
            (spine_points[0] + spine_points[1]) / 2 + DOWN * 0.08,
            spine_points[1],
            (spine_points[1] + spine_points[2]) / 2 + DOWN * 0.08,
            spine_points[2],
        ])
        stems = VGroup(*[Line(d.get_center(), p, color=PRIMARY, stroke_width=3) for d, p in zip(tracking, spine_points)])
        temporal_label = txt("temporal: how does this spot change over time?", PRIMARY, 22).to_edge(UP, buff=0.35)
        self.play(FadeOut(spatial), ReplacementTransform(spatial_label, temporal_label), LaggedStart(*[Create(s) for s in stems], lag_ratio=0.18), Create(line))
        self.play(ShowPassingFlash(line.copy().set_stroke(width=10), time_width=0.25), run_time=SLOW)
        self.wait(BEAT)
        self.play(FadeIn(spatial), run_time=NORMAL)
        continuous = txt("not three sparks — one continuous event", WHITE_ISH, 23).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(continuous, shift=UP * 0.15))
        self.wait(LONG)


class Scene10_CascadedPipeline(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Four drafts of the same flying-dog video improve one property at a time:
        # more pages, cleaner motion, higher quality, then crisp detail.
        title = txt("same scene — four revisions", ACCENT, 25).to_edge(UP, buff=0.3)
        prompt = VGroup(RoundedRectangle(width=1.45, height=0.68, corner_radius=0.12, color=WHITE_ISH), txt("dog flying", size=17)).move_to(LEFT * 5.65 + UP * 1.8)
        prompt[1].move_to(prompt[0])
        clip = VGroup(RoundedRectangle(width=0.9, height=0.65, corner_radius=0.1, color=ACCENT), txt("CLIP", ACCENT, 17)).next_to(prompt, DOWN, buff=0.32)
        clip[1].move_to(clip[0])
        self.play(FadeIn(title), GrowFromCenter(prompt), GrowFromCenter(clip), Create(Arrow(prompt.get_bottom(), clip.get_top(), color=ACCENT, buff=0.08)))
        self.wait(BEAT)
        drafts = [
            dog_image_stack(3, 0.85, 0.68, 0.25, 0.01),
            dog_image_stack(7, 0.88, 0.70, 0.45, 0.018),
            dog_image_stack(7, 1.12, 0.86, 0.78, 0.025),
            dog_image_stack(7, 1.36, 1.02, 1.0, 0.035),
        ]
        xs = [-3.75, -1.05, 1.7, 4.55]
        specs = [(r"16 \times 64^2", "moving sketch", MUTED), (r"76 \times 64^2", "smoother motion", WHITE_ISH), (r"76 \times 256^2", "cleaner", SECONDARY), (r"76 \times 768^2", "final", SECONDARY)]
        gears = VGroup()
        for i, draft in enumerate(drafts):
            draft.scale(1.1)
            draft.move_to([xs[i], 0.35, 0])
            if i == 0:
                self.play(Create(Arrow(clip.get_right(), draft.get_left(), color=ACCENT, buff=0.12)), LaggedStart(*[FadeIn(p) for p in draft], lag_ratio=0.15))
            else:
                g = VGroup(gear(0.20, ACCENT), txt(["+ frames", "+ quality", "+ detail"][i - 1], ACCENT, 15)).arrange(DOWN, buff=0.08).move_to([(xs[i - 1] + xs[i]) / 2, 0.35, 0])
                gears.add(g)
                self.play(GrowFromCenter(g[0]), FadeIn(g[1]), LaggedStart(*[FadeIn(p) for p in draft], lag_ratio=0.1), run_time=SLOW)
            label = VGroup(MathTex(specs[i][0], color=WHITE_ISH, font_size=25), txt(specs[i][1], specs[i][2], 17)).arrange(DOWN, buff=0.08).move_to([xs[i], -1.75, 0])
            self.play(Write(label[0]), FadeIn(label[1]))
            self.wait(BEAT)
        self.play(Circumscribe(drafts[-1], color=SECONDARY))
        self.wait(LONG)


class Scene11_IdentityInit(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A three-channel mixing board starts at 0/1/0, preserving the current
        # frame exactly; video training raises the side channels to blend time.
        title = txt("before video training", size=23).to_edge(UP, buff=0.28)
        frames = VGroup(room_frame(-0.8, 1.25, 1.05), room_frame(0, 1.25, 1.05), room_frame(0.8, 1.25, 1.05))
        frames.arrange(RIGHT, buff=1.0).move_to(LEFT * 2.25 + UP * 1.65)
        channels = VGroup()
        handles = VGroup()
        values = [0, 1, 0]
        colors = [MUTED, ACCENT, MUTED]
        for frame, value, color in zip(frames, values, colors):
            track = RoundedRectangle(width=0.48, height=2.0, corner_radius=0.12, color=color, stroke_width=3).next_to(frame, DOWN, buff=0.2)
            fill_height = max(0.04, 1.7 * value)
            fill = Rectangle(width=0.34, height=fill_height, color=color, fill_color=color, fill_opacity=0.65, stroke_width=0)
            fill.move_to(track.get_bottom() + UP * (0.12 + fill_height / 2))
            handle = RoundedRectangle(width=0.7, height=0.18, corner_radius=0.06, color=color, fill_color=color, fill_opacity=1).move_to(track.get_bottom() + UP * (0.18 + value * 1.62))
            channels.add(VGroup(track, fill))
            handles.add(handle)
        labels = VGroup(*[txt(s, c, 17).next_to(f, UP, buff=0.12) for s, c, f in zip(["previous", "current", "next"], colors, frames)])
        self.play(FadeIn(title), LaggedStart(*[GrowFromCenter(c) for c in channels], lag_ratio=0.15), LaggedStart(*[GrowFromCenter(h) for h in handles], lag_ratio=0.15))
        self.wait(BEAT)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in frames], lag_ratio=0.2), FadeIn(labels))
        self.wait(BEAT)
        weights = VGroup(MathTex(r"\times 0", color=MUTED), MathTex(r"\times 1", color=ACCENT), MathTex(r"\times 0", color=MUTED))
        for w, c in zip(weights, channels):
            w.next_to(c[0], DOWN, buff=0.12)
        output_box = room_frame(0, 1.55, 1.35).move_to(RIGHT * 4.75 + UP * 0.55)
        output_arrow = Arrow(channels.get_right() + RIGHT * 0.15, output_box.get_left(), color=ACCENT, buff=0.15)
        self.play(LaggedStart(*[Write(w) for w in weights], lag_ratio=0.2), Create(output_arrow), GrowFromCenter(output_box))
        equation = MathTex(r"0\cdot\mathrm{prev}+1\cdot\mathrm{current}+0\cdot\mathrm{next}=\mathrm{current}", color=WHITE_ISH, font_size=28).to_edge(DOWN, buff=0.25)
        self.play(Write(equation))
        self.wait(BEAT)
        callout = VGroup(RoundedRectangle(width=3.3, height=0.85, corner_radius=0.12, color=ACCENT), txt("identity start preserves the image model", ACCENT, 17)).move_to(RIGHT * 4.3 + DOWN * 1.55)
        callout[1].move_to(callout[0])
        self.play(GrowFromCenter(callout))
        self.wait(BEAT)
        after = txt("during video fine-tuning…", PRIMARY, 23).to_edge(UP, buff=0.28)
        new_output = room_frame(0.1, 1.55, 1.35).move_to(output_box)
        new_weights = VGroup(MathTex(r"\approx \times 0.35", color=PRIMARY, font_size=27), MathTex(r"\times 0.5", color=ACCENT, font_size=27), MathTex(r"\approx \times 0.35", color=PRIMARY, font_size=27))
        for w, c in zip(new_weights, channels):
            w.next_to(c[0], DOWN, buff=0.12)
        self.play(
            ReplacementTransform(title, after),
            handles[0].animate.shift(UP * 0.58).set_color(PRIMARY),
            handles[2].animate.shift(UP * 0.58).set_color(PRIMARY),
            channels[0][1].animate.stretch_to_fit_height(0.65).set_color(PRIMARY).shift(UP * 0.28),
            channels[2][1].animate.stretch_to_fit_height(0.65).set_color(PRIMARY).shift(UP * 0.28),
            *[ReplacementTransform(weights[i], new_weights[i]) for i in range(3)],
            ReplacementTransform(output_box, new_output),
            FadeOut(equation),
            FadeOut(callout),
            run_time=SLOW,
        )
        self.play(FadeIn(txt("output blends neighboring motion", PRIMARY, 19).next_to(new_output, DOWN, buff=0.2)))
        self.wait(LONG)


class Scene12_BeadNecklace(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Spatial attention beautifies isolated beads; temporal attention then
        # threads and aligns them into a single object that can hold together.
        starts = [LEFT * 4 + UP * 1.2, LEFT * 1.6 + DOWN * 1.2, UP * 1.5, RIGHT * 2 + DOWN * 1.0, RIGHT * 4.2 + UP * 1.0]
        beads = VGroup(*[Circle(0.43, color=MUTED, fill_color=MUTED, fill_opacity=0.45, stroke_width=3).move_to(p) for p in starts])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in beads], lag_ratio=0.18), run_time=SLOW)
        self.wait(BEAT)
        spatial_label = txt("spatial attention", SECONDARY, 23).to_edge(UP, buff=0.35)
        details = VGroup(*[Circle(0.22, color=SECONDARY, stroke_width=3).move_to(b) for b in beads])
        self.play(FadeIn(spatial_label), beads.animate.set_color(SECONDARY).set_fill(SECONDARY, opacity=0.75), LaggedStart(*[Create(d) for d in details], lag_ratio=0.15))
        self.wait(BEAT)
        target_points = [np.array([-4, 0.4, 0]), np.array([-2, -0.45, 0]), ORIGIN + DOWN * 0.8, np.array([2, -0.45, 0]), np.array([4, 0.4, 0])]
        curve = VMobject(color=PRIMARY, stroke_width=5).set_points_smoothly(target_points)
        temporal_label = txt("temporal attention", PRIMARY, 23).to_edge(UP, buff=0.35)
        self.play(ReplacementTransform(spatial_label, temporal_label), Create(curve), run_time=SLOW)
        for bead, detail, point in zip(beads, details, target_points):
            self.play(bead.animate.move_to(point), detail.animate.move_to(point), run_time=FAST)
            self.wait(FAST)
        coherent = txt("one coherent video", PRIMARY, 24).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(coherent, shift=UP * 0.2))
        self.wait(LONG)


class Scene13_TwoPhaseLearning(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Phase one solves a one-frame denoising task; phase two solves a missing
        # middle-frame task, making each teacher's lesson physically visible.
        divider = Line(LEFT * 5.8, RIGHT * 5.8, color=MUTED, stroke_width=2).shift(DOWN * 0.25)
        phase1 = txt("PHASE 1 — image training", SECONDARY, 22).move_to(LEFT * 4.25 + UP * 3)
        noisy = simple_video_strip([0], 1.35, 1.25, SECONDARY, noise=True).move_to(LEFT * 4.65 + UP * 1.55)
        clean = simple_video_strip([0], 1.35, 1.25, SECONDARY).move_to(RIGHT * 4.65 + UP * 1.55)
        model1 = network_block("MODEL", 1.75).move_to(UP * 1.55)
        model1[1].shift(UP * 0.24)
        grid = VGroup(*[Square(0.12, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.5) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.08).move_to(model1.get_center() + DOWN * 0.25)
        arrows1 = VGroup(Arrow(noisy.get_right(), model1.get_left(), color=SECONDARY, buff=0.2), Arrow(model1.get_right(), clean.get_left(), color=SECONDARY, buff=0.2))
        self.play(FadeIn(phase1), GrowFromCenter(noisy), LaggedStart(*[Create(a) for a in arrows1], lag_ratio=0.25), GrowFromCenter(model1), FadeIn(grid), GrowFromCenter(clean), run_time=SLOW)
        self.wait(BEAT)
        task1 = VGroup(txt("remove noise from one frame", WHITE_ISH, 17), txt("learns what objects look like", SECONDARY, 18)).arrange(DOWN, buff=0.05).move_to(UP * 0.42)
        self.play(FadeIn(task1))
        self.wait(BEAT)
        phase2 = txt("PHASE 2 — video fine-tuning", PRIMARY, 22).move_to(LEFT * 4.1 + DOWN * 0.55)
        input_strip = simple_video_strip([-0.2, 0, 0.2], 0.9, 0.82, PRIMARY).move_to(LEFT * 4.35 + DOWN * 1.7)
        input_strip[1][1] = MathTex(r"?", color=ACCENT, font_size=42).move_to(input_strip[1][0])
        model2 = network_block("MODEL", 1.75).move_to(DOWN * 1.7)
        model2[1].shift(UP * 0.24)
        connections = VGroup(*[Line(model2.get_center() + LEFT * 0.45 + DOWN * 0.25 + RIGHT * i * 0.45, model2.get_center() + LEFT * 0.05 + DOWN * 0.25 + RIGHT * i * 0.45, color=PRIMARY, stroke_width=4) for i in range(2)])
        revealed = simple_video_strip([0], 1.25, 1.0, PRIMARY).move_to(RIGHT * 4.55 + DOWN * 1.7)
        arrows2 = VGroup(Arrow(input_strip.get_right(), model2.get_left(), color=PRIMARY, buff=0.18), Arrow(model2.get_right(), revealed.get_left(), color=PRIMARY, buff=0.18))
        self.play(Create(divider), FadeIn(phase2))
        self.play(LaggedStart(*[GrowFromCenter(f) for f in input_strip], lag_ratio=0.2), LaggedStart(*[Create(a) for a in arrows2], lag_ratio=0.25), GrowFromCenter(model2), FadeIn(connections), GrowFromCenter(revealed), run_time=SLOW)
        self.wait(BEAT)
        task2 = VGroup(txt("fill in the missing middle frame", WHITE_ISH, 17), txt("learns how things move", PRIMARY, 18)).arrange(DOWN, buff=0.05).move_to(DOWN * 3.0)
        self.play(FadeIn(task2))
        self.wait(BEAT)
        callout_box = RoundedRectangle(width=3.15, height=0.42, corner_radius=0.1, color=ACCENT, fill_color=BG, fill_opacity=1).move_to(RIGHT * 3.9 + DOWN * 0.25)
        callout = txt("same model — two different teachers", ACCENT, 15).move_to(callout_box)
        self.play(GrowFromCenter(callout_box), FadeIn(callout), Indicate(model1, color=ACCENT), Indicate(model2, color=ACCENT))
        self.wait(LONG)


class Scene14_VerbsToMotion(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A noun occupies one point. A verb only becomes visible when that point
        # traces a path, which then turns into successive frames of the dog.
        noun_dot = Dot(radius=0.2, color=SECONDARY).move_to(LEFT * 3.4 + UP * 0.55)
        noun_word = txt("dog", SECONDARY, 34).next_to(noun_dot, DOWN, buff=0.45)
        noun_note = txt("a thing", MUTED, 18).next_to(noun_word, DOWN, buff=0.12)

        verb_path = Line(LEFT * 0.6, RIGHT * 4.5, color=PRIMARY, stroke_width=6).shift(DOWN * 0.1)
        path_dots = VGroup(*[
            Dot(verb_path.point_from_proportion(alpha), radius=0.16, color=SECONDARY)
            for alpha in (0.08, 0.5, 0.92)
        ])
        verb_word = txt("running", ACCENT, 34).move_to(RIGHT * 2 + DOWN * 1.15)
        verb_note = txt("a path through time", PRIMARY, 18).next_to(verb_word, DOWN, buff=0.12)

        self.play(GrowFromCenter(noun_dot), FadeIn(noun_word, shift=UP * 0.12))
        self.wait(BEAT)
        self.play(Create(verb_path), LaggedStart(*[GrowFromCenter(dot) for dot in path_dots], lag_ratio=0.25))
        self.play(FadeIn(verb_word, shift=UP * 0.12))
        self.wait(BEAT)
        self.play(FadeIn(noun_note), FadeIn(verb_note))
        self.wait(BEAT)

        phase_one = Group(noun_dot, noun_word, noun_note, verb_path, path_dots, verb_word, verb_note)
        self.play(FadeOut(phase_one))

        words = ["A", "dog", "running", "through", "the", "park"]
        tokens = VGroup(*[
            txt(word, ACCENT if word == "running" else SECONDARY if word == "dog" else WHITE_ISH, 25)
            for word in words
        ])
        tokens.arrange(RIGHT, buff=0.2).scale_to_fit_width(10.7).to_edge(UP, buff=0.28)
        self.play(LaggedStart(*[FadeIn(token, shift=UP * 0.1) for token in tokens], lag_ratio=0.08))
        self.wait(BEAT)

        flight_path = Line(LEFT * 4.7, RIGHT * 4.6, color=PRIMARY, stroke_width=5).shift(DOWN * 0.45)
        frames = Group()
        for alpha, position in zip((0.12, 0.5, 0.88), (-0.15, 0, 0.15)):
            frame = dog_image_frame(position, 2.05, 1.55, 1.0).move_to(flight_path.point_from_proportion(alpha))
            frames.add(frame)
        direction_arrows = VGroup(*[
            Arrow(
                flight_path.point_from_proportion(alpha),
                flight_path.point_from_proportion(alpha + 0.08),
                color=PRIMARY,
                buff=0,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.35,
            )
            for alpha in (0.29, 0.69)
        ])
        self.play(Create(flight_path))
        self.play(LaggedStart(*[GrowFromCenter(frame) for frame in frames], lag_ratio=0.25), run_time=SLOW)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in direction_arrows], lag_ratio=0.3))
        this_arc = VGroup(txt("running", ACCENT, 23), txt("is this trajectory", PRIMARY, 21)).arrange(RIGHT, buff=0.14).to_edge(DOWN, buff=0.28)
        self.play(Indicate(tokens[2], color=ACCENT), FadeIn(this_arc))
        self.wait(LONG)

        phase_two = Group(tokens, flight_path, frames, direction_arrows, this_arc)
        self.play(FadeOut(phase_two))

        snapshot = dog_image_frame(0, 2.3, 1.75, 1.0).move_to(LEFT * 3.45 + UP * 0.25)
        snapshot_label = VGroup(txt("image model", MUTED, 21), txt("running = snapshot", MUTED, 18)).arrange(DOWN, buff=0.08).next_to(snapshot, DOWN, buff=0.22)
        trajectory = Line(RIGHT * 0.4, RIGHT * 5.25, color=PRIMARY, stroke_width=5).shift(DOWN * 0.1)
        small_frames = Group(*[
            dog_image_frame(pos, 1.48, 1.16, 1.0).move_to(trajectory.point_from_proportion(alpha))
            for pos, alpha in zip((-0.12, 0, 0.12), (0.1, 0.5, 0.9))
        ])
        trajectory_label = VGroup(txt("video model", PRIMARY, 21), txt("running = trajectory", PRIMARY, 18)).arrange(DOWN, buff=0.08).next_to(trajectory, DOWN, buff=0.58)
        self.play(GrowFromCenter(snapshot), FadeIn(snapshot_label))
        self.play(Create(trajectory), LaggedStart(*[GrowFromCenter(frame) for frame in small_frames], lag_ratio=0.2), FadeIn(trajectory_label), run_time=SLOW)
        conclusion = txt("verbs → motion", ACCENT, 28).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(conclusion), Circumscribe(Group(trajectory, small_frames), color=ACCENT))
        self.wait(LONG)


class Scene15_LatentBlueprint(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A five-frame dense pixel volume compresses into a much smaller five-frame
        # latent blueprint, with braces making the cost difference unavoidable.
        pixel_stack = VGroup(*[grid_panel(8, 8, 2.55, WARM, 0.28).shift(RIGHT * i * 0.15 + UP * i * 0.12) for i in range(5)])
        pixel_stack.move_to(LEFT * 4.1 + UP * 0.25)
        self.play(LaggedStart(*[GrowFromCenter(g) for g in pixel_stack], lag_ratio=0.12), run_time=SLOW)
        heavy = txt("heavy computation", WARM, 21).next_to(pixel_stack, DOWN, buff=0.35)
        self.play(FadeIn(heavy))
        self.wait(BEAT)
        encoder = MathTex(r"\mathcal{E}", color=ACCENT, font_size=64)
        compress = Arrow(LEFT * 1.1, RIGHT * 1.1, color=PRIMARY, stroke_width=5).move_to(ORIGIN)
        self.play(GrowFromCenter(encoder), Create(compress))
        self.wait(BEAT)
        latent_stack = VGroup(*[grid_panel(3, 3, 1.25, ACCENT, 0.75).shift(RIGHT * i * 0.12 + UP * i * 0.1) for i in range(5)])
        latent_stack.move_to(RIGHT * 4 + UP * 0.2)
        self.play(LaggedStart(*[GrowFromCenter(g) for g in latent_stack], lag_ratio=0.12), run_time=SLOW)
        efficient = txt("efficient computation", SECONDARY, 21).next_to(latent_stack, DOWN, buff=0.35)
        self.play(FadeIn(efficient))
        self.wait(BEAT)
        left_math = MathTex(r"H \times W \times 3", color=WARM).next_to(pixel_stack, UP, buff=0.35)
        right_math = MathTex(r"h \times w \times C", color=ACCENT).next_to(latent_stack, UP, buff=0.35)
        left_brace = Brace(pixel_stack, LEFT, color=WARM)
        right_brace = Brace(latent_stack, RIGHT, color=PRIMARY)
        left_desc = txt("many tiny pixel details", WARM, 17).rotate(PI / 2).next_to(left_brace, LEFT, buff=0.12)
        right_desc = txt("compressed blueprint", PRIMARY, 17).rotate(-PI / 2).next_to(right_brace, RIGHT, buff=0.12)
        cost = MathTex(r"\times 4\ \mathrm{cost}", color=WARM, font_size=34).next_to(pixel_stack, DOWN, buff=0.9)
        savings = MathTex(r"\div 16", color=PRIMARY, font_size=42).next_to(latent_stack, DOWN, buff=0.9)
        self.play(Write(left_math), Write(right_math), GrowFromCenter(left_brace), GrowFromCenter(right_brace), FadeIn(left_desc), FadeIn(right_desc))
        self.wait(BEAT)
        self.play(GrowFromCenter(cost), GrowFromCenter(savings))
        self.wait(LONG)


class Scene16_TemporalInjection(Scene):
    def construct(self):
        self.camera.background_color = BG

        # A large centered factory visibly receives a noisy video on the left and
        # emits a pixel video on the right; temporal links stabilize its output.
        input_stack = VGroup(*[
            simple_video_strip([0], 0.92, 1.12, MUTED, noise=True).shift(RIGHT * i * 0.16 + UP * i * 0.13)
            for i in reversed(range(3))
        ]).move_to(LEFT * 5.25 + UP * 0.45)
        blocks = VGroup(
            network_block("Diffusion Model", 2.15).scale(1.18),
            network_block("Decoder", 1.62).scale(1.18),
            network_block("Upsampler", 1.72).scale(1.18),
        )
        blocks[0].move_to(LEFT * 2.65 + UP * 0.45)
        blocks[1].move_to(LEFT * 0.02 + UP * 0.45)
        blocks[2].move_to(RIGHT * 2.25 + UP * 0.45)
        output = Group(*[
            dog_image_frame(0, 1.12, 1.18, 0.72).shift(RIGHT * i * 0.2 + UP * i * 0.13)
            for i in reversed(range(3))
        ]).move_to(RIGHT * 5.05 + UP * 0.45)
        for page in output:
            page[0].set_color(WARM)
        output[0][3].scale(0.58).shift(LEFT * 0.2 + UP * 0.25)
        output[1][3].scale(1.22).shift(RIGHT * 0.16 + DOWN * 0.2)
        output[2][3].rotate(0.28).shift(LEFT * 0.12 + DOWN * 0.05)

        input_arrow = Arrow(input_stack.get_right(), blocks[0].get_left(), color=PRIMARY, buff=0.12, stroke_width=7, tip_length=0.24)
        connectors = VGroup(*[
            Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), color=MUTED, buff=0.12, stroke_width=5, tip_length=0.2)
            for i in range(2)
        ])
        output_arrow = Arrow(blocks[-1].get_right(), output.get_left(), color=PRIMARY, buff=0.12, stroke_width=7, tip_length=0.24)
        input_label = VGroup(txt("INPUT", PRIMARY, 22), txt("latent noise video", MUTED, 17)).arrange(DOWN, buff=0.06).next_to(input_stack, UP, buff=0.2)
        output_label = VGroup(txt("OUTPUT", PRIMARY, 22), txt("pixel video", WARM, 17)).arrange(DOWN, buff=0.06).next_to(output, UP, buff=0.2)

        self.play(FadeIn(input_stack), FadeIn(input_label))
        self.play(GrowArrow(input_arrow))
        self.play(
            LaggedStart(*[GrowFromCenter(block) for block in blocks], lag_ratio=0.2),
            LaggedStart(*[GrowArrow(arrow) for arrow in connectors], lag_ratio=0.25),
        )
        self.play(GrowArrow(output_arrow), FadeIn(output), FadeIn(output_label))
        self.wait(BEAT)
        internals = VGroup()
        for block in blocks:
            dots = VGroup(*[
                Square(0.22, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.45)
                for _ in range(3)
            ]).arrange(RIGHT, buff=0.2).move_to(block.get_center() + DOWN * 0.34)
            internals.add(dots)
        self.play(LaggedStart(*[FadeIn(g) for g in internals], lag_ratio=0.18))
        flicker_path = VMobject(color=WARM, stroke_width=5).set_points_as_corners([
            output.get_bottom() + DOWN * 0.22 + LEFT * 0.48,
            output.get_bottom() + DOWN * 0.02,
            output.get_bottom() + DOWN * 0.28 + RIGHT * 0.48,
        ])
        flicker = txt("identity jumps every frame", WARM, 20).next_to(flicker_path, DOWN, buff=0.12)
        before_badge = txt("BEFORE TEMPORAL INJECTION", WARM, 22).move_to(DOWN * 1.7)
        self.play(Create(flicker_path), FadeIn(flicker), FadeIn(before_badge))
        self.play(
            output[0][3].animate.shift(RIGHT * 0.12 + DOWN * 0.1),
            output[1][3].animate.shift(LEFT * 0.1 + UP * 0.12),
            output[2][3].animate.rotate(-0.45),
            run_time=FAST,
        )
        self.wait(BEAT)
        machine = gear(0.48).move_to(UP * 2.75)
        self.play(GrowFromCenter(machine))
        self.wait(BEAT)
        temporal_links = VGroup()
        for block, dots in zip(blocks, internals):
            target = block.get_top() + UP * 0.3
            self.play(machine.animate.move_to(target).rotate(PI / 2), run_time=NORMAL)
            links = VGroup(*[Line(dots[i].get_right(), dots[i + 1].get_left(), color=PRIMARY, stroke_width=4) for i in range(2)])
            temporal_links.add(links)
            self.play(LaggedStart(*[Create(link) for link in links], lag_ratio=0.25))
            self.wait(BEAT)
        stable = Group(*[
            dog_image_frame(0, 1.12, 1.18, 1.0).shift(RIGHT * i * 0.2 + UP * i * 0.13)
            for i in reversed(range(3))
        ]).move_to(output)
        stable_path = Line(
            stable.get_bottom() + DOWN * 0.16 + LEFT * 0.5,
            stable.get_bottom() + DOWN * 0.16 + RIGHT * 0.5,
            color=PRIMARY,
            stroke_width=5,
        )
        stable_label = txt("same dog aligns across frames", SECONDARY, 18).next_to(stable_path, DOWN, buff=0.12)
        after_badge = txt("AFTER TEMPORAL INJECTION", PRIMARY, 22).move_to(before_badge)
        self.play(
            ReplacementTransform(output, stable),
            ReplacementTransform(flicker_path, stable_path),
            ReplacementTransform(flicker, stable_label),
            ReplacementTransform(before_badge, after_badge),
        )
        self.play(ShowPassingFlash(stable_path.copy().set_stroke(width=11), time_width=0.3), run_time=SLOW)
        self.wait(LONG)


class Scene17_PainterToFilmmaker(Scene):
    def construct(self):
        self.camera.background_color = BG

        # One polished dog image duplicates into five posed frames; a smooth
        # temporal spine turns those frames into a film the viewer can read.
        title = txt("the same model learns to direct time", ACCENT, 27).to_edge(UP, buff=0.28)
        image = dog_image_frame(0, 2.55, 2.15, 1.0, 0.0).move_to(LEFT * 3.9 + UP * 0.35)
        image_label = VGroup(txt("PAINTER", SECONDARY, 25), txt("one beautiful frame", WHITE_ISH, 18)).arrange(DOWN, buff=0.08).next_to(image, DOWN, buff=0.22)
        brush = Line(LEFT * 0.45, RIGHT * 0.45, color=ACCENT, stroke_width=6).rotate(0.45).next_to(image, RIGHT, buff=0.2)
        palette = VGroup(Circle(0.3, color=SECONDARY), *[Dot(color=c, radius=0.045).shift(v) for c, v in [(SECONDARY, LEFT * 0.1), (ACCENT, RIGHT * 0.1), (PRIMARY, UP * 0.1)]]).next_to(image, LEFT, buff=0.2)
        self.play(FadeIn(title), GrowFromCenter(image), Create(brush), GrowFromCenter(palette), FadeIn(image_label))
        self.wait(BEAT)
        add_time = VGroup(gear(0.34, PRIMARY), txt("add time", PRIMARY, 20)).arrange(DOWN, buff=0.12).move_to(LEFT * 0.55 + UP * 0.45)
        self.play(GrowFromCenter(add_time[0]), FadeIn(add_time[1]))
        self.wait(BEAT)
        frames = Group(*[dog_image_frame(-0.12 + i * 0.06, 1.0, 0.82, 1.0) for i in range(5)])
        frames.arrange(RIGHT, buff=0.14).move_to(RIGHT * 3.05 + UP * 0.55)
        self.play(LaggedStart(*[TransformFromCopy(image, frame) for frame in frames], lag_ratio=0.16), run_time=SLOW)
        self.wait(BEAT)
        spine_y = frames.get_bottom()[1] - 0.5
        points = [np.array([frame.get_center()[0], spine_y, 0]) for frame in frames]
        spine = VMobject(color=PRIMARY, stroke_width=5).set_points_smoothly(points)
        stems = VGroup(*[Line(frame.get_bottom(), point, color=PRIMARY, stroke_width=2) for frame, point in zip(frames, points)])
        video_label = VGroup(txt("FILMMAKER", PRIMARY, 25), txt("one coherent sequence", WHITE_ISH, 18)).arrange(DOWN, buff=0.08).next_to(spine, DOWN, buff=0.16)
        reel = VGroup(Circle(0.32, color=PRIMARY, stroke_width=4), *[Circle(0.065, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.5).shift(rotate_vector(RIGHT * 0.17, a)) for a in np.linspace(0, TAU, 5, endpoint=False)]).next_to(frames, UP, buff=0.2)
        clapper = VGroup(Rectangle(width=0.7, height=0.38, color=ACCENT), Rectangle(width=0.7, height=0.12, color=ACCENT, fill_color=ACCENT, fill_opacity=0.35).next_to(ORIGIN, UP, buff=0)).next_to(reel, RIGHT, buff=0.15)
        self.play(LaggedStart(*[Create(stem) for stem in stems], lag_ratio=0.12), Create(spine), GrowFromCenter(reel), GrowFromCenter(clapper), FadeIn(video_label))
        self.play(ShowPassingFlash(spine.copy().set_stroke(width=11), time_width=0.25), run_time=SLOW)
        self.wait(BEAT)
        insight = txt("beautiful frames + temporal memory = filmmaking", WHITE_ISH, 21).move_to(DOWN * 2.5)
        self.play(FadeIn(insight))
        self.wait(BEAT)
        self.play(FadeOut(image), FadeOut(image_label), FadeOut(brush), FadeOut(palette), FadeOut(add_time), FadeOut(frames), FadeOut(stems), FadeOut(spine), FadeOut(video_label), FadeOut(reel), FadeOut(clapper), FadeOut(insight), FadeOut(title))
        words = VGroup(txt("MOTION", PRIMARY, 36), txt("MEMORY", PRIMARY, 36), txt("CONSISTENCY", PRIMARY, 36)).arrange(RIGHT, buff=0.75)
        icons = VGroup(
            VGroup(*[Square(0.24, color=PRIMARY) for _ in range(3)]).arrange(RIGHT, buff=0.16),
            VGroup(*[Dot(color=PRIMARY, radius=0.07) for _ in range(4)]).arrange(RIGHT, buff=0.22),
            MathTex(r"\square = \square", color=PRIMARY),
        )
        for icon, word in zip(icons, words):
            icon.next_to(word, DOWN, buff=0.35)
        for word, icon in zip(words, icons):
            self.play(GrowFromCenter(word), FadeIn(icon, shift=UP * 0.15))
            self.wait(BEAT)
        self.wait(LONG)
