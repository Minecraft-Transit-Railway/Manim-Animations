import math

from manim import *

HALF_WIDTH = config.frame_width / 2
HALF_HEIGHT = config.frame_height / 2
PIXELS_PER_UNIT_X = config.pixel_width / HALF_WIDTH
PIXELS_PER_UNIT_Y = config.pixel_height / HALF_HEIGHT

EDGE_PADDING = 1
SMALL_VALUE = 0.0001

RAIL_STROKE_WIDTH = 16
TRAIN_CAR_COUNT = 4
TRAIN_WIDTH = 0.2
TRAIN_LENGTH = 3

PLATFORM_COLOR = ManimColor("#993333")
SIDING_COLOR = ManimColor("#E5E533")
TURN_BACK_COLOR = ManimColor("#334CB2")
ONE_WAY_ARROW_COLOR = ManimColor("#AAFFAA")


def create_text_object(text: list[str], index: int):
    letters = ""
    for text_part in text:
        for letter in text_part:
            if letter not in letters:
                letters += letter
    template = TexTemplate()
    template.add_to_preamble(r"""
        \usepackage[T1]{fontenc}
        \usepackage[sfdefault]{noto}
        \renewcommand{\bfdefault}{sb}
    """)
    text_object = Tex(*[r" \notosans\bfseries " + text_part + " " for text_part in [letters, text[index], letters]], tex_template=template)
    return text_object[1], text_object[1].width, text_object.height


def combine_paths(*objects: VMobject):
    new_object = VMobject()
    for path_object in objects:
        new_object.append_points(path_object.get_points())
    return new_object


def animate_train(path: VMobject, reverse: bool, start_from_point: bool, end_at_point: bool):
    car_length = TRAIN_LENGTH / TRAIN_CAR_COUNT
    car_gap = 0.04
    cars = []
    path_length = path.get_arc_length()
    path_offset = TRAIN_LENGTH / path_length
    start_point = 0 if start_from_point else path_offset
    end_point = 1 + (path_offset if end_at_point else 0)
    tracker = ValueTracker(end_point if reverse else start_point)

    for i in range(TRAIN_CAR_COUNT):
        car = Rectangle(width=car_length - car_gap * 2, height=TRAIN_WIDTH, fill_opacity=1, fill_color=WHITE, stroke_width=0)
        car_copy = car.copy()

        def update_car(shape, car_number=i):
            point_1 = path.point_from_proportion(min(1, max(0, tracker.get_value() - car_length / path_length * car_number)))
            point_2 = path.point_from_proportion(min(1, max(0, tracker.get_value() - car_length / path_length * (car_number + 1))))
            shape.become(car_copy)
            shape.move_to((point_1 + point_2) / 2)
            shape.rotate(math.atan2(point_2[1] - point_1[1], point_2[0] - point_1[0]))

        car.add_updater(update_car)
        cars.append(car)

    reset_animation = InstantAnimation(lambda: tracker.set_value(end_point if reverse else start_point))
    return cars, Succession(
        Add(*cars),
        reset_animation,
        tracker.animate.set_value(start_point if reverse else end_point)
    ), reset_animation


def create_one_way_arrows(path: VMobject):
    path_length = path.get_arc_length()
    arrows = VGroup()
    value = 0
    interval = 1 / path_length
    while value + interval <= 1:
        point_1 = path.point_from_proportion(value)
        point_2 = path.point_from_proportion(value + interval)
        arrow = Polygon((-TRAIN_WIDTH / 2, TRAIN_WIDTH, 0), (TRAIN_WIDTH / 2, 0, 0), (-TRAIN_WIDTH / 2, -TRAIN_WIDTH, 0), fill_opacity=1, fill_color=ONE_WAY_ARROW_COLOR, stroke_width=0)
        arrow.move_to((point_1 + point_2) / 2)
        arrow.rotate(math.atan2(point_2[1] - point_1[1], point_2[0] - point_1[0]))
        arrows.add(arrow)
        value += interval
    return Create(arrows)


class InstantAnimation(Animation):

    def __init__(self, callback, **kwargs):
        super().__init__(VMobject(), run_time=0, **kwargs)
        self.callback = callback

    def begin(self):
        self.callback()
