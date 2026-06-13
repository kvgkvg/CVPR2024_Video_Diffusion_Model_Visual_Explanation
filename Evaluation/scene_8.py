from section_common import *


class Scene8(EvalScene):
    scene_number = 8

    def construct(self):
        heading = title("CLIP can recognize nouns and miss relations")
        self.play(Write(heading), run_time=1.4)

        prompt = panel(
            "person on a horse · in air over a gate · grass · people · trees",
            ALIGNMENT, 10.8, 0.85, SMALL_SIZE,
        ).move_to(UP * 2.25)
        self.cue(4.2)
        self.play(FadeIn(prompt), run_time=1.3)
        self.cue(7.0)
        self.play(Indicate(prompt, color=ALIGNMENT), run_time=1.2)

        def photo_card(filename, caption, color):
            image = image_asset(filename, width=5.45, section=SECTION)
            frame = SurroundingRectangle(image, color=color, buff=0.06, corner_radius=0.12)
            cap = label(caption, color, SMALL_SIZE, weight=BOLD).next_to(frame, DOWN, buff=0.16)
            return Group(frame, image, cap)

        bad = photo_card("clip_relation_missing.png", "nouns present · relation missing", FAILURE)
        good = photo_card("clip_relation_satisfied.png", "relation satisfied", DIVERSITY)
        bad.move_to(LEFT * 3.25 + DOWN * 0.35)
        good.move_to(RIGHT * 3.25 + DOWN * 0.35)

        self.cue(12.2)
        self.play(FadeIn(bad), run_time=1.4)
        bad_relation = pill("not airborne · not over gate", FAILURE).next_to(bad, DOWN, buff=0.25)
        self.cue(16.0)
        self.play(FadeIn(bad_relation), Circumscribe(bad[0], color=FAILURE), run_time=1.4)

        self.cue(19.4)
        self.play(FadeIn(good), run_time=1.4)
        good_relation = pill("airborne + over gate", DIVERSITY).next_to(good, DOWN, buff=0.25)
        self.cue(21.5)
        self.play(FadeIn(good_relation), Circumscribe(good[0], color=DIVERSITY), run_time=1.3)

        bad_score = pill("CLIPScore 24.3", ALIGNMENT).next_to(bad, UP, buff=0.18)
        good_score = pill("CLIPScore 21.3", ALIGNMENT).next_to(good, UP, buff=0.18)
        self.cue(23.3)
        self.play(FadeOut(prompt), run_time=0.5)
        self.cue(24.0)
        self.play(FadeIn(bad_score), FadeIn(good_score), run_time=1.3)
        wrong = label("higher score, less faithful", FAILURE, BODY_SIZE).to_edge(DOWN, buff=0.22)
        self.cue(27.0)
        self.play(Write(wrong), Indicate(bad_score, color=FAILURE), run_time=1.5)

        concepts = VGroup(
            pill("person", QUALITY), pill("horse", QUALITY), pill("outdoor", QUALITY),
        ).arrange(RIGHT, buff=0.45).move_to(UP * 0.45)
        self.cue(30.5)
        self.play(
            FadeOut(bad), FadeOut(good),
            FadeOut(bad_relation), FadeOut(good_relation),
            FadeOut(bad_score), FadeOut(good_score), FadeOut(wrong),
            FadeIn(concepts),
            run_time=1.6,
        )
        self.cue(33.0)
        self.play(LaggedStart(*[Indicate(c, color=QUALITY) for c in concepts], lag_ratio=0.18), run_time=1.6)

        relation = panel("composition + spatial relationships", FAILURE, 5.8, 0.9, BODY_SIZE).move_to(DOWN * 0.75)
        self.cue(36.0)
        self.play(FadeIn(relation), run_time=1.2)
        self.cue(38.0)
        self.play(Circumscribe(relation, color=FAILURE), run_time=1.4)
        conclusion = label("high semantic score ≠ every prompt claim is visible", ALIGNMENT, BODY_SIZE).to_edge(DOWN, buff=0.25)
        self.cue(40.2)
        self.play(Write(conclusion), run_time=1.5)
        self.finish_to_audio()
