from section_common import *


class Scene9(EvalScene):
    scene_number = 9

    def construct(self):
        heading = title("TIFA turns prompt claims into questions")
        self.play(Write(heading), run_time=1.4)

        prompt = panel("empty bedroom\nTV on a dresser", ALIGNMENT, 3.2, 1.25).move_to(LEFT * 4.4 + UP * 0.55)
        llm = panel("language model\ndecomposes claims", PRIMARY, 3.0, 1.25).move_to(UP * 0.55)
        questions = VGroup(
            panel("Is there a TV?", QUALITY, 3.0, 0.72),
            panel("Is it on a dresser?", TEMPORAL, 3.0, 0.72),
            panel("Is the room empty?", DIVERSITY, 3.0, 0.72),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 4.25 + UP * 0.1)
        first_arrow = edge_arrow(prompt, llm, RIGHT, LEFT, ALIGNMENT)
        q_arrows = VGroup(*[
            anchored_arrow(llm.get_edge_center(RIGHT), q.get_edge_center(LEFT), q[0].get_stroke_color(), buff=0.08)
            for q in questions
        ])
        self.cue(3.0)
        self.play(FadeIn(prompt), run_time=1.3)
        self.cue(7.0)
        self.play(Create(first_arrow), FadeIn(llm), run_time=1.3)
        for cue_time, arrow, question in zip((12.0, 17.2, 20.5), q_arrows, questions):
            self.cue(cue_time)
            self.play(Create(arrow), FadeIn(question), run_time=1.1)

        expected = label("expected answers: yes · yes · yes", ALIGNMENT, SMALL_SIZE).to_edge(DOWN, buff=0.35)
        self.cue(22.0)
        self.play(Write(expected), run_time=1.0)

        image = panel("generated image", PRIMARY, 3.1, 1.45, BODY_SIZE).move_to(LEFT * 4.1 + UP * 0.25)
        vqa = panel("visual question\nanswering", ALIGNMENT, 3.0, 1.25).move_to(UP * 0.25)
        answers = VGroup(
            panel("TV exists: yes", DIVERSITY, 3.2, 0.72),
            panel("on dresser: no", FAILURE, 3.2, 0.72),
            panel("room empty: yes", DIVERSITY, 3.2, 0.72),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 4.1 + UP * 0.05)
        answer_arrows = VGroup(
            edge_arrow(image, vqa, RIGHT, LEFT, PRIMARY),
            *[
                anchored_arrow(vqa.get_edge_center(RIGHT), answer.get_edge_center(LEFT), answer[0].get_stroke_color(), buff=0.08)
                for answer in answers
            ],
        )
        self.cue(23.5)
        self.play(
            FadeOut(prompt), FadeOut(llm), FadeOut(questions), FadeOut(first_arrow), FadeOut(q_arrows), FadeOut(expected),
            FadeIn(image), Create(answer_arrows[0]), FadeIn(vqa),
            run_time=1.6,
        )
        for cue_time, arrow, answer in zip((28.0, 30.5, 32.5), answer_arrows[1:], answers):
            self.cue(cue_time)
            self.play(Create(arrow), FadeIn(answer), run_time=1.0)

        diagnostic = SurroundingRectangle(answers[1], color=FAILURE, buff=0.15)
        self.cue(34.5)
        self.play(Create(diagnostic), Indicate(answers[1], color=FAILURE), run_time=1.4)
        final = label("missing claim: explicit evidence, not one opaque score", ALIGNMENT, BODY_SIZE).to_edge(DOWN, buff=0.3)
        final.scale_to_fit_width(12.0).to_edge(DOWN, buff=0.3)
        self.cue(39.0)
        self.play(Write(final), run_time=1.6)
        self.finish_to_audio()
