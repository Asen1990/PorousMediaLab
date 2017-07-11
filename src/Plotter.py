import math
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
from matplotlib.colors import ListedColormap

sns.set_style("whitegrid")


def custom_plot(lab, x, y, ttl='', y_lbl='', x_lbl=''):
    plt.figure()
    ax = plt.subplot(111)
    plt.plot(x, y, lw=3)
    plt.title(ttl)
    plt.xlim(x[0], x[-1])
    plt.ylabel(y_lbl)
    plt.xlabel(x_lbl)
    ax.grid(linestyle='-', linewidth=0.2)
    plt.show()


def plot_depths(lab, element, depths=[0, 1, 2, 3, 4], years_to_plot=10, days=True):
    plt.figure()
    ax = plt.subplot(111)
    if element == 'Temperature':
        plt.title('Temperature at specific depths')
        plt.ylabel('Temperature, C')
    else:
        plt.title(element + ' concentration at specific depths')
        plt.ylabel('mmol/L')
    if lab.tend > years_to_plot:
        num_of_elem = int(years_to_plot / lab.dt)
    else:
        num_of_elem = len(lab.time)
    if days:
        t = lab.time[-num_of_elem:] * 365
        plt.xlabel('Days, [day]')
    else:
        t = lab.time[-num_of_elem:]
        plt.xlabel('Years, [year]')
    for depth in depths:
        lbl = str(depth) + ' cm'
        plt.plot(t, lab.species[element]['concentration'][
                 int(depth / lab.dx)][-num_of_elem:], lw=3, label=lbl)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(linestyle='-', linewidth=0.2)
    plt.show()


def plot_times(lab, element, time_slices=[0, 1, 2, 3, 4]):
    plt.figure()
    ax = plt.subplot(111)
    if element == 'Temperature':
        plt.title('Temperature profile')
        plt.xlabel('Temperature, C')
    else:
        plt.title(element + ' concentration')
        plt.xlabel('mmol/L')
    plt.ylabel('Depth, cm')
    for tms in time_slices:
        lbl = '%.2f day' % (tms * 365)
        plt.plot(lab.species[element]['concentration'][
                 :, int(tms / lab.dt)], -lab.x, lw=3, label=lbl)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=2)
    ax.grid(linestyle='-', linewidth=0.2)
    plt.show()


def plot_profiles(lab):
    for element in sorted(lab.species):
        plot_profile(lab, element)


def plot_profile(lab, element):
    plt.figure()
    plt.plot(lab.profiles[element], -lab.x,
             sns.xkcd_rgb["denim blue"], lw=3, label=element)
    if element == 'Temperature':
        plt.title('Temperature profile after %.2f days')
        plt.xlabel('Temperature, C')
    else:
        plt.title('%s concentration' % (element, ))
        plt.xlabel('mmol/L')
    plt.ylabel('Depth, cm')
    ax = plt.gca()
    ax.ticklabel_format(useOffset=False)
    ax.grid(linestyle='-', linewidth=0.2)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_contourplots(lab, **kwargs):
    for element in sorted(lab.species):
        contour_plot(lab, element, **kwargs)


def contour_plot(lab, element, labels=False, days=False, last_year=False):
    plt.figure()
    plt.title(element + ' concentration')
    resoluion = 100
    n = math.ceil(lab.time.size / resoluion)
    if last_year:
        k = n - int(1 / lab.dt)
    else:
        k = 1
    if days:
        X, Y = np.meshgrid(lab.time[k::n] * 365, -lab.x)
        plt.xlabel('Days, [day]')
    else:
        X, Y = np.meshgrid(lab.time[k::n], -lab.x)
        plt.xlabel('Time')
    z = lab.species[element]['concentration'][:, k - 1:-1:n]
    CS = plt.contourf(X, Y, z, 51, cmap=ListedColormap(
        sns.color_palette("Blues", 51)), origin='lower')
    if labels:
        plt.clabel(CS, inline=1, fontsize=10, colors='w')
    cbar = plt.colorbar(CS)
    plt.ylabel('Depth, [cm]')
    ax = plt.gca()
    ax.ticklabel_format(useOffset=False)
    cbar.ax.set_ylabel('%s [mmol/L]' % element)
    if element == 'Temperature':
        plt.title('Temperature contour plot')
        cbar.ax.set_ylabel('Temperature, C')
    plt.show()


def plot_contourplots_of_rates(lab, **kwargs):
    elements = sorted(lab.species)
    if 'Temperature' in elements:
        elements.remove('Temperature')
    for element in elements:
        contour_plot_of_rates(lab, element, **kwargs)


def contour_plot_of_rates(lab, element, labels=False, days=True, last_year=False):
    plt.figure()
    plt.title('Rate of %s consumption/production' % element)
    resoluion = 100
    n = math.ceil(lab.time.size / resoluion)
    if last_year:
        k = n - int(1 / lab.dt)
    else:
        k = 1
    z = lab.species[element]['rates'][:, k - 1:-1:n]
    lim = np.max(np.abs(z))
    lim = np.linspace(-lim - 0.1, +lim + 0.1, 51)
    if days:
        X, Y = np.meshgrid(lab.time[k::n] * 365, -lab.x)
        plt.xlabel('Days, [day]')
    else:
        X, Y = np.meshgrid(lab.time[k::n], -lab.x)
        plt.xlabel('Years, [year]')
    CS = plt.contourf(X, Y, z, 20, cmap=ListedColormap(sns.color_palette(
        "RdBu_r", 101)), origin='lower', levels=lim, extend='both')
    if labels:
        plt.clabel(CS, inline=1, fontsize=10, colors='w')
    cbar = plt.colorbar(CS)
    plt.ylabel('Depth, [cm]')
    ax = plt.gca()
    ax.ticklabel_format(useOffset=False)
    cbar.ax.set_ylabel('Rate %s [mmol/L/yr]' % element)
    plt.show()
