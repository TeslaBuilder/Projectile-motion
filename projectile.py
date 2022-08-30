import turtle
# This part was abandoned due to time limit.

class Projectile(turtle.RawTurtle):

    def __init__(self, tk_canvas):
        super().__init__(tk_canvas)
        self.speed(6)
        self.pendown()
        self.current_type = 0
        self.trajectory_x = 0
        self.trajectory_y = 0
        self.plt_location = 0
        self.shapes = ["square", "circle", "Bomb.gif", "Explode.gif", "Arrow.gif", "Broken_arrow.gif", "Bouncy_bomb.gif"]

    def set_type(self, arg1):
        self.current_type = arg1
        self.shape(self.shapes[arg1])

    def set_trajectory(self, arg1, arg2):
        self.trajectory_x = arg1
        self.trajectory_y = arg2

    def run(self):
        if self.plt_location < len(self.trajectory_x):
            self.goto(self.trajectory_x[self.plt_location], self.trajectory_y[self.plt_location])
            self.plt_location += 1
            print("frame:", self.plt_location)
        else:
            self.finish()
        turtle.ontimer(self.run, 1000)

    def finish(self):
        if self.current_type == 0:
            self.shape(self.shapes[1])
        if self.current_type == 2:
            self.shape(self.shapes[3])
