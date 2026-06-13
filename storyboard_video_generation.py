from pathlib import Path

from manim import *


# --- 3b1b-inspired palette ---
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

TITLE_SIZE = 48
SECTION_SIZE = 34
BODY_SIZE = 26
SMALL_SIZE = 20
MIN_SIZE = 18

ASSET_DIR = Path(__file__).parent / "assets"
CONTACT_SHEET = ASSET_DIR / "airport_storyboard_contact_sheet.png"
PANEL_DIR = ASSET_DIR / "airport_storyboard_panels"

PROMPT = (
    "Two men stand in the airport\n"
    "waiting room and stare at the\n"
    "airplane through the window."
)


def caption(text, size=BODY_SIZE, color=WHITE, weight=NORMAL):
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)


def image_panel(path, height=1.8):
    image = ImageMobject(str(path)).set_height(height)
    frame = SurroundingRectangle(image, color=BLUE_C, buff=0.02, stroke_width=2)
    return Group(image, frame)


def soft_card(title, subtitle, color=PRIMARY, width=2.8, height=1.05):
    box = RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=2,
        fill_color=BG,
        fill_opacity=0.82,
    )
    t = caption(title, SMALL_SIZE, color, BOLD)
    s = caption(subtitle, MIN_SIZE - 2, GREY_C)
    text = VGroup(t, s).arrange(DOWN, buff=0.12).move_to(box)
    return VGroup(box, text)


def glow_rect(mobject, color=ACCENT, buff=0.06):
    return SurroundingRectangle(mobject, color=color, buff=buff, stroke_width=4)


class StoryboardVideoGenerationExplainer(Scene):
    """A visual-first explanation of storyboard research directions in video diffusion."""

    def construct(self):
        self.camera.background_color = BG
        scenes = [
            self.scene_1_hook_image_first,
            self.scene_2_prompt_becomes_shots,
            self.scene_3_visual_prior_overlays,
            self.scene_4_concurrent_directions,
            self.scene_5_scripts,
            self.scene_6_boxes,
            self.scene_7_visual_tokens,
            self.scene_8_scene_graphs,
            self.scene_9_aha_summary,
        ]
        for i, scene in enumerate(scenes):
            scene()
            if i < len(scenes) - 1:
                self.play(FadeOut(*self.mobjects), run_time=0.9)
                self.wait(0.35)

    def make_storyboard_strip(self, height=1.55, buff=0.14):
        panels = Group(
            *[
                image_panel(PANEL_DIR / f"airport_storyboard_panel_{i}.png", height=height)
                for i in range(1, 5)
            ]
        ).arrange(RIGHT, buff=buff)
        return panels

    def scene_1_hook_image_first(self):
        title = caption("Storyboard Video Generation", TITLE_SIZE, PRIMARY, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.35)

        sheet = ImageMobject(str(CONTACT_SHEET)).set_width(12.4).shift(DOWN * 0.2)
        self.play(FadeIn(sheet, scale=0.96), run_time=1.75)
        self.wait(1.0)

        question = caption("Before making pixels, what should the movie know?", BODY_SIZE, ACCENT)
        question.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=1.0)
        self.wait(2.1)

    def scene_2_prompt_becomes_shots(self):
        prompt_box = RoundedRectangle(
            corner_radius=0.1,
            width=5.3,
            height=1.55,
            stroke_color=PRIMARY,
            stroke_width=2,
            fill_color=PRIMARY,
            fill_opacity=0.08,
        )
        prompt_text = caption(PROMPT, SMALL_SIZE, WHITE).move_to(prompt_box)
        prompt_group = VGroup(prompt_box, prompt_text).to_edge(UP, buff=0.55)
        self.play(FadeIn(prompt_group), run_time=1.1)
        self.wait(0.8)

        strip = self.make_storyboard_strip(height=1.45).shift(DOWN * 0.35)
        arrow = Arrow(prompt_group.get_bottom(), strip.get_top(), buff=0.18, color=GREY_C)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.25) for p in strip], lag_ratio=0.24), run_time=2.3)
        self.wait(1.0)

        labels = VGroup(
            caption("establish", MIN_SIZE, GREY_C),
            caption("characters", MIN_SIZE, GREY_C),
            caption("gaze", MIN_SIZE, GREY_C),
            caption("target", MIN_SIZE, GREY_C),
        )
        for label, panel in zip(labels, strip):
            label.next_to(panel, DOWN, buff=0.15)
        self.play(LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.14), run_time=1.0)
        self.wait(1.9)

    def scene_3_visual_prior_overlays(self):
        title = caption("The hidden middle: visual prior", SECTION_SIZE, ACCENT, BOLD).to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.15)

        panel = image_panel(PANEL_DIR / "airport_storyboard_panel_3.png", height=3.65).shift(DOWN * 0.15)
        self.play(FadeIn(panel), run_time=1.25)
        self.wait(0.8)

        image = panel[0]
        # Overlay approximate semantic structure on the real drawing.
        left_man = Rectangle(width=0.7, height=1.75, color=PRIMARY, stroke_width=3).move_to(
            image.get_center() + LEFT * 1.3 + DOWN * 0.15
        )
        right_man = Rectangle(width=0.65, height=1.45, color=SECONDARY, stroke_width=3).move_to(
            image.get_center() + LEFT * 0.15 + DOWN * 0.35
        )
        window = Rectangle(width=2.65, height=2.45, color=TEAL_E, stroke_width=3).move_to(
            image.get_center() + RIGHT * 1.25 + UP * 0.15
        )
        gaze_1 = Arrow(left_man.get_right(), window.get_center() + LEFT * 0.25, buff=0.08, color=YELLOW_C, stroke_width=3)
        gaze_2 = Arrow(right_man.get_right(), window.get_center() + LEFT * 0.1, buff=0.08, color=YELLOW_C, stroke_width=3)
        overlays = VGroup(left_man, right_man, window, gaze_1, gaze_2)

        concepts = VGroup(
            soft_card("location", "where things are", PRIMARY, 2.2, 0.8),
            soft_card("relations", "who looks where", YELLOW_C, 2.2, 0.8),
            soft_card("timing", "which shot next", SECONDARY, 2.2, 0.8),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.4)

        self.play(Create(left_man), Create(right_man), run_time=0.95)
        self.play(Create(window), GrowArrow(gaze_1), GrowArrow(gaze_2), run_time=1.25)
        self.play(FadeIn(concepts, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
        self.play(overlays.animate.set_opacity(0.35), concepts.animate.set_opacity(0.75), run_time=0.75)
        self.wait(0.85)

    def scene_4_concurrent_directions(self):
        title = caption("Concurrent work: four ways to encode the plan", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.15)

        strip = self.make_storyboard_strip(height=1.2, buff=0.1).shift(UP * 1.05)
        self.play(FadeIn(strip), run_time=1.25)
        self.wait(0.45)

        center = soft_card("storyboard", "condition", ACCENT, 2.0, 0.85).shift(DOWN * 0.25)
        self.play(FadeIn(center, scale=0.9), run_time=0.8)
        self.wait(0.35)

        directions = VGroup(
            soft_card("scripts", "VideoDirectorGPT\nFree-Bloom", PRIMARY, 2.55, 1.0),
            soft_card("boxes", "LLM-Grounded VDM\nDirecT2V", SECONDARY, 2.55, 1.0),
            soft_card("visual tokens", "VisorGPT", TEAL_E, 2.55, 1.0),
            soft_card("scene graphs", "Dysen-VDM", PURPLE_C, 2.55, 1.0),
        )
        directions.arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.45)

        arrows = VGroup(
            *[
                Arrow(center.get_bottom(), card.get_top(), buff=0.12, color=GREY_C, stroke_width=2)
                for card in directions
            ]
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.15)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in directions], lag_ratio=0.12), run_time=1.25)
        self.wait(2.0)

    def scene_5_scripts(self):
        title = caption("1. Scripts: plan the movie in words", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        methods = caption("VideoDirectorGPT / Free-Bloom", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(methods), run_time=1.15)

        strip = self.make_storyboard_strip(height=1.15, buff=0.12).to_edge(UP, buff=1.35)
        self.play(FadeIn(strip), run_time=1.15)
        self.wait(0.55)

        llm = soft_card("LLM director", "expand one prompt", PURPLE_C, 2.15, 0.82).shift(LEFT * 4.25 + DOWN * 1.05)
        script_lines = [
            ("shot_1", "airport room"),
            ("shot_2", "men by window"),
            ("shot_3", "follow gaze"),
            ("shot_4", "plane outside"),
        ]
        cards = VGroup()
        for shot, text in script_lines:
            box = RoundedRectangle(
                corner_radius=0.06,
                width=2.35,
                height=0.78,
                stroke_color=PRIMARY,
                stroke_width=2,
                fill_color=BG,
                fill_opacity=0.84,
            )
            body = VGroup(
                caption(shot, MIN_SIZE - 1, PRIMARY, BOLD),
                caption(text, MIN_SIZE - 2, WHITE),
                caption("camera + timing", MIN_SIZE - 5, GREY_C),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            body.move_to(box)
            cards.add(VGroup(box, body))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.28, 0.18)).shift(DOWN * 1.15 + RIGHT * 1.35)

        self.play(FadeIn(llm), GrowArrow(Arrow(strip.get_bottom(), llm.get_top(), buff=0.15, color=GREY_C)), run_time=1.0)
        self.wait(0.45)
        self.play(
            GrowArrow(Arrow(llm.get_right(), cards.get_left(), buff=0.15, color=GREY_C)),
            LaggedStart(*[FadeIn(card, shift=UP * 0.15) for card in cards], lag_ratio=0.12),
            run_time=1.65,
        )
        note = caption("Representation: ordered shot descriptions", SMALL_SIZE, ACCENT).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)

    def scene_6_boxes(self):
        title = caption("2. Boxes: ground each frame in space", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        methods = caption("LLM-Grounded VDM / DirecT2V", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(methods), run_time=1.15)

        panels = self.make_storyboard_strip(height=1.45, buff=0.13).shift(UP * 0.55)
        self.play(FadeIn(panels), run_time=1.15)
        self.wait(0.55)

        overlays = VGroup()
        for i, panel in enumerate(panels):
            image = panel[0]
            man_box = Rectangle(width=0.5, height=1.0, color=PRIMARY, stroke_width=3).move_to(
                image.get_center() + LEFT * (0.65 - 0.1 * i) + DOWN * 0.05
            )
            window_box = Rectangle(width=0.9, height=0.9, color=TEAL_E, stroke_width=3).move_to(
                image.get_center() + RIGHT * 0.62 + UP * 0.05
            )
            plane_box = Rectangle(width=0.75, height=0.32, color=YELLOW_C, stroke_width=3).move_to(
                image.get_center() + RIGHT * 0.73 + UP * 0.1
            )
            overlays.add(VGroup(man_box, window_box, plane_box))

        self.play(LaggedStart(*[Create(o) for o in overlays], lag_ratio=0.18), run_time=1.75)
        self.wait(0.65)

        condition = soft_card("box condition", "object + position + frame", SECONDARY, 3.2, 0.85)
        condition.to_edge(DOWN, buff=0.55)
        self.play(GrowArrow(Arrow(panels.get_bottom(), condition.get_top(), buff=0.15, color=GREY_C)), FadeIn(condition), run_time=1.15)
        self.wait(2.0)

    def scene_7_visual_tokens(self):
        title = caption("3. Visual tokens: turn layout into a language", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        methods = caption("VisorGPT", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(methods), run_time=1.15)

        panel = image_panel(PANEL_DIR / "airport_storyboard_panel_3.png", height=3.0).shift(LEFT * 3.3 + DOWN * 0.15)
        self.play(FadeIn(panel), run_time=1.15)
        self.wait(0.55)

        bbox = Rectangle(width=0.72, height=1.35, color=PRIMARY, stroke_width=3).move_to(panel[0].get_center() + LEFT * 0.55 + DOWN * 0.25)
        mask = RoundedRectangle(corner_radius=0.06, width=1.75, height=1.25, color=TEAL_E, stroke_width=3).move_to(
            panel[0].get_center() + RIGHT * 0.9 + UP * 0.2
        )
        keypoint = Dot(panel[0].get_center() + LEFT * 1.1 + UP * 0.35, color=YELLOW_C, radius=0.07)
        self.play(Create(bbox), Create(mask), FadeIn(keypoint), run_time=1.25)
        self.wait(0.6)

        token_rows = VGroup(
            caption("[BBOX person x1 y1 x2 y2]", MIN_SIZE, PRIMARY),
            caption("[MASK window region]", MIN_SIZE, TEAL_E),
            caption("[KEYPOINT gaze anchor]", MIN_SIZE, YELLOW_C),
            caption("[SEP] [NEXT FRAME]", MIN_SIZE, GREY_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).shift(RIGHT * 2.55 + DOWN * 0.05)
        token_box = SurroundingRectangle(token_rows, color=TEAL_E, buff=0.25, corner_radius=0.06)
        self.play(
            GrowArrow(Arrow(panel.get_right(), token_box.get_left(), buff=0.15, color=GREY_C)),
            FadeIn(VGroup(token_box, token_rows), shift=LEFT * 0.15),
            run_time=1.3,
        )

        note = caption("The LLM no longer sees only words; it sees visual-prior tokens.", SMALL_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)

    def scene_8_scene_graphs(self):
        title = caption("4. Scene graphs: track relations through time", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        methods = caption("Dysen-VDM", SMALL_SIZE, GREY_C).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(methods), run_time=1.15)

        panels = self.make_storyboard_strip(height=1.05, buff=0.12).to_edge(UP, buff=1.35)
        self.play(FadeIn(panels), run_time=1.15)
        self.wait(0.55)

        graphs = VGroup()
        relation_sets = [
            ("men", "in", "airport"),
            ("men", "look", "window"),
            ("gaze", "points", "plane"),
            ("plane", "outside", "window"),
        ]
        for left, rel, right in relation_sets:
            n1 = Circle(radius=0.28, color=PRIMARY, fill_opacity=0.18)
            n2 = Circle(radius=0.28, color=TEAL_E, fill_opacity=0.18).shift(RIGHT * 1.65)
            labels = VGroup(caption(left, MIN_SIZE - 3, PRIMARY), caption(right, MIN_SIZE - 3, TEAL_E))
            labels[0].move_to(n1)
            labels[1].move_to(n2)
            edge = Arrow(n1.get_right(), n2.get_left(), buff=0.06, color=GREY_C, stroke_width=2)
            rel_label = caption(rel, MIN_SIZE - 4, YELLOW_C).next_to(edge, UP, buff=0.04)
            g = VGroup(edge, rel_label, n1, n2, labels)
            gbox = SurroundingRectangle(g, color=PURPLE_C, buff=0.18, corner_radius=0.05)
            graphs.add(VGroup(gbox, g))
        graphs.arrange(RIGHT, buff=0.25).scale(0.9).shift(DOWN * 0.95)

        arrows = VGroup(
            *[
                Arrow(panels[i].get_bottom(), graphs[i].get_top(), buff=0.12, color=GREY_C, stroke_width=2)
                for i in range(4)
            ]
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.0)
        self.wait(0.35)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.12) for g in graphs], lag_ratio=0.16), run_time=1.55)

        note = caption("The representation remembers what changed, not just what appeared.", SMALL_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)

    def scene_9_aha_summary(self):
        prompt = soft_card("text prompt", "compressed intent", PRIMARY, 2.25, 0.85).shift(LEFT * 4.7)
        storyboard = Group(ImageMobject(str(CONTACT_SHEET)).set_width(4.3))
        storyboard.add(SurroundingRectangle(storyboard[0], color=ACCENT, buff=0.03, stroke_width=3))
        storyboard.shift(LEFT * 0.85)
        model = soft_card("video diffusion", "paint pixels", PURPLE_C, 2.35, 0.85).shift(RIGHT * 2.65)
        video = soft_card("coherent video", "same story world", GREEN_C, 2.35, 0.85).shift(RIGHT * 5.0)

        self.play(FadeIn(prompt), run_time=0.75)
        self.wait(0.3)
        self.play(GrowArrow(Arrow(prompt.get_right(), storyboard.get_left(), buff=0.1, color=GREY_C)), FadeIn(storyboard), run_time=1.25)
        self.wait(0.35)
        self.play(GrowArrow(Arrow(storyboard.get_right(), model.get_left(), buff=0.1, color=GREY_C)), FadeIn(model), run_time=1.1)
        self.wait(0.35)
        self.play(GrowArrow(Arrow(model.get_right(), video.get_left(), buff=0.1, color=GREY_C)), FadeIn(video), run_time=1.0)

        insight = caption("Plan the story world first. Generate frames second.", BODY_SIZE, ACCENT, BOLD)
        insight.to_edge(DOWN, buff=0.55)
        self.play(Write(insight), run_time=1.25)
        self.wait(3.0)
