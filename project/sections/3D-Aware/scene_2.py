from section_common import *


class Scene2(AwareScene):
    scene_number = 2

    def construct(self):
        heading = title("Layered Neural Atlases: edit once")
        video = frame_strip(5, PRIMARY, 5.6, 1.4).move_to(LEFT * 3.6 + UP * 1.25)
        moving = VGroup()
        for index, frame in enumerate(video):
            person = subject_icon(ACCENT, 0.34).move_to(frame.get_center() + LEFT * 0.28 + RIGHT * 0.14 * index)
            moving.add(person)
        source = Group(video, moving)

        fg = atlas_grid(ACCENT, 2.7, 1.7).move_to(RIGHT * 3.5 + UP * 1.35)
        bg = atlas_grid(SECONDARY, 2.7, 1.7).move_to(RIGHT * 3.5 + DOWN * 1.3)
        fg_icon = subject_icon(ACCENT, 0.7).move_to(fg)
        bg_marks = VGroup(
            Line(bg.get_left() + RIGHT * 0.2, bg.get_right() + LEFT * 0.2, color=SECONDARY),
            Triangle(color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.16).scale(0.4).move_to(bg),
        )
        fg_group = Group(fg, fg_icon)
        bg_group = Group(bg, bg_marks)
        fg_label = label("foreground atlas", ACCENT, SMALL_SIZE).next_to(fg, UP, buff=0.15)
        bg_label = label("background atlas", SECONDARY, SMALL_SIZE).next_to(bg, DOWN, buff=0.15)
        split_fg = edge_arrow(source, fg_group, RIGHT, LEFT, ACCENT)
        split_bg = edge_arrow(source, bg_group, RIGHT, LEFT, SECONDARY)

        self.play(Write(heading), run_time=1.3)
        self.cue(3.8)
        self.play(LaggedStart(*[FadeIn(frame) for frame in video], lag_ratio=0.15), FadeIn(moving), run_time=2.3)
        self.cue(9.0)
        self.play(Create(split_fg), FadeIn(fg_group), Write(fg_label), run_time=2.2)
        self.cue(12.5)
        self.play(Create(split_bg), FadeIn(bg_group), Write(bg_label), run_time=2.2)

        mappings = VGroup(
            label("learned mappings", PURPLE, SMALL_SIZE).move_to(ORIGIN + RIGHT * 0.2),
            label("shared across every frame", WHITE, SMALL_SIZE).move_to(DOWN * 0.48 + RIGHT * 0.2),
        )
        self.cue(16.0)
        self.play(Write(mappings[0]), run_time=1.2)
        self.cue(19.9)
        self.play(Write(mappings[1]), run_time=1.3)

        edited_icon = subject_icon(ERROR, 0.7).move_to(fg)
        edit_tag = pill("edit once", ERROR, MIN_SIZE).next_to(fg, RIGHT, buff=0.2)
        self.cue(27.1)
        self.play(FadeIn(edit_tag), Transform(fg_icon, edited_icon), run_time=2.0)
        self.cue(30.6)
        self.play(
            *[person.animate.set_color(ERROR) for person in moving],
            LaggedStart(*[Indicate(frame, color=ERROR) for frame in video], lag_ratio=0.12),
            run_time=2.5,
        )
        result = label("one atlas edit → consistent video", ERROR, BODY_SIZE).to_edge(DOWN, buff=0.22)
        self.play(FadeOut(mappings), Write(result), run_time=1.6)
        self.finish_to_audio()
