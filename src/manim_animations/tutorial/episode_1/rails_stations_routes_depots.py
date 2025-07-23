from manim_animations.common import *

text = ["Rails", "Stations", "Routes", "Depots"]

line_position = config.frame_width / 3
depot_position = 2

scale = 0.05
line_size = 6 * scale
station_radius_1 = 7 * scale
station_radius_2 = 5 * scale


class RailsStationsRoutesDepots(Scene):

    def construct(self):
        self.wait()
        write_text_1, move_text_1 = self.create_text(0)
        write_text_2, move_text_2 = self.create_text(1)
        write_text_3, move_text_3 = self.create_text(2)
        write_text_4, move_text_4 = self.create_text(3)

        half_line_size = line_size / 2
        create_rail_1, remove_rail_1 = self.create_rail(half_line_size)
        create_rail_2, remove_rail_2 = self.create_rail(-half_line_size)
        create_sleepers, remove_sleepers = self.create_sleepers()
        self.play(write_text_1, create_sleepers, create_rail_1, create_rail_2)
        self.wait()
        self.play(move_text_1)

        create_station_1_1, move_station_1_1 = self.create_station_circle(station_radius_1, WHITE, 2, 0)
        create_station_1_2, move_station_1_2 = self.create_station_circle(station_radius_2, BLACK, 2, 0)
        create_station_2_1, move_station_2_1 = self.create_station_circle(station_radius_1, WHITE, -2, -3)
        create_station_2_2, move_station_2_2 = self.create_station_circle(station_radius_2, BLACK, -2, -3)
        self.play(write_text_2, Succession(AnimationGroup(create_station_1_1, create_station_1_2), AnimationGroup(create_station_2_1, create_station_2_2)))
        self.wait()
        self.play(move_text_2)

        create_route, shrink_route = self.create_route()
        self.play(write_text_3, remove_rail_1, remove_rail_2, remove_sleepers, create_route)
        self.wait()
        self.play(move_text_3)

        self.play(write_text_4, shrink_route, self.create_depot(), move_station_1_1, move_station_1_2, move_station_2_1, move_station_2_2)
        self.wait()
        self.play(move_text_4)
        self.wait()

    @staticmethod
    def create_text(index):
        text_object, text_width, text_height = create_text_object(text, index)
        text_object.scale(2)
        return Write(text_object), text_object.animate.shift(LEFT * (HALF_WIDTH - text_width / 2 - EDGE_PADDING) + DOWN * (index - (len(text) - 1) / 2) / 2).scale(0.5)

    @staticmethod
    def create_sleepers():
        sleepers = VGroup()
        sleeper_interval = HALF_HEIGHT / 20
        sleeper_y = HALF_HEIGHT - sleeper_interval / 2
        while sleeper_y > -HALF_HEIGHT:
            sleeper = Line((line_position - line_size, sleeper_y, 0), (line_position + line_size, sleeper_y, 0), stroke_color=DARK_BROWN, stroke_width=10)
            sleepers.add(sleeper)
            sleeper_y -= sleeper_interval
        return Create(sleepers), Uncreate(sleepers)

    @staticmethod
    def create_rail(offset):
        rail_1 = Line((line_position + offset, HALF_HEIGHT, 0), (line_position + offset, -HALF_HEIGHT, 0), stroke_color=LIGHT_GRAY)
        rail_2 = Line((line_position + offset, -HALF_HEIGHT, 0), (line_position + offset, -HALF_HEIGHT, 0), stroke_color=LIGHT_GRAY)
        return Create(rail_1), Transform(rail_1, rail_2)

    @staticmethod
    def create_station_circle(radius, fill_color, offset_1, offset_2):
        circle_1 = Circle(radius * SMALL_VALUE, fill_opacity=1, fill_color=fill_color, stroke_width=0).shift(RIGHT * line_position + UP * offset_1)
        circle_2 = Circle(radius * 1.2, fill_opacity=1, fill_color=fill_color, stroke_width=0).shift(RIGHT * line_position + UP * offset_1)
        circle_3 = Circle(radius, fill_opacity=1, fill_color=fill_color, stroke_width=0).shift(RIGHT * line_position + UP * offset_1)
        circle_4 = Circle(radius, fill_opacity=1, fill_color=fill_color, stroke_width=0).shift(RIGHT * line_position + UP * offset_2)
        return Succession(Transform(circle_1, circle_2, run_time=0.3, rate_func=rush_into), Transform(circle_1, circle_3, run_time=0.2, rate_func=rush_from)), Transform(circle_1, circle_4)

    @staticmethod
    def create_route():
        route_1 = Rectangle(width=line_size, height=SMALL_VALUE, fill_opacity=1, fill_color=RED_C, stroke_width=0).set_z_index(-1).shift(RIGHT * line_position + UP * HALF_HEIGHT)
        route_2 = Rectangle(width=line_size, height=config.frame_height, fill_opacity=1, fill_color=RED_C, stroke_width=0).set_z_index(-1).shift(RIGHT * line_position)
        route_3 = Rectangle(width=line_size, height=HALF_HEIGHT + depot_position, fill_opacity=1, fill_color=RED_C, stroke_width=0).set_z_index(-1).shift(RIGHT * line_position + DOWN * (HALF_HEIGHT - depot_position) / 2)
        return Transform(route_1, route_2), Transform(route_1, route_3)

    @staticmethod
    def create_depot():
        depot_1 = Rectangle(width=line_size, height=SMALL_VALUE, stroke_color=GREEN_C, fill_color=GREEN_A, fill_opacity=1).shift(RIGHT * line_position + UP * HALF_HEIGHT)
        depot_2 = Rectangle(width=1, height=1.5, stroke_color=GREEN_C, fill_color=GREEN_A, fill_opacity=1).shift(RIGHT * line_position + UP * depot_position)
        return Transform(depot_1, depot_2)
