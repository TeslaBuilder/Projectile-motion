import math
import time
import matplotlib

import tkinter as tk
import numpy as np

from tkinter import ttk
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

matplotlib.use('TkAgg')


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
        self.initial_angle = tk.DoubleVar(value=60.0)
        self.initial_x = tk.DoubleVar(value=0.0)
        self.initial_y = tk.DoubleVar(value=0.0)
        self.gravity = tk.DoubleVar(value=9.8)
        self.time_step = tk.DoubleVar(value=0.1)
        # self.mass = tk.DoubleVar(value=1.0)

        self.initial_vx = self.initial_velocity.get() * np.cos(self.initial_angle.get())
        self.initial_vy = self.initial_velocity.get() * np.sin(self.initial_angle.get())
        self.max_flight_time = -2 * self.initial_velocity.get() / self.gravity.get()
        self.x_max_coord = self.initial_x.get() + self.max_flight_time.get() * self.initial_vx.get()
        self.y_max_coord = np.square(self.initial_velocity.get()) * np.suare(np.sin(self.initial_angle.get())) / 2 * self.gravity.get()
        self.figure = Figure(constrained_layout=True, figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor('whitesmoke')
        self.axes = self.figure.add_subplot()
        self.line, = self.axes.plot(self.x_max_coord + 100, self.y_max_coord + 50, 'g', label='plot')
        self.axes.autoscale(enable=True, axis="x", tight=False)
        self.axes.autoscale(enable=True, axis="y", tight=False)
        self.axes.set_title('Projectile motion')
        self.axes.set_xlabel('meter')
        self.axes.set_ylabel('meter')
        # create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.figure_canvas.draw()
        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self, pack_toolbar=False)
        self.toolbar.update()
        # create axes
        self.figure_canvas.get_tk_widget().grid(column=10, row=0, rowspan=20, columnspan=20, padx=10, pady=20)

        self.fig = plt.Figure()
        self.t = np.arange(0, self.max_flight_time.get(), self.time_step.get())

        def animate(i):
            # line.set_ydata(np.sin(t + i / 10.0))  # update the data
            self.line1.set_ydata(self.initial_angle.get() * np.cos(
                np.sqrt(self.gravity.get() / self.length.get()) * (self.t + i / (1 / self.time_step.get()))))
            return self.line1,

        def update_point(n, x, y, point):
            point.set_data(np.array([x[n], y[n]]))
            return point,

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=22, rowspan=10, columnspan=10, padx=10, pady=20)

        self.ax = self.fig.add_subplot(111)
        self.theta = self.initial_angle.get() * np.cos(
            np.sqrt(self.gravity.get() / self.length.get()) * self.t)
        self.line1, = self.ax.plot(self.t, self.theta, linestyle='dotted')
        self.point, = self.ax.plot([self.t[0]], [self.theta[0]], 'o')
        self.ani = animation.FuncAnimation(self.fig, update_point, len(self.t), fargs=(self.t, self.theta, self.point),
                                           interval=self.time_rate.get(), blit=True)
        plt.show()

        tk.Checkbutton(self, text='autoscale', variable=self.autoscale, onvalue=1, offvalue=0,
                       command=self.autoscale_cb_changed) \
            .grid(column=10, row=9, padx=10, pady=0)

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

        # get damping of pendulum
        #ttk.Label(self, text="Damping: ") \
        #    .grid(column=0, row=5, sticky=tk.E, **options)
        #ttk.Scale(self, variable=self.damping, command=self.damping_slider_changed,
        #          orient='horizontal', length=150, from_=1, to=50) \
        #    .grid(column=1, row=5, sticky=tk.W, **options)
        #ttk.Spinbox(self, textvariable=self.damping, command=self.damping_spinbox_changed,
        #            increment=0.1, wrap=True, width=5, from_=1, to=50) \
        #    .grid(column=2, row=5, sticky=tk.W, **options)

        # get force_amplitude of pendulum
        #ttk.Label(self, text="Force Amplitude: ") \
        #    .grid(column=0, row=6, sticky=tk.E, **options)
        #ttk.Scale(self, variable=self.force_amplitude, command=self.force_amplitude_slider_changed,
        #          orient='horizontal', length=150, from_=1, to=50) \
        #    .grid(column=1, row=6, sticky=tk.W, **options)
        #ttk.Spinbox(self, textvariable=self.force_amplitude, command=self.force_amplitude_spinbox_changed,
        #            increment=0.1, wrap=True, width=5, from_=1, to=50) \
        #    .grid(column=2, row=6, sticky=tk.W, **options)

        # get force_frequency of pendulum
        #ttk.Label(self, text="Force Frequency: ") \
        #    .grid(column=0, row=7, sticky=tk.E, **options)
        #ttk.Scale(self, variable=self.force_frequency, command=self.force_frequency_slider_changed,
        #          orient='horizontal', length=150, from_=1, to=50) \
        #    .grid(column=1, row=7, sticky=tk.W, **options)
        #ttk.Spinbox(self, textvariable=self.force_frequency, command=self.force_frequency_spinbox_changed,
        #            increment=0.1, wrap=True, width=5, from_=1, to=50) \
        #    .grid(column=2, row=7, sticky=tk.W, **options)

        # set time_step of pendulum
        ttk.Label(self, text="Time Step: ") \
            .grid(column=0, row=5, sticky=tk.E, **options)
        ttk.Label(self, text="(s)") \
            .grid(column=4, row=5, sticky=tk.W, **options)
        ttk.Scale(self, variable=self.time_step, command=self.time_step_slider_changed,
                  orient='horizontal', length=150, from_=0.01, to=0.1) \
            .grid(column=1, row=5, sticky=tk.W, **options)
        ttk.Spinbox(self, textvariable=self.time_step, command=self.time_step_spinbox_changed,
                    increment=0.01, wrap=True, width=5, from_=0.01, to=0.1) \
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

    def show_animation(self):
        self.update()
        self.update_plot()

    def update(self):

        t_initial = 0
        t_stop = 30
        t = np.arange(t_initial, t_stop, self.time_step.get())

        # Catch the choice of numerical method
        def euler(dt, v, i_theta):
            dt = dt * np.sqrt(self.gravity.get() / self.length.get())
            d_theta = dt * v
            dv = dt * (-np.sin(i_theta))
            v = v + dv
            i_theta = i_theta + d_theta
            return v, i_theta

        def euler_array(v_0, i_theta, t_0, t_end):
            temp_list = []
            t_temp = t_0
            while t_temp < t_end:
                v_0, i_theta = euler(self.time_step.get(), v_0, i_theta)
                t_temp = t_temp + self.time_step.get()
                temp_list.append((t, i_theta, v_0))
            return temp_list

        if self.dropdown_value.get() == 'Euler':
            euler_list = []
            euler_list = euler_array(self.initial_angular_velocity.get(), self.initial_angle.get(), t_initial, t_stop)
            t = [x[0] for x in euler_list]
            theta = [x[1] for x in euler_list]
        elif self.dropdown_value.get() == 'Improved Euler':
            theta = self.initial_angle.get() * np.cos(np.sqrt(self.gravity.get() / self.length.get()) * t)
        elif self.dropdown_value.get() == 'RK4':
            theta = self.initial_angle.get() * np.cos(np.sqrt(self.gravity.get() / self.length.get()) * t)
        else:
            theta = self.initial_angle.get() * np.cos(np.sqrt(self.gravity.get() / self.length.get()) * t)

        self.line.set_data(t, theta)

        if self.autoscale.get() == 0:
            ax1_lim = ((min(t), min(theta)), (max(t), max(theta)))
            self.axes.update_datalim(ax1_lim)
        else:
            self.axes.relim()
        self.axes.autoscale(enable=True, axis="y", tight=True)
        self.figure_canvas.draw()
        plt.ion()
        self.fig = plt.Figure()

        self.t = np.arange(0, 30, self.time_step.get())

    def update_plot(self):
        time.sleep(1)
        def init():
            self.line1.set_ydata(self.initial_angle.get() * np.cos(
                np.sqrt(self.gravity.get() / self.length.get()) * self.t))
            # time_text.set_text('')
            return self.line1,

        def animate(i):
            self.line1.set_ydata(self.initial_angle.get() * np.cos(
                np.sqrt(self.gravity.get() / self.length.get()) * (self.t + i / 10)))
            return self.line1,

        def update_point(n, x, y, point):
            point.set_data(np.array([x[n], y[n]]))
            return point,

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=0, row=22, rowspan=10, columnspan=10, padx=10, pady=20)

        self.ax = self.fig.add_subplot(111)

        self.theta = self.initial_angle.get() * np.cos(
            np.sqrt(self.gravity.get() / self.length.get()) * self.t)

        self.line1, = self.ax.plot(self.t, self.theta, linestyle='dotted')
        self.point, = self.ax.plot([self.t[0]], [self.theta[0]], 'o')

        self.ani = animation.FuncAnimation(self.fig, update_point, len(self.t), fargs=(self.t, self.theta, self.point),
                                           interval=self.time_rate.get() / 10, blit=True)
        plt.show()
