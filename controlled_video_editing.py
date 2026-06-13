from pathlib import Path

from manim import *


BG = "#1C1C1C"
BLUE_C = "#58C4DD"
TEAL_E = "#49A88F"
GREEN_C = "#83C167"
YELLOW_C = "#FFFF00"
RED_C = "#FC6255"
PURPLE_C = "#9A72AC"
MAROON_C = "#C55F73"
GREY_C = "#888888"

PRIMARY = BLUE_C
SECONDARY = GREEN_C
ACCENT = YELLOW_C
MONO = "Consolas"

TITLE_SIZE = 46
SECTION_SIZE = 34
BODY_SIZE = 26
SMALL_SIZE = 20
MIN_SIZE = 18

ASSET_DIR = Path(__file__).parent / "assets" / "controlled_editing"
SOURCE_STRIP = ASSET_DIR / "source_jeep_contact_sheet.png"
STRUCTURE_SHEET = ASSET_DIR / "structure_controls_contact_sheet.png"
VARIANTS_SHEET = ASSET_DIR / "edit_variants_contact_sheet.png"
POINT_SWAP = ASSET_DIR / "point_swap_control.png"
RISK_PIPELINE = ASSET_DIR / "editing_risk_pipeline.png"


def caption(text, size=BODY_SIZE, color=WHITE, weight=NORMAL):
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)


def soft_card(title, subtitle, color=PRIMARY, width=2.8, height=0.92):
    box = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2,
        fill_color=BG,
        fill_opacity=0.84,
    )
    text = VGroup(
        caption(title, SMALL_SIZE, color, BOLD),
        caption(subtitle, MIN_SIZE - 2, GREY_C),
    ).arrange(DOWN, buff=0.1).move_to(box)
    return VGroup(box, text)


def image_card(path, width=8.0, color=PRIMARY):
    image = ImageMobject(str(path)).set_width(width)
    frame = SurroundingRectangle(image, color=color, buff=0.03, stroke_width=2)
    return Group(image, frame)


def pill(text, color=PRIMARY):
    label = caption(text, MIN_SIZE, color, BOLD)
    box = RoundedRectangle(
        corner_radius=0.13,
        width=max(1.2, label.width + 0.34),
        height=0.42,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.08,
    )
    return VGroup(box, label.move_to(box))


class ControlledVideoEditingExplainer(Scene):
    """Controlled video editing research directions from the CVPR 2024 tutorial."""

    def construct(self):
        self.camera.background_color = BG
        scenes = [
            self.scene_1_hook,
            self.scene_2_problem_statement,
            self.scene_3_naive_failure,
            self.scene_4_control_handles,
            self.scene_5_research_landscape,
            self.scene_6_pix2video,
            self.scene_7_controlvideo_family,
            self.scene_8_magicedit_magicprop,
            self.scene_9_rerender_videocontrolnet,
            self.scene_10_videoswap_points,
            self.scene_11_safety_risks,
            self.scene_12_summary,
        ]
        for i, scene in enumerate(scenes):
            scene()
            if i < len(scenes) - 1:
                self.play(FadeOut(*self.mobjects), run_time=1.0)
                self.wait(0.55)

    def scene_1_hook(self):
        title = caption("Controlled Video Editing", TITLE_SIZE, PRIMARY, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        strip = image_card(SOURCE_STRIP, width=11.2, color=PRIMARY).shift(DOWN * 0.05)
        self.play(FadeIn(strip, scale=0.97), run_time=2.0)
        self.wait(1.2)

        question = caption("Change the video, but do not break time.", BODY_SIZE, ACCENT, BOLD)
        question.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=1.0)
        self.wait(16.3)

    def scene_2_problem_statement(self):
        title = caption("The bargain: edit one thing, preserve the rest", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.35)

        before = soft_card("source video", "motion + identity + scene", PRIMARY, 3.1, 0.92).shift(LEFT * 4.2 + UP * 0.35)
        edit = soft_card("edit request", "snow, style, swap, pose...", ACCENT, 3.1, 0.92).shift(ORIGIN + UP * 0.35)
        after = soft_card("edited video", "only requested parts change", GREEN_C, 3.1, 0.92).shift(RIGHT * 4.2 + UP * 0.35)
        arrows = VGroup(
            Arrow(before.get_right(), edit.get_left(), buff=0.15, color=GREY_C),
            Arrow(edit.get_right(), after.get_left(), buff=0.15, color=GREY_C),
        )
        self.play(FadeIn(before), run_time=0.9)
        self.play(GrowArrow(arrows[0]), FadeIn(edit), run_time=1.0)
        self.play(GrowArrow(arrows[1]), FadeIn(after), run_time=1.0)

        constraints = VGroup(
            pill("preserve motion", PRIMARY),
            pill("preserve background", TEAL_E),
            pill("preserve identity", PURPLE_C),
            pill("change appearance", ACCENT),
        ).arrange(RIGHT, buff=0.18).shift(DOWN * 1.5)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in constraints], lag_ratio=0.12), run_time=1.3)
        self.wait(17.8)

    def scene_3_naive_failure(self):
        title = caption("Naive frame-by-frame editing flickers", SECTION_SIZE, ACCENT, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.35)

        frames = VGroup()
        for i in range(5):
            box = RoundedRectangle(
                corner_radius=0.04,
                width=1.55,
                height=1.08,
                stroke_color=PRIMARY,
                fill_color=PRIMARY if i % 2 == 0 else TEAL_E,
                fill_opacity=0.12 + 0.04 * (i % 2),
                stroke_width=2,
            )
            car = Polygon(LEFT * 0.45 + DOWN * 0.1, RIGHT * 0.42 + DOWN * 0.1, RIGHT * 0.25 + UP * 0.16, LEFT * 0.3 + UP * 0.17, color=ACCENT, fill_opacity=0.25)
            car.move_to(box)
            frames.add(VGroup(box, car))
        frames.arrange(RIGHT, buff=0.42).shift(UP * 0.5)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in frames], lag_ratio=0.12), run_time=1.6)

        jitter = VGroup()
        for f in frames:
            jitter.add(Arrow(f.get_bottom(), f.get_bottom() + DOWN * 0.65 + RIGHT * (0.2 if len(jitter) % 2 == 0 else -0.2), buff=0.08, color=RED_C))
        self.play(LaggedStart(*[GrowArrow(a) for a in jitter], lag_ratio=0.1), run_time=1.2)
        warning = caption("Each frame invents a slightly different answer.", SMALL_SIZE, RED_C).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(warning), run_time=0.9)
        self.wait(17.3)

    def scene_4_control_handles(self):
        title = caption("The trick: edit through structure", SECTION_SIZE, ACCENT, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.35)

        sheet = image_card(STRUCTURE_SHEET, width=10.3, color=PRIMARY).shift(UP * 0.15)
        self.play(FadeIn(sheet, scale=0.97), run_time=1.8)
        self.wait(0.9)

        controls = VGroup(
            pill("depth", PRIMARY),
            pill("edges", TEAL_E),
            pill("pose", GREEN_C),
            pill("flow", PURPLE_C),
            pill("points", ACCENT),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in controls], lag_ratio=0.1), run_time=1.2)
        self.wait(19.8)

    def scene_5_research_landscape(self):
        title = caption("Concurrent work: many handles for the same promise", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.35)

        groups = VGroup(
            soft_card("Depth / ControlNet", "Gen-1, Pix2Video\nControlVideo, Control-A-Video\nMake-Your-Video, MagicEdit", PRIMARY, 3.55, 1.35),
            soft_card("Temporal propagation", "MagicProp\nRerender A Video\nVideoControlNet", TEAL_E, 3.55, 1.35),
            soft_card("Subject / point control", "VideoSwap\nsemantic points\nbackground preservation", PURPLE_C, 3.55, 1.35),
        ).arrange(RIGHT, buff=0.35).shift(UP * 0.35)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.12) for g in groups], lag_ratio=0.16), run_time=1.6)

        center = soft_card("controlled editing", "what is allowed to change?", ACCENT, 3.1, 0.9).to_edge(DOWN, buff=0.65)
        arrows = VGroup(*[Arrow(g.get_bottom(), center.get_top(), buff=0.15, color=GREY_C) for g in groups])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), FadeIn(center), run_time=1.4)
        self.wait(22.8)

    def scene_6_pix2video(self):
        title = caption("Pix2Video: image diffusion, video constraints", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = caption("Ceylan et al. 2023", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle), run_time=1.35)

        stages = VGroup(
            soft_card("source frames", "the video we edit", PRIMARY, 2.5, 0.85),
            soft_card("DDIM inversion", "recover initial noise", PURPLE_C, 2.65, 0.85),
            soft_card("depth-guided SD", "edit frame by frame", TEAL_E, 2.65, 0.85),
            soft_card("temporal glue", "previous frame attention\nlatent guidance", GREEN_C, 2.75, 1.05),
        ).arrange(RIGHT, buff=0.28).shift(UP * 0.45)
        self.play(FadeIn(stages[0]), run_time=0.8)
        pipeline_arrows = VGroup()
        for i in range(3):
            arrow = Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.12, color=GREY_C)
            pipeline_arrows.add(arrow)
            self.play(GrowArrow(arrow), FadeIn(stages[i + 1]), run_time=1.0)
            self.wait(0.35)

        note = caption("The edit changes the scene; the motion should still feel like one video.", MIN_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.75)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.5)

        # Clear the explanation before showing the large visual result so the
        # contact sheet does not cover the pipeline labels.
        self.play(
            FadeOut(stages, shift=UP * 0.12),
            FadeOut(pipeline_arrows),
            FadeOut(note),
            run_time=1.0,
        )

        variants = image_card(VARIANTS_SHEET, width=9.2, color=PRIMARY).shift(DOWN * 0.45)
        self.play(FadeIn(variants, scale=0.97), run_time=1.6)
        self.wait(21.2)

    def scene_7_controlvideo_family(self):
        title = caption("ControlVideo family: inflate image control into time", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = caption("Zhang et al. 2023 / Zhao et al. 2023 / Control-A-Video", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle), run_time=1.35)

        sd = soft_card("Stable Diffusion", "pretrained image prior", PRIMARY, 2.8, 0.88).shift(LEFT * 4.2 + UP * 0.7)
        cn = soft_card("ControlNet", "depth / edge / pose", TEAL_E, 2.8, 0.88).shift(LEFT * 4.2 + DOWN * 0.6)
        inflate = soft_card("inflate in time", "reuse weights across frames", PURPLE_C, 3.0, 0.98).shift(ORIGIN + UP * 0.05)
        smooth = soft_card("interleaved smoothing", "denoise frames together", GREEN_C, 3.2, 0.98).shift(RIGHT * 4.0 + UP * 0.05)
        self.play(FadeIn(sd), FadeIn(cn), run_time=1.0)
        self.play(GrowArrow(Arrow(sd.get_right(), inflate.get_left(), buff=0.15, color=GREY_C)), GrowArrow(Arrow(cn.get_right(), inflate.get_left(), buff=0.15, color=GREY_C)), FadeIn(inflate), run_time=1.2)
        self.play(GrowArrow(Arrow(inflate.get_right(), smooth.get_left(), buff=0.15, color=GREY_C)), FadeIn(smooth), run_time=1.0)

        handles = VGroup(pill("depth maps", PRIMARY), pill("canny edges", TEAL_E), pill("human poses", GREEN_C)).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.65)
        self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.12) for h in handles], lag_ratio=0.15), run_time=1.0)
        self.wait(25.8)

    def scene_8_magicedit_magicprop(self):
        title = caption("High fidelity needs propagation", SECTION_SIZE, ACCENT, BOLD).to_edge(UP, buff=0.4)
        subtitle = caption("MagicEdit / MagicProp / Make-Your-Video", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle), run_time=1.35)

        key = soft_card("key edited frame", "strong local edit", ACCENT, 2.8, 0.9).shift(LEFT * 4.4 + UP * 0.2)
        frames = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.9, height=0.65, color=PRIMARY, fill_opacity=0.12) for _ in range(7)]).arrange(RIGHT, buff=0.18).shift(RIGHT * 0.45 + UP * 0.2)
        arrows = VGroup(*[Arrow(key.get_right(), f.get_left(), buff=0.08, color=GREY_C, stroke_width=2) for f in frames])
        self.play(FadeIn(key), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(f, scale=0.9) for f in frames], lag_ratio=0.08), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.05), run_time=1.4)

        cards = VGroup(
            soft_card("MagicEdit", "high-fidelity coherent edits", PURPLE_C, 3.15, 0.82),
            soft_card("MagicProp", "motion-aware appearance propagation", TEAL_E, 3.15, 0.82),
            soft_card("Make-Your-Video", "textual + structural guidance", GREEN_C, 3.15, 0.82),
        ).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.65)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.14), run_time=1.2)
        self.wait(25.8)

    def scene_9_rerender_videocontrolnet(self):
        title = caption("Rerendering: preserve motion while repainting appearance", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = caption("Rerender A Video / VideoControlNet / FlowVid", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle), run_time=1.35)

        source = soft_card("source video", "I, P, B frames", PRIMARY, 2.65, 0.9).shift(LEFT * 4.6 + UP * 0.25)
        flow = soft_card("motion guide", "optical flow", TEAL_E, 2.65, 0.9).shift(LEFT * 1.55 + UP * 0.25)
        rerender = soft_card("diffusion repaint", "new style/content", PURPLE_C, 2.85, 0.9).shift(RIGHT * 1.7 + UP * 0.25)
        result = soft_card("consistent video", "same trajectory", GREEN_C, 2.65, 0.9).shift(RIGHT * 4.75 + UP * 0.25)
        flow_group = VGroup(source, flow, rerender, result)
        self.play(FadeIn(source), run_time=0.8)
        for i, card in enumerate(flow_group[1:]):
            self.play(GrowArrow(Arrow(flow_group[i].get_right(), card.get_left(), buff=0.12, color=GREY_C)), FadeIn(card), run_time=1.0)
            self.wait(0.35)

        wave = VGroup()
        for i in range(9):
            wave.add(Arc(radius=0.35 + i * 0.08, start_angle=-PI / 4, angle=PI / 2, color=ACCENT, stroke_opacity=0.15 + i * 0.07).shift(DOWN * 1.55 + LEFT * 0.2))
        note = caption("The hard part is imperfect flow: motion helps, but errors also propagate.", SMALL_SIZE, ACCENT).to_edge(DOWN, buff=0.6)
        self.play(Create(wave), FadeIn(note), run_time=1.3)
        self.wait(25.8)

    def scene_10_videoswap_points(self):
        title = caption("VideoSwap: control semantic points, not just pixels", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = caption("Gu et al. 2024", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), FadeIn(subtitle), run_time=1.35)

        panel = image_card(POINT_SWAP, width=9.4, color=PURPLE_C).shift(UP * 0.15)
        self.play(FadeIn(panel, scale=0.97), run_time=1.8)
        self.wait(0.8)

        goals = VGroup(
            pill("replace subject", PURPLE_C),
            pill("keep background", TEAL_E),
            pill("align motion", PRIMARY),
            pill("allow shape change", ACCENT),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in goals], lag_ratio=0.1), run_time=1.1)
        self.wait(24.8)

    def scene_11_safety_risks(self):
        title = caption("Why it matters: precision cuts both ways", SECTION_SIZE, ACCENT, BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.35)

        panel = image_card(RISK_PIPELINE, width=8.4, color=YELLOW_C).shift(LEFT * 2.6 + DOWN * 0.05)
        self.play(FadeIn(panel, scale=0.97), run_time=1.7)

        risks = VGroup(
            soft_card("good uses", "film, localization,\naccessibility, repair", GREEN_C, 3.0, 1.05),
            soft_card("dangerous uses", "deceptive edits,\nimpersonation,\nevidence tampering", RED_C, 3.0, 1.18),
            soft_card("needed defenses", "provenance,\nwatermarking,\nred-team evaluation", ACCENT, 3.0, 1.18),
        ).arrange(DOWN, buff=0.28).shift(RIGHT * 4.0 + DOWN * 0.05)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in risks], lag_ratio=0.18), run_time=1.6)
        self.wait(25.8)

    def scene_12_summary(self):
        title = caption("Controlled editing = change budget", TITLE_SIZE, ACCENT, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.45)

        items = VGroup(
            soft_card("what changes?", "style, subject, scene", ACCENT, 2.75, 0.9),
            soft_card("what stays?", "motion, layout, identity", PRIMARY, 2.75, 0.9),
            soft_card("what controls?", "depth, edges, flow, points", TEAL_E, 2.95, 0.9),
            soft_card("what protects?", "provenance + evaluation", GREEN_C, 2.95, 0.9),
        ).arrange(RIGHT, buff=0.28).shift(UP * 0.35)
        self.play(FadeIn(items[0]), run_time=0.8)
        for i, card in enumerate(items[1:]):
            self.play(GrowArrow(Arrow(items[i].get_right(), card.get_left(), buff=0.1, color=GREY_C)), FadeIn(card), run_time=0.95)
            self.wait(0.3)

        model_list = caption(
            "Pix2Video  |  ControlVideo  |  Control-A-Video  |  MagicEdit  |  MagicProp  |  Rerender A Video  |  VideoSwap  |  VideoControlNet",
            MIN_SIZE,
            GREY_C,
        ).to_edge(DOWN, buff=0.75)
        insight = caption("The research direction is a toolbox for editing with constraints.", BODY_SIZE, ACCENT, BOLD)
        insight.next_to(model_list, UP, buff=0.4)
        self.play(FadeIn(insight), FadeIn(model_list), run_time=1.1)
        self.wait(25.8)
