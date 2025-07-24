from manim_animations.common import *

TEXT_1 = ["Siding", "Platform 1", "Platform 2"]
TEXT_2 = ["South Sand Bay", "Desert Plains"]

POINT_3 = (-TRAIN_LENGTH / 2, 0, 0)
POINT_4 = (TRAIN_LENGTH / 2, 0, 0)
POINT_2 = (POINT_3[0] - 1.5, 0, 0)
POINT_1 = (POINT_2[0] - TRAIN_LENGTH, 0, 0)
POINT_5 = (POINT_4[0] + 1.5, 0, 0)
POINT_6 = (POINT_5[0] + TRAIN_LENGTH, 0, 0)

RAIL_OFFSET_1 = 0.5
RAIL_OFFSET_2 = -0.5
TEXT_PADDING = 0.05
TEXT_OFFSET_1 = 0.4
TEXT_OFFSET_2 = 0.8
CURVE_HANDLE = 0.8

POINT_3_1 = (POINT_3[0], RAIL_OFFSET_1, 0)
POINT_3_2 = (POINT_3[0], RAIL_OFFSET_2, 0)
POINT_4_1 = (POINT_4[0], RAIL_OFFSET_1, 0)
POINT_4_2 = (POINT_4[0], RAIL_OFFSET_2, 0)


class RailLayout2(Scene):

    def construct(self):
        self.wait()

        text_1, text_1_width, text_1_height = create_text_object(TEXT_1, 0)
        text_1.shift(RIGHT * (POINT_1[0] + text_1_width / 2 + TEXT_PADDING) + UP * TEXT_OFFSET_1)

        text_2_1, text_2_1_width, text_2_1_height = create_text_object(TEXT_1, 1)
        text_2_1.shift(RIGHT * (POINT_3[0] + text_2_1_width / 2 + TEXT_PADDING) + UP * (TEXT_OFFSET_1 + RAIL_OFFSET_1))

        text_2_2, text_2_2_width, text_2_2_height = create_text_object(TEXT_1, 2)
        text_2_2.shift(RIGHT * (POINT_3[0] + text_2_2_width / 2 + TEXT_PADDING) + UP * (-TEXT_OFFSET_1 + RAIL_OFFSET_2))

        text_3, text_3_width, text_3_height = create_text_object(TEXT_1, 1)
        text_3.shift(RIGHT * (POINT_5[0] + text_3_width / 2 + TEXT_PADDING) + UP * TEXT_OFFSET_1)

        text_4_1, text_4_1_width, text_4_1_height = create_text_object(TEXT_2, 0)
        text_4_1.shift(RIGHT * (POINT_3[0] + text_4_1_width / 4 + TEXT_PADDING) + UP * (TEXT_OFFSET_2 + RAIL_OFFSET_1)).scale(0.5)

        text_4_2, text_4_2_width, text_4_2_height = create_text_object(TEXT_2, 0)
        text_4_2.shift(RIGHT * (POINT_3[0] + text_4_2_width / 4 + TEXT_PADDING) + UP * (-TEXT_OFFSET_2 + RAIL_OFFSET_2)).scale(0.5)

        text_5, text_5_width, text_5_height = create_text_object(TEXT_2, 1)
        text_5.shift(RIGHT * (POINT_5[0] + text_5_width / 4 + TEXT_PADDING) + UP * TEXT_OFFSET_2).scale(0.5)

        self.play(self.create_rails(), Write(text_1), Write(text_2_1), Write(text_2_2), Write(text_3), Write(text_4_1), Write(text_4_2), Write(text_5))

        path_1 = combine_paths(Line(POINT_1, POINT_2), self.create_curved_rail(POINT_2, POINT_3_1), Line(POINT_3_1, POINT_4_1))
        path_2 = combine_paths(Line(POINT_3_1, POINT_4_1), self.create_curved_rail(POINT_4_1, POINT_5), Line(POINT_5, POINT_6))
        path_3 = combine_paths(Line(POINT_6, POINT_5), self.create_curved_rail(POINT_5, POINT_4_2), Line(POINT_4_2, POINT_3_2))
        path_4 = combine_paths(Line(POINT_4_2, POINT_3_2), self.create_curved_rail(POINT_3_2, POINT_2), Line(POINT_2, POINT_1))

        trains_1, animate_trains_1, reset_trains_1 = animate_train(path_1, False, False, False)
        self.add(*trains_1)
        reset_trains_1.begin()
        self.update_mobjects(0)
        self.wait(0.5)
        self.play(animate_trains_1, run_time=2)

        trains_3, _, reset_trains_3 = animate_train(path_1, False, False, False)
        self.add(*trains_3)
        reset_trains_3.begin()
        self.update_mobjects(0)

        trains_2, animate_trains_2, _ = animate_train(path_2, False, False, False)
        self.wait(0.5)
        self.remove(*trains_1)
        self.play(animate_trains_2, run_time=2)
        self.wait(0.5)
        self.remove(*trains_2, *trains_3)

        for i in range(3):
            trains_2_1, animate_trains_2_1, reset_trains_2_1 = animate_train(path_1, False, False, False)
            trains_1_3, animate_trains_1_3, _ = animate_train(path_3, False, False, False)
            self.play(animate_trains_1_3, animate_trains_2_1, run_time=2)
            self.wait(0.5)
            self.remove(*trains_1_3, *trains_2_1)

            trains_2_2, animate_trains_2_2, reset_trains_2_2 = animate_train(path_2, False, False, False)
            trains_1_4, animate_trains_1_4, _ = animate_train(path_4, False, False, False)
            self.play(animate_trains_1_4, animate_trains_2_2, run_time=2)
            self.wait(0.5)
            if i < 2: self.remove(*trains_1_4, *trains_2_2)

        self.wait()

    @staticmethod
    def create_rails():
        rail_1 = Line(POINT_1, POINT_2, stroke_color=SIDING_COLOR, stroke_width=RAIL_STROKE_WIDTH)
        rail_2_1 = RailLayout2.create_curved_rail(POINT_2, POINT_3_1)
        rail_2_2 = RailLayout2.create_curved_rail(POINT_2, POINT_3_2)
        rail_3_1 = Line(POINT_3_1, POINT_4_1, stroke_color=PLATFORM_COLOR, stroke_width=RAIL_STROKE_WIDTH)
        rail_3_2 = Line(POINT_3_2, POINT_4_2, stroke_color=PLATFORM_COLOR, stroke_width=RAIL_STROKE_WIDTH)
        rail_4_1 = RailLayout2.create_curved_rail(POINT_4_1, POINT_5)
        rail_4_2 = RailLayout2.create_curved_rail(POINT_4_2, POINT_5)
        rail_5 = Line(POINT_5, POINT_6, stroke_color=PLATFORM_COLOR, stroke_width=RAIL_STROKE_WIDTH)
        return Succession(Create(rail_1), AnimationGroup(Create(VGroup(rail_2_1, rail_3_1, rail_4_1)), Create(VGroup(rail_2_2, rail_3_2, rail_4_2))), Create(rail_5), run_time=1)

    @staticmethod
    def create_curved_rail(point_1, point_2):
        sign = 1 if point_2[0] > point_1[0] else -1
        handle_1 = (point_1[0] + CURVE_HANDLE * sign, point_1[1], 0)
        handle_2 = (point_2[0] - CURVE_HANDLE * sign, point_2[1], 0)
        return CubicBezier(point_1, handle_1, handle_2, point_2, stroke_color=GRAY, stroke_width=RAIL_STROKE_WIDTH)
