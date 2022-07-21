import random
from graphics import *
import time
win = GraphWin()
size = (20, 20)
van_centroid = (10, 14)
sign = (5, 5)
field = [[0 for i in range(size[1])] for j in range(size[0])]
square_size = 400 / 20
prob_being_criminal = 0.5
citizens = set()


def is_empty(row, col):
    if field[row][col] != 3 and field[row][col] != 2:
        return True
    else:
        return False


# van
def create_van():
    for i in range(van_centroid[0]-2, van_centroid[0]+2):
        for j in range(van_centroid[1]-1, van_centroid[1]+1):
            field[i][j] = 2


# sign
def create_sign():
    for i in range(sign[0], sign[0]+2):
        field[i][sign[1]] = 3


# recognition_area
def create_recognition_area():
    for i in range(van_centroid[0]-3, van_centroid[0]+3):
        for j in range(van_centroid[1]-4, van_centroid[1]-1):
            field[i][j] = 1


class Citizen:
    def __init__(self, watchlist, x, y):
        self.being_criminal = watchlist
        self.row = x
        self.col = y
        self.has_seen_sign = False
        self.prob_forward = 0.8
        self.direction = True
        #add_citizen_to_field(self.row, self.col, watchlist)
        self.player = Circle(Point(self.col*square_size + 60, self.row*square_size+60), 8)
        color = {True: "White", False:"Green"}
        self.player.setFill(color[watchlist])
        self.dx = 0
        self.dy = 0

    def update_prob(self):
        if self.being_criminal:
            self.prob_forward = 0.1
        else:
            self.prob_forward = 0.9

    def move_forward(self):
        if self.col < size[1] - 1:
            if is_empty(self.row, self.col + 1):
                self.dx = square_size
                self.dy = 0
                self.col += 1
                return "Moved"
            else:
                self.dy = 0
                self.dx = 0
        else:
            return "end"
        return "did not move"

    def move_backward(self):
        if self.col > 0:
            if is_empty(self.row, self.col - 1):
                self.dx = -square_size
                self.dy = 0
                self.col -= 1
                return "Moved"
            else:
                self.dy = 0
                self.dx = 0
        else:
            return "end"
        return "did not move"

    def move_up(self):
        if self.row > 0:
            if is_empty(self.row - 1, self.col):
                self.dy = -square_size
                self.dx = 0
                self.row -= 1
                return "Moved"
            else:
                self.dy = 0
                self.dx = 0
        else:
            return "end"
        return "did not move"

    def move_down(self):
        if self.row < size[0] - 1:
            if is_empty(self.row + 1, self.col):
                self.dy = square_size
                self.dx = 0
                self.row += 1
                return "Moved"
            else:
                self.dy = 0
                self.dx = 0
        else:
            return "end"
        return "did not move"


def add_random_citizens(number):
    for n in range(number):
        q = random.uniform(0, 1)
        row = random.randint(0, size[0] - 1)
        if q <= prob_being_criminal:
            new_citizen = Citizen(True, row, 0)
        else:
            new_citizen = Citizen(False, row, 0)
        citizens.add(new_citizen)
        new_citizen.player.draw(win)


def initiate_field(win):
    c = Rectangle(Point(50, 50), Point(450, 450))
    c.draw(win)
    for i in range(size[0]):
        for j in range(size[1]):
            color = {2: "Blue", 1:"Yellow", 3:"Red"}
            if field[i][j] != 0 and field[i][j] != 4 and field[i][j] != 5:
                t = Rectangle(Point(j * square_size + 50, i * square_size + 50),
                              Point((j + 1) * square_size + 50, (i + 1) * square_size + 50))
                t.setFill(color[field[i][j]])
                t.draw(win)


def update_field():
    for c in citizens:
        c.player.move(c.dx, c.dy)


def process(counter_captured=0, number=100):
    for r in range(number):
        time.sleep(0.8)
        add_random_citizens(5)
        ended = []
        for c in citizens:
            if field[c.row][c.col] == 1 and c.being_criminal:
                counter_captured += 1
                ended.append(c)
            else:
                if not c.has_seen_sign and max(abs(c.row - sign[0]-1), abs(c.col - sign[1])) <= 2:
                    c.has_seen_sign = True
                    c.update_prob()
                p = random.uniform(0, 1)
                if p <= c.prob_forward:
                    c.direction = True
                    movement = c.move_forward()
                    if movement == "did not move":
                        movement = c.move_up()
                        if movement == "did not move":
                            movement = c.move_down()
                else:
                    c.direction = False
                    movement = c.move_backward()
                    if movement == "did not move":
                        movement = c.move_down()
                        if movement == "did not move":
                            movement = c.move_up()
                if movement == "end":
                    ended.append(c)
        update_field()
        for c in ended:
            citizens.remove(c)
            c.player.undraw()
            del c
    return counter_captured


if __name__ == "__main__":
    create_van()
    create_sign()
    create_recognition_area()
    initiate_field(win)
    add_random_citizens(10)
    process()
    #print(counter_captured)
    win.getMouse()
    win.close()


