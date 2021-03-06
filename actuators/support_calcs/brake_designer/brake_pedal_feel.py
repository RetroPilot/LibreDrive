import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from numpy.polynomial import polynomial as Poly

"""
Pedal Displacement
Fp * Lp * As = dmc * ki * lp * Amc

Fp: pedal force by driver (with preload of ~50N)
Lp: distance between pedal pad and top fixed pivot of pedal arm
As: internal section areas of PFS (pedal feel simulator)

dmc (mm): main cylinder piston displacement
ki: stiffness during each stage (see below)
lp: distance between push rod and top fixed pivot of pedal arm
Amc: internal section area of main cylinder


ki: {
    ka*kb/(ka+kb)   @ dmc:[0.5,A*Lmc)
    kb              @ dmc:[A*Lmc,B*Lmc)
    kb+kc           @ dmc:[B*Lmc,Lmc]
    }

Where:
ka, kb, kc: three spring stiffness constants in main cylinder
Lmc: maximum main cylinder displacement
A, B: regions where 0 < A < B < 1 
"""


def pedal_force_disp(dmc, krange, midvals, pre_load, max_load):
    Fp = []

    # kabc = [ka * kb / (ka + kb), kb, kb + kc]
    intersect_x = [krange[0] * dmc[-1], krange[1] * dmc[-1]]
    intersect_y = midvals
    for disp in dmc:
        if disp < intersect_x[0]:
            m = (intersect_y[0] - pre_load) / (intersect_x[0] - 0)
            b = pre_load
        elif intersect_x[0] <= disp < intersect_x[1]:
            m = (intersect_y[1] - intersect_y[0]) / (intersect_x[1] - intersect_x[0])
            b = intersect_y[0] - m*intersect_x[0]
        else:
            m = (max_load - intersect_y[1]) / (dmc[-1] - intersect_x[1])
            b = max_load - m * dmc[-1]
        # Fp.append( disp * ki * lp * Amc / (Lp * As) )
        Fp.append(disp * m + b)

    c, stats = Poly.polyfit(dmc, Fp, 3, full=True)
    ffit = Poly.polyval(dmc, c)

    eq = 'f(x) = {:.2f} + {:.2f}*x + {:.2f}*x^2'.format(c[0], c[1], c[2])

    return ffit, eq


def pressure_disp(pforce, bore, pratio, response):
    Amc = np.pi * (bore/1000 / 2) ** 2

    x = np.array(pforce)
    pressure = x * pratio / Amc

    p_min = pressure[0]
    p_max = pressure[-1]
    p_mid = (p_max - p_min) / 2

    x0 = (np.abs(pressure - p_mid)).argmin()
    # x0 = 10

    a = 1
    k = response

    s = p_min + (p_max - p_min) * (1 / (1 + np.exp(-k * (x - x0)))) ** a

    eq = 'f(x) = {:.2f} + ({:.2f}  - {:.2f}) * (1 / (1 + e^(-{:.2f} * (x - {:.2f}))))^{:.2f}'.format(p_min,p_max,p_min,k,x0,a)

    return s, eq

# Pedal Displacement
dp_min = 0
dp_max = 20
dp_step = 0.1
dp = np.arange(dp_min, dp_max, dp_step)

# Pedal Ratio
l_ratio = 8
Lp = 160
lp = Lp/l_ratio

# Pedal Preload
fp_pre = 0
fp_max = 400
p_resp = 0.02

# Main cylinder
dmc = dp / l_ratio
mc_bore = 22

# Pedal Feel regions
regions = [0.33, 0.66]
midvals = [80, 180]

# Calculate values
Fp, Fp_eq = pedal_force_disp(dmc, regions, midvals, fp_pre, fp_max)
Pmc, Pmc_eq = pressure_disp(Fp, mc_bore, l_ratio, p_resp)


# Plot stuff
f, (ax1, ax2, ax3) = plt.subplots(1, 3)
f.tight_layout()
plt.subplots_adjust(left=0.25, bottom=0.4, top=0.75)
plt.figtext(.5,.9,'Pedal Feel Thingy', fontsize=12, ha='center')
stitle1 = plt.figtext(0.5,.85,'Pedal Force:{}'.format(Fp_eq),fontsize=10,ha='center')
stitle2 = plt.figtext(0.5,.8,'Piston Pressure:{}'.format(Pmc_eq),fontsize=10,ha='center')

ax_ka = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_kb = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_response = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_bore = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_ratio = plt.axes([0.25, 0.05, 0.65, 0.03])

s_ka = Slider(ax_ka, 'Pedal Feel Stage 1', fp_pre, fp_max, valinit=midvals[0])
s_kb = Slider(ax_kb, 'Pedal Feel Stage 2', fp_pre, fp_max, valinit=midvals[1])
s_response = Slider(ax_response, 'Pedal Response', 0, 0.5, valinit=p_resp)
s_bore = Slider(ax_bore, 'Master Cylinder Bore', 0.01, 50, valinit=mc_bore)
s_ratio = Slider(ax_ratio, 'Pedal Ratio', 0.01, 20, valinit=l_ratio)

l1, = ax1.plot(dp, dmc)
ax1.set_xlabel('Pedal Displacement (mm)')
ax1.set_ylabel('Piston Displacement (mm)')

l2, = ax2.plot(dp, Fp)
ax2.set_xlabel('Pedal Displacement (mm)')
ax2.set_ylabel('Pedal Force (N)')

pdisp, peq = pressure_disp(Fp, mc_bore, l_ratio, p_resp)
l3, = ax3.plot(dp, pdisp)
ax3.set_xlabel('Pedal Displacement (mm)')
ax3.set_ylabel('Piston Pressure (Pa)')


def update(val):
    global regions, dmc, fp_pre, Lp, lp
    ka = s_ka.val
    kb = s_kb.val
    resp = s_response.val
    bore = s_bore.val
    ratio = s_ratio.val

    yA = ka
    yB = kb
    Fp, Fp_eq = pedal_force_disp(dmc, regions, [yA, yB], fp_pre, fp_max)
    l2.set_ydata(Fp)

    pdisp, peq = pressure_disp(Fp, bore, ratio, resp)
    l3.set_ydata(pdisp)

    ax2.relim()
    ax2.autoscale_view(True, True, True)

    ax3.relim()
    ax3.autoscale_view(True, True, True)

    stitle1.set_text(Fp_eq)
    stitle2.set_text(peq)

    f.canvas.draw_idle()


s_ka.on_changed(update)
s_kb.on_changed(update)
s_response.on_changed(update)
s_bore.on_changed(update)
s_ratio.on_changed(update)

plt.show()
