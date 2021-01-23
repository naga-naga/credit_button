import PySimpleGUI as sg
import pymunk
import random

class Credit():
    # x, y: 置く座標
    # size: tuple(width, height)
    def __init__(self, x, y, size):
        mass = 10
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 0.5
        self.shape.friction = 0.8
        self.gui_credit_figure = None


class Playfield():
    def __init__(self, graph_elem, screensize):
        self.graph_elem = graph_elem
        self.space = pymunk.Space()
        self.space.gravity = 0, 100
        self.screensize = screensize
        self.add_wall((0, screensize[1]), (screensize[0], screensize[1])) # ground
        self.add_wall((0, 0), (0, screensize[1])) # left
        self.add_wall((screensize[0], 0), (screensize[0], screensize[1])) # right
        self.arena_credits = []

    def add_wall(self, pt_from, pt_to):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        ground_shape = pymunk.Segment(body, pt_from, pt_to, 1.0)
        ground_shape.friction = 0.8
        ground_shape.elasticity = 0.99
        self.space.add(ground_shape)

    def add_credits(self, num_credits = 10):
        for _ in range(num_credits):
            x = random.randint(0, self.screensize[0])
            y = random.randint(0, self.screensize[1]/4)
            credit = Credit(x, y, (100, 59)) # 単位の画像のサイズ
            self.arena_credits.append(credit)
            self.space.add(credit.body, credit.shape)
            credit.gui_credit_figure = self.graph_elem.draw_image("credit.png", location=(x, y))


def main():
    screensize = sg.Window.get_screen_size()

    # ---------- ウィンドウ作成 ----------
    graph_elem = sg.Graph(canvas_size=screensize, graph_bottom_left=(0, screensize[1]), graph_top_right=(screensize[0], 0), enable_events=True, key="-GRAPH-", background_color="lightblue")

    layout = [
        [graph_elem]
    ]
    window1 = sg.Window("Falling Credits", layout, finalize=True, location=(0, 0), keep_on_top=True, element_padding=(0, 0), margins=(0, 0), no_titlebar=True, right_click_menu=[[""], ["Exit"]], transparent_color="lightblue")

    area = Playfield(graph_elem, screensize)

    layout2 = [
        [sg.Button("❎", border_width=0, button_color=("white", sg.theme_background_color()), key="Exit")],
        [sg.Button("単位が欲しい", key="Credit"), sg.Button("単位がもっと欲しい", key="10_Credits"), sg.Button("単位がもっともっと欲しい", key="50_Credits"), sg.Button("吹き飛ばす", key="smash")]
    ]
    window2 = sg.Window("Buttons", layout2, keep_on_top=True, grab_anywhere=True, no_titlebar=True, finalize=True)

    # ---------- イベントループ ----------
    while True:
        window, event, values = sg.read_all_windows(timeout=0)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Credit":
            area.add_credits(1)
        elif event == "10_Credits":
            area.add_credits(10)
        elif event == "50_Credits":
            area.add_credits(50)
        elif event == "smash":
            for credit in area.arena_credits:
                credit.body.apply_impulse_at_local_point((0, 500), (screensize[0]/2, screensize[1]))

        area.space.step(0.02)

        for credit in area.arena_credits:
            if credit.body.position[1] > screensize[1]:
                credit.body.position = credit.body.position[0], screensize[1] - 30

            graph_elem.relocate_figure(credit.gui_credit_figure, credit.body.position[0], credit.body.position[1])

    window1.close()
    window2.close()

if __name__ == "__main__":
    main()

