import random

from manim_animations.common import *

TEXT = ["Two-Way", "One-Way", "Platform", "Siding", "Turn Back"]

RAIL_PADDING = EDGE_PADDING * 4
RAIL_LEFT = HALF_WIDTH - RAIL_PADDING * 2 - TRAIN_LENGTH
RAIL_RIGHT = HALF_WIDTH


class RailTypes(Scene):

    def construct(self):
        self.add(*self.draw_background())
        self.wait()

        rail_1 = self.create_rail(GRAY, 3, False)
        self.play(self.create_text(0, 3), Create(rail_1))

        _, animate_trains_1_1, _ = animate_train(rail_1, False, True, True)
        _, animate_trains_1_2, _ = animate_train(rail_1, True, True, True)
        self.play(Succession(animate_trains_1_1, animate_trains_1_2, run_time=5, rate_func=linear))

        rail_2 = self.create_rail(GRAY, 1.5, False)
        self.play(self.create_text(1, 1.5), Create(rail_2), create_one_way_arrows(rail_2))

        _, animate_trains_2_1, _ = animate_train(rail_2, False, True, True)
        _, animate_trains_2_2, _ = animate_train(rail_2, False, True, True)
        self.play(Succession(animate_trains_2_1, animate_trains_2_2, run_time=5, rate_func=linear))

        passenger_dots, add_passengers, animate_passengers = self.create_passengers()
        rail_3 = self.create_rail(PLATFORM_COLOR, 0, False)
        self.play(self.create_text(2, 0), Create(rail_3), add_passengers)

        _, animate_trains_3_1, reset_trains_3_1 = animate_train(Line((RAIL_LEFT, 0, 0), (RAIL_RIGHT - RAIL_PADDING, 0, 0)), False, True, False)
        _, animate_trains_3_2, _ = animate_train(Line((RAIL_LEFT + RAIL_PADDING, 0, 0), (RAIL_RIGHT, 0, 0)), False, False, True)
        self.play(animate_trains_3_1.set_rate_func(rush_from).set_run_time(2))
        self.play(animate_passengers)
        self.remove(*passenger_dots)
        reset_trains_3_1.begin()
        self.play(animate_trains_3_2.set_rate_func(rush_into).set_run_time(2))

        rail_4 = self.create_rail(SIDING_COLOR, -1.5, True)
        self.play(self.create_text(3, -1.5), Create(rail_4))

        _, animate_trains_4_1, reset_trains_4_1 = animate_train(Line((RAIL_LEFT + RAIL_PADDING, -1.5, 0), (RAIL_RIGHT, -1.5, 0)), False, False, True)
        self.play(animate_trains_4_1.set_rate_func(rush_into).set_run_time(2))
        reset_trains_4_1.begin()
        self.update_mobjects(0)
        self.wait()
        self.play(animate_trains_4_1.set_rate_func(rush_into).set_run_time(2))

        rail_5 = self.create_rail(TURN_BACK_COLOR, -3, True)
        self.play(self.create_text(4, -3), Create(rail_5))

        _, animate_trains_5_1, reset_trains_5_1 = animate_train(Line((RAIL_RIGHT, -3, 0), (RAIL_LEFT + RAIL_PADDING, -3, 0)), False, True, False)
        _, animate_trains_5_2, _ = animate_train(Line((RAIL_LEFT + RAIL_PADDING, -3, 0), (RAIL_RIGHT, -3, 0)), False, False, True)
        self.play(animate_trains_5_1.set_rate_func(rush_from).set_run_time(2))
        reset_trains_5_1.begin()
        self.play(animate_trains_5_2.set_rate_func(rush_into).set_run_time(2))

        self.wait()

    @staticmethod
    def draw_background():
        background_1 = Rectangle(width=EDGE_PADDING, height=config.frame_height, fill_opacity=1, fill_color=BLACK, stroke_width=0).shift(RIGHT * (HALF_WIDTH - EDGE_PADDING / 2)).set_z_index(1)
        left_width = config.frame_width - EDGE_PADDING * 7 - TRAIN_LENGTH
        background_2 = Rectangle(width=left_width, height=config.frame_height, fill_opacity=1, fill_color=BLACK, stroke_width=0).shift(LEFT * (HALF_WIDTH - left_width / 2)).set_z_index(1)
        background_3 = RailTypes.create_gradient_rectangle(EDGE_PADDING, config.frame_height, True).align_to(background_1, LEFT).shift(LEFT * EDGE_PADDING).set_z_index(1)
        background_4 = RailTypes.create_gradient_rectangle(EDGE_PADDING, config.frame_height, False).align_to(background_2, RIGHT).shift(RIGHT * EDGE_PADDING).set_z_index(1)
        return [background_1, background_2, background_3, background_4]

    @staticmethod
    def create_text(index, offset):
        text_object, text_width, _ = create_text_object(TEXT, index)
        text_object.shift(LEFT * (HALF_WIDTH - text_width / 2 - EDGE_PADDING) + UP * offset).set_z_index(2)
        return Write(text_object)

    @staticmethod
    def create_gradient_rectangle(width, height, flipped):
        new_width = 16 if config.quality == "low_quality" else 256
        new_height = round(height / width * new_width)
        rgba = np.zeros((new_height, new_width, 4), dtype=np.uint8)
        rgba[..., 3] = np.tile(np.linspace(0 if flipped else 255, 255 if flipped else 0, new_width, dtype=np.uint8), (new_height, 1))
        return ImageMobject(rgba).set(width=width, height=height)

    @staticmethod
    def create_rail(rail_color, offset, skip_first_rail):
        point_1 = (RAIL_LEFT, offset, -1)
        point_2 = (RAIL_LEFT + RAIL_PADDING, offset, -1)
        point_3 = (RAIL_RIGHT - RAIL_PADDING, offset, -1)
        point_4 = (RAIL_RIGHT, offset, -1)
        if rail_color == GRAY: return Line(point_1, point_4, stroke_color=GRAY, stroke_width=RAIL_STROKE_WIDTH)
        rail_1 = Line(point_1, point_2, stroke_color=GRAY, stroke_width=RAIL_STROKE_WIDTH)
        rail_2 = Line(point_2, point_3, stroke_color=rail_color, stroke_width=RAIL_STROKE_WIDTH)
        rail_3 = Line(point_3, point_4, stroke_color=GRAY, stroke_width=RAIL_STROKE_WIDTH)
        return VGroup(rail_2, rail_3) if skip_first_rail else VGroup(rail_1, rail_2, rail_3)

    @staticmethod
    def create_passengers():
        dots = []
        move_dots = []
        passengers_per_car = 10
        car_length = TRAIN_LENGTH / TRAIN_CAR_COUNT
        for i in range(TRAIN_CAR_COUNT):
            for _ in range(passengers_per_car):
                x = random.uniform(RAIL_LEFT + RAIL_PADDING, RAIL_RIGHT - RAIL_PADDING)
                y = random.uniform(-1, -TRAIN_WIDTH)
                dot = Dot((x, y, 0))
                dots.append(dot)
                move_dots.append(dot.animate.move_to((random.uniform(RAIL_LEFT + RAIL_PADDING + i * car_length + 0.1, RAIL_LEFT + RAIL_PADDING + (i + 1) * car_length - 0.1), 0, 0)))
        return dots, FadeIn(*dots, lag_ratio=1 / (TRAIN_CAR_COUNT * passengers_per_car)), AnimationGroup(*move_dots)
