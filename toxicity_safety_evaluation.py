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

ASSET_DIR = Path(__file__).parent / "assets" / "toxicity_safety"
PIPELINE_IMG = ASSET_DIR / "moderation_pipeline.png"
RED_TEAM_IMG = ASSET_DIR / "red_team_abstract.png"
STEERING_IMG = ASSET_DIR / "safe_diffusion_steering.png"


def caption(text, size=BODY_SIZE, color=WHITE, weight=NORMAL):
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)


def soft_card(title, subtitle, color=PRIMARY, width=2.8, height=0.95):
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


def image_card(path, width=7.0, color=PRIMARY):
    image = ImageMobject(str(path)).set_width(width)
    frame = SurroundingRectangle(image, color=color, buff=0.03, stroke_width=2)
    return Group(image, frame)


def pill(text, color=PRIMARY):
    label = caption(text, MIN_SIZE, color, BOLD)
    box = RoundedRectangle(
        corner_radius=0.12,
        width=max(1.25, label.width + 0.35),
        height=0.42,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.1,
        stroke_width=2,
    )
    return VGroup(box, label.move_to(box))


class ToxicitySafetyEvaluationExplainer(Scene):
    """Measuring and mitigating toxicity in video generation."""

    def construct(self):
        self.camera.background_color = BG
        scenes = [
            self.scene_1_hook,
            self.scene_2_goal_tension,
            self.scene_3_moderation_pipeline,
            self.scene_4_filter_failure,
            self.scene_5_measurement_map,
            self.scene_6_safe_diffusion,
            self.scene_7_concept_erasure,
            self.scene_8_red_teaming_loop,
            self.scene_9_summary,
        ]
        for index, scene in enumerate(scenes):
            scene()
            if index < len(scenes) - 1:
                self.play(FadeOut(*self.mobjects), run_time=1.0)
                self.wait(0.45)

    def scene_1_hook(self):
        title = caption("Measuring and Mitigating Toxicity", TITLE_SIZE, PRIMARY, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        panel = image_card(PIPELINE_IMG, width=11.6, color=PRIMARY).shift(DOWN * 0.05)
        self.play(FadeIn(panel, scale=0.97), run_time=2.0)
        self.wait(1.0)

        question = caption("When does a green check mark actually mean safe?", BODY_SIZE, ACCENT)
        question.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=1.0)
        self.wait(7.0)

    def scene_2_goal_tension(self):
        title = caption("Moderation is a balance, not a switch", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.3)

        left = soft_card("keep users safe", "block harmful outputs", GREEN_C, 3.2, 0.95).shift(LEFT * 3.75)
        right = soft_card("protect creativity", "avoid over-censoring", PRIMARY, 3.2, 0.95).shift(RIGHT * 3.75)
        bar = Line(LEFT * 4.4, RIGHT * 4.4, color=GREY_C, stroke_width=5).shift(DOWN * 0.55)
        fulcrum = Triangle(color=ACCENT, fill_opacity=0.2).scale(0.45).next_to(bar, DOWN, buff=0.02)
        beam = Line(LEFT * 3.6, RIGHT * 3.6, color=ACCENT, stroke_width=4).move_to(bar)

        self.play(FadeIn(left), FadeIn(right), run_time=1.15)
        self.wait(0.7)
        self.play(Create(bar), FadeIn(fulcrum), Create(beam), run_time=1.1)
        self.wait(0.8)

        safe_zone = VGroup(
            pill("violence", RED_C),
            pill("explicit", RED_C),
            pill("hate", RED_C),
        ).arrange(RIGHT, buff=0.18).next_to(left, DOWN, buff=0.7)
        creative_zone = VGroup(
            pill("fiction", PRIMARY),
            pill("art", PRIMARY),
            pill("education", PRIMARY),
        ).arrange(RIGHT, buff=0.18).next_to(right, DOWN, buff=0.7)
        self.play(FadeIn(safe_zone, shift=UP * 0.1), FadeIn(creative_zone, shift=UP * 0.1), run_time=1.1)
        self.wait(7.0)

    def scene_3_moderation_pipeline(self):
        title = caption("The common defense: gates around the model", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.3)

        prompt = soft_card("input prompt", "text check", PRIMARY, 2.25, 0.82).shift(LEFT * 5.0 + UP * 0.3)
        input_gate = soft_card("moderator", "before generation", GREEN_C, 2.35, 0.82).shift(LEFT * 2.3 + UP * 0.3)
        model = soft_card("video model", "generate frames", PURPLE_C, 2.35, 0.82).shift(RIGHT * 0.35 + UP * 0.3)
        output_gate = soft_card("moderator", "after generation", GREEN_C, 2.35, 0.82).shift(RIGHT * 3.0 + UP * 0.3)
        video = soft_card("video", "image + text + motion", PRIMARY, 2.25, 0.82).shift(RIGHT * 5.45 + UP * 0.3)
        flow = VGroup(prompt, input_gate, model, output_gate, video)
        arrows = VGroup(
            *[
                Arrow(flow[i].get_right(), flow[i + 1].get_left(), buff=0.12, color=GREY_C)
                for i in range(len(flow) - 1)
            ]
        )

        self.play(FadeIn(prompt), run_time=0.8)
        for arrow, card in zip(arrows, flow[1:]):
            self.play(GrowArrow(arrow), FadeIn(card), run_time=0.9)
            self.wait(0.25)

        checks = VGroup(
            soft_card("text", "prompt + captions", TEAL_E, 2.2, 0.72),
            soft_card("image", "frames", TEAL_E, 2.2, 0.72),
            soft_card("video", "motion context", TEAL_E, 2.2, 0.72),
        ).arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in checks], lag_ratio=0.14), run_time=1.1)
        self.wait(7.0)

    def scene_4_filter_failure(self):
        title = caption("Why gates fail: surface form is not intent", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(Write(title), run_time=1.3)

        panel = image_card(RED_TEAM_IMG, width=7.0, color=YELLOW_C).shift(LEFT * 2.8 + DOWN * 0.1)
        self.play(FadeIn(panel, scale=0.97), run_time=1.7)
        self.wait(0.7)

        cards = VGroup(
            soft_card("same intent", "many wordings", PRIMARY, 2.8, 0.82),
            soft_card("simple filter", "keyword surface", GREEN_C, 2.8, 0.82),
            soft_card("hidden failure", "needs testing", RED_C, 2.8, 0.82),
        ).arrange(DOWN, buff=0.32).shift(RIGHT * 3.8 + DOWN * 0.05)
        arrows = VGroup(
            Arrow(cards[0].get_bottom(), cards[1].get_top(), buff=0.12, color=GREY_C),
            Arrow(cards[1].get_bottom(), cards[2].get_top(), buff=0.12, color=GREY_C),
        )
        self.play(FadeIn(cards[0], shift=LEFT * 0.15), run_time=0.75)
        self.play(GrowArrow(arrows[0]), FadeIn(cards[1], shift=LEFT * 0.15), run_time=0.9)
        self.play(GrowArrow(arrows[1]), FadeIn(cards[2], shift=LEFT * 0.15), run_time=0.9)

        note = caption("Adversarial tests search semantic space, not just banned words.", SMALL_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(8.0)

    def scene_5_measurement_map(self):
        title = caption("Measurement turns safety into a map", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.3)

        rows = ["prompt", "frame", "motion", "audio"]
        cols = ["violence", "explicit", "hate", "self-harm"]
        grid = VGroup()
        cells = {}
        for r, row in enumerate(rows):
            row_label = caption(row, MIN_SIZE, PRIMARY).move_to(LEFT * 4.8 + UP * (1.5 - r * 0.65))
            grid.add(row_label)
            for c, col in enumerate(cols):
                value = (r * 3 + c * 2) % 5
                color = [GREEN_C, GREEN_C, YELLOW_C, RED_C, MAROON_C][value]
                cell = Square(side_length=0.48, color=color, fill_color=color, fill_opacity=0.22)
                cell.move_to(LEFT * 2.5 + RIGHT * c * 1.2 + UP * (1.5 - r * 0.65))
                cells[(r, c)] = cell
                grid.add(cell)
        col_labels = VGroup(
            *[
                caption(col, MIN_SIZE - 2, GREY_C).move_to(LEFT * 2.5 + RIGHT * i * 1.2 + UP * 2.05)
                for i, col in enumerate(cols)
            ]
        )
        grid.add(col_labels)
        frame = SurroundingRectangle(VGroup(*cells.values()), color=PRIMARY, buff=0.22, stroke_width=2)

        self.play(FadeIn(col_labels), run_time=0.8)
        self.play(Create(frame), LaggedStart(*[FadeIn(cells[k]) for k in cells], lag_ratio=0.035), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(m) for m in grid[:4]], lag_ratio=0.08), run_time=0.9)
        self.wait(0.8)

        evaluator = soft_card("evaluator", "score + human review", PURPLE_C, 3.0, 0.9).shift(RIGHT * 4.0 + UP * 0.7)
        report = soft_card("risk report", "where the model fails", ACCENT, 3.0, 0.9).shift(RIGHT * 4.0 + DOWN * 0.9)
        self.play(GrowArrow(Arrow(frame.get_right(), evaluator.get_left(), buff=0.2, color=GREY_C)), FadeIn(evaluator), run_time=1.0)
        self.play(GrowArrow(Arrow(evaluator.get_bottom(), report.get_top(), buff=0.12, color=GREY_C)), FadeIn(report), run_time=1.0)
        self.wait(8.0)

    def scene_6_safe_diffusion(self):
        title = caption("Mitigation 1: steer the diffusion trajectory", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.3)

        panel = image_card(STEERING_IMG, width=9.6, color=PRIMARY).shift(DOWN * 0.2)
        self.play(FadeIn(panel, scale=0.97), run_time=1.8)
        self.wait(0.8)

        attract = pill("toward prompt", PRIMARY).shift(LEFT * 3.2 + DOWN * 2.85)
        repel = pill("away from unsafe region", RED_C).shift(RIGHT * 0.3 + DOWN * 2.85)
        result = pill("safer output", GREEN_C).shift(RIGHT * 4.0 + DOWN * 2.85)
        self.play(FadeIn(attract), FadeIn(repel), FadeIn(result), run_time=1.1)
        self.wait(8.0)

    def scene_7_concept_erasure(self):
        title = caption("Mitigation 2: erase a concept from the model", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.3)

        original = soft_card("trained model", "knows many concepts", PRIMARY, 3.0, 0.92).shift(LEFT * 4.2 + UP * 0.2)
        concept = soft_card("target concept", "remove direction", RED_C, 2.8, 0.92).shift(LEFT * 0.65 + UP * 1.25)
        edited = soft_card("edited model", "less likely to generate it", GREEN_C, 3.0, 0.92).shift(RIGHT * 3.4 + UP * 0.2)
        arrow1 = Arrow(original.get_right(), concept.get_left(), buff=0.15, color=GREY_C)
        arrow2 = Arrow(concept.get_right(), edited.get_left(), buff=0.15, color=GREY_C)
        self.play(FadeIn(original), run_time=0.85)
        self.play(GrowArrow(arrow1), FadeIn(concept), run_time=1.0)
        self.play(GrowArrow(arrow2), FadeIn(edited), run_time=1.0)
        self.wait(0.8)

        weights = VGroup()
        for i in range(9):
            node = Circle(radius=0.16, color=PRIMARY if i != 4 else RED_C, fill_opacity=0.18)
            node.shift(LEFT * 0.7 + RIGHT * (i % 3) * 0.55 + DOWN * (i // 3) * 0.45 + DOWN * 1.2)
            weights.add(node)
        slash = VGroup(
            Line(weights[4].get_corner(UL), weights[4].get_corner(DR), color=RED_C, stroke_width=4),
            Line(weights[4].get_corner(DL), weights[4].get_corner(UR), color=RED_C, stroke_width=4),
        )
        risk = soft_card("watch out", "overblocking + misalignment", ACCENT, 3.35, 0.82).shift(RIGHT * 3.25 + DOWN * 1.45)
        self.play(LaggedStart(*[FadeIn(n) for n in weights], lag_ratio=0.05), run_time=1.0)
        self.play(Create(slash), FadeIn(risk), run_time=1.0)
        self.wait(7.5)

    def scene_8_red_teaming_loop(self):
        title = caption("Red teaming: make failure visible before release", SECTION_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.3)

        steps = VGroup(
            soft_card("generate tests", "benign + adversarial", PRIMARY, 2.7, 0.82),
            soft_card("measure failures", "model + moderator", RED_C, 2.7, 0.82),
            soft_card("patch defense", "rules or model update", GREEN_C, 2.7, 0.82),
            soft_card("repeat", "new attack surface", ACCENT, 2.7, 0.82),
        ).arrange_in_grid(rows=2, cols=2, buff=(1.0, 0.65)).shift(DOWN * 0.1)
        arrows = VGroup(
            Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.15, color=GREY_C),
            Arrow(steps[1].get_bottom(), steps[3].get_top(), buff=0.15, color=GREY_C),
            Arrow(steps[3].get_left(), steps[2].get_right(), buff=0.15, color=GREY_C),
            Arrow(steps[2].get_top(), steps[0].get_bottom(), buff=0.15, color=GREY_C),
        )
        self.play(FadeIn(steps[0]), run_time=0.8)
        for arrow, card in zip(arrows, [steps[1], steps[3], steps[2], steps[0]]):
            self.play(GrowArrow(arrow), FadeIn(card), run_time=0.9)
            self.wait(0.25)

        note = caption("Red teaming is useful because it is iterative, not because it is exhaustive.", SMALL_SIZE, ACCENT)
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(8.0)

    def scene_9_summary(self):
        title = caption("Safety evaluation is a loop", TITLE_SIZE, ACCENT, BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.4)

        items = VGroup(
            soft_card("moderate", "input + output", PRIMARY, 2.4, 0.82),
            soft_card("measure", "risk map", TEAL_E, 2.4, 0.82),
            soft_card("attack", "red team", RED_C, 2.4, 0.82),
            soft_card("mitigate", "steer + erase", GREEN_C, 2.4, 0.82),
        ).arrange(RIGHT, buff=0.55).shift(UP * 0.2)
        arrows = VGroup(
            *[
                Arrow(items[i].get_right(), items[(i + 1) % len(items)].get_left(), buff=0.12, color=GREY_C)
                for i in range(len(items) - 1)
            ]
        )
        loop_back = CurvedArrow(items[-1].get_bottom(), items[0].get_bottom(), angle=-TAU / 4, color=GREY_C)
        self.play(FadeIn(items[0]), run_time=0.8)
        for arrow, card in zip(arrows, items[1:]):
            self.play(GrowArrow(arrow), FadeIn(card), run_time=0.95)
            self.wait(0.25)
        self.play(Create(loop_back), run_time=1.1)

        insight = caption(
            "The goal is not perfect certainty. It is continuous pressure against misuse.",
            SMALL_SIZE,
            ACCENT,
        )
        if insight.width > 12.2:
            insight.set_width(12.2)
        insight.to_edge(DOWN, buff=0.65)
        self.play(FadeIn(insight, shift=UP * 0.12), run_time=1.0)
        self.wait(10.5)
