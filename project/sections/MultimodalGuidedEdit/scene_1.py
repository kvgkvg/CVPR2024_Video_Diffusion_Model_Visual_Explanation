from section_common import *


class Scene1(GuidedScene):
    scene_number = 1

    def construct(self):
        heading = title("One sentence, many valid videos")
        prompt = panel('"make the person dance energetically"', INSTRUCTION, 6.0, 1.0, SMALL_SIZE).move_to(UP * 1.95)
        self.play(Write(heading), run_time=1.4)
        self.cue(0.6)
        self.play(FadeIn(prompt), run_time=1.4)

        cards = VGroup(*[
            RoundedRectangle(
                width=1.55,
                height=0.9,
                corner_radius=0.1,
                color=MOTION if index % 2 == 0 else APPEARANCE,
                fill_color=MOTION if index % 2 == 0 else APPEARANCE,
                fill_opacity=0.07,
            )
            for index in range(12)
        ]).arrange_in_grid(rows=3, cols=4, buff=(0.35, 0.25)).move_to(DOWN * 0.3)
        people = VGroup(*[
            person_icon(
                MOTION if index % 2 == 0 else APPEARANCE,
                0.27 + 0.02 * (index % 3),
                -0.55 + 0.1 * index,
            ).move_to(card.get_center() + RIGHT * (0.16 if index % 2 else -0.16))
            for index, card in enumerate(cards)
        ])
        possibilities = VGroup(cards, people)
        many = label("many plausible trajectories, rhythms, and appearances", GREY, SMALL_SIZE).next_to(cards, DOWN, buff=0.2)
        self.cue(6.8)
        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.08), run_time=1.8)
        self.cue(12.0)
        self.play(LaggedStart(*[FadeIn(person) for person in people], lag_ratio=0.07), Write(many), run_time=2.0)
        self.cue(15.1)
        self.play(Indicate(prompt, color=WHITE), run_time=1.5)

        constraints = VGroup(
            pill("pose fixes trajectory", MOTION),
            pill("audio fixes rhythm", AUDIO),
            pill("reference fixes identity", APPEARANCE),
        ).arrange(RIGHT, buff=0.55).to_edge(DOWN, buff=0.3)
        self.cue(20.6)
        self.play(FadeIn(constraints[0]), *[cards[i].animate.set_opacity(0.12) for i in range(4, 12)], *[people[i].animate.set_opacity(0.12) for i in range(4, 12)], run_time=1.6)
        self.cue(24.4)
        self.play(FadeIn(constraints[1]), *[cards[i].animate.set_opacity(0.12) for i in (1, 2, 3)], *[people[i].animate.set_opacity(0.12) for i in (1, 2, 3)], run_time=1.4)
        self.cue(26.7)
        self.play(FadeIn(constraints[2]), cards[0].animate.set_color(ACCENT), people[0].animate.set_color(ACCENT), run_time=1.4)

        chosen = VGroup(cards[0], people[0])
        target_card = panel("the intended edit", ACCENT, 3.2, 1.3, BODY_SIZE).move_to(DOWN * 0.05)
        self.cue(29.9)
        self.play(
            FadeOut(many),
            *[FadeOut(cards[i]) for i in range(1, 12)],
            *[FadeOut(people[i]) for i in range(1, 12)],
            ReplacementTransform(chosen, target_card),
            run_time=2.5,
        )
        focus = SurroundingRectangle(target_card, color=ACCENT, buff=0.18)
        self.cue(34.3)
        self.play(Create(focus), run_time=1.4)
        shrink = label("each modality removes a different ambiguity", SECONDARY, BODY_SIZE).next_to(target_card, DOWN, buff=0.35)
        self.cue(38.8)
        self.play(Write(shrink), Indicate(target_card, color=WHITE), run_time=2.0)
        self.finish_to_audio()
