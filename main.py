import pyxel
from random import shuffle

BLOCK_SIZE = 9
TEXT_HEIGHT = 6
FRAME_BORDER = 1 # TODO: write a func to extend pyxel.rectb() to support border size
FRAME_POS = (3 - FRAME_BORDER,
             TEXT_HEIGHT + 2,
             4 * BLOCK_SIZE + FRAME_BORDER * 7, 
             4 * BLOCK_SIZE + FRAME_BORDER * 7)
MAP_START = (FRAME_POS[0] + 1, FRAME_POS[1] + 1)  # frame border == 1


def get_map():
    arr = list(range(16))
    shuffle(arr)
    return arr


class App:
    def __init__(self):
        pyxel.init(FRAME_POS[2] + 4, TEXT_HEIGHT + 2 +
                   FRAME_POS[2] + 2, caption="Number Puzzle")
        self.map = get_map()
        pyxel.load('./resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(1)
        self.draw_ui()
        self.draw_map_squares()

    def draw_ui(self):
        pyxel.rect(*FRAME_POS, 5)  # frame background
        pyxel.rectb(*FRAME_POS, 9)  # frame

    def draw_map_squares(self):
        def get_block_pos(x, y):
            return MAP_START[0] + x * BLOCK_SIZE + x + 1, MAP_START[1] + y * BLOCK_SIZE + y + 1

        def get_best_text_pos_offset(v):
            # get best position to keep tetx in center
            if v > 9:
                return [1, 2]
            else:
                return [3, 2]

        for i in range(4):
            for j in range(4):
                val = self.map[i*4+j]
                if val != 0:
                    x, y = get_block_pos(i, j)
                    pyxel.blt(x, y, 0, 0, 0, BLOCK_SIZE, BLOCK_SIZE)
                    off = get_best_text_pos_offset(val)
                    x_t, y_t = x + off[0], y + off[1]
                    pyxel.text(x_t, y_t, str(self.map[i*4+j]), 4)
                else:
                    pyxel.blt(*get_block_pos(i, j), 0, BLOCK_SIZE,
                              0, BLOCK_SIZE, BLOCK_SIZE)

        pyxel.text(3, 1, "Numpuz", 8)


App()
