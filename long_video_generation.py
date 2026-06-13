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

ASSET_DIR = Path(__file__).parent / "assets"
CONTACT_SHEET = ASSET_DIR / "long_video_train_contact_sheet.png"
PANEL_DIR = ASSET_DIR / "long_video_train_panels"


def caption(text, size=BODY_SIZE, color=WHITE, weight=NORMAL):
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)


def image_panel(path, height=1.55, color=PRIMARY):
    image = ImageMobject(str(path)).set_height(height)
    frame = SurroundingRectangle(image, color=color, buff=0.02, stroke_width=2)
    return Group(image, frame)


def soft_card(title, subtitle, color=PRIMARY, width=2.65, height=0.92):
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


def timeline_line(width=10.8, y=-2.3):
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=GREY_C, stroke_width=2).shift(UP * y)
    ticks = VGroup(*[Line(UP * 0.08, DOWN * 0.08, color=GREY_C, stroke_width=2).move_to(line.point_from_proportion(i / 10)) for i in range(11)])
    return VGroup(line, ticks)


class LongVideoGenerationExplainer(Scene):
    """CVPR 2024 tutorial section 2.6: long video generation."""

    def construct(self):
        self.camera.background_color = BG
        scenes = [
            self.scene_1_hook,
            self.scene_2_short_window_problem,
            self.scene_3_keyframe_pivot,
            self.scene_4_nuwa_xl_highlights,
            self.scene_5_diffusion_over_diffusion,
            self.scene_6_masking_conditions,
            self.scene_7_training_scale,
            self.scene_8_other_directions,
            self.scene_9_summary,
        ]
        for i, scene in enumerate(scenes):
            scene()
            if i < len(scenes) - 1:
                self.play(FadeOut(*self.mobjects), run_time=1.05)
                self.wait(0.55)

    def make_keyframes(self, height=1.25, buff=0.12):
        return Group(
            *[
                image_panel(PANEL_DIR / f"train_keyframe_{i}.png", height=height)
                for i in range(1, 6)
            ]
        ).arrange(RIGHT, buff=buff)

    def scene_1_hook(self):
        title = caption("Long Video Generation", TITLE_SIZE, PRIMARY, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.65)

        sheet = ImageMobject(str(CONTACT_SHEET)).set_width(12.7).shift(DOWN * 0.1)
        self.play(FadeIn(sheet, scale=0.96), run_time=2.1)
        self.wait(1.15)

        question = caption("Why not generate a long video in one shot?", BODY_SIZE, ACCENT)
        question.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=1.2)
        self.wait(4.6)

    def scene_2_short_window_problem(self):
        title = caption("The naive idea: just keep making clips", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.4)

        keyframes = self.make_keyframes(height=1.28).shift(UP * 0.55)
        self.play(FadeIn(keyframes), run_time=1.55)
        self.wait(0.7)

        timeline = timeline_line(width=10.8, y=-1.25)
        self.play(Create(timeline), run_time=1.15)

        window = RoundedRectangle(
            corner_radius=0.05,
            width=2.15,
            height=2.1,
            color=RED_C,
            stroke_width=4,
        ).move_to(keyframes[0])
        label = caption("short context", SMALL_SIZE, RED_C).next_to(window, DOWN, buff=0.18)
        self.play(Create(window), FadeIn(label), run_time=1.1)
        self.wait(1.0)

        for target in keyframes[1:]:
            self.play(window.animate.move_to(target), label.animate.next_to(window, DOWN, buff=0.18), run_time=1.15)
            self.wait(0.32)

        drift = caption("Local clips can drift: identity, scene, and story memory fade.", SMALL_SIZE, RED_C)
        drift.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(drift), run_time=1.05)
        self.wait(6.4)

    def scene_3_keyframe_pivot(self):
        title = caption("Shift perspective: plan sparse anchors first", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.4)

        keyframes = self.make_keyframes(height=1.35).shift(UP * 0.35)
        self.play(FadeIn(keyframes), run_time=1.55)
        self.wait(0.75)

        anchors = VGroup()
        for panel in keyframes:
            dot = Dot(panel.get_bottom() + DOWN * 0.3, radius=0.07, color=ACCENT)
            anchors.add(dot)
        base = Line(anchors[0].get_center(), anchors[-1].get_center(), color=GREY_C, stroke_width=2)
        self.play(Create(base), LaggedStart(*[FadeIn(d) for d in anchors], lag_ratio=0.12), run_time=1.45)
        self.wait(0.8)

        prompt_cards = VGroup(
            soft_card("prompt 1", "sunrise pass", PRIMARY, 1.65, 0.65),
            soft_card("prompt 2", "green valley", PRIMARY, 1.65, 0.65),
            soft_card("prompt 3", "city bridge", PRIMARY, 1.65, 0.65),
            soft_card("prompt 4", "sunset coast", PRIMARY, 1.65, 0.65),
            soft_card("prompt 5", "night station", PRIMARY, 1.65, 0.65),
        ).arrange(RIGHT, buff=0.1).to_edge(DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in prompt_cards], lag_ratio=0.12), run_time=1.65)

        aha = caption("Long videos become a timeline problem before a pixel problem.", SMALL_SIZE, ACCENT)
        aha.next_to(prompt_cards, UP, buff=0.35)
        self.play(FadeIn(aha), run_time=1.05)
        self.wait(5.8)

    def scene_4_nuwa_xl_highlights(self):
        title = caption("NUWA-XL: long video by hierarchy", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = caption("Microsoft Research: diffusion over diffusion", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        sheet = ImageMobject(str(CONTACT_SHEET)).set_width(6.4).shift(LEFT * 3.1 + DOWN * 0.1)
        frame = SurroundingRectangle(sheet, color=PRIMARY, buff=0.03, stroke_width=3)
        self.play(FadeIn(sheet, scale=0.96), Create(frame), run_time=1.65)
        self.wait(0.7)

        highlights = VGroup(
            soft_card("very long training", "> 3K frames", PRIMARY, 3.0, 0.86),
            soft_card("parallel inference", "many chunks at once", SECONDARY, 3.0, 0.86),
            soft_card("high-res data", "around 1K x 1K", TEAL_E, 3.0, 0.86),
        ).arrange(DOWN, buff=0.3).shift(RIGHT * 3.35 + DOWN * 0.08)
        arrows = VGroup(
            *[
                Arrow(frame.get_right(), card.get_left(), buff=0.18, color=GREY_C, stroke_width=2)
                for card in highlights
            ]
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.14), run_time=1.25)
        self.play(LaggedStart(*[FadeIn(card, shift=LEFT * 0.12) for card in highlights], lag_ratio=0.16), run_time=1.65)
        self.wait(7.8)

    def scene_5_diffusion_over_diffusion(self):
        title = caption("NUWA-XL: diffusion over diffusion", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = caption("coarse-to-fine hierarchical generation", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        keyframes = self.make_keyframes(height=1.05).to_edge(UP, buff=1.25)
        self.play(FadeIn(keyframes), run_time=1.45)
        self.wait(0.7)

        global_model = soft_card("Global diffusion", "text prompts -> keyframes", PURPLE_C, 3.0, 0.85).shift(LEFT * 3.5 + DOWN * 0.65)
        local_model = soft_card("Local diffusion", "fill between anchors", TEAL_E, 3.0, 0.85).shift(RIGHT * 3.5 + DOWN * 0.65)
        self.play(FadeIn(global_model), GrowArrow(Arrow(keyframes.get_bottom(), global_model.get_top(), buff=0.15, color=GREY_C)), run_time=1.35)
        self.wait(0.95)

        gaps = VGroup()
        for left, right in zip(keyframes[:-1], keyframes[1:]):
            gap = VGroup(
                RoundedRectangle(corner_radius=0.04, width=0.38, height=0.72, color=GREEN_C, fill_opacity=0.15),
                RoundedRectangle(corner_radius=0.04, width=0.38, height=0.72, color=GREEN_C, fill_opacity=0.15),
            ).arrange(RIGHT, buff=0.04)
            gap.move_to((left.get_right() + right.get_left()) / 2)
            gaps.add(gap)

        self.play(
            GrowArrow(Arrow(global_model.get_right(), local_model.get_left(), buff=0.15, color=GREY_C)),
            FadeIn(local_model),
            run_time=1.35,
        )
        self.wait(0.8)
        self.play(LaggedStart(*[FadeIn(g, scale=0.7) for g in gaps], lag_ratio=0.18), run_time=2.0)

        note = caption("Global sketches the story. Local fills the missing frames.", SMALL_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(7.0)

    def scene_6_masking_conditions(self):
        title = caption("Same backbone, different conditions", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        subtitle = caption("the mask decides which diffusion job is being solved", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(subtitle), run_time=1.4)

        global_card = soft_card("Global model", "mask all frames", PURPLE_C, 3.0, 0.86).shift(LEFT * 3.45 + UP * 1.0)
        local_card = soft_card("Local model", "keep first + last", TEAL_E, 3.0, 0.86).shift(LEFT * 3.45 + DOWN * 1.35)
        self.play(FadeIn(global_card), FadeIn(local_card), run_time=1.2)
        self.wait(0.7)

        global_frames = VGroup()
        local_frames = VGroup()
        for i in range(5):
            g = Rectangle(width=0.7, height=0.55, color=GREY_C, fill_color=GREY_C, fill_opacity=0.22)
            l_color = PRIMARY if i in (0, 4) else GREY_C
            l_opacity = 0.12 if i in (0, 4) else 0.32
            l = Rectangle(width=0.7, height=0.55, color=l_color, fill_color=l_color, fill_opacity=l_opacity)
            if i not in (0, 4):
                cross = VGroup(
                    Line(l.get_corner(UL), l.get_corner(DR), color=RED_C, stroke_width=2),
                    Line(l.get_corner(DL), l.get_corner(UR), color=RED_C, stroke_width=2),
                )
                l = VGroup(l, cross)
            global_frames.add(g)
            local_frames.add(l)
        global_frames.arrange(RIGHT, buff=0.12).shift(RIGHT * 2.2 + UP * 1.0)
        local_frames.arrange(RIGHT, buff=0.12).shift(RIGHT * 2.2 + DOWN * 1.35)

        global_label = caption("text only -> sparse keyframes", SMALL_SIZE, PURPLE_C).next_to(global_frames, DOWN, buff=0.18)
        local_label = caption("endpoints -> interpolate the middle", SMALL_SIZE, TEAL_E).next_to(local_frames, DOWN, buff=0.18)
        self.play(
            GrowArrow(Arrow(global_card.get_right(), global_frames.get_left(), buff=0.16, color=GREY_C)),
            LaggedStart(*[FadeIn(f, scale=0.85) for f in global_frames], lag_ratio=0.1),
            run_time=1.45,
        )
        self.play(FadeIn(global_label), run_time=0.8)
        self.wait(0.8)
        self.play(
            GrowArrow(Arrow(local_card.get_right(), local_frames.get_left(), buff=0.16, color=GREY_C)),
            LaggedStart(*[FadeIn(f, scale=0.85) for f in local_frames], lag_ratio=0.1),
            run_time=1.45,
        )
        self.play(FadeIn(local_label), run_time=0.8)
        self.wait(7.8)

    def scene_7_training_scale(self):
        title = caption("Training scale teaches long-range consistency", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.35)

        strip = self.make_keyframes(height=1.2, buff=0.11).shift(UP * 0.55)
        self.play(FadeIn(strip), run_time=1.45)
        self.wait(0.75)

        phases = VGroup(
            soft_card("early", "short fragments", GREY_C, 2.2, 0.82),
            soft_card("5M videos", "better transitions", PRIMARY, 2.2, 0.82),
            soft_card("10M videos", "longer coherence", GREEN_C, 2.2, 0.82),
        ).arrange(RIGHT, buff=0.55).shift(DOWN * 1.25)
        arrows = VGroup(
            Arrow(phases[0].get_right(), phases[1].get_left(), buff=0.12, color=GREY_C),
            Arrow(phases[1].get_right(), phases[2].get_left(), buff=0.12, color=GREY_C),
        )
        self.play(FadeIn(phases[0]), run_time=0.9)
        self.wait(0.55)
        self.play(GrowArrow(arrows[0]), FadeIn(phases[1]), run_time=1.15)
        self.wait(0.55)
        self.play(GrowArrow(arrows[1]), FadeIn(phases[2]), run_time=1.15)

        note = caption("More long examples make the model practice continuity, not just image quality.", SMALL_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(6.8)

    def scene_8_other_directions(self):
        title = caption("Concurrent directions: how to extend time", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.4)

        strip = self.make_keyframes(height=0.95, buff=0.1).to_edge(UP, buff=1.15)
        self.play(FadeIn(strip), run_time=1.35)
        self.wait(0.65)

        cards = VGroup(
            soft_card("LVDM", "autoregressive + interpolation", PRIMARY, 3.2, 0.9),
            soft_card("VideoGen", "cascaded, reference-guided", SECONDARY, 3.2, 0.9),
            soft_card("VidRD", "reuse context, diffuse next", TEAL_E, 3.2, 0.9),
        ).arrange(RIGHT, buff=0.35).shift(DOWN * 0.65)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in cards], lag_ratio=0.16), run_time=1.65)
        self.wait(0.8)

        # Give each direction a visual grammar.
        lvdm_arrows = VGroup(*[Arrow(strip[i].get_right(), strip[i + 1].get_left(), buff=0.05, color=PRIMARY, stroke_width=2) for i in range(4)])
        cascade = VGroup(
            Rectangle(width=1.1, height=0.45, color=SECONDARY),
            Rectangle(width=1.45, height=0.6, color=SECONDARY),
            Rectangle(width=1.9, height=0.78, color=SECONDARY),
        ).arrange(RIGHT, buff=0.12).next_to(cards[1], DOWN, buff=0.35)
        reuse = VGroup(
            Arc(radius=0.42, start_angle=PI * 0.2, angle=PI * 1.45, color=TEAL_E),
            Arrow(LEFT * 0.05, RIGHT * 0.35, color=TEAL_E, buff=0),
        ).next_to(cards[2], DOWN, buff=0.32)

        self.play(Create(lvdm_arrows), run_time=1.2)
        self.wait(0.55)
        self.play(FadeIn(cascade), run_time=1.05)
        self.wait(0.55)
        self.play(FadeIn(reuse), run_time=1.05)

        note = caption("Different machinery, same pressure: keep context while the timeline grows.", SMALL_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(5.6)

    def scene_9_summary(self):
        title = caption("Long video = memory + hierarchy", TITLE_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.45)

        raw = soft_card("short clip model", "small temporal window", RED_C, 2.7, 0.9).shift(LEFT * 4.3 + UP * 0.1)
        anchors = soft_card("keyframe plan", "global story anchors", PRIMARY, 2.7, 0.9).shift(LEFT * 1.35 + UP * 0.1)
        fill = soft_card("interpolation", "local missing frames", TEAL_E, 2.7, 0.9).shift(RIGHT * 1.65 + UP * 0.1)
        video = soft_card("long video", "coherent over time", GREEN_C, 2.7, 0.9).shift(RIGHT * 4.65 + UP * 0.1)

        flow = VGroup(raw, anchors, fill, video)
        arrows = VGroup(
            Arrow(raw.get_right(), anchors.get_left(), buff=0.12, color=GREY_C),
            Arrow(anchors.get_right(), fill.get_left(), buff=0.12, color=GREY_C),
            Arrow(fill.get_right(), video.get_left(), buff=0.12, color=GREY_C),
        )
        self.play(FadeIn(raw), run_time=0.9)
        self.wait(0.45)
        for arrow, card in zip(arrows, flow[1:]):
            self.play(GrowArrow(arrow), FadeIn(card), run_time=1.15)
            self.wait(0.45)

        sheet = ImageMobject(str(CONTACT_SHEET)).set_width(8.6).to_edge(DOWN, buff=0.45)
        frame = SurroundingRectangle(sheet, color=ACCENT, buff=0.03, stroke_width=3)
        self.play(FadeIn(sheet), Create(frame), run_time=1.65)
        self.wait(9.6)
