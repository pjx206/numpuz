import pyxel
import numpy as np
import sys

# TODO: Add config manager to save these information
BLOCK_SIZE = 11  # Minimum size recommended: 9
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
    if DEBUG:
        blocks = np.array(list(range(1, 16)) + [0])
        blocks[-2], blocks[-1] = blocks[-1], blocks[-2]
    else:
        blocks = np.arange(16, dtype='uint8')
        np.random.shuffle(blocks)
    pos0 = blocks.tolist().index(0)
    return blocks.reshape((4, 4)), (pos0 // 4, pos0 % 4)


class Game:
    def __init__(self):
        self.blocks, self.blank_pos = get_map()
        self.step = 0
        log('[*] map info', self.blocks)
        log('[*] initial blank@', self.blank_pos, sep='')

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
        self.step += 1
        log('[*] blank@', self.blank_pos, sep='')

    def draw(self):
        pyxel.cls(1)
        self.draw_ui()
        self.draw_map_blocks()

    def draw_ui(self):
        pyxel.rect(*FRAME_POS, 5)  # frame background
        pyxel.rectb(*FRAME_POS, 9)  # frame
        pyxel.text(3, 1, 'step: {}'.format(self.step), 9)

    def draw_map_blocks(self):
        def get_block_pos(row, col):
            return BLOCKS_START[0] + col * BLOCK_SIZE + col + 1, BLOCKS_START[1] + row * BLOCK_SIZE + row + 1

        def get_best_text_pos_offset(v):
            # get best position to keep text in center
            if v > 9:
                return [2, 3]
            else:
                return [4, 3]

        for i in range(4):
            for j in range(4):
                val = self.blocks[i, j]
                if val != 0:
                    x, y = get_block_pos(i, j)
                    pyxel.rect(x, y, BLOCK_SIZE, BLOCK_SIZE, 10)
                    off = get_best_text_pos_offset(val)
                    x_t, y_t = x + off[0], y + off[1]
                    pyxel.text(x_t, y_t, str(self.blocks[i, j]), 4)

    @property
    def status(self):
        blocks: np.ndarray = self.blocks.reshape((16, 1))
        if all([blocks[i] == i + 1 for i in range(15)]):
            return 'WIN'
        return 'RUNNING'


class Welcome:
    def __init__(self):
        pyxel.text(3, 1, "Numpuz", 8)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(16, 24, "Numpuz", pyxel.frame_count % 16)

class Win:
    def __init__(self):
        self._status = 'DISPLAYING'
        self.y = 50
    
    def update(self):
        if pyxel.btnr(pyxel.KEY_ENTER):
            self._status = 'GOBACK'
        if pyxel.frame_count % 4 == 0:
            self.y -= 4
        if self.y < -10:
            self._status = 'GOBACK'

    def draw(self):
        pyxel.cls(pyxel.frame_count % 7)
        pyxel.text(20, self.y, 'Win~', 15)
    
    @property
    def status(self):
        return self._status


class App:
    def __init__(self):
        pyxel.init(FRAME_POS[2] + 4, TEXT_HEIGHT + 2 +
                   FRAME_POS[2] + 2, caption="Number Puzzle")
        pyxel.load('./resource.pyxres')
        self.current = None
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if self.current is None:
            self.current = Welcome()
        elif isinstance(self.current, Welcome):
            if pyxel.btnr(pyxel.KEY_ENTER) and isinstance(self.current, Welcome):
                self.current = Game()            
        elif  isinstance(self.current, Game):
            if self.current.status == 'WIN':
                self.current = Win()
        elif isinstance(self.current, Win):
            if self.current.status == 'GOBACK':
                self.current = Welcome()

        self.current.update()
    
    def draw(self):
        self.current.draw()

App()
