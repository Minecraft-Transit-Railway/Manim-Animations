from manim_animations.common import *

TEXT_1 = ["Siding", "Platform 1"]
TEXT_2 = ["Desert Plains", "South Sand Bay"]

POINT_3 = (-TRAIN_LENGTH / 2, 0, 0)
POINT_4 = (TRAIN_LENGTH / 2, 0, 0)
POINT_2 = (POINT_3[0] - 1.5, 0, 0)
POINT_1 = (POINT_2[0] - TRAIN_LENGTH, 0, 0)
POINT_5 = (POINT_4[0] + 1.5, 0, 0)
POINT_6 = (POINT_5[0] + TRAIN_LENGTH, 0, 0)

TEXT_PADDING = 0.05
TEXT_OFFSET_1 = 0.4
TEXT_OFFSET_2 = 0.8


class RailLayout1(Scene):

    def construct(self):
        self.wait()

        text_1, text_1_width, text_1_height = create_text_object(TEXT_1, 0)
        text_1.shift(RIGHT * (POINT_1[0] + text_1_width / 2 + TEXT_PADDING) + UP * TEXT_OFFSET_1)

        text_2, text_2_width, text_2_height = create_text_object(TEXT_1, 1)
        text_2.shift(RIGHT * (POINT_3[0] + text_2_width / 2 + TEXT_PADDING) + UP * TEXT_OFFSET_1)

        text_3, text_3_width, text_3_height = create_text_object(TEXT_1, 1)
        text_3.shift(RIGHT * (POINT_5[0] + text_3_width / 2 + TEXT_PADDING) + UP * TEXT_OFFSET_1)

        text_4, text_4_width, text_4_height = create_text_object(TEXT_2, 0)
        text_4.shift(RIGHT * (POINT_3[0] + text_4_width / 4 + TEXT_PADDING) + UP * TEXT_OFFSET_2).scale(0.5)

        text_5, text_5_width, text_5_height = create_text_object(TEXT_2, 1)
        text_5.shift(RIGHT * (POINT_5[0] + text_5_width / 4 + TEXT_PADDING) + UP * TEXT_OFFSET_2).scale(0.5)

        self.play(self.create_rails(), Write(text_1), Write(text_2), Write(text_3), Write(text_4), Write(text_5))

        for i in range(2):
            trains_1_1, animate_trains_1_1, reset_trains_1_1 = animate_train(Line(POINT_1, POINT_4), False, False, False)
            self.add(*trains_1_1)
            reset_trains_1_1.begin()
            self.update_mobjects(0)
            self.wait(0.5)
            self.play(animate_trains_1_1, run_time=2)

            trains_2_1, animate_trains_2_1, reset_trains_2_1 = animate_train(Line(POINT_1, POINT_4), False, False, False)
            if i == 1:
                self.add(*trains_2_1)
                reset_trains_2_1.begin()
                self.update_mobjects(0)

            trains_1_2, animate_trains_1_2, _ = animate_train(Line(POINT_3, POINT_6), False, False, False)
            self.wait(0.5)
            self.remove(*trains_1_1)
            if i == 0:
                self.play(animate_trains_1_2, run_time=2)
            else:
                self.play(animate_trains_1_2, animate_trains_2_1, run_time=2)

            self.wait(0.5)
            if i == 0:
                trains_2_2, animate_trains_2_2, _ = animate_train(Line(POINT_3, POINT_6), False, False, False)
                trains_1_3, animate_trains_1_3, _ = animate_train(Line(POINT_6, POINT_1), False, False, False)
                self.remove(*trains_1_2)
                self.play(animate_trains_1_3, run_time=2)
                self.remove(*trains_1_3)
            else:
                point_middle = ((POINT_4[0] + POINT_5[0]) / 2, 0, 0)
                trains_2_2, animate_trains_2_2, _ = animate_train(Line(POINT_3, point_middle), False, False, False)
                trains_1_3, animate_trains_1_3, _ = animate_train(Line(POINT_6, point_middle), False, False, False)
                self.remove(*trains_1_2)
                self.remove(*trains_2_1)
                self.play(animate_trains_1_3, animate_trains_2_2, run_time=2)

                circle = Circle(0.5, fill_opacity=0.5, fill_color=ORANGE, stroke_color=ORANGE).shift(np.array(point_middle)).set_z_index(-1)
                for j in range(3):
                    self.play(GrowFromCenter(circle), run_time=0.5)
                    if j < 2: self.play(FadeOut(circle), run_time=0.2)

        self.wait()

    @staticmethod
    def create_rails():
        rail_1 = Line(POINT_1, POINT_2, stroke_color=SIDING_COLOR, stroke_width=RAIL_STROKE_WIDTH).set_z_index(-2)
        rail_2 = Line(POINT_2, POINT_3, stroke_color=GRAY, stroke_width=RAIL_STROKE_WIDTH).set_z_index(-2)
        rail_3 = Line(POINT_3, POINT_4, stroke_color=PLATFORM_COLOR, stroke_width=RAIL_STROKE_WIDTH).set_z_index(-2)
        rail_4 = Line(POINT_4, POINT_5, stroke_color=GRAY, stroke_width=RAIL_STROKE_WIDTH).set_z_index(-2)
        rail_5 = Line(POINT_5, POINT_6, stroke_color=PLATFORM_COLOR, stroke_width=RAIL_STROKE_WIDTH).set_z_index(-2)
        return Create(VGroup(rail_1, rail_2, rail_3, rail_4, rail_5))
