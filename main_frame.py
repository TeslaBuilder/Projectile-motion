import turtle
import math
import time
import matplotlib

import tkinter as tk
import numpy as np
import projectile as pjt

from turtle import *
from tkinter import ttk
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

matplotlib.use('TkAgg')

#self.scr = TurtleScreen(self.canvas)
#turtle.register_shape("Broken_arrow.gif")
#turtle.register_shape("Bomb.gif")
#turtle.register_shape("Explode.gif")
#turtle.register_shape("Arrow.gif")


#plt1 = pjt.Projectile()
#plt1.set_type(0)
#plt1.set_trajectory(trajectory_x, trajectory_y)
#plt1.run()


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        options = dict(padx=5, pady=5)
        set_font = "Bahnschrift 15 bold"
        self.option_add("*font", set_font)
        style = ttk.Style()
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=20)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=4)
        # TK common variables

        # Common variables
        self.initial_velocity = tk.DoubleVar(value=100.0)
        self.initial_angle = tk.DoubleVar(value=40.0)
        self.initial_x = tk.DoubleVar(value=0.0)
        self.initial_y = tk.DoubleVar(value=0.0)
        self.gravity = tk.DoubleVar(value=9.8)
        self.time_step = tk.DoubleVar(value=1)
        self.dropdown_value = tk.StringVar(self)
        # self.mass = tk.DoubleVar(value=1.0)
        self.time_tracker = [0]
        self.trajectory_x = [0]
        self.trajectory_y = [0]

        # Calculated value
        self.initial_vx = self.initial_velocity.get() * np.cos(self.initial_angle.get())
        self.initial_vy = self.initial_velocity.get() * np.sin(self.initial_angle.get())
        self.max_flight_time = -2 * self.initial_velocity.get() / self.gravity.get()
        self.x_max_coord = self.initial_x.get() + self.max_flight_time * self.initial_vx
        self.y_max_coord = np.square(self.initial_velocity.get()) * np.square(np.sin(self.initial_angle.get())) / 2 * self.gravity.get()
        self.velocity_x = [self.initial_vx]
        self.velocity_y = [self.initial_vy]

        # Draw figure
        self.figure = Figure(constrained_layout=True, figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor('whitesmoke')
        self.axes = self.figure.add_subplot()
        self.line, = self.axes.plot(self.x_max_coord + 100, self.y_max_coord + 50, 'g', label='plot')
        self.axes.autoscale(enable=True, axis="x", tight=False)
        self.axes.autoscale(enable=True, axis="y", tight=False)
        self.axes.set_title('Projectile motion')
        self.axes.set_xlabel('meter')
        self.axes.set_ylabel('meter')

        # Create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.figure_canvas.draw()
        # Pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self, pack_toolbar=False)
        self.toolbar.update()
        # create axes
        #self.figure_canvas.get_tk_widget().grid(column=10, row=0, rowspan=20, columnspan=20, padx=10, pady=20)


        # self.t = np.arange(0, self.max_flight_time.get(), self.time_step.get())

        def animate(i):
            self.dt = self.time_step.get()
            self.ax = [0]                    # Acceleration was a component for drag calculation
            self.ay = [self.gravity.get()]
            self.time_tracker.append(self.time_tracker[i] + self.dt)
            self.velocity_x.append(self.velocity_x[i] + self.dt * self.ax[i])  # Update the velocity
            self.velocity_y.append(self.velocity_y[i] + self.dt * self.ay[i])
            self.v = self.initial_velocity.get()
            cos = self.velocity_x[-1]/self.v # note: should deal with vel=0 properly
            sin = self.velocity_y[-1]/self.v
            # Update position
            self.trajectory_x.append(self.trajectory_x[i] + self.dt * self.velocity_x[i])
            self.trajectory_y.append(self.trajectory_y[i] + self.dt * self.velocity_y[i])
            # Calculate updated velocity
            #drag = area * density * 0.5 * cd * v ** 2
            #ax.append(-(drag * cos) / M)
            #ay.append(-g - (drag * sin / M))
            self.line.set_xdata(self.trajectory_x[:-1])
            self.line.set_ydata(self.trajectory_y[:-1])
            return self.line,

        self.fig = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=22, rowspan=10, columnspan=10, padx=10, pady=20)
        self.ax = self.fig.add_subplot(211)
        self.line, = self.ax.plot([], [], 'o')
        self.ax.set_ylabel("y (meters)")
        self.ax.set_xlabel("x (meters)")
        self.ax.set_xlim(0, 1000)
        self.ax.set_ylim(0, 500)
        self.ax.autoscale(False)
        self.ani = animation.FuncAnimation(self.fig, animate, interval=self.time_step.get(), blit=True)
        plt.show()

        # get initial velocity
        ttk.Label(self, text="Initial velocity: ") \
            .grid(column=0, row=0, sticky=tk.E, **options)
        ttk.Label(self, text="(m/s)") \
            .grid(column=4, row=0, sticky=tk.W, **options)
        ttk.Scale(self, variable=self.initial_velocity, command=self.initial_velocity_slider_changed,
                  orient='horizontal', length=150, from_=0, to=1000) \
            .grid(column=1, row=0, sticky=tk.W, **options)
        ttk.Spinbox(self, textvariable=self.initial_velocity, command=self.initial_velocity_spinbox_changed,
                    increment=0.1, wrap=True, width=5, from_=1, to=50) \
            .grid(column=2, row=0, sticky=tk.W, **options)

        # get initial angle
        ttk.Label(self, text="Initial angle: ") \
            .grid(column=0, row=1, sticky=tk.E, **options)
        ttk.Label(self, text=" (deg)") \
            .grid(column=4, row=1, sticky=tk.W, **options)
        ttk.Scale(self, variable=self.initial_angle, command=self.initial_angle_slider_changed,
                  orient='horizontal', length=150, from_=0, to=90) \
            .grid(column=1, row=1, sticky=tk.W, **options)
        ttk.Spinbox(self, textvariable=self.initial_angle, command=self.initial_angle_spinbox_changed,
                    increment=0.1, wrap=True, width=5, from_=1, to=90) \
            .grid(column=2, row=1, sticky=tk.W, **options)

        # get gravity
        ttk.Label(self, text="Gravity: ") \
            .grid(column=0, row=2, sticky=tk.E, **options)
        ttk.Label(self, text="(m/s^2)") \
            .grid(column=4, row=2, sticky=tk.W, **options)
        ttk.Scale(self, variable=self.gravity, command=self.gravity_slider_changed,
                  orient='horizontal', length=150, from_=1, to=50) \
            .grid(column=1, row=2, sticky=tk.W, **options)
        ttk.Spinbox(self, textvariable=self.gravity, command=self.gravity_spinbox_changed,
                    increment=0.1, wrap=True, width=5, from_=1, to=50) \
            .grid(column=2, row=2, sticky=tk.W, **options)

        # get initial x coordinate
        ttk.Label(self, text="Initial x coord") \
            .grid(column=0, row=3, sticky=tk.E, **options)
        ttk.Label(self, text="(m)") \
            .grid(column=4, row=3, sticky=tk.W, **options)
        ttk.Scale(self, variable=self.initial_x, command=self.initial_x_cord_slider_changed,
                  orient='horizontal', length=150, from_=1, to=5000) \
            .grid(column=1, row=3, sticky=tk.W, **options)
        ttk.Spinbox(self, textvariable=self.initial_x, command=self.initial_x_cord_spinbox_changed,
                    increment=0.1, wrap=True, width=5, from_=1, to=5000) \
            .grid(column=2, row=3, sticky=tk.W, **options)

        # get initial y coordinate
        ttk.Label(self, text="Initial y coord") \
            .grid(column=0, row=4, sticky=tk.E, **options)
        ttk.Label(self, text="(m)") \
            .grid(column=4, row=4, sticky=tk.W, **options)
        ttk.Scale(self, variable=self.initial_y, command=self.initial_y_cord_slider_changed,
                  orient='horizontal', length=150, from_=1, to=5000) \
            .grid(column=1, row=4, sticky=tk.W, **options)
        ttk.Spinbox(self, textvariable=self.initial_y, command=self.initial_y_cord_spinbox_changed,
                    increment=0.1, wrap=True, width=5, from_=1, to=5000) \
            .grid(column=2, row=4, sticky=tk.W, **options)

        # set time_step
        ttk.Label(self, text="Time Step: ") \
            .grid(column=0, row=5, sticky=tk.E, **options)
        ttk.Label(self, text="(s)") \
            .grid(column=4, row=5, sticky=tk.W, **options)
        ttk.Scale(self, variable=self.time_step, command=self.time_step_slider_changed,
                  orient='horizontal', length=150, from_=1, to=100) \
            .grid(column=1, row=5, sticky=tk.W, **options)
        ttk.Spinbox(self, textvariable=self.time_step, command=self.time_step_spinbox_changed,
                    increment=0.01, wrap=True, width=5, from_=1, to=100) \
            .grid(column=2, row=5, sticky=tk.W, **options)


        # Create a Tkinter dropdown
        # Dictionary with options
        choices = ['Euler', 'Improved Euler', 'RK4']
        # Find the length of maximum character in the option
        menu_width = len(max(choices, key=len))
        popup_menu = ttk.OptionMenu(self, self.dropdown_value, choices[0], *choices, command=self.popup_menu_changed)
        ttk.Label(self, text="Choose a numerical method").grid(row=10, column=0, sticky=tk.EW)
        popup_menu.grid(row=10, column=1)
        # set the default option
        popup_menu.config(width=menu_width)

        def change_dropdown(*args):
            pass
            # print(self.dropdown_value.get())

        # link function to change dropdown
        self.dropdown_value.trace('w', change_dropdown)

        style.configure("TMenubutton", font=set_font)
        style.configure("TRadiobutton", font=set_font)
        style.configure('TMenubutton', borderwidth=1)

        self.grid(padx=50, pady=50, sticky=tk.NSEW)

    def initial_velocity_slider_changed(self, passed_value):

        self.initial_velocity.set(round(float(passed_value), 1))
        self.update()

    def initial_velocity_spinbox_changed(self):

        self.initial_velocity.set(round(self.initial_velocity.get(), 1))
        self.update()

    def initial_angle_slider_changed(self, passed_value):

        self.initial_angle.set(round(float(passed_value), 1))
        self.update()

    def initial_angle_spinbox_changed(self):

        self.initial_angle.set(round(self.initial_angle.get(), 1))
        self.update()

    def gravity_slider_changed(self, passed_value):

        self.gravity.set(round(float(passed_value), 1))
        self.update()

    def gravity_spinbox_changed(self):

        self.gravity.set(round(self.gravity.get(), 1))
        self.update()

    def initial_x_cord_slider_changed(self, passed_value):

        self.initial_x.set(round(float(passed_value), 1))
        self.update()

    def initial_x_cord_spinbox_changed(self):

        self.initial_x.set(round(self.initial_x.get(), 1))
        self.update()

    def initial_y_cord_slider_changed(self, passed_value):

        self.initial_y_velocity.set(round(float(passed_value), 1))
        self.update()

    def initial_y_cord_spinbox_changed(self):

        self.initial_y.set(round(self.initial_y.get(), 1))
        self.update()

    def time_step_slider_changed(self, passed_value):

        self.time_step.set(round(float(passed_value), 2))
        self.update()

    def time_step_spinbox_changed(self):
        time.sleep(1)
        self.time_step.set(round(self.time_step.get(), 2))
        self.update()

    def popup_menu_changed(self, passed_value):
        self.update()


