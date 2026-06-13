# === PRODUCTION PLAN ===
# Core insight (one sentence): A video is a world that must remember itself.
#
# Color encoding:
#   PRIMARY   = time / motion / cross-frame relationships
#   SECONDARY = space / single-frame appearance
#   WARM      = cost / artifact / failure
#   ACCENT    = the mechanism under the spotlight
#   MUTED     = older / inert / raw material
#   WHITE_ISH = text
#
# Scene list:
#   Scene01_ImageVsVideoParadox — one image passes; a video consistency line breaks
#   Scene02_ResearchCity — camera lands in the foundation-model district
#   Scene03_FlipbookMissingPages — guessed gaps judder beside one continuous ribbon
#   Scene04_SpaceTimeUNetJellyCube — separate denoising breaks a trajectory
#   Scene05_InflatingImageToVideo — temporal bridges connect beautiful isolated frames
#   Scene06_TunnelVsTable — reconstruction tunnel vs token communication table
#   Scene07_PatchifyMosaic — noisy mosaic becomes cards, then clean output
#   Scene08_DiTScalingThreeSizes — three model sizes improve the same output
#   Scene09_TwoConveyorBelts — clean image data and flawed video data feed one model
#   Scene10_TwoSlidersTradeoff — frame quality and motion consistency balance
#   Scene11_TwoMemoryBanks — appearance and motion memories connect together
#   Scene12_MotionFreeGuidanceDial — two paths define a controllable motion signal
#   Scene13_SharedLatentRoom — incompatible inputs become one latent language
#   Scene14_SpatialVsSpatiotemporalAttention — links inside a frame vs across time
#   Scene15_PhotorealismLayers — realism factors separate and recombine
#   Scene16_RedundancyHeatmapOverheat — redundant pixels drive compute into the red
#   Scene17_SeparableVsJointMotion — angular dots contrast with a smooth path
#   Scene18_FITCompressionGate — token flood compresses before expensive attention
#   Scene19_ErrorScannerBaselineVsSnap — many temporal errors vs few
#   Scene20_SoraSpaceTimePatches — a cube becomes a visual sentence
#   Scene21_StatusLedgerBesideTheScene — a separate ledger tracks prompt details over time
#   Scene22_SoraScalingThreeMeters — detail, structure, and stability rise with compute
#   Scene23_RealismVsPhysicsSplit — cinematic appearance vs physical correctness
#   Scene24_UniversalTokenizerMachine — different modalities become identical tokens
#   Scene25_NextTokenPrediction — context repeatedly fills the next blank
#   Scene26_FourRepairToolsOnePatient — four operations reduce one clip's flicker
#   Scene27_GlassWorldMustRememberItself — a glass world passes two tests, then cracks
#
# Key transforms:
#   - film strip -> space-time cube
#   - noisy mosaic -> token cards -> clean output
#   - image and video -> identical latent blocks
#   - recurring cube -> space-time tokens -> glass world
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

ROOT = os.path.dirname(__file__)
A22 = os.path.join(ROOT, "images", "2.2")
A23 = os.path.join(ROOT, "images", "2.3")


def txt(s, color=WHITE_ISH, size=24):
    return Text(s, color=color, font_size=max(size, 16))


def footer(s, color=WHITE_ISH, size=23):
    t = txt(s, color, size)
    if t.width > 11.5:
        t.scale_to_fit_width(11.5)
    return t.to_edge(DOWN, buff=0.22)


def box(w=2, h=1.2, color=MUTED, fill=BG, opacity=0.05, radius=0.08):
    return RoundedRectangle(width=w, height=h, corner_radius=radius, color=color, stroke_width=3,
                            fill_color=fill, fill_opacity=opacity)


def photo_box(path, w=2, h=1.3, color=SECONDARY, opacity=1):
    border = box(w, h, color, BG, 1)
    image = ImageMobject(path).set_opacity(opacity)
    image.scale_to_fit_width(w - 0.12)
    if image.height > h - 0.12:
        image.scale_to_fit_height(h - 0.12)
    return Group(border, image.move_to(border))


def filmstrip(paths, w=1.0, h=0.7, color=PRIMARY, opacity=1):
    return Group(*[photo_box(p, w, h, color, opacity) for p in paths]).arrange(RIGHT, buff=0.08)


def token_grid(rows, cols, side=0.28, color=ACCENT, buff=0.05):
    return VGroup(*[Square(side, color=color, fill_color=color, fill_opacity=0.18)
                    for _ in range(rows * cols)]).arrange_in_grid(rows, cols, buff=buff)


def core(label="", w=2.2, h=1.2, color=ACCENT):
    body = box(w, h, color, color, 0.12, 0.15)
    if not label:
        return body
    label_mob = txt(label, size=18)
    if label_mob.width > w - 0.18:
        label_mob.scale_to_fit_width(w - 0.18)
    if label_mob.height > h - 0.15:
        label_mob.scale_to_fit_height(h - 0.15)
    return VGroup(body, label_mob.move_to(body))


def video_cube(w=2.8, h=1.8, color=PRIMARY):
    front = box(w, h, color, color, 0.04)
    back = front.copy().shift(RIGHT * 0.42 + UP * 0.34).set_opacity(0.45)
    edges = VGroup(*[Line(a, b, color=color, stroke_width=2)
                     for a, b in zip(front.get_vertices(), back.get_vertices())])
    return VGroup(back, edges, front)


def person(color=SECONDARY, scale=1, pose=0):
    head = Circle(0.14, color=color, fill_color=color, fill_opacity=0.25).shift(UP * 0.48)
    torso = Line(UP * 0.32, DOWN * 0.28, color=color, stroke_width=4)
    limbs = VGroup(
        Line(UP * 0.12, LEFT * (0.34 + 0.1 * pose) + UP * 0.05, color=color, stroke_width=4),
        Line(UP * 0.12, RIGHT * (0.34 - 0.08 * pose) + DOWN * 0.02, color=color, stroke_width=4),
        Line(DOWN * 0.28, LEFT * 0.27 + DOWN * (0.62 - 0.08 * pose), color=color, stroke_width=4),
        Line(DOWN * 0.28, RIGHT * 0.27 + DOWN * (0.62 + 0.08 * pose), color=color, stroke_width=4),
    )
    return VGroup(head, torso, limbs).scale(scale)


def noise_field(side=2, seed=1, count=80):
    rng = np.random.default_rng(seed)
    border = Square(side, color=MUTED)
    dots = VGroup(*[Dot([rng.uniform(-side/2, side/2), rng.uniform(-side/2, side/2), 0],
                        radius=0.025, color=WARM if i % 5 == 0 else MUTED) for i in range(count)])
    return VGroup(border, dots)


def slider(label, color, y):
    rail = Line(LEFT * 2, RIGHT * 2, color=color, stroke_width=4).shift(LEFT * 2.65 + UP * y)
    knob = Dot(rail.get_center(), radius=0.14, color=color)
    return VGroup(rail, knob, txt(label, color, 18).next_to(rail, LEFT, buff=0.2))


def meter(label, level, color):
    frame = box(0.42, 1.35, MUTED, BG, 0)
    fill = Rectangle(width=0.25, height=max(0.08, 1.08 * level), stroke_width=0,
                     fill_color=color, fill_opacity=0.75).align_to(frame, DOWN).shift(UP * 0.12)
    return VGroup(frame, fill, txt(label, size=12).next_to(frame, DOWN, buff=0.06))


def drawn_chair(color=ACCENT, scale=1):
    seat = Polygon(LEFT*.5+UP*.15, RIGHT*.5+UP*.15, RIGHT*.42+DOWN*.12, LEFT*.42+DOWN*.12,
                   color=color, fill_color=color, fill_opacity=.2)
    back = Rectangle(width=.9, height=.75, color=color, fill_color=color, fill_opacity=.12).next_to(seat, UP, buff=0)
    legs = VGroup(Line(seat.get_corner(DL), seat.get_corner(DL)+DOWN*.65, color=color, stroke_width=5),
                  Line(seat.get_corner(DR), seat.get_corner(DR)+DOWN*.65, color=color, stroke_width=5))
    return VGroup(back, seat, legs).scale(scale)


def attention_links(mobs, color=PRIMARY, curved=True):
    links = VGroup()
    for a, b in zip(mobs[:-1], mobs[1:]):
        links.add(ArcBetweenPoints(a.get_top(), b.get_top(), angle=-PI/2, color=color, stroke_width=3)
                  if curved else Line(a.get_center(), b.get_center(), color=color, stroke_width=3))
    return links


class Scene01_ImageVsVideoParadox(Scene):
    def construct(self):
        self.camera.background_color = BG
        # One output passes; five individually-good outputs fail when forced to agree.
        divider = DashedLine(UP*2.9, DOWN*2.9, color=MUTED)
        prompts = VGroup(core("same prompt", 1.5, .6), core("same prompt", 1.5, .6)).arrange(RIGHT, buff=5.2).shift(UP*2)
        models = VGroup(core("model", 1.2, .8, MUTED), core("model", 1.2, .8, MUTED)).arrange(RIGHT, buff=5.5).shift(UP*.75)
        self.play(Create(divider), FadeIn(prompts), FadeIn(models)); self.wait(BEAT)
        image = photo_box(os.path.join(A22, "dog_0.jpg"), 2.5, 1.65, SECONDARY).shift(LEFT*3.4+DOWN*.85)
        check = txt("✓", SECONDARY, 34).next_to(image, RIGHT, buff=.2)
        strip = filmstrip([os.path.join(A22, f"dog_{i}.jpg") for i in range(1,6)], .85, .62, MUTED).shift(RIGHT*3.35+DOWN*.75)
        strip[1].stretch(1.13, 1); strip[2].stretch(.9, 0); strip[3].shift(UP*.12); strip[4].rotate(.08)
        self.play(FadeIn(image, shift=DOWN*.2), GrowFromCenter(check)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN*.15) for f in strip], lag_ratio=.12)); self.wait(BEAT)
        defects = VGroup(*[Circle(.18, color=WARM).move_to(strip[i]).shift(v) for i,v in enumerate([UP*.1,RIGHT*.15,DOWN*.12,LEFT*.15,DOWN*.15])])
        self.play(LaggedStart(*[Create(d) for d in defects], lag_ratio=.15))
        points = [f.get_center()+DOWN*.05 for f in strip]
        line = VMobject(color=WARM, stroke_width=5).set_points_as_corners(points[:3]+[points[2]+DOWN*.3, points[3]+UP*.35, points[4]])
        self.play(Create(line), Indicate(line, color=WARM)); self.play(line.animate.set_stroke(opacity=.35)); self.wait(BEAT)
        cap = VGroup(txt("A video is not many good images.", WHITE_ISH, 17),
                     txt("It is one consistent world over time.", PRIMARY, 17)).arrange(DOWN, buff=.1).to_edge(DOWN, buff=.18)
        self.play(Write(cap)); self.wait(LONG)


class Scene02_ResearchCity(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        # A taxonomy becomes a navigable city, and the camera descends into one district.
        names = ["Pioneering", "Open Source", "Training Efficient", "Long Video", "Multimodal", "Foundation Models"]
        positions = [LEFT*4+UP*1.7, UP*2, RIGHT*3.8+UP*1.5, LEFT*4+DOWN*1.5, DOWN*2, RIGHT*3.7+DOWN*1.2]
        districts = VGroup()
        for n,p in zip(names, positions):
            road = VGroup(*[box(.75,.45,MUTED,MUTED,.07) for _ in range(6)]).arrange_in_grid(2,3,buff=.08)
            districts.add(VGroup(road, txt(n,MUTED,10).next_to(road,DOWN,buff=.08)).move_to(p))
        self.play(LaggedStart(*[FadeIn(d) for d in districts], lag_ratio=.08)); self.wait(BEAT)
        target = districts[-1]
        self.play(self.camera.frame.animate.move_to(target).scale(.58), target.animate.set_color(ACCENT),
                  target[0].animate.set_opacity(.12), run_time=SLOW); self.wait(BEAT)
        symbols = ["cube","tokens","balance","bridge","factory","tower","tokenizer"]
        buildings = VGroup(*[VGroup(box(.42,.7,ACCENT,ACCENT,.15),txt(s,WHITE_ISH,4).next_to(ORIGIN,DOWN,buff=.02)) for s in symbols])
        for b in buildings:
            b[1].next_to(b[0], DOWN, buff=.02)
        buildings.arrange(RIGHT,buff=.12).scale(.62).move_to(target).shift(UP*.08)
        self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in buildings],lag_ratio=.1)); self.wait(BEAT)
        self.play(FadeIn(footer("Foundation video models: large scale, high compute, stronger temporal modeling", size=11)))
        self.wait(LONG)


class Scene03_FlipbookMissingPages(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Sparse walking poses invite wrong guesses; a continuous ribbon needs no repair.
        divider = DashedLine(UP*2.8, DOWN*2.8, color=MUTED)
        pages = VGroup(*[box(.38,1.1,MUTED) for _ in range(15)]).arrange(RIGHT,buff=.035).scale(.78).shift(LEFT*3.4+UP*.55)
        key_ids = [0,4,9,14]
        poses = VGroup(*[person(SECONDARY,.3,np.sin(i)).move_to(pages[k]).shift(UP*.12*np.sin(i)) for i,k in enumerate(key_ids)])
        self.play(Create(divider), LaggedStart(*[Create(p) for p in pages],lag_ratio=.02), FadeIn(poses)); self.wait(BEAT)
        robot = VGroup(box(.55,.42,ACCENT,ACCENT,.12),Circle(.07,color=ACCENT).shift(LEFT*.15+DOWN*.25),Circle(.07,color=ACCENT).shift(RIGHT*.15+DOWN*.25)).shift(LEFT*5+DOWN*1.25)
        guesses = VGroup()
        for j,k in enumerate([1,2,3,5,6,7,8,10,11,12,13]):
            g=person(WARM,.27,(j%3)-1).move_to(pages[k])
            if j%4==0:g[0].scale(1.5)
            if j%4==1:g[2][0].stretch(1.5,0)
            if j%4==2:g.shift(RIGHT*.09)
            guesses.add(g)
        self.play(FadeIn(robot),LaggedStart(*[FadeIn(g) for g in guesses],lag_ratio=.06),run_time=SLOW); self.wait(BEAT)
        ribbon = VMobject(color=PRIMARY,stroke_width=7).set_points_smoothly([RIGHT*.5+DOWN*.2,RIGHT*2+UP*.8,RIGHT*3.5+DOWN*.3,RIGHT*5+UP*.55])
        smooth = VGroup(*[person(PRIMARY,.28,np.sin(i)).move_to(ribbon.point_from_proportion(i/9)) for i in range(10)])
        self.play(Create(ribbon),LaggedStart(*[FadeIn(p) for p in smooth],lag_ratio=.05),run_time=SLOW)
        cap=VGroup(txt("Old way: generate keyframes, then guess the gaps.",WHITE_ISH,12),txt("Lumiere: generate the temporal span together.",PRIMARY,12)).arrange(DOWN,buff=.08).to_edge(DOWN,buff=.15)
        self.play(Write(cap)); self.wait(LONG)


class Scene04_SpaceTimeUNetJellyCube(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same trajectory breaks under independent slices and survives whole-volume denoising.
        strip=VGroup(*[box(.65,.5,SECONDARY) for _ in range(6)]).arrange(RIGHT,buff=.08)
        self.play(LaggedStart(*[Create(f) for f in strip],lag_ratio=.08)); self.wait(BEAT)
        cube=video_cube(3.2,2.0,PRIMARY)
        self.play(ReplacementTransform(strip,cube),run_time=SLOW); self.wait(BEAT)
        thread=VMobject(color=PRIMARY,stroke_width=6).set_points_smoothly([cube.get_left()+DOWN*.45,cube.get_center()+UP*.5,cube.get_right()+DOWN*.2])
        self.play(Create(thread)); self.wait(BEAT)
        left=cube.copy().scale(.75).shift(LEFT*3.5); right=cube.copy().scale(.75).shift(RIGHT*3.5)
        broken=VGroup(*[Line(LEFT*4.7+RIGHT*i*.45+UP*((i%2)*.4-.2),LEFT*4.35+RIGHT*i*.45+UP*(((i+1)%2)*.4-.2),color=WARM,stroke_width=5) for i in range(5)])
        whole=VMobject(color=PRIMARY,stroke_width=6).set_points_smoothly([RIGHT*4.7+DOWN*.5,RIGHT*3.5+UP*.55,RIGHT*2.3+DOWN*.2])
        self.play(FadeOut(cube,thread),FadeIn(left,right),Create(broken),Create(whole),run_time=SLOW)
        self.play(Indicate(broken,color=WARM),Indicate(whole,color=PRIMARY)); self.wait(BEAT)
        self.play(Write(footer("STUNet denoises video as one space-time object."))); self.wait(LONG)


class Scene05_InflatingImageToVideo(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Image knowledge already paints well; temporal bridges carry identity forward.
        machine=core("image model",2.0,1.2,SECONDARY).shift(LEFT*4.7+UP*1.4)
        hero=photo_box(os.path.join(A22,"dog_2.jpg"),2.5,1.65,SECONDARY).shift(LEFT*1.5+UP*1.4)
        self.play(GrowFromCenter(machine),FadeIn(hero)); self.wait(BEAT)
        islands=Group(*[photo_box(os.path.join(A22,f"dog_{i}.jpg"),1.8,1.2,SECONDARY) for i in [3,4,5]]).arrange(RIGHT,buff=1.0).shift(DOWN*.9)
        self.play(LaggedStart(*[FadeIn(x) for x in islands],lag_ratio=.15)); self.wait(BEAT)
        bridges=VGroup(*[ArcBetweenPoints(a.get_right(),b.get_left(),angle=-PI/2,color=PRIMARY,stroke_width=5) for a,b in zip(islands[:-1],islands[1:])])
        self.play(LaggedStart(*[Create(b) for b in bridges],lag_ratio=.2)); self.wait(BEAT)
        flow=Dot(bridges[0].get_start(),radius=.1,color=ACCENT)
        self.play(MoveAlongPath(flow,bridges[0]),MoveAlongPath(flow.copy(),bridges[1]),run_time=SLOW)
        self.play(Indicate(islands,color=PRIMARY),Write(footer("Keep image knowledge. Add temporal connections."))); self.wait(LONG)


class Scene06_TunnelVsTable(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The reconstructed cube visibly dissolves into token cards before they begin talking.
        divider=DashedLine(UP*2.8,DOWN*2.8,color=MUTED)
        tunnel=VGroup(Polygon(LEFT*2+UP*1.1,RIGHT*2+UP*.3,RIGHT*2+DOWN*.3,LEFT*2+DOWN*1.1,color=MUTED),
                       Polygon(LEFT*2+UP*.3,RIGHT*2+UP*1.1,RIGHT*2+DOWN*1.1,LEFT*2+DOWN*.3,color=MUTED)).scale(.65).shift(LEFT*3.5)
        cube=video_cube(1.0,.65,SECONDARY).shift(LEFT*5.4)
        self.play(Create(divider),Create(tunnel),FadeIn(cube)); self.wait(BEAT)
        self.play(cube.animate.scale(.42).move_to(tunnel),run_time=SLOW); self.play(cube.animate.scale(1/.42).move_to(LEFT*1.2),run_time=SLOW)
        table=Circle(1.15,color=ACCENT).shift(RIGHT*3.5)
        tokens=VGroup(*[Square(.28,color=ACCENT,fill_color=ACCENT,fill_opacity=.2).move_to(table.point_at_angle(a)) for a in np.linspace(0,TAU,10,endpoint=False)])
        token_grid_mid=token_grid(2,5,.28,ACCENT,.08).move_to(cube)
        self.play(Create(table),ReplacementTransform(cube,token_grid_mid),run_time=SLOW); self.wait(BEAT)
        self.play(ReplacementTransform(token_grid_mid,tokens),run_time=SLOW); self.wait(BEAT)
        links=VGroup(*[Line(tokens[i],tokens[(i+4)%10],color=PRIMARY,stroke_width=2) for i in range(10)])
        long_link=ArcBetweenPoints(tokens[0].get_center(),tokens[6].get_center(),angle=-PI/2,color=PRIMARY,stroke_width=6)
        self.play(LaggedStart(*[Create(l) for l in links],lag_ratio=.08),Create(long_link))
        self.play(Indicate(long_link,color=PRIMARY),Write(footer("Transformers let distant visual tokens talk."))); self.wait(LONG)


class Scene07_PatchifyMosaic(Scene):
    def construct(self):
        self.camera.background_color = BG
        # One noisy mosaic fractures, queues through a Transformer, and becomes a clean picture.
        noisy=noise_field(2.8,7,150).shift(LEFT*4.7)
        self.play(FadeIn(noisy)); self.wait(BEAT)
        tiles=token_grid(4,4,.55,ACCENT,.06).move_to(noisy)
        self.play(Create(tiles),FadeOut(noisy),run_time=SLOW); self.wait(BEAT)
        queue=tiles.copy().arrange_in_grid(2,8,buff=.08).scale(.55).move_to(LEFT*2.2)
        transformer=core("Transformer",2.4,2.0,ACCENT).shift(RIGHT*1.1)
        in_arrow=Arrow(queue.get_right(),transformer.get_left(),color=ACCENT,buff=.12,stroke_width=4)
        self.play(ReplacementTransform(tiles,queue),GrowFromCenter(transformer),GrowArrow(in_arrow),run_time=SLOW); self.wait(BEAT)
        clean_cards=token_grid(4,4,.4,SECONDARY,.05).move_to(transformer)
        self.play(FadeOut(queue),FadeIn(clean_cards),run_time=SLOW); self.wait(BEAT)
        output=photo_box(os.path.join(A22,"dog_grass.png"),2.8,1.9,SECONDARY).shift(RIGHT*4.7)
        out_arrow=Arrow(transformer.get_right(),output.get_left(),color=SECONDARY,buff=.12,stroke_width=4)
        self.play(GrowArrow(out_arrow),FadeOut(clean_cards),FadeIn(output),run_time=SLOW)
        self.play(Indicate(output[0],color=SECONDARY),Write(footer("DiT turns diffusion into token processing."))); self.wait(LONG)


class Scene08_DiTScalingThreeSizes(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Three sizes receive one prompt; quality improvement is visible in their outputs.
        prompt=core("same prompt",1.8,.65,WHITE_ISH).shift(UP*2.6)
        models=VGroup(core("Small",1.2,.8,MUTED),core("Medium",1.6,1.05,MUTED),core("Large",2.0,1.3,ACCENT)).arrange(RIGHT,buff=1.0).shift(UP*.8)
        self.play(FadeIn(prompt),LaggedStart(*[GrowFromCenter(m) for m in models],lag_ratio=.15)); self.wait(BEAT)
        outputs=Group(photo_box(os.path.join(A22,"dog_grass_pixelated.png"),2.5,1.6,WARM,.35),
                      photo_box(os.path.join(A22,"dog_grass_pixelated.png"),2.5,1.6,SECONDARY,.7),
                      photo_box(os.path.join(A22,"dog_grass.png"),2.5,1.6,ACCENT)).arrange(RIGHT,buff=.65).shift(DOWN*1.25)
        prompt_arrows=VGroup(*[Arrow(prompt.get_bottom(),m.get_top(),color=WHITE_ISH,buff=.08,stroke_width=3) for m in models])
        output_arrows=VGroup(*[Arrow(m.get_bottom(),o.get_top(),color=ACCENT,buff=.08,stroke_width=3) for m,o in zip(models,outputs)])
        self.play(LaggedStart(*[GrowArrow(a) for a in prompt_arrows],lag_ratio=.12))
        self.play(LaggedStart(*[GrowArrow(a) for a in output_arrows],*[FadeIn(o) for o in outputs],lag_ratio=.1),run_time=SLOW)
        self.play(Indicate(outputs,color=ACCENT),Write(footer("Scaling improves generation quality."))); self.wait(LONG)


class Scene09_TwoConveyorBelts(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Dense clean cards and sparse flawed clips visibly pass their habits into one output.
        belt1=Line(LEFT*5+UP*1.5,LEFT*.8+UP*1.5,color=SECONDARY,stroke_width=8)
        belt2=Line(LEFT*5+DOWN*1.1,LEFT*.8+DOWN*1.1,color=MUTED,stroke_width=8)
        clean=VGroup(*[box(.45,.35,SECONDARY,SECONDARY,.15) for _ in range(14)]).arrange(RIGHT,buff=.07).scale(.8).move_to(belt1)
        messy=VGroup(*[box(.58,.42,MUTED,MUTED,.08) for _ in range(6)]).arrange(RIGHT,buff=.18).scale(.8).move_to(belt2)
        flaws=VGroup(txt("blur",WARM,12).move_to(messy[1]),txt("MARK",WARM,11).rotate(.25).move_to(messy[3]),token_grid(2,2,.1,WARM,.01).move_to(messy[5]))
        model=core("model",2.0,2.0,ACCENT).shift(RIGHT*1)
        output=photo_box(os.path.join(A22,"dog_1.jpg"),2.2,1.5,WARM,.65).shift(RIGHT*4.5)
        inherited=VGroup(txt("MARK",WARM,14).rotate(.25).move_to(output),Circle(.32,color=WARM).move_to(output).shift(RIGHT*.55+DOWN*.25))
        self.play(Create(belt1),LaggedStart(*[FadeIn(x) for x in clean],lag_ratio=.03)); self.wait(BEAT)
        self.play(Create(belt2),LaggedStart(*[FadeIn(x) for x in messy],lag_ratio=.08),FadeIn(flaws)); self.wait(BEAT)
        feeds=VGroup(Arrow(belt1.get_right(),model.get_left()+UP*.45,color=SECONDARY,buff=.08),Arrow(belt2.get_right(),model.get_left()+DOWN*.45,color=WARM,buff=.08))
        self.play(GrowFromCenter(model),GrowArrow(feeds[0]),GrowArrow(feeds[1])); self.wait(BEAT)
        self.play(FadeIn(output),FadeIn(inherited),run_time=SLOW)
        self.play(Indicate(flaws,color=WARM),Indicate(inherited,color=WARM),Write(footer("Video models need more, but often learn from less."))); self.wait(LONG)


class Scene10_TwoSlidersTradeoff(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Two independent controls expose opposite failure modes before meeting at balance.
        frame_slider=slider("Frame Quality",SECONDARY,1.2); motion_slider=slider("Motion Consistency",PRIMARY,-.2)
        crisp_flicker=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in [0,2,1,4]],1.0,.7,WARM).shift(RIGHT*3.3+UP*.6)
        blurry_smooth=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(4)],1.0,.7,PRIMARY,.35).move_to(crisp_flicker)
        balanced=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(4)],1.0,.7,PRIMARY).move_to(crisp_flicker)
        self.play(Create(frame_slider),Create(motion_slider),FadeIn(crisp_flicker)); self.wait(BEAT)
        self.play(frame_slider[1].animate.move_to(frame_slider[0].get_right()),motion_slider[1].animate.move_to(motion_slider[0].get_left()),Indicate(crisp_flicker,color=WARM),run_time=SLOW)
        self.play(frame_slider[1].animate.move_to(frame_slider[0].get_left()),motion_slider[1].animate.move_to(motion_slider[0].get_right()),FadeOut(crisp_flicker),FadeIn(blurry_smooth),run_time=SLOW)
        self.play(frame_slider[1].animate.move_to(frame_slider[0].point_from_proportion(.72)),motion_slider[1].animate.move_to(motion_slider[0].point_from_proportion(.72)),FadeOut(blurry_smooth),FadeIn(balanced),run_time=SLOW); self.wait(BEAT)
        self.play(Indicate(VGroup(frame_slider,motion_slider),color=ACCENT),Write(footer("Text-to-video quality is a balance problem."))); self.wait(LONG)


class Scene11_TwoMemoryBanks(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Appearance and motion memories plug into separate ports, then cooperate.
        image_bank=core("image memory",2.4,1.5,SECONDARY).shift(LEFT*4)
        video_bank=core("video memory",2.4,1.5,PRIMARY).shift(RIGHT*4)
        model=core("model",2.0,1.7,ACCENT)
        frozen=filmstrip([os.path.join(A22,"dog_0.jpg")]*4,.85,.58,SECONDARY).shift(DOWN*2)
        soft_motion=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(4)],.85,.58,PRIMARY,.3).move_to(frozen)
        balanced=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(4)],.85,.58,PRIMARY).move_to(frozen)
        self.play(GrowFromCenter(image_bank),GrowFromCenter(video_bank),GrowFromCenter(model)); self.wait(BEAT)
        left_cable=ArcBetweenPoints(image_bank.get_right(),model.get_left(),angle=-.4,color=SECONDARY,stroke_width=5)
        right_cable=ArcBetweenPoints(video_bank.get_left(),model.get_right(),angle=.4,color=PRIMARY,stroke_width=5)
        image_lessons=VGroup(*[txt(x,SECONDARY,13) for x in ["texture","lighting","shape","composition"]]).arrange(DOWN,buff=.08).next_to(image_bank,DOWN,buff=.15)
        video_lessons=VGroup(*[txt(x,PRIMARY,13) for x in ["motion","camera","consistency","transition"]]).arrange(DOWN,buff=.08).next_to(video_bank,DOWN,buff=.15)
        self.play(FadeIn(image_lessons,video_lessons)); self.wait(BEAT)
        self.play(Create(left_cable),FadeIn(frozen)); self.play(Indicate(frozen[0][0],color=WARM)); self.wait(BEAT)
        self.play(FadeOut(left_cable,frozen),Create(right_cable),FadeIn(soft_motion)); self.wait(BEAT)
        self.play(Create(left_cable),FadeOut(soft_motion),FadeIn(balanced),run_time=SLOW)
        self.play(Write(footer("Learn appearance from images. Learn motion from videos."))); self.wait(LONG)


class Scene12_MotionFreeGuidanceDial(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A controller compares a dynamic path with a clean static path, then dials their difference.
        path_a=Line(LEFT*5+UP*1.5,LEFT*.5+UP*1.5,color=PRIMARY,stroke_width=5)
        path_b=Line(LEFT*5+DOWN*.7,LEFT*.5+DOWN*.7,color=SECONDARY,stroke_width=5)
        moving=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(3)],.8,.55,PRIMARY).move_to(path_a)
        static=filmstrip([os.path.join(A22,"dog_0.jpg")]*3,.8,.55,SECONDARY).move_to(path_b)
        labels=VGroup(txt("Path A: motion-conditioned",PRIMARY,18).move_to(LEFT*2.75+UP*2.15),
                      txt("Path B: motion-free",SECONDARY,18).move_to(LEFT*2.75+DOWN*1.4))
        controller=core("A - B",1.5,1.6,ACCENT).shift(RIGHT*.8+UP*.4)
        signal=Arrow(controller.get_right(),RIGHT*2.6+UP*.4,color=ACCENT,buff=.08,stroke_width=5)
        dial_c=Circle(.8,color=ACCENT).shift(RIGHT*4+UP*.4); hand=Line(dial_c.get_center(),dial_c.get_center()+rotate_vector(UP*.62,-1),color=ACCENT,stroke_width=5)
        result_static=filmstrip([os.path.join(A22,"dog_0.jpg")]*3,.72,.5,WARM).shift(RIGHT*4+DOWN*1.4)
        result_warp=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in [0,3,5]],.72,.5,WARM,.55).move_to(result_static); result_warp[1].stretch(1.35,0)
        result_balanced=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(3)],.72,.5,PRIMARY).move_to(result_static)
        self.play(Create(path_a),Create(path_b),FadeIn(moving,static,labels)); self.wait(BEAT)
        self.play(GrowFromCenter(controller),GrowArrow(signal),Create(dial_c),Create(hand)); self.wait(BEAT)
        self.play(FadeIn(result_static),run_time=NORMAL)
        self.play(Rotate(hand,2,about_point=dial_c.get_center()),FadeOut(result_static),FadeIn(result_warp),run_time=SLOW)
        self.play(Rotate(hand,-1,about_point=dial_c.get_center()),FadeOut(result_warp),FadeIn(result_balanced),run_time=SLOW)
        self.play(Write(footer("Control motion without damaging spatial quality."))); self.wait(LONG)


class Scene13_SharedLatentRoom(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Different inputs are rejected, encoded, emerge beside the encoder, then enter together.
        image=photo_box(os.path.join(A22,"panda.jpg"),1.8,1.2,SECONDARY).shift(LEFT*5+UP*1.25)
        cube=video_cube(1.8,1.2,PRIMARY).shift(LEFT*5+DOWN*1.25)
        transformer=core("same\nTransformer",1.8,3.4,MUTED).shift(RIGHT*4.6)
        reject=txt("× incompatible shapes",WARM,16).next_to(transformer,UP,buff=.15)
        self.play(FadeIn(image,cube),GrowFromCenter(transformer)); self.wait(BEAT)
        stops=[transformer.get_left()+LEFT*1.25+UP*1.05,transformer.get_left()+LEFT*1.25+DOWN*1.05]
        self.play(image.animate.move_to(stops[0]),cube.animate.move_to(stops[1]),run_time=SLOW)
        self.play(Indicate(transformer,color=WARM),FadeIn(reject),
                  image.animate.shift(LEFT*.75),cube.animate.shift(LEFT*.75),run_time=NORMAL); self.wait(BEAT)
        encoder=core("Joint Causal\n3D Encoder",2.3,2.3,ACCENT).shift(LEFT*1.35)
        image_route=CurvedArrow(image.get_center(),encoder.get_right()+UP*.45,angle=-.55,color=ACCENT,stroke_width=4)
        video_route=CurvedArrow(cube.get_center(),encoder.get_right()+DOWN*.45,angle=.55,color=ACCENT,stroke_width=4)
        self.play(FadeOut(reject),GrowFromCenter(encoder),Create(image_route),Create(video_route)); self.wait(BEAT)
        self.play(MoveAlongPath(image,image_route),MoveAlongPath(cube,video_route),run_time=SLOW)
        self.play(image.animate.move_to(encoder).scale(.15).set_opacity(0),
                  cube.animate.move_to(encoder).scale(.15).set_opacity(0),run_time=NORMAL)
        self.remove(image,cube)
        def latent_block():
            body=box(1.45,.72,ACCENT,ACCENT,.12)
            stripes=VGroup(*[Line(UP*.25,DOWN*.25,color=SECONDARY if i%2==0 else PRIMARY,stroke_width=5)
                             for i in range(6)]).arrange(RIGHT,buff=.12).move_to(body)
            return VGroup(body,stripes)
        lat1=latent_block().next_to(encoder,LEFT,buff=.35).shift(UP*.52)
        lat2=latent_block().next_to(encoder,LEFT,buff=.35).shift(DOWN*.52)
        self.play(FadeOut(image_route,video_route),
                  LaggedStart(FadeIn(lat1,shift=LEFT*.25),FadeIn(lat2,shift=LEFT*.25),lag_ratio=.18)); self.wait(BEAT)
        self.play(FadeOut(encoder),run_time=NORMAL); self.wait(BEAT)
        accept=VGroup(Arrow(lat1.get_right(),transformer.get_left()+UP*.55,color=PRIMARY,buff=.08),
                      Arrow(lat2.get_right(),transformer.get_left()+DOWN*.55,color=PRIMARY,buff=.08))
        self.play(transformer[0].animate.set_stroke(PRIMARY).set_fill(PRIMARY,opacity=.12),
                  GrowArrow(accept[0]),GrowArrow(accept[1])); self.wait(BEAT)
        self.play(lat1.animate.next_to(transformer,LEFT,buff=.18).shift(UP*.55),
                  lat2.animate.next_to(transformer,LEFT,buff=.18).shift(DOWN*.55),run_time=SLOW)
        self.play(Write(footer("Different inputs, one latent language."))); self.wait(LONG)


class Scene14_SpatialVsSpatiotemporalAttention(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Short links explain one frame; long arcs track one moving ball through time.
        frame=box(4.0,2.6,SECONDARY).shift(LEFT*3.6+UP*.45)
        actor=person(SECONDARY,.65).move_to(frame).shift(LEFT*1)
        ball=Dot(frame.get_center()+RIGHT*.25,radius=.15,color=ACCENT)
        table=Rectangle(width=1.0,height=.35,color=SECONDARY).move_to(frame).shift(RIGHT*1.2+DOWN*.65)
        inside=VGroup(Line(actor.get_center(),ball,color=SECONDARY),Line(ball,table.get_center(),color=SECONDARY))
        self.play(Create(frame),FadeIn(actor,ball,table),Create(inside)); self.wait(BEAT)
        row=VGroup(*[box(1.05,.8,PRIMARY) for _ in range(5)]).arrange(RIGHT,buff=.16).shift(RIGHT*3.2+UP*.5)
        balls=VGroup(*[Dot(r.get_center()+RIGHT*(i-2)*.12,radius=.08,color=ACCENT) for i,r in enumerate(row)])
        self.play(LaggedStart(*[Create(r) for r in row],*[FadeIn(b) for b in balls],lag_ratio=.06)); self.wait(BEAT)
        arcs=attention_links(balls,PRIMARY,True)
        self.play(LaggedStart(*[Create(a) for a in arcs],lag_ratio=.12))
        self.play(Indicate(inside,color=SECONDARY),Indicate(arcs,color=PRIMARY),Write(footer("Understand the frame. Then understand the motion."))); self.wait(LONG)


class Scene15_PhotorealismLayers(Scene):
    def construct(self):
        self.camera.background_color = BG
        # One finished scene separates into six realism factors, then those factors recombine.
        image=photo_box(os.path.join(A23,"polar_bear.jpg"),5.2,3.5,SECONDARY)
        self.play(FadeIn(image)); self.wait(BEAT)
        names=["Object","Material","Environment","Lighting","Motion","Physics"]
        colors=[SECONDARY,ACCENT,PRIMARY,ACCENT,PRIMARY,WARM]
        layers=VGroup(*[VGroup(box(2.5,1.25,c,c,.08),txt(n,c,18)) for n,c in zip(names,colors)])
        for layer in layers: layer[1].move_to(layer[0])
        layers.arrange_in_grid(2,3,buff=(.55,.55)).shift(UP*.25)
        self.play(FadeOut(image),LaggedStart(*[FadeIn(layer,shift=UP*.15) for layer in layers],lag_ratio=.14),run_time=SLOW); self.wait(BEAT)
        links=VGroup(*[Arrow(layers[i].get_right(),layers[i+1].get_left(),color=ACCENT,buff=.08,stroke_width=3) for i in [0,1,3,4]])
        self.play(LaggedStart(*[GrowArrow(a) for a in links],lag_ratio=.12)); self.wait(BEAT)
        recombined=photo_box(os.path.join(A23,"polar_bear.jpg"),5.2,3.5,SECONDARY)
        self.play(FadeOut(layers),FadeIn(recombined),run_time=SLOW)
        self.play(Write(footer("Realism is layered."))); self.wait(LONG)


class Scene16_RedundancyHeatmapOverheat(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A difference map reveals that brute-force compute is spent mostly on unchanged regions.
        sheet=photo_box(os.path.join(A23,"contact_sheet.jpg"),7.0,4.2,SECONDARY).shift(LEFT*1.7)
        self.play(FadeIn(sheet)); self.wait(BEAT)
        gray=Rectangle(width=6.6,height=3.8,color=MUTED,fill_color=MUTED,fill_opacity=.35).move_to(sheet)
        hot=VGroup(*[Circle(.2,color=WARM,fill_color=WARM,fill_opacity=.35).move_to(sheet).shift(v) for v in [LEFT*2+UP,LEFT*.4+DOWN*.7,RIGHT*1.2+UP*.4,RIGHT*2+DOWN*1]])
        self.play(FadeIn(gray),LaggedStart(*[GrowFromCenter(h) for h in hot],lag_ratio=.15)); self.wait(BEAT)
        machine=core("process ALL regions",2.3,1.3,WARM).shift(RIGHT*4.6+UP*1.15)
        low=meter("compute",.15,MUTED).shift(RIGHT*4.7+DOWN*.35)
        high=meter("compute",1,WARM).move_to(low)
        self.play(GrowFromCenter(machine),FadeIn(low)); self.wait(BEAT)
        self.play(FadeOut(low),FadeIn(high),machine[0].animate.set_fill(WARM,opacity=.4),run_time=SLOW); self.wait(BEAT)
        compressed=VGroup(*[box(.3,.24,MUTED,MUTED,.18) for _ in range(8)]).arrange_in_grid(2,4,buff=.04).shift(RIGHT*3+DOWN*1.8)
        snap=core("Snap",1.7,1.0,ACCENT).shift(RIGHT*5+DOWN*1.8)
        snap_arrow=Arrow(compressed.get_right(),snap.get_left(),color=ACCENT,buff=.08,stroke_width=4)
        self.play(GrowFromCenter(snap),FadeIn(compressed),GrowArrow(snap_arrow),FadeOut(high),FadeIn(low),LaggedStart(*[Indicate(h,color=ACCENT) for h in hot],lag_ratio=.12))
        self.play(Write(footer("Video has redundancy. Use it."))); self.wait(LONG)


class Scene17_SeparableVsJointMotion(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Isolated positions connect into corners; one joint analysis draws a natural curve.
        divider=DashedLine(UP*2.7,DOWN*2.7,color=MUTED)
        left_pts=VGroup(*[Dot(LEFT*5+RIGHT*i*.75+UP*((i%2)*.7-.4),color=MUTED) for i in range(6)])
        angular=VMobject(color=WARM,stroke_width=5).set_points_as_corners([p.get_center() for p in left_pts])
        smooth=VMobject(color=PRIMARY,stroke_width=6).set_points_smoothly([RIGHT*.7+DOWN*.4,RIGHT*2+UP*.75,RIGHT*3.5+DOWN*.2,RIGHT*5+UP*.45])
        self.play(Create(divider),LaggedStart(*[GrowFromCenter(p) for p in left_pts],lag_ratio=.1)); self.wait(BEAT)
        self.play(Create(angular)); self.wait(BEAT)
        self.play(Create(smooth),run_time=SLOW); self.play(Indicate(angular,color=WARM),Indicate(smooth,color=PRIMARY))
        self.play(Write(footer("Motion is a space-time curve."))); self.wait(LONG)


class Scene18_FITCompressionGate(Scene):
    def construct(self):
        self.camera.background_color = BG
        # FIT inserts before a jammed Transformer, reducing the flood before expensive processing.
        pile=token_grid(6,8,.22,WARM,.025).shift(LEFT*4.8)
        gate=core("Transformer",1.4,3.0,WARM).shift(RIGHT*2.2)
        self.play(LaggedStart(*[FadeIn(t) for t in pile],lag_ratio=.01),GrowFromCenter(gate)); self.wait(BEAT)
        jam=VGroup(*[Square(.2,color=WARM,fill_color=WARM,fill_opacity=.4)
                     for _ in range(10)]).arrange_in_grid(5,2,buff=.02).next_to(gate,LEFT,buff=.03)
        self.play(pile.animate.next_to(jam,LEFT,buff=.04),FadeIn(jam),Indicate(gate,color=WARM),run_time=SLOW); self.wait(BEAT)
        self.play(pile.animate.shift(LEFT*3),run_time=NORMAL)
        fit=core("FIT\ncompress",1.9,1.4,ACCENT).shift(LEFT*.4)
        into_fit=Arrow(pile.get_right(),fit.get_left(),color=ACCENT,buff=.08,stroke_width=4)
        self.play(GrowFromCenter(fit),GrowArrow(into_fit),run_time=SLOW); self.wait(BEAT)
        few=token_grid(2,3,.3,ACCENT,.06).next_to(fit,RIGHT,buff=.32)
        self.play(FadeOut(into_fit,jam),ReplacementTransform(pile,few),
                  gate[0].animate.set_stroke(PRIMARY).set_fill(PRIMARY,opacity=.12),run_time=SLOW); self.wait(BEAT)
        prompt=core("prompt",1.25,.5,WHITE_ISH).next_to(few,UP,buff=.12)
        rider=VGroup(few,prompt)
        through=Arrow(few.get_right(),gate.get_right()+RIGHT*.4,buff=0,color=PRIMARY,stroke_width=4)
        self.play(FadeIn(prompt),GrowArrow(through)); self.wait(BEAT)
        self.play(MoveAlongPath(rider,through),run_time=SLOW); self.wait(BEAT)
        self.play(Indicate(gate,color=PRIMARY)); self.wait(BEAT)
        decompress=core("decompress",1.5,1.0,ACCENT).shift(RIGHT*3.8)
        processed=few.copy().move_to(gate.get_right()+RIGHT*.5)
        self.play(FadeOut(through,prompt),ReplacementTransform(few,processed),
                  GrowFromCenter(decompress),run_time=SLOW); self.wait(BEAT)
        output=video_cube(1.0,.68,SECONDARY).shift(RIGHT*5.35)
        self.play(ReplacementTransform(processed,output),run_time=SLOW)
        self.play(Write(footer("Compress before expensive attention."))); self.wait(LONG)


class Scene19_ErrorScannerBaselineVsSnap(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same scanner drops many red markers on baseline and almost none on Snap.
        divider=DashedLine(UP*2.7,DOWN*2.7,color=MUTED)
        clean=photo_box(os.path.join(A23,"dinosaur.jpg"),4.5,2.8,PRIMARY)
        baseline=photo_box(os.path.join(A23,"dinosaur.jpg"),4.5,2.8,MUTED,.68)
        baseline[1].stretch(1.22,0).rotate(.05).shift(RIGHT*.12)
        flicker=Rectangle(width=4.1,height=2.35,stroke_width=0,fill_color=WARM,fill_opacity=.12).move_to(baseline)
        clips=Group(Group(baseline,flicker),clean).arrange(RIGHT,buff=1.0).shift(UP*.4)
        scanners=VGroup(*[Line(c.get_top(),c.get_bottom(),color=ACCENT,stroke_width=5).align_to(c,LEFT) for c in clips])
        self.play(Create(divider),FadeIn(clips),Create(scanners)); self.wait(BEAT)
        self.play(scanners[0].animate.align_to(clips[0],RIGHT),run_time=SLOW)
        many=VGroup(*[txt("×",WARM,30).move_to(clips[0]).shift(v) for v in [LEFT+UP*.6,RIGHT*.5+UP,LEFT*.4+DOWN*.6,RIGHT+DOWN*.4]])
        self.play(LaggedStart(*[GrowFromCenter(x) for x in many],lag_ratio=.15)); self.wait(BEAT)
        self.play(scanners[1].animate.align_to(clips[1],RIGHT),run_time=SLOW)
        few=txt("×",WARM,26).move_to(clips[1]).shift(RIGHT*.7+DOWN*.4)
        self.play(GrowFromCenter(few)); self.play(Indicate(many,color=WARM),Indicate(few,color=ACCENT))
        self.play(Write(footer("Better video = fewer errors across time."))); self.wait(LONG)


class Scene20_SoraSpaceTimePatches(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The recurring cube is sliced into time-bearing blocks and aligned with a text sentence.
        cube=video_cube(3.5,2.2,PRIMARY)
        self.play(Create(cube)); self.wait(BEAT)
        blocks=token_grid(3,5,.42,ACCENT,.1).move_to(cube)
        self.play(FadeOut(cube),FadeIn(blocks),run_time=SLOW); self.wait(BEAT)
        row=blocks.copy().arrange(RIGHT,buff=.1).scale(.72).shift(DOWN*.8)
        self.play(ReplacementTransform(blocks,row),run_time=SLOW); self.wait(BEAT)
        words=VGroup(*[core(w,1.0,.45,WHITE_ISH) for w in ["word","word","word","word","word"]]).arrange(RIGHT,buff=.14).shift(UP*.8)
        arrows=VGroup(*[Arrow(a.get_right(),b.get_left(),buff=.05,color=WHITE_ISH,stroke_width=2) for a,b in zip(words[:-1],words[1:])])
        self.play(LaggedStart(*[FadeIn(w) for w in words],lag_ratio=.1),Create(arrows))
        self.play(Write(footer("Sora reads video as space-time tokens."))); self.wait(LONG)


class Scene21_StatusLedgerBesideTheScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        # A separate status ledger stays readable while one scene element glitches in sync.
        names=["woman","Tokyo street","neon","red dress","wet road","pedestrians","camera style"]
        rows=VGroup()
        for n in names:
            tag=box(2.1,.48,ACCENT,ACCENT,.07)
            dot=Dot(radius=.11,color=MUTED).move_to(tag.get_left()+RIGHT*.25)
            label=txt(n,WHITE_ISH,15).move_to(tag).shift(RIGHT*.2)
            rows.add(VGroup(tag,dot,label))
        rows.arrange(DOWN,buff=.12).shift(LEFT*4.7+UP*.25)
        scene=photo_box(os.path.join(A23,"tokyo.jpg"),7.3,4.8,SECONDARY).shift(RIGHT*2)
        self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=.06),FadeIn(scene)); self.wait(BEAT)
        self.play(LaggedStart(*[r[1].animate.set_color(SECONDARY) for r in rows],lag_ratio=.12),run_time=SLOW); self.wait(BEAT)
        glitch=Rectangle(width=.7,height=1.3,color=WARM,fill_color=WARM,fill_opacity=.35).move_to(scene).shift(RIGHT*1.6+DOWN*.2)
        self.play(rows[5][1].animate.set_color(WARM),FadeIn(glitch),run_time=NORMAL); self.wait(BEAT)
        self.play(rows[5][1].animate.set_color(SECONDARY),FadeOut(glitch),run_time=NORMAL)
        self.play(Write(footer("Prompt following must persist over time."))); self.wait(LONG)


class Scene22_SoraScalingThreeMeters(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same target improves while three explicit quality meters rise together.
        panels=Group(photo_box(os.path.join(A22,"dog_grass_pixelated.png"),2.7,1.7,WARM,.35),
                     photo_box(os.path.join(A22,"dog_grass_pixelated.png"),2.7,1.7,SECONDARY,.7),
                     photo_box(os.path.join(A22,"dog_grass.png"),2.7,1.7,ACCENT)).arrange(RIGHT,buff=.65).shift(UP*.9)
        self.play(LaggedStart(*[FadeIn(p) for p in panels],lag_ratio=.2)); self.wait(BEAT)
        groups=VGroup()
        for p,level,color in zip(panels,[.2,.55,.95],[WARM,SECONDARY,ACCENT]):
            groups.add(VGroup(meter("detail",level,color),meter("structure",level,color),meter("stability",level,color)).arrange(RIGHT,buff=.15).next_to(p,DOWN,buff=.3))
        self.play(LaggedStart(*[FadeIn(g) for g in groups],lag_ratio=.2)); self.wait(BEAT)
        self.play(Indicate(groups,color=ACCENT),Write(footer("Scaling improves structure, detail, and motion."))); self.wait(LONG)


class Scene23_RealismVsPhysicsSplit(Scene):
    def construct(self):
        self.camera.background_color = BG
        # The same cinematic composite earns a realism pass and multiple physics failures.
        divider=DashedLine(UP*2.8,DOWN*2.8,color=MUTED)
        left=box(5.3,3.5,SECONDARY,SECONDARY,.06).shift(LEFT*3.3+UP*.25)
        sand=VGroup(*[Dot(left.get_center()+np.array([x,y,0]),radius=.035,color=ACCENT) for x,y in zip(np.linspace(-2.2,2.2,24),-.8+.08*np.sin(np.linspace(0,8,24)))])
        chair=drawn_chair(ACCENT,.7).move_to(left).shift(RIGHT*.55+DOWN*.35)
        tool=Line(left.get_left()+RIGHT*.5+UP*.8,chair.get_center()+LEFT*.3,color=WHITE_ISH,stroke_width=6)
        self.play(Create(divider),Create(left),FadeIn(sand),Create(chair),Create(tool)); self.wait(BEAT)
        pass_mark=txt("VISUAL REALISM: HIGH ✓",SECONDARY,15).next_to(left,DOWN,buff=.25)
        self.play(GrowFromCenter(pass_mark)); self.wait(BEAT)
        right=left.copy().shift(RIGHT*6.6); right_sand=sand.copy().shift(RIGHT*6.6); right_chair=chair.copy().stretch(1.25,0).shift(RIGHT*6.6); right_tool=tool.copy().shift(RIGHT*6.6+RIGHT*.35)
        faults=VGroup(*[Circle(.25,color=WARM,stroke_width=4).move_to(right).shift(v) for v in [LEFT+DOWN*.7,DOWN*.4,RIGHT*.7+DOWN*.25,LEFT*.9+UP*.8,RIGHT+UP*.7]])
        self.play(Create(right),FadeIn(right_sand),Create(right_chair),Create(right_tool),LaggedStart(*[Create(f) for f in faults],lag_ratio=.12),run_time=SLOW)
        score=txt("WORLD UNDERSTANDING: INCOMPLETE",WARM,13).next_to(right,DOWN,buff=.25)
        self.play(Write(score),Write(footer("Looks real. Not always physically correct."))); self.wait(LONG)


class Scene24_UniversalTokenizerMachine(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Four incompatible shapes pass through separate doors and emerge as one visual language.
        inputs=VGroup(txt("A",WHITE_ISH,28),Square(.5,color=SECONDARY),video_cube(.75,.5,PRIMARY),VGroup(*[Line(ORIGIN,UP*h,color=PRIMARY) for h in [.2,.5,.8,.35]]).arrange(RIGHT,buff=.05)).arrange(DOWN,buff=.55).shift(LEFT*5)
        machine=box(3.0,5.2,ACCENT,ACCENT,.06).shift(LEFT*1.8)
        doors=VGroup(*[core(n,1.4,.62,MUTED) for n in ["Text tokenizer","Image tokenizer","Video tokenizer","Audio tokenizer"]]).arrange(DOWN,buff=.42).move_to(machine)
        self.play(LaggedStart(*[FadeIn(i) for i in inputs],lag_ratio=.12),Create(machine),LaggedStart(*[FadeIn(d) for d in doors],lag_ratio=.1)); self.wait(BEAT)
        self.play(Indicate(inputs,color=WARM)); self.wait(BEAT)
        uniform=VGroup(*[token_grid(1,4,.2,ACCENT,.04) for _ in range(4)]).arrange(DOWN,buff=.55).shift(RIGHT*1.2)
        model=core("one autoregressive model",2.5,1.5,PRIMARY).shift(RIGHT*4.7)
        self.play(inputs.animate.move_to(doors).set_opacity(0),LaggedStart(*[FadeIn(u,shift=RIGHT*.2) for u in uniform],lag_ratio=.1),run_time=SLOW)
        self.play(GrowFromCenter(model),uniform.animate.move_to(model),run_time=SLOW)
        self.play(Write(footer("Make every modality speak token language."))); self.wait(LONG)


class Scene25_NextTokenPrediction(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Known multimodal context repeatedly fills the next blank until a video sequence exists.
        colors=[WHITE_ISH,PRIMARY,PRIMARY,ACCENT,PRIMARY]
        labels=["text","vid","vid","aud","vid"]
        tokens=VGroup(*[core(l,.9,.65,c) for l,c in zip(labels,colors)]).arrange(RIGHT,buff=.18).shift(LEFT*1+UP*.6)
        blank=box(.9,.65,MUTED).next_to(tokens,RIGHT,buff=.18)
        self.play(LaggedStart(*[FadeIn(t) for t in tokens],lag_ratio=.1),Create(blank)); self.wait(BEAT)
        bracket=Brace(tokens,UP,color=ACCENT); arrow=Arrow(bracket.get_right()+UP*.15,blank.get_top(),color=ACCENT,buff=.08)
        self.play(Create(bracket),GrowArrow(arrow)); self.wait(BEAT)
        predicted=core("vid",.9,.65,PRIMARY).move_to(blank)
        self.play(GrowFromCenter(predicted),FadeOut(blank)); self.wait(BEAT)
        extras=VGroup(*[core("vid",.9,.65,PRIMARY) for _ in range(3)]).arrange(RIGHT,buff=.18).next_to(predicted,RIGHT,buff=.18)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in extras],lag_ratio=.3),run_time=SLOW)
        video=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(5)],1.0,.68,PRIMARY).shift(DOWN*1.6)
        self.play(FadeIn(video),Write(footer("Video generation as next-token prediction."))); self.wait(LONG)


class Scene26_FourRepairToolsOnePatient(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Four distinct operations work on one flickering patient, reducing disagreement after each pass.
        patient=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(5)],1.1,.75,WARM,.55)
        patient[1].rotate(.08); patient[3].stretch(1.12,1)
        self.play(FadeIn(patient)); self.wait(BEAT)
        labels=VGroup(*[txt(n,WHITE_ISH,18) for n in ["Latent-Shift","VideoFactory","PYoCo","VideoFusion"]]).arrange(RIGHT,buff=.65).shift(UP*2.5)
        self.play(LaggedStart(*[FadeIn(l) for l in labels],lag_ratio=.15))
        baton=Dot(patient[0].get_center(),radius=.1,color=PRIMARY)
        self.play(baton.animate.move_to(patient[2]),Indicate(labels[0],color=ACCENT),run_time=SLOW)
        bridges=attention_links(patient,PRIMARY,True)
        self.play(LaggedStart(*[Create(b) for b in bridges],lag_ratio=.1),Indicate(labels[1],color=ACCENT))
        grains=VGroup(*[Dot(f.get_center(),radius=.05,color=ACCENT) for f in patient])
        self.play(LaggedStart(*[GrowFromCenter(g) for g in grains],lag_ratio=.1),Indicate(labels[2],color=ACCENT)); self.wait(BEAT)
        base=Rectangle(width=patient.width,height=.18,color=SECONDARY,fill_color=SECONDARY,fill_opacity=.35).next_to(patient,DOWN,buff=.65)
        residuals=VGroup(*[Dot(base.get_center()+RIGHT*x,radius=.04,color=WARM) for x in np.linspace(-2,2,5)])
        self.play(GrowFromCenter(base),FadeIn(residuals),residuals.animate.scale(.2).set_opacity(.2),Indicate(labels[3],color=ACCENT))
        clean_patient=filmstrip([os.path.join(A22,f"dog_{i}.jpg") for i in range(5)],1.1,.75,PRIMARY).move_to(patient)
        self.play(FadeOut(patient),FadeIn(clean_patient),Write(footer("Different tools, same goal: reduce flicker."))); self.wait(LONG)


class Scene27_GlassWorldMustRememberItself(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        # The final glass world remembers its look and prompt, then cracks when tested for physics.
        names=["single image","many frames","space-time volume","tokens","scaled Transformers","moving mini-world"]
        steps=VGroup()
        for i,n in enumerate(names):
            r=box(1.5+i*.5,.42,ACCENT if i==5 else MUTED,ACCENT,.04)
            r.shift(LEFT*4.7+RIGHT*i*.9+DOWN*2.5+UP*i*.75)
            steps.add(VGroup(r,txt(n,WHITE_ISH,8).move_to(r)))
        self.play(LaggedStart(*[GrowFromEdge(s[0],DOWN) for s in steps],*[FadeIn(s[1]) for s in steps],lag_ratio=.05),run_time=SLOW); self.wait(BEAT)
        labs=VGroup(*[txt(n,ACCENT,10) for n in ["Lumiere","DiT","GenTron","W.A.L.T","Snap","Sora","VideoPoet"]]).arrange(DOWN,buff=.12).shift(RIGHT*5+DOWN*.2)
        self.play(LaggedStart(*[FadeIn(l,shift=LEFT*.1) for l in labs],lag_ratio=.08)); self.wait(BEAT)
        glass=video_cube(1.5,1.0,ACCENT).move_to(steps[-1]).shift(UP*.9)
        hand=VGroup(Arc(radius=1.0,start_angle=.1,angle=.8*PI,color=WHITE_ISH,stroke_width=5),
                    *[Line(ORIGIN,rotate_vector(RIGHT*(.65+.07*i),.25+i*.2),color=WHITE_ISH,stroke_width=4) for i in range(4)]).move_to(glass).shift(DOWN*.85)
        self.play(Create(glass),Create(hand)); self.wait(BEAT)
        tests=VGroup(txt("Consistency ✓",SECONDARY,13),txt("Prompt ✓",SECONDARY,13),txt("Physics",WARM,13)).arrange(DOWN,buff=.18).next_to(glass,RIGHT,buff=.8)
        self.play(FadeOut(steps,labs),self.camera.frame.animate.move_to(glass).scale(.62),FadeIn(tests[0])); self.wait(BEAT)
        self.play(FadeIn(tests[1])); self.wait(BEAT)
        cracks=VGroup(*[Line(glass.get_center(),glass.get_center()+rotate_vector(RIGHT*.7,a),color=WARM,stroke_width=2) for a in [.2,1.5,3.0,4.6]])
        self.play(FadeIn(tests[2]),Create(cracks),run_time=SLOW)
        final=VGroup(txt("A video model can make a world appear.",WHITE_ISH,9),
                     txt("The next challenge is making that world understand itself.",ACCENT,9)).arrange(DOWN,buff=.1,aligned_edge=LEFT).next_to(glass,DOWN,buff=.85)
        self.play(Write(final[0])); self.wait(BEAT); self.play(Write(final[1])); self.wait(LONG+1)
