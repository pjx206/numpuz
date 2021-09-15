import pyxel
import numpy as np
import sys

BLOCK_SIZE = 20  # Minimum size recommended: 9
TEXT_HEIGHT = 6
FRAME_BORDER = 1  # TODO: write a func to extend pyxel.rectb() to support border size
FRAME_POS = (3 - FRAME_BORDER,
             TEXT_HEIGHT + 2,
             4 * BLOCK_SIZE + FRAME_BORDER * 7,
             4 * BLOCK_SIZE + FRAME_BORDER * 7)
BLOCKS_START = (FRAME_POS[0] + 1, FRAME_POS[1] + 1)  # frame border == 1
DEBUG = True if len(sys.argv) > 1 and '-d' in sys.argv else False

def log(*value, sep=' ', end='\n', file=sys.stdout, flush=False):
    if not DEBUG:
        return
    print(*value, sep=sep, end=end, file=file, flush=flush)

def get_map():
    blocks = np.arange(16, dtype='uint8')
    np.random.shuffle(blocks)
    pos0 = blocks.tolist().index(0)
    return blocks.reshape((4, 4)), (pos0 // 4, pos0 % 4)


class App:
    def __init__(self):
        pyxel.init(FRAME_POS[2] + 4, TEXT_HEIGHT + 2 +
                   FRAME_POS[2] + 2, caption="Number Puzzle")
        self.blocks, self.blank_pos = get_map()
        log('[*] map info', self.blocks)
        log('[*] initial blank@', self.blank_pos, sep='')
        pyxel.load('./resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        self.update_blocks()

    def update_blocks(self):
        row, col = self.blank_pos
        blks = self.blocks
        if pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(pyxel.GAMEPAD_1_UP):
            if row == 3:
                return
            blks[row, col], blks[row+1, col] = blks[row+1, col], blks[row, col]
            row += 1
        elif pyxel.btnr(pyxel.KEY_DOWN) or pyxel.btnr(pyxel.GAMEPAD_1_DOWN):
            if row == 0:
                return
            blks[row, col], blks[row-1, col] = blks[row-1, col], blks[row, col]
            row -= 1
        elif pyxel.btnr(pyxel.KEY_LEFT) or pyxel.btnr(pyxel.GAMEPAD_1_LEFT):
            if col == 3:
                return
            blks[row, col], blks[row, col+1] = blks[row, col+1], blks[row, col]
            col += 1
        elif pyxel.btnr(pyxel.KEY_RIGHT) or pyxel.btnr(pyxel.GAMEPAD_1_RIGHT):
            if col == 0:
                return
            blks[row, col], blks[row, col-1] = blks[row, col-1], blks[row, col]
            col -= 1
        else:
            return
        self.blank_pos = row, col
        log('[*] blank@', self.blank_pos, sep='')

    def draw(self):
        pyxel.cls(1)
        self.draw_ui()
        self.draw_map_blocks()

    def draw_ui(self):
        pyxel.rect(*FRAME_POS, 5)  # frame background
        pyxel.rectb(*FRAME_POS, 9)  # frame

    def draw_map_blocks(self):
        def get_block_pos(row, col):
            return BLOCKS_START[0] + col * BLOCK_SIZE + col + 1, BLOCKS_START[1] + row * BLOCK_SIZE + row + 1

        def get_best_text_pos_offset(v):
            # get best position to keep text in center
            if v > 9:
                return [1, 2]
            else:
                return [3, 2]

        for i in range(4):
            for j in range(4):
                val = self.blocks[i, j]
                if val != 0:
                    x, y = get_block_pos(i, j)
                    pyxel.rect(x, y, BLOCK_SIZE, BLOCK_SIZE, 10)
                    off = get_best_text_pos_offset(val)
                    x_t, y_t = x + off[0], y + off[1]
                    pyxel.text(x_t, y_t, str(self.blocks[i, j]), 4)

        pyxel.text(3, 1, "Numpuz", 8)


App()
