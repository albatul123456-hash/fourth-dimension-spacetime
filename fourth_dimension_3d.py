import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Basic Sciences Club | Fourth Dimension
# Units: c = 1, time in years, distance in light-years.
T_MAX = 10.0
state = {'running': True, 't': 0.0}

fig = plt.figure(figsize=(14, 8), facecolor='#071225')
ax = fig.add_axes([0.05, 0.23, 0.59, 0.69], projection='3d')
ax.set_facecolor('#071225')
info = fig.add_axes([0.68, 0.29, 0.29, 0.57])
info.set_facecolor('#10233b')
info.set_xticks([]); info.set_yticks([])
for spine in info.spines.values(): spine.set_color('#365574')

fig.suptitle('THE FOURTH DIMENSION  |  SPACETIME', color='white', fontsize=20, weight='bold', y=0.98)
fig.text(0.5, 0.935, 'Light cone  •  Worldlines  •  Time dilation', ha='center', color='#a9cce8', fontsize=11)

# Future and past light cones from the origin (x^2+y^2=t^2).
angles = np.linspace(0, 2*np.pi, 55)
heights = np.linspace(0, T_MAX, 32)
H, A = np.meshgrid(heights, angles)
X = H * np.cos(A)
Y = H * np.sin(A)
ax.plot_surface(X, Y, H, alpha=0.12, color='#3ca6ff', linewidth=0, shade=False)
ax.plot_surface(X*0.35, Y*0.35, -H*0.35, alpha=0.09, color='#bd82ff', linewidth=0, shade=False)
for t_ring in [2.5, 5, 7.5, 10]:
    ax.plot(t_ring*np.cos(angles), t_ring*np.sin(angles), np.full_like(angles,t_ring), color='#4b9dcc', alpha=0.32, lw=0.8)

# Earth worldline and moving spacecraft worldline.
ax.plot([0,0],[0,0],[0,T_MAX], color='#40d9ff', lw=3, label='Earth worldline')
ship_line, = ax.plot([], [], [], color='#ffcc66', lw=2.5, label='Spacecraft worldline')
earth_dot, = ax.plot([], [], [], marker='o', markersize=10, color='#40d9ff', linestyle='None')
ship_dot, = ax.plot([], [], [], marker='o', markersize=10, color='#ffcc66', linestyle='None')
connector, = ax.plot([], [], [], '--', color='white', lw=1, alpha=0.5)
ax.set_xlim(-10, 10); ax.set_ylim(-10, 10); ax.set_zlim(-3.6, 10)
ax.set_xlabel('x (light-years)', color='white', labelpad=8)
ax.set_ylabel('y (light-years)', color='white', labelpad=8)
ax.set_zlabel('ct (light-years)', color='white', labelpad=8)
ax.tick_params(colors='#b9d0e8', labelsize=8)
ax.view_init(elev=23, azim=-64)
ax.set_box_aspect((1,1,0.95))
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.fill = False
    axis.line.set_color('#6e8ca8')
ax.legend(loc='upper left', fontsize=9, facecolor='#10233b', labelcolor='white')

info.text(0.07, 0.92, 'RELATIVITY LAB', color='#a9cce8', fontsize=14, weight='bold', transform=info.transAxes)
earth_text = info.text(0.07, 0.74, '', color='#40d9ff', fontsize=15, transform=info.transAxes)
ship_text = info.text(0.07, 0.58, '', color='#ffcc66', fontsize=15, transform=info.transAxes)
speed_text = info.text(0.07, 0.42, '', color='white', fontsize=12, transform=info.transAxes)
gamma_text = info.text(0.07, 0.32, '', color='white', fontsize=12, transform=info.transAxes)
info.text(0.07, 0.13, 'Question: Is there one universal\n"now" for every observer?', color='#d1def2', fontsize=11, transform=info.transAxes)

slider_ax = fig.add_axes([0.17, 0.12, 0.55, 0.035], facecolor='#1c3552')
speed_slider = Slider(slider_ax, 'Speed / c', 0.0, 0.99, valinit=0.60, valstep=0.01, color='#ffcc66')
speed_slider.label.set_color('white'); speed_slider.valtext.set_color('white')
play_ax = fig.add_axes([0.76, 0.11, 0.10, 0.06])
reset_ax = fig.add_axes([0.87, 0.11, 0.10, 0.06])
play_button = Button(play_ax, 'Pause', color='#1c3552', hovercolor='#365574')
reset_button = Button(reset_ax, 'Reset', color='#1c3552', hovercolor='#365574')
play_button.label.set_color('white'); reset_button.label.set_color('white')


def draw():
    t = state['t']
    beta = speed_slider.val
    gamma = 1.0 / np.sqrt(1.0 - beta**2)
    proper_time = t / gamma
    timeline = np.linspace(0, t, 100)
    ship_line.set_data(beta * timeline, np.zeros_like(timeline))
    ship_line.set_3d_properties(timeline)
    earth_dot.set_data([0], [0]); earth_dot.set_3d_properties([t])
    ship_dot.set_data([beta*t], [0]); ship_dot.set_3d_properties([t])
    connector.set_data([0,beta*t], [0,0]); connector.set_3d_properties([t,t])
    earth_text.set_text(f'EARTH CLOCK\n{t:5.2f} years')
    ship_text.set_text(f'SHIP CLOCK\n{proper_time:5.2f} years')
    speed_text.set_text(f'Speed: {beta:.2f} c')
    gamma_text.set_text(f'Lorentz factor: {gamma:.3f}')
    return ship_line, earth_dot, ship_dot, connector, earth_text, ship_text, speed_text, gamma_text


def animate(_frame):
    if state['running']:
        state['t'] += 0.04
        if state['t'] > T_MAX:
            state['t'] = 0.0
    return draw()


def toggle(_event):
    state['running'] = not state['running']
    play_button.label.set_text('Pause' if state['running'] else 'Play')
    fig.canvas.draw_idle()


def reset(_event):
    state['t'] = 0.0
    state['running'] = True
    play_button.label.set_text('Pause')
    draw()
    fig.canvas.draw_idle()


def speed_changed(_value):
    draw()
    fig.canvas.draw_idle()

play_button.on_clicked(toggle)
reset_button.on_clicked(reset)
speed_slider.on_changed(speed_changed)
draw()
ani = FuncAnimation(fig, animate, interval=40, blit=False, cache_frame_data=False)
plt.show()
