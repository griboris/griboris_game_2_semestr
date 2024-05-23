import tkinter
import random
import os
from PIL import Image, ImageTk


class Game:
    def __init__(self):

        self.VRM_WIDTH = 32
        self.VRM_HEIGHT = 24

        self.GAMESTATUS_TITLE = 0
        self.GAMESTATUS_START = 1
        self.GAMESTATUS_MAIN = 2
        self.GAMESTATUS_MISS = 3
        self.GAMESTATUS_OVER = 4
        self.GAMESTATUS_DIFFICULTY = 5

        self.ENEMY_MAX = 5

        self.gameStatus = self.GAMESTATUS_TITLE

        self.gameTime = 0

        self.KEY_LEFT = "Left"
        self.KEY_RIGHT = "Right"
        self.KEY_SPACE = "space"

        self.basePath = os.path.abspath(os.path.dirname(__file__))

        self.blankRow = [0] * self.VRM_WIDTH
        self.vrm = [self.blankRow] * self.VRM_HEIGHT

        self.indexOffset = 0
        self.speed = 1

        self.roadWidth = 12
        self.roadX = 10

        self.mx = 16
        self.my = 20

        self.ex = [0] * self.ENEMY_MAX
        self.ey = [0] * self.ENEMY_MAX
        self.ev = [0] * self.ENEMY_MAX
        self.es = [0] * self.ENEMY_MAX

        self.enemy_count = 0

        self.score = 0

        self.key = ""
        self.keyOff = False

        self.difficulty = None


    def pressKey(self, e):

        self.key = e.keysym
        self.keyOff = False


    def releaseKey(self, e):

        self.keyOff = True


    def title(self):

        if self.key == self.KEY_SPACE:

            self.gameStatus = self.GAMESTATUS_DIFFICULTY

            self.selectDifficulty()


    def gameStart(self):

        if self.gameTime < 24:
            self.generateRoad(False)

        if self.gameTime == 50:

            self.gameStatus = self.GAMESTATUS_MAIN
            self.gameTime = 0


    def gameMain(self):

        self.generateRoad()

        self.movePlayer()

        self.moveEnemy()

        self.score = self.score + 1


    def generateRoad(self, isMove=True):

        if isMove == True:
            v = random.randint(0, 2) - 1
            if (self.roadX + v > 0 and self.roadX + v < self.VRM_WIDTH - self.roadWidth - 1):
                self.roadX = self.roadX + v

        for i in range(self.speed):

            newRow = [2] * self.VRM_WIDTH
            for w in range(self.roadWidth):
                newRow[self.roadX + w] = 0

            newRow[self.roadX - 1] = 1
            newRow[self.roadX + self.roadWidth] = 1


            self.indexOffset -= 1
            if self.indexOffset < 0:
                self.indexOffset = self.VRM_HEIGHT - 1

            self.vrm[self.indexOffset] = newRow


    def movePlayer(self):

        if self.key == self.KEY_LEFT and self.mx > 0:
            self.mx -= 1

        if self.key == self.KEY_RIGHT and self.mx < self.VRM_WIDTH:
            self.mx += 1

        ty = self.indexOffset + self.my
        if ty > self.VRM_HEIGHT - 1:
            ty = ty - self.VRM_HEIGHT

        if self.vrm[ty][self.mx] > 0:
            self.gameStatus = self.GAMESTATUS_MISS
            self.gameTime = 0


    def moveEnemy(self):

        if self.enemy_count < self.ENEMY_MAX and self.gameTime % 150 == 0:
            self.enemy_count += 1

        for e in range(self.enemy_count):
            if self.es[e] > 0:
                if self.es[e] == 2 and self.ey[e] < 15:

                    if self.ex[e] > self.mx:
                        self.ex[e] -= 1

                    if self.ex[e] < self.mx:
                        self.ex[e] += 1

                self.ey[e] = self.ey[e] + 1
                if self.ey[e] > 23:
                    self.es[e] = 0

                if abs(self.ex[e] - self.mx) < 2 and abs(self.ey[e] - self.my) < 2:

                    self.gameStatus = self.GAMESTATUS_MISS
                    self.gameTime = 0

            else:

                if self.gameTime > 100 and random.randint(0, 10) > 8:

                    self.ex[e] = self.roadX + random.randint(0, self.roadWidth)
                    self.ey[e] = 0
                    self.ev[e] = 0
                    self.es[e] = random.randint(1, 2)


    def miss(self):

        if self.gameTime > 25:

            self.gameStatus = self.GAMESTATUS_OVER
            self.gameTime = 0


    def gameover(self):

        if (self.gameTime > 10 and self.key == self.KEY_SPACE) or self.gameTime > 50:

            self.gameStatus = self.GAMESTATUS_TITLE
            self.gameTime = 0


    def setDifficulty(self, difficulty):

        self.difficulty = difficulty

        self.score = 0

        self.mx = 16
        self.my = 20

        self.blankRow = [0] * self.VRM_WIDTH
        self.vrm = [self.blankRow] * self.VRM_HEIGHT

        self.indexOffset = 0

        for i in range(0, self.ENEMY_MAX):
            self.es[i] = 0

        self.enemy_count = 0

        self.vrm = [self.blankRow] * self.VRM_HEIGHT
        self.indexOffset = 0

        #
        if self.difficulty == "easy":
            self.ENEMY_MAX = 7

            self.roadWidth = 20
            self.roadX = 6

            self.speed = 3

        if self.difficulty == "medium":
            self.ENEMY_MAX = 5

            self.roadWidth = 16
            self.roadX = 8

            self.speed = 2

        if self.difficulty == "hard":
            self.ENEMY_MAX = 6

            self.roadWidth = 12
            self.roadX = 10

            self.speed = 1
        #

        self.gameStatus = self.GAMESTATUS_START
        self.gameTime = 0
        self.ex = [0] * self.ENEMY_MAX
        self.ey = [0] * self.ENEMY_MAX
        self.ev = [0] * self.ENEMY_MAX
        self.es = [0] * self.ENEMY_MAX

        self.enemy_count = 0

        canvas.delete("MENU")


    def selectDifficulty(self):

        canvas.create_rectangle(0, 0, gPos(self.VRM_WIDTH), gPos(self.VRM_HEIGHT), fill="Black")

        self.writeText(8, 5, "CHOOSE DIFFICULTY:", tag="MENU")

        # easy_button = canvas.create_text(gPos(12), gPos(9), text="Easy", anchor="w", tag="MENU", font=("Arial", 12))
        self.writeText(12, 9, "EASY", "MENU")
        easy_button = canvas.create_rectangle(gPos(11), gPos(8), gPos(16), gPos(10),
                                              fill="", outline="",tag="MENU")

        # medium_button = canvas.create_text(gPos(18), gPos(9), text="Medium", anchor="w", tag="MENU", font=("Arial", 12))
        self.writeText(12, 13, "MEDIUM", "MENU")
        medium_button = canvas.create_rectangle(gPos(11), gPos(12), gPos(18), gPos(14),
                                                fill="", outline="", tag="MENU")

        # hard_button = canvas.create_text(gPos(24), gPos(9), text="Hard", anchor="w", tag="MENU", font=("Arial", 12))
        self.writeText(12, 17, "HARD", "MENU")
        hard_button = canvas.create_rectangle(gPos(11), gPos(16), gPos(16), gPos(18),
                                              fill="", outline="", tag="MENU")

        canvas.tag_bind(easy_button, "<Button-1>", lambda _: self.setDifficulty("easy"))
        canvas.tag_bind(medium_button, "<Button-1>", lambda _: self.setDifficulty("medium"))
        canvas.tag_bind(hard_button, "<Button-1>", lambda _: self.setDifficulty("hard"))


    def drawScreen(self):

        canvas.delete("TEXT1")
        canvas.delete("BG1")
        canvas.delete("PLAYER")
        canvas.delete("ENEMY")

        if (self.gameStatus == self.GAMESTATUS_START
                or self.gameStatus == self.GAMESTATUS_MAIN
                or self.gameStatus == self.GAMESTATUS_MISS):

            for row in range(self.VRM_HEIGHT):
                vrow = row + self.indexOffset

                if vrow > self.VRM_HEIGHT - 1:
                    vrow = vrow - self.VRM_HEIGHT

                for col in range(self.VRM_WIDTH):
                    canvas.create_image(gPos(col), gPos(row), image=img_chr[self.vrm[vrow][col]], tag="BG1")

        if self.gameStatus == self.GAMESTATUS_MAIN:
            canvas.create_image(gPos(self.mx), gPos(self.my), image=img_mycar, tag="PLAYER")

            for e in range(self.enemy_count):
                if self.es[e] > 0:
                    canvas.create_image(gPos(self.ex[e]), gPos(self.ey[e]), image=img_othercar, tag="ENEMY")

        if self.gameStatus == self.GAMESTATUS_MISS:
            canvas.create_image(gPos(self.mx), gPos(self.my), image=img_bang, tag="PLAYER")

        if self.gameStatus == self.GAMESTATUS_TITLE:
            canvas.create_rectangle(0, 0, gPos(self.VRM_WIDTH), gPos(self.VRM_HEIGHT), fill="Black")
            self.writeText(9, 6, "CAR RACE", "TEXT1")

            if self.gameTime < 25:
                self.writeText(9, 13, "PUSH SPACE KEY", "TEXT1")

            if self.gameTime == 50:
                self.gameTime = 0

        if self.gameStatus == self.GAMESTATUS_START:
            if self.gameTime > 30 and self.gameTime < 50:
                self.writeText(14, 13, "START", "TEXT1")

        if self.gameStatus == self.GAMESTATUS_OVER:
            self.writeText(12, 11, "GAME OVER", "TEXT1")

        self.writeText(0, 0, "SCORE " + "{:06}".format(self.score), "TEXT1")

        if self.gameStatus == self.GAMESTATUS_DIFFICULTY:
            self.selectDifficulty()


    def writeText(self, x, y, str, tag="text1"):
        str = str.upper()

        for i in range(len(str)):
            o = ord(str[i])

            if o >= 48 and o <= 57:
                canvas.create_image(gPos(x + i), gPos(y), image=img_font[o - 48], tag=tag)

            if o >= 65 and o <= 90:
                canvas.create_image(gPos(x + i), gPos(y), image=img_font[o - 55], tag=tag)


    def main(self):

        self.gameTime += 1

        if self.gameStatus == self.GAMESTATUS_TITLE:
            self.title()

        if self.gameStatus == self.GAMESTATUS_START:
            self.gameStart()

        if self.gameStatus == self.GAMESTATUS_MAIN:
            self.gameMain()

        if self.gameStatus == self.GAMESTATUS_MISS:
            self.miss()

        if self.gameStatus == self.GAMESTATUS_OVER:
            self.gameover()

        self.drawScreen()

        if self.keyOff == True:
            self.key = ""
            self.keyOff = False

        root.after(50, self.main)


def loadImage(filePath):
    img = Image.open(filePath).convert("RGBA")
    return img.resize((img.width * 2, img.height * 2), Image.NEAREST)


def gPos(value):
    return value * 8 * 2 + 8


game = Game()


root = tkinter.Tk()
root.geometry(str(gPos(game.VRM_WIDTH) - 8) + "x" + str(gPos(game.VRM_HEIGHT) - 8))
root.title("Car Race")
root.bind("<KeyPress>", game.pressKey)
root.bind("<KeyRelease>", game.releaseKey)

canvas = tkinter.Canvas(width=gPos(game.VRM_WIDTH) - 8, height=gPos(game.VRM_HEIGHT) - 8)
canvas.pack()


img_mycar = ImageTk.PhotoImage(loadImage(game.basePath + os.sep + "Images" + os.sep + "mycar.png"))
img_othercar = ImageTk.PhotoImage(loadImage(game.basePath + os.sep + "Images" + os.sep + "othercar.png"))
img_bang = ImageTk.PhotoImage(loadImage(game.basePath + os.sep + "Images" + os.sep + "bang.png"))
img_chr = [
    ImageTk.PhotoImage(loadImage(game.basePath + os.sep + "Images" + os.sep + "road.png")),
    ImageTk.PhotoImage(loadImage(game.basePath + os.sep + "Images" + os.sep + "block.png")),
    ImageTk.PhotoImage(loadImage(game.basePath + os.sep + "Images" + os.sep + "green.png"))
]

img_allfont = loadImage(game.basePath + os.sep + "Images" + os.sep + "font.png")
img_font = []
for w in range(0, img_allfont.width, 16):
    img = ImageTk.PhotoImage(img_allfont.crop((w, 0, w + 16, 16)))
    img_font.append(img)


game.main()


root.mainloop()
