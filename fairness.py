# === PRODUCTION PLAN ===
# Core insight (one sentence): Generative models can reproduce and amplify
# social bias, while Diversity Fine-Tuning broadens concepts from inside the
# model instead of only patching prompts at inference time.
#
# Color encoding:
#   PRIMARY   = DFT mechanism / solution process
#   SECONDARY = fairness achieved / diverse output / success
#   WARM      = bias / stereotypes / amplified imbalance / failure
#   ACCENT    = quantitative metrics / thresholds / measurement
#   MUTED     = baseline model / neutral prompt / inactive background
#
# Scene list:
#   Scene01_EvaluationWheel — evaluation wheel zooms into Fairness
#   Scene02_StereotypicalBiases — two-floor job building: narrow vs diverse
#   Scene03_WorseThanReality — distorted mirror shrinks 34% into 3%
#   Scene04_PromptQualifiers — backend sticky note fails to rewrite habit
#   Scene05_DFT_CoreIdea — CEO node expands from one avatar to a gallery
#   Scene06_SyntheticImages — seven prompt reels make synthetic examples
#   Scene07_PromptParaphrasing — rigid tags become a natural caption
#   Scene08_FineTuning — diverse study material changes neutral exam answers
#   Scene09_DisparateImpact — tilted balance scale and 0.8 threshold
#   Scene10_QuantitativeResults — bars grow toward the fairness line
#   Scene11_QualitativeResults — narrow lens versus wide lens
#   Scene12_QualityRealism — fairness moves right while quality stays high
#   Scene13_FairnessSummary — fairness bandage moves to pre-training
#
# Key transforms (moments where one thing morphs INTO another):
#   - Scene05: one CEO edge -> six diverse CEO concept edges
#   - Scene13: fairness patch at prompt editing -> fairness built into pre-training
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

SKIN_LIGHT = "#F5D5B8"
SKIN_MEDIUM = "#C68642"
SKIN_DARK = "#8D5524"
HAIR = "#4A3728"

FAST = 0.4
NORMAL = 0.8
SLOW = 1.5
BEAT = 1.2
LONG = 2.5

ROOT = os.path.dirname(__file__)
A41 = os.path.join(ROOT, "images", "4.1")


def T(text, size=18, color=WHITE_ISH, max_width=11.5):
    mob = Text(text, font_size=size, color=color)
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def box(width, height, color=MUTED, fill=None, opacity=0.07, radius=0.1, stroke=2):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=radius,
        stroke_color=color,
        stroke_width=stroke,
        fill_color=fill or color,
        fill_opacity=opacity,
    )


def image_panel(filename, width, height, color=SECONDARY, opacity=0.04):
    frame = box(width, height, color, BG, opacity, 0.1, 2)
    picture = ImageMobject(os.path.join(A41, filename))
    picture.scale_to_fit_width(width - 0.12)
    if picture.height > height - 0.12:
        picture.scale_to_fit_height(height - 0.12)
    picture.move_to(frame)
    return Group(frame, picture)


def avatar(skin=SKIN_LIGHT, radius=0.24, hair_angle=20, hair_color=HAIR, body=False):
    face = Circle(radius=radius, stroke_width=1.5, stroke_color=WHITE_ISH,
                  fill_color=skin, fill_opacity=0.92)
    hair = Arc(
        radius=radius * 0.98,
        start_angle=hair_angle * DEGREES,
        angle=140 * DEGREES,
        color=hair_color,
        stroke_width=2.4,
    ).move_to(face)
    eye_l = Dot(face.get_center() + LEFT * radius * 0.32 + UP * radius * 0.08,
                radius=radius * 0.045, color=BG)
    eye_r = Dot(face.get_center() + RIGHT * radius * 0.32 + UP * radius * 0.08,
                radius=radius * 0.045, color=BG)
    mob = VGroup(face, hair, eye_l, eye_r)
    if body:
        shoulders = Arc(radius=radius * 1.1, start_angle=25 * DEGREES,
                        angle=130 * DEGREES, color=skin, stroke_width=2).shift(DOWN * radius * 1.15)
        mob.add(shoulders)
    return mob


def job_card(job, color, skin, identical=True):
    shell = box(1.18, 1.35, color, BG, 0.07, 0.08, 1.6)
    av = avatar(skin, 0.22, 20 if identical else (hash(job) % 90 - 25)).move_to(shell.get_center() + UP * 0.16)
    label = T(job, 7.2, MUTED, 1.0).next_to(av, DOWN, buff=0.18)
    return VGroup(shell, av, label)


def mini_image_card(skin, color=SECONDARY, w=1.15, h=1.25):
    shell = box(w, h, color, BG, 0.08, 0.08, 1.5)
    av = avatar(skin, 0.24, hash(str(skin)) % 90 - 20, body=True).move_to(shell)
    return VGroup(shell, av)


def bar(x, base_y, width, height, color):
    r = Rectangle(width=width, height=max(height, 0.025), stroke_width=0,
                  fill_color=color, fill_opacity=0.85)
    r.move_to([x, base_y + max(height, 0.025) / 2, 0])
    return r


def arrow_between(start, end, color=MUTED, width=2.5):
    return Arrow(start, end, buff=0.08, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.13)


class Scene01_EvaluationWheel(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: evaluation is a wheel of criteria; the camera of attention narrows onto fairness.
        labels = ["Aesthetics", "Photo Realism", "Quality", "Originality", "Alignment", "Fairness", "Toxicity"]
        center = np.array([0, 0.35, 0])
        sectors = VGroup()
        texts = VGroup()
        step = TAU / 7
        for i, label in enumerate(labels):
            is_fair = label == "Fairness"
            start = i * step - step / 2
            sector = AnnularSector(
                inner_radius=0.9, outer_radius=2.7, angle=step * 0.96, start_angle=start,
                fill_color=PRIMARY if is_fair else MUTED,
                fill_opacity=0.40 if is_fair else 0.25,
                stroke_color=PRIMARY if is_fair else MUTED,
                stroke_width=2 if is_fair else 1,
            ).move_arc_center_to(center)
            sectors.add(sector)
            mid = start + step * 0.48
            txt = T(label, 13 if is_fair else 10.5, PRIMARY if is_fair else WHITE_ISH, 1.7)
            txt.move_to(center + 2.08 * np.array([np.cos(mid), np.sin(mid), 0]))
            texts.add(txt)
        cap = Circle(radius=0.9, fill_color=BG, fill_opacity=1, stroke_width=0).move_to(center)
        cap_text = T("Evaluation\nDimensions", 10, MUTED).move_to(center)
        headline = T("Fairness: a new evaluation dimension", 19, PRIMARY).move_to([0, -2.8, 0])

        self.play(LaggedStart(*[GrowFromCenter(s) for s in sectors], lag_ratio=0.1), run_time=SLOW)
        self.play(FadeIn(cap), Write(cap_text)); self.wait(BEAT)
        self.play(LaggedStart(*[Write(t) for t in texts], lag_ratio=0.08)); self.wait(BEAT)
        self.play(*[s.animate.set_fill(opacity=0.07) for i, s in enumerate(sectors) if labels[i] != "Fairness"])
        self.wait(BEAT)
        self.play(Indicate(sectors[5], color=PRIMARY, scale_factor=1.06)); self.wait(BEAT)
        self.play(Write(headline)); self.wait(LONG)


class Scene02_StereotypicalBiases(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the top floor of status contains repeated faces; the lower floor contains broader variation.
        top_header = T("High-paying occupations", 14, WARM).move_to([-2.0, 3.1, 0])
        bot_header = T("Low-paying occupations", 14, SECONDARY).move_to([-2.0, -0.42, 0])
        top_jobs = ["Architect", "Lawyer", "Politician", "Doctor", "CEO", "Judge", "Engineer"]
        bot_jobs = ["Janitor", "Dishwasher", "Fast-food", "Cashier", "Teacher", "Social", "Housekeep"]
        xs = [-5.25, -3.65, -2.05, -0.45, 1.15, 2.75, 4.35]
        top_cards = VGroup(*[job_card(j, WARM, SKIN_LIGHT, True).move_to([x, 1.55, 0]) for j, x in zip(top_jobs, xs)])
        skins = [SKIN_LIGHT, SKIN_MEDIUM, SKIN_DARK, SKIN_MEDIUM, SKIN_LIGHT, SKIN_DARK, SKIN_MEDIUM]
        bot_cards = VGroup(*[job_card(j, SECONDARY, sk, False).move_to([x, -1.75, 0]) for j, x, sk in zip(bot_jobs, xs, skins)])
        divider = Line([-6.2, 0, 0], [6.2, 0, 0], color=WARM, stroke_width=2.5)
        scanner = Rectangle(width=12.8, height=0.06, stroke_width=0, fill_color=ACCENT, fill_opacity=0.7).move_to([-12, 1.55, 0])
        similar = T("All look similar.", 12, WARM).move_to([4.1, 2.85, 0])
        line1 = T("The model is not just generating jobs.", 16, WARM).move_to([0, -2.85, 0])
        line2 = T("It is generating social stereotypes.", 16, WARM).move_to([0, -3.32, 0])

        self.play(Write(top_header), LaggedStart(*[GrowFromCenter(c[0]) for c in top_cards], lag_ratio=0.07))
        self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(VGroup(c[1], c[2])) for c in top_cards], lag_ratio=0.07)); self.wait(BEAT)
        self.play(Write(similar)); self.wait(BEAT)
        self.play(Create(divider)); self.wait(BEAT)
        self.play(Write(bot_header), LaggedStart(*[GrowFromCenter(c[0]) for c in bot_cards], lag_ratio=0.07))
        self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(VGroup(c[1], c[2])) for c in bot_cards], lag_ratio=0.07)); self.wait(BEAT)
        self.add(scanner)
        self.play(scanner.animate.move_to([12, 1.55, 0]), run_time=SLOW); self.wait(BEAT)
        self.play(Write(line1)); self.wait(BEAT)
        self.play(Write(line2)); self.wait(LONG)


class Scene03_WorseThanReality(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: a warped mirror takes an unequal reality bar and squeezes it into a much smaller model-output bar.
        left_title = T("Reality", 22, SECONDARY).move_to([-3.55, 2.35, 0])
        right_title = T("Generated", 22, WARM).move_to([3.55, 2.35, 0])
        left_container = Rectangle(width=4.4, height=0.62, stroke_color=MUTED, stroke_width=1.5).move_to([-3.55, 0.9, 0])
        right_container = Rectangle(width=4.4, height=0.62, stroke_color=MUTED, stroke_width=1.5).move_to([3.55, 0.9, 0])
        real_bar = bar(-5.75 + 4.4 * 0.34 / 2, 0.59, 4.4 * 0.34, 0.62, SECONDARY)
        gen_bar = bar(1.35 + 4.4 * 0.03 / 2, 0.59, 4.4 * 0.03, 0.62, WARM)
        real_label = T("34% women judges", 18, SECONDARY).move_to([-3.55, 1.62, 0])
        gen_label = T("3% women judges", 18, WARM).move_to([3.55, 1.62, 0])
        mirror_frame = box(0.5, 2.8, ACCENT, BG, 0, 0.1, 2).move_to([0, 0.65, 0])
        wave = ParametricFunction(lambda t: np.array([0.12 * np.sin(6 * t), t, 0]),
                                  t_range=[-0.65, 1.9], color=ACCENT, stroke_width=2.2)
        wave.move_to(mirror_frame)
        curve = CurvedArrow([-1.45, 0.9, 0], [1.45, 0.9, 0], angle=0.55, color=WARM, stroke_width=3)
        title = T("Bias amplification.", 28, WARM).move_to([0, -1.95, 0])
        sub = T("The model amplifies what is already unequal.", 18, WHITE_ISH).move_to([0, -2.65, 0])

        self.play(Write(left_title), Create(left_container)); self.play(GrowFromEdge(real_bar, LEFT), Write(real_label)); self.wait(BEAT)
        self.play(FadeIn(mirror_frame), Create(wave)); self.wait(BEAT)
        self.play(Write(right_title), Create(right_container)); self.wait(BEAT)
        self.play(Create(curve)); self.wait(BEAT)
        self.play(GrowFromEdge(gen_bar, LEFT), Write(gen_label)); self.wait(BEAT)
        self.play(Write(title)); self.play(FadeIn(sub)); self.wait(LONG)


class Scene04_PromptQualifiers(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: a sticky note rides on the prompt, while the machine's internal habit remains underneath.
        prompt = VGroup(box(3.35, 0.72, MUTED, BG, 0.07), T('"photo of a CEO"', 19)).move_to([-4.25, 1.35, 0])
        sticky = VGroup(box(1.35, 0.48, ACCENT, ACCENT, 0.92, 0.06, 1.2),
                        T('"female"', 15, BG)).rotate(6 * DEGREES).move_to([-4.0, 1.85, 0])
        backend = VGroup(
            Circle(0.16, fill_color=ACCENT, fill_opacity=1, stroke_width=0),
            Line([-0.18, -0.18, 0], [0.18, -0.18, 0], color=ACCENT, stroke_width=2),
            T("backend adds note", 14, ACCENT).shift(DOWN * 0.45),
        ).move_to([-4.25, 2.55, 0])
        modified = VGroup(box(2.45, 0.55, ACCENT, BG, 0.08, 0.07, 1.4),
                          T('CEO + "female"', 14, ACCENT)).move_to([-1.05, 1.35, 0])
        machine = VGroup(box(3.05, 2.25, PRIMARY, BG, 0.08, 0.18, 2.2).move_to([1.65, 0.9, 0]),
                         T("T2I model", 20, PRIMARY).move_to([1.65, 1.7, 0]))
        habit = VGroup(
            T("learned habit", 16, WARM),
            VGroup(*[avatar(SKIN_LIGHT, 0.19, 20).move_to([0.95 + i * 0.58, 0.55, 0]) for i in range(3)]),
            Line([0.1, 0.1, 0], [3.1, 0.1, 0], color=WARM, stroke_width=2),
        ).arrange(DOWN, buff=0.2).move_to([1.65, 0.48, 0])
        machine.add(habit)
        output = VGroup(box(2.35, 1.08, WARM, BG, 0.07, 0.1, 2).move_to([4.75, 0.9, 0]),
                        avatar(SKIN_LIGHT, 0.24).move_to([4.75, 1.08, 0]),
                        T("same old default", 14, WARM).move_to([4.75, 0.47, 0]))
        arrow1 = arrow_between([-2.55, 1.35, 0], [-2.3, 1.35, 0], ACCENT, 3)
        arrow2 = arrow_between([0.25, 1.35, 0], [0.22, 1.22, 0], ACCENT, 3)
        arrow3 = arrow_between([3.15, 0.9, 0], [3.55, 0.9, 0], WARM, 3)
        bottom1 = T("Prompt editing changes the request,", 22).move_to([0, -2.35, 0])
        bottom2 = T("not the model's internal concept.", 22, WARM).move_to([0, -2.9, 0])

        self.play(GrowFromCenter(prompt[0]), Write(prompt[1])); self.wait(BEAT)
        self.play(FadeIn(backend), FadeIn(sticky, shift=DOWN * 0.25)); self.wait(BEAT)
        self.play(Create(arrow1), ReplacementTransform(VGroup(prompt.copy(), sticky.copy()), modified)); self.wait(BEAT)
        self.play(GrowFromCenter(machine[0]), Write(machine[1]), FadeIn(habit)); self.wait(BEAT)
        self.play(Create(arrow2), modified.animate.move_to([0.35, 1.28, 0]).scale(0.62).set_opacity(0.0)); self.wait(BEAT)
        self.play(Create(arrow3), GrowFromCenter(output)); self.wait(BEAT)
        self.play(Write(bottom1)); self.play(Write(bottom2)); self.wait(LONG)


class Scene05_DFT_CoreIdea(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the dictionary entry for CEO grows from one prototype to a web of examples.
        ceo = VGroup(Circle(0.38, fill_color=PRIMARY, fill_opacity=0.9, stroke_width=0), T("CEO", 16)).move_to([0, 0.6, 0])
        single_line = Line([0.38, 0.6, 0], [2.15, 0.6, 0], color=MUTED, stroke_width=2)
        single = avatar(SKIN_LIGHT, 0.3).move_to([2.6, 0.6, 0])
        narrow = T("narrow concept", 10, MUTED).move_to([2.6, 0.05, 0])
        train = arrow_between([-4, 0.6, 0], [-0.48, 0.6, 0], ACCENT, 2.6)
        train_text = T("DFT training", 11, ACCENT).move_to([-2.2, 1.0, 0])
        positions = [[2.2, 0.6, 0], [1.1, 2.45, 0], [-1.1, 2.45, 0], [-2.2, 0.6, 0], [-1.1, -1.25, 0], [1.1, -1.25, 0]]
        skins = [SKIN_LIGHT, SKIN_MEDIUM, SKIN_DARK, SKIN_LIGHT, SKIN_MEDIUM, SKIN_DARK]
        colors = [PRIMARY, SECONDARY, ACCENT, PRIMARY, SECONDARY, ACCENT]
        lines = VGroup(*[Line(ceo.get_center(), p, color=c, stroke_width=2) for p, c in zip(positions, colors)])
        avs = VGroup(*[avatar(sk, 0.27, i * 22 - 30).move_to(p) for i, (sk, p) in enumerate(zip(skins, positions))])
        broad = T("broader concept", 10, SECONDARY).move_to([2.35, -0.05, 0])
        cmp1 = T('Prompt editing: "Please imagine a different CEO."', 12, MUTED).move_to([0, -2.55, 0])
        cmp2 = T('DFT: "Rebuild what CEO means inside the model."', 13, SECONDARY).move_to([0, -3.05, 0])

        self.play(GrowFromCenter(ceo[0]), Write(ceo[1])); self.wait(BEAT)
        self.play(Create(single_line), FadeIn(single), Write(narrow)); self.wait(BEAT)
        self.play(Create(train), Write(train_text)); self.wait(BEAT)
        self.play(FadeOut(train), FadeOut(train_text),
                  ReplacementTransform(single_line, lines[0]), FadeOut(single), FadeOut(narrow),
                  LaggedStart(*[Create(l) for l in lines[1:]], lag_ratio=0.12)); self.wait(BEAT)
        self.play(LaggedStart(*[GrowFromCenter(a) for a in avs], lag_ratio=0.1)); self.wait(BEAT)
        self.play(Write(broad)); self.wait(BEAT)
        self.play(FadeIn(cmp1), FadeIn(cmp2)); self.wait(LONG)


class Scene06_SyntheticImages(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: a slot machine systematically explores identity and context instead of sampling one vague prompt.
        headers = ["shot\ntype", "age", "ethnicity", "gender", "job", "clothes", "place"]
        values = [["close-up", "portrait", "full body"], ["older", "young", "adult"], ["Italian", "Liberian", "Russian"],
                  ["man", "woman", "man"], ["doctor", "teacher", "CEO"], ["suit", "color\ndress", "ethnic"], ["office", "classroom", "market"]]
        xs = [-5.1, -3.4, -1.7, 0.0, 1.7, 3.4, 5.1]
        reels = VGroup()
        selected = VGroup()
        for h, vals, x in zip(headers, values, xs):
            shell = box(1.45, 2.35, ACCENT, BG, 0.07)
            head = T(h, 12.5, MUTED, 1.35).move_to([x, 2.65, 0])
            win = Rectangle(width=1.28, height=0.58, stroke_width=0, fill_color=ACCENT, fill_opacity=0.17).move_to([x, 1.05, 0])
            vals_m = VGroup(*[T(v, 12, WHITE_ISH, 1.18).move_to([x, y, 0]) for v, y in zip(vals, [1.55, 1.05, 0.55])])
            group = VGroup(shell.move_to([x, 1.05, 0]), head, win, vals_m)
            reels.add(group)
            selected.add(vals_m[1].copy())
        sentence_box = box(11.1, 0.78, PRIMARY, BG, 0.08).move_to([0, -0.75, 0])
        sentence = T("A young Liberian woman teacher in a colorful dress, standing in a classroom.", 14, WHITE_ISH, 10.4).move_to(sentence_box)
        t2i = VGroup(box(2.55, 0.85, PRIMARY, BG, 0.1), T("T2I Model", 16, PRIMARY)).move_to([-2.7, -2.15, 0])
        out = image_panel("synthetic_training_collage.png", 3.35, 1.25, SECONDARY).move_to([1.25, -2.25, 0])
        out_label = T("Synthetic image pool", 13, SECONDARY).next_to(out, UP, buff=0.08)
        note = T("~880,000 diverse prompts", 18, ACCENT).move_to([3.95, -2.25, 0])

        self.play(LaggedStart(*[GrowFromCenter(r[0]) for r in reels], lag_ratio=0.08),
                  LaggedStart(*[FadeIn(r[1]) for r in reels], lag_ratio=0.08)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(VGroup(r[2], r[3])) for r in reels], lag_ratio=0.15)); self.wait(BEAT)
        self.play(LaggedStart(*[s.animate.move_to(sentence_box.get_center()) for s in selected], lag_ratio=0.05),
                  GrowFromCenter(sentence_box)); self.play(ReplacementTransform(selected, sentence)); self.wait(BEAT)
        self.play(Create(arrow_between([-1.25, -1.17, 0], [-2.25, -1.72, 0], PRIMARY)), FadeIn(t2i)); self.wait(BEAT)
        self.play(Create(arrow_between([-1.35, -2.15, 0], [-0.55, -2.15, 0], SECONDARY)), GrowFromCenter(out[0]), FadeIn(out[1]), Write(out_label)); self.wait(BEAT)
        self.play(FadeIn(note)); self.wait(LONG)


class Scene07_PromptParaphrasing(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: rigid tags are polished through a language machine into a caption that sounds like training data.
        title_l = T("Rigid template", 13, MUTED).move_to([-4.5, 2.0, 0])
        tag_specs = [("adult", ACCENT), ("Russian", PRIMARY), ("female", SECONDARY),
                     ("assistant", MUTED), ("ethnic clothing", WARM), ("market", MUTED)]
        tags = VGroup()
        for i, (txt, col) in enumerate(tag_specs):
            x = -5.55 + (i % 3) * 1.05
            y = 1.0 if i < 3 else 0.34
            tags.add(VGroup(box(1.0, 0.42, col, col, 0.18 if col != MUTED else 0.12), T(txt, 8.3, WHITE_ISH, 0.9)).move_to([x, y, 0]))
        machine = VGroup(box(2.4, 2.2, PRIMARY, BG, 0.08, 0.15),
                         T("GPT-3.5", 15, PRIMARY).move_to([0, 1.28, 0]),
                         T("Paraphraser", 10, MUTED).move_to([0, 0.95, 0]))
        gear = VGroup(Circle(0.3, color=ACCENT, stroke_width=2),
                      *[Line(ORIGIN, 0.18 * np.array([np.cos(a), np.sin(a), 0]), color=ACCENT, stroke_width=1.5)
                        for a in np.linspace(0, TAU, 8, endpoint=False)]).move_to([0, 0.45, 0])
        machine.add(gear)
        title_r = T("Natural sentence", 13, SECONDARY).move_to([4.2, 2.0, 0])
        bubble = VGroup(box(4.0, 2.4, SECONDARY, BG, 0.08, 0.2),
                        T("An adult Russian woman assistant,\nher ethnic clothing intricately\ndetailed, showcasing beautiful\nhandcrafted jewelry in a vibrant\nmarket.", 9.5, WHITE_ISH, 3.6)).move_to([4.2, 0.7, 0])
        chain = VGroup(arrow_between([4.2, -0.58, 0], [4.2, -1.25, 0], SECONDARY),
                       VGroup(box(1.4, 0.5, PRIMARY, BG, 0.08), T("T2I Model", 8.5, PRIMARY)).move_to([4.2, -1.55, 0]),
                       arrow_between([4.2, -1.82, 0], [4.2, -2.18, 0], SECONDARY),
                       avatar(SKIN_MEDIUM, 0.19).move_to([4.2, -2.42, 0]))
        bottom = T("Prompts sound real, not robotic.", 16, PRIMARY).move_to([0, -3.2, 0])

        self.play(Write(title_l), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in tags], lag_ratio=0.1)); self.wait(BEAT)
        self.play(Create(arrow_between([-3.2, 0.65, 0], [-1.28, 0.7, 0], MUTED)), GrowFromCenter(machine[0]), Write(machine[1]), Write(machine[2])); self.wait(BEAT)
        self.play(Create(gear)); self.play(Rotate(gear, angle=PI), run_time=NORMAL); self.wait(BEAT)
        self.play(Create(arrow_between([1.25, 0.7, 0], [2.15, 0.7, 0], PRIMARY)), Write(title_r), GrowFromCenter(bubble[0]), Write(bubble[1])); self.wait(BEAT)
        self.play(FadeIn(chain)); self.wait(BEAT)
        self.play(Write(bottom)); self.wait(LONG)


class Scene08_FineTuning(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the model studies diverse material before the exam, so the neutral exam question produces diverse answers.
        divider = DashedLine([-6.3, -0.25, 0], [6.3, -0.25, 0], color=MUTED, dash_length=0.14)
        train_title = T("Training phase", 13, ACCENT).move_to([-4.5, 2.8, 0])
        cards = image_panel("synthetic_training_collage.png", 4.55, 1.65, SECONDARY).move_to([-1.75, 1.5, 0])
        model = VGroup(box(1.8, 1.4, WARM, BG, 0.08), T("T2I Model", 11, WARM)).move_to([5.25, 1.5, 0])
        flames = VGroup(*[Triangle(fill_color=WARM, fill_opacity=0.72, stroke_width=0).scale(0.13).move_to([4.85 + i * 0.2, 2.26, 0]) for i in range(3)])
        fire_text = T("fine-tuning", 9, WARM).move_to([5.25, 0.55, 0])
        eval_title = T("Evaluation phase", 13, SECONDARY).move_to([-4.5, -0.62, 0])
        prompt = VGroup(box(2.8, 0.55, MUTED, BG, 0.06), T('"photo of a CEO"', 12)).move_to([-4, -1.42, 0])
        dft = VGroup(box(2.2, 1.2, SECONDARY, BG, 0.1), T("DFT Model", 12, SECONDARY), T("no qualifiers added", 9, MUTED).shift(DOWN * 0.35)).move_to([0, -1.42, 0])
        outs = VGroup(*[avatar(s, 0.19, i * 25 - 25).move_to([3.75 + (i % 3) * 0.48, -1.22 - (i // 3) * 0.45, 0])
                        for i, s in enumerate([SKIN_LIGHT, SKIN_MEDIUM, SKIN_DARK, SKIN_MEDIUM, SKIN_LIGHT, SKIN_DARK])])
        out_label = T("Diverse output", 10, SECONDARY).next_to(outs, DOWN, buff=0.15)
        bottom1 = T("No explicit qualifiers during evaluation.", 14, SECONDARY).move_to([0, -2.9, 0])
        bottom2 = T("Diversity comes from the model, not the prompt.", 13).move_to([0, -3.38, 0])

        self.play(Write(train_title), GrowFromCenter(cards[0]), FadeIn(cards[1], shift=RIGHT * 0.25)); self.wait(BEAT)
        self.play(Create(arrow_between([0.6, 1.5, 0], [4.25, 1.5, 0], ACCENT)), GrowFromCenter(model), FadeIn(flames), Write(fire_text)); self.wait(BEAT)
        self.play(Create(divider), Write(eval_title)); self.wait(BEAT)
        self.play(GrowFromCenter(prompt[0]), Write(prompt[1])); self.wait(BEAT)
        self.play(Create(arrow_between([-2.55, -1.42, 0], [-1.15, -1.42, 0], SECONDARY)), FadeIn(dft)); self.wait(BEAT)
        self.play(Create(arrow_between([1.15, -1.42, 0], [3.35, -1.42, 0], SECONDARY)), LaggedStart(*[GrowFromCenter(o) for o in outs], lag_ratio=0.08), FadeIn(out_label)); self.wait(BEAT)
        self.play(Write(bottom1), Write(bottom2)); self.wait(LONG)


class Scene09_DisparateImpact(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: counting subgroup outputs turns into a DI ratio; a heavy light-skin side makes the scale visibly unbalanced.
        title = T("Disparate Impact compares two subgroup probabilities", 22, WHITE_ISH).move_to([0, 3.0, 0])

        beam = Line([-2.65, 1.15, 0], [2.95, 0.65, 0], color=MUTED, stroke_width=4)
        pivot = Triangle(fill_color=MUTED, fill_opacity=1, stroke_width=0).scale(0.24).rotate(PI).move_to([0.12, 0.48, 0])
        pole = Line([0.12, -0.65, 0], [0.12, 0.48, 0], color=MUTED, stroke_width=3)
        base = Line([-0.42, -0.65, 0], [0.66, -0.65, 0], color=MUTED, stroke_width=3)

        left_chain = DashedLine([-2.65, 1.15, 0], [-2.65, 0.5, 0], color=MUTED, dash_length=0.1)
        right_chain = DashedLine([2.95, 0.65, 0], [2.95, -0.05, 0], color=MUTED, dash_length=0.1)
        left_pan = Arc(radius=0.78, start_angle=200 * DEGREES, angle=140 * DEGREES,
                       color=PRIMARY, stroke_width=3).move_to([-2.65, 0.2, 0])
        right_pan = Arc(radius=0.82, start_angle=200 * DEGREES, angle=140 * DEGREES,
                        color=ACCENT, stroke_width=3).move_to([2.95, -0.35, 0])

        left_dots = VGroup(*[
            Circle(0.16, fill_color=SKIN_MEDIUM, fill_opacity=0.95, stroke_width=0).move_to([-2.84 + i * 0.38, 0.02, 0])
            for i in range(2)
        ]).set_z_index(2)
        right_positions = [[2.58, -0.52, 0], [2.86, -0.58, 0], [3.14, -0.52, 0], [2.72, -0.30, 0], [3.00, -0.28, 0]]
        right_dots = VGroup(*[
            Circle(0.13, fill_color=SKIN_LIGHT, fill_opacity=0.95, stroke_width=0).move_to(p)
            for p in right_positions
        ]).set_z_index(2)
        left_label = T("medium skin", 18, PRIMARY).move_to([-2.65, -0.85, 0])
        right_label = T("light skin", 18, ACCENT).move_to([2.95, -1.15, 0])

        formula = VGroup(
            T("DI =", 22).move_to([-1.0, -2.0, 0]),
            T("P(medium skin)", 16, PRIMARY).move_to([1.0, -1.75, 0]),
            Line([-0.25, -2.0, 0], [2.25, -2.0, 0], color=WHITE_ISH, stroke_width=1.5),
            T("P(light skin)", 16, ACCENT).move_to([1.0, -2.3, 0]),
        )
        threshold = NumberLine(
            x_range=[0, 1, 0.2],
            length=5.0,
            color=MUTED,
            include_numbers=False,
            stroke_width=2,
        ).move_to([0, -3.0, 0])
        mark_08 = Line(threshold.n2p(0.8) + DOWN * 0.16, threshold.n2p(0.8) + UP * 0.16, color=ACCENT, stroke_width=3)
        mark_value = Dot(threshold.n2p(0.02), radius=0.08, color=WARM)
        threshold_label = T("0.8 threshold", 15, ACCENT).next_to(mark_08, UP, buff=0.16)
        value = T("DI = 0.02", 22, WARM).move_to([-2.9, -3.22, 0])
        warn = T("strongly biased", 16, WARM).move_to([3.05, -3.22, 0])

        self.play(Write(title)); self.wait(BEAT)
        self.play(Create(pole), Create(base), FadeIn(pivot), Create(beam)); self.wait(BEAT)
        self.play(Create(left_chain), Create(right_chain), Create(left_pan), Create(right_pan)); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(d) for d in left_dots], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(d) for d in right_dots], lag_ratio=0.08),
                  Write(left_label), Write(right_label)); self.wait(BEAT)
        self.play(Write(formula)); self.wait(BEAT)
        self.play(Create(threshold), Create(mark_08), Write(threshold_label)); self.wait(BEAT)
        self.play(FadeIn(mark_value), Write(value), Write(warn)); self.wait(LONG)


class Scene10_QuantitativeResults(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: DFT bars climb toward the fairness finish line while baseline bars barely leave the floor.
        title = T("Disparate Impact scores", 16).move_to([0, 3.3, 0])
        axis = Line([-5.5, -2.2, 0], [5.5, -2.2, 0], color=MUTED, stroke_width=1.5)
        legend = VGroup(Rectangle(width=0.45, height=0.25, fill_color=WARM, fill_opacity=0.85, stroke_width=0).move_to([-4.7, 2.95, 0]),
                        T("Baseline SD-1.5", 10, MUTED).move_to([-3.7, 2.95, 0]),
                        Rectangle(width=0.45, height=0.25, fill_color=SECONDARY, fill_opacity=0.85, stroke_width=0).move_to([-1.6, 2.95, 0]),
                        T("SD-1.5 DFT", 10, SECONDARY).move_to([-0.75, 2.95, 0]))
        base_y, scale = -2.2, 3.4
        vals = [0.02, 0.66, 0.20, 0.85]
        xs = [-3.1, -1.9, 1.9, 3.1]
        cols = [WARM, SECONDARY, WARM, SECONDARY]
        bars = VGroup(*[bar(x, base_y, 0.75, v * scale, c) for x, v, c in zip(xs, vals, cols)])
        labs = VGroup(*[T(f"{v:.2f}", 10 if c == WARM else 11, c).next_to(b, UP, buff=0.1) for v, c, b in zip(vals, cols, bars)])
        groups = VGroup(T("medium / light", 10, MUTED).move_to([-2.5, -2.55, 0]),
                        T("dark / light", 10, MUTED).move_to([2.5, -2.55, 0]))
        threshold_y = base_y + 0.8 * scale
        threshold = DashedLine([-5.5, threshold_y, 0], [5.5, threshold_y, 0], color=ACCENT, dash_length=0.15)
        thresh_label = T("0.8 fairness threshold", 11, ACCENT).move_to([4.2, threshold_y + 0.2, 0])
        glow = SurroundingRectangle(bars[3], color=SECONDARY, stroke_width=2.5, buff=0.05)
        check = T("OK", 15, SECONDARY).next_to(bars[3], UP, buff=0.45)
        bottom = T("Diverse fine-tuning substantially reduces skin-tone bias.", 14, SECONDARY).move_to([0, -3.2, 0])

        self.play(Write(title), Create(axis), FadeIn(legend), FadeIn(groups)); self.wait(BEAT)
        self.play(Create(threshold), Write(thresh_label)); self.wait(BEAT)
        for b, l in zip(bars, labs):
            self.play(GrowFromEdge(b, DOWN), FadeIn(l), run_time=NORMAL)
            self.wait(BEAT / 2)
        self.wait(BEAT)
        self.play(Create(glow), Write(check)); self.wait(BEAT)
        self.play(Write(bottom)); self.wait(LONG)


class Scene11_QualitativeResults(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: the same prompt enters two lenses; one sees a narrow cone, the other opens to a broader field.
        prompt = VGroup(box(6.5, 0.52, MUTED, BG, 0.08, 0.08), T('"photo of a professional person"', 12)).move_to([0, 3.0, 0])
        divider = DashedLine([0, 3.4, 0], [0, -2.8, 0], color=MUTED, dash_length=0.14)
        left_title = T("Baseline model", 15, WARM).move_to([-3.0, 2.35, 0])
        right_title = T("Diversity fine-tuned model", 15, SECONDARY, 4.8).move_to([3.0, 2.35, 0])
        cone_l = Polygon([-3, 1.9, 0], [-4.3, 0.4, 0], [-1.7, 0.4, 0], fill_color=WARM, fill_opacity=0.12, stroke_color=WARM)
        cone_r = Polygon([3, 1.9, 0], [0.6, 0.4, 0], [5.4, 0.4, 0], fill_color=SECONDARY, fill_opacity=0.1, stroke_color=SECONDARY)
        left = image_panel("baseline_professionals.png", 2.75, 2.75, WARM).move_to([-3.0, -0.65, 0])
        right = image_panel("dft_professionals.png", 2.75, 2.75, SECONDARY).move_to([3.0, -0.65, 0])
        labels = VGroup(T("Similar results", 11, WARM).move_to([-3.0, -2.5, 0]),
                        T("Diverse results", 11, SECONDARY).move_to([3.0, -2.5, 0]))
        bottom = VGroup(T("Same prompt.", 16).move_to([-1.8, -3.2, 0]),
                        T("Different model.", 16, PRIMARY).move_to([1.8, -3.2, 0]))

        self.play(GrowFromCenter(prompt[0]), Write(prompt[1])); self.wait(BEAT)
        self.play(Create(divider)); self.wait(BEAT)
        self.play(Write(left_title), FadeIn(cone_l)); self.wait(BEAT)
        self.play(GrowFromCenter(left[0]), FadeIn(left[1])); self.wait(BEAT)
        self.play(Indicate(left, color=WARM, scale_factor=1.03)); self.wait(BEAT)
        self.play(Write(right_title), FadeIn(cone_r)); self.wait(BEAT)
        self.play(GrowFromCenter(right[0]), FadeIn(right[1])); self.wait(BEAT)
        self.play(FadeIn(labels)); self.wait(BEAT)
        self.play(Write(bottom)); self.wait(LONG)


class Scene12_QualityRealism(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: DFT moves right on fairness while staying on the same high-quality line.
        origin = np.array([-4.7, -2.05, 0])
        x_axis = Arrow(origin, [4.9, -2.05, 0], color=SECONDARY, stroke_width=3, buff=0)
        y_axis = Arrow(origin, [-4.7, 3.05, 0], color=PRIMARY, stroke_width=3, buff=0)
        x_lab = T("Fairness / Diversity", 18, SECONDARY).move_to([3.0, -2.62, 0])
        y_lab = T("Quality / Realism", 18, PRIMARY).rotate(PI / 2).move_to([-5.48, 0.55, 0])
        ticks = VGroup(
            T("Low", 13, MUTED).move_to([-3.25, -2.42, 0]),
            T("High", 13, MUTED).move_to([3.75, -2.42, 0]),
            T("Low", 13, MUTED).move_to([-5.1, -1.1, 0]),
            T("High", 13, MUTED).move_to([-5.05, 2.45, 0]),
        )

        quality_line = DashedLine([-3.4, 1.75, 0], [3.65, 1.75, 0], color=PRIMARY, dash_length=0.18, stroke_width=2.5)
        quality_label = T("same high quality / realism", 17, PRIMARY).move_to([0.2, 2.12, 0])
        base = VGroup(
            Circle(0.29, fill_color=WARM, fill_opacity=0.95, stroke_width=0),
            T("Baseline", 18, WARM).next_to(ORIGIN, UP, buff=0.28),
        ).move_to([-2.7, 1.75, 0])
        dft = VGroup(
            Circle(0.29, fill_color=SECONDARY, fill_opacity=0.95, stroke_width=0),
            T("DFT", 18, SECONDARY).next_to(ORIGIN, UP, buff=0.28),
        ).move_to([2.7, 1.75, 0])
        fairness_arrow = Arrow([-2.28, 1.75, 0], [2.28, 1.75, 0], color=SECONDARY, stroke_width=3, buff=0,
                               max_tip_length_to_length_ratio=0.08)
        fair_label = T("more fair", 19, SECONDARY).move_to([0, 1.28, 0])
        study = VGroup(box(4.65, 0.72, SECONDARY, BG, 0.08),
                       T("Blind study preferred DFT", 18, SECONDARY, 4.2)).move_to([-1.65, -0.48, 0])
        noise = VGroup(box(4.25, 0.72, MUTED, BG, 0.05),
                       T("Synthetic data may be noisy", 17, MUTED, 3.8)).move_to([1.9, -1.23, 0])
        bottom = T("More diversity without sacrificing image quality.", 22, SECONDARY).move_to([0, -3.25, 0])

        self.play(Create(x_axis), Create(y_axis), Write(x_lab), Write(y_lab), FadeIn(ticks)); self.wait(BEAT)
        self.play(Create(quality_line), Write(quality_label)); self.wait(BEAT)
        self.play(GrowFromCenter(base[0]), Write(base[1])); self.wait(BEAT)
        self.play(Create(fairness_arrow), Write(fair_label)); self.wait(BEAT)
        self.play(GrowFromCenter(dft[0]), Write(dft[1])); self.wait(BEAT)
        self.play(FadeIn(study)); self.wait(BEAT)
        self.play(FadeIn(noise)); self.wait(BEAT)
        self.play(Write(bottom)); self.wait(LONG)


class Scene13_FairnessSummary(Scene):
    def construct(self):
        self.camera.background_color = BG
        # Visual answer: a late fairness patch slides backward into training, then every generated frame passes the scan.
        names = ["Pre-training", "Fine-tuning", "Prompt edit", "Generation"]
        xs = [-4.65, -1.55, 1.55, 4.65]
        pipes = VGroup()
        for n, x in zip(names, xs):
            col = SECONDARY if n == "Generation" else MUTED
            pipes.add(VGroup(box(2.35, 0.88, col, BG, 0.08),
                             T(n, 16, col, 2.1)).move_to([x, 2.0, 0]))
        arrs = VGroup(*[arrow_between([xs[i] + 1.25, 2.0, 0], [xs[i + 1] - 1.25, 2.0, 0], MUTED, 2.2) for i in range(3)])
        late_patch = VGroup(box(1.85, 0.48, WARM, WARM, 0.92, 0.07, 1.2),
                            T("late patch", 14, BG)).move_to([1.55, 2.72, 0])
        built_patch = VGroup(box(1.85, 0.48, PRIMARY, PRIMARY, 0.92, 0.07, 1.2),
                             T("built in", 14, BG)).move_to([-4.65, 2.72, 0])
        msg_late = T("Patching the prompt is too late.", 21, WARM).move_to([0, 0.92, 0])
        msg_built = T("DFT moves fairness into learning.", 21, PRIMARY).move_to([0, 0.92, 0])

        frames = VGroup()
        skins = [SKIN_LIGHT, SKIN_MEDIUM, SKIN_DARK, SKIN_LIGHT, SKIN_MEDIUM, SKIN_DARK]
        for i, x in enumerate([-4.8, -2.9, -1.0, 0.9, 2.8, 4.7]):
            col = WARM if i == 3 else SECONDARY
            frame_rect = box(1.25, 1.25, col, BG, 0.04, 0.07, 1.8).move_to([x, -1.05, 0])
            face = avatar(skins[i], 0.22).move_to([x, -1.08, 0])
            holes = VGroup(*[Rectangle(width=0.11, height=0.11, fill_color=col, fill_opacity=0.55, stroke_width=0).move_to([x + dx, -0.45, 0])
                             for dx in [-0.36, 0.36]])
            frame = VGroup(frame_rect, face, holes)
            frames.add(frame)
        scan = Line([-5.55, -1.05, 0], [-5.55, -1.05, 0], color=PRIMARY, stroke_width=3.5)
        fail = T("X", 22, WARM).move_to(frames[3].get_center() + UP * 0.58)
        checks = VGroup(*[T("OK", 16, SECONDARY).move_to(f.get_center() + UP * 0.58) for f in frames])
        film_label = T("Every frame must keep representation stable.", 19, PRIMARY).move_to([0, 0.08, 0])
        final1 = T("Not patched at the end.", 22, WARM).move_to([-2.25, -2.92, 0])
        final2 = T("Built from the start.", 22, SECONDARY).move_to([2.25, -2.92, 0])

        self.play(LaggedStart(*[GrowFromCenter(p) for p in pipes], lag_ratio=0.1),
                  LaggedStart(*[Create(a) for a in arrs], lag_ratio=0.1)); self.wait(BEAT)
        self.play(FadeIn(late_patch), Write(msg_late)); self.wait(BEAT)
        self.play(ReplacementTransform(late_patch, built_patch),
                  FadeOut(msg_late), pipes[0][0].animate.set_stroke(PRIMARY).set_fill(PRIMARY, opacity=0.10)); self.wait(BEAT)
        self.play(Write(msg_built)); self.wait(BEAT)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in frames], lag_ratio=0.08)); self.wait(BEAT)
        self.play(scan.animate.put_start_and_end_on([-5.55, -1.05, 0], [5.55, -1.05, 0]), run_time=SLOW)
        self.play(FadeIn(fail), Flash(frames[3], color=WARM)); self.wait(BEAT)
        self.play(ReplacementTransform(fail, checks[3]),
                  *[frames[i][0].animate.set_stroke(SECONDARY) for i in range(6)]); self.wait(BEAT)
        self.play(LaggedStart(*[FadeIn(m) for i, m in enumerate(checks) if i != 3], lag_ratio=0.08),
                  Write(film_label)); self.wait(BEAT)
        self.play(Write(final1), Write(final2)); self.wait(LONG)
