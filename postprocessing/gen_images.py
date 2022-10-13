# -*- coding: utf-8 -*-
# Version date: Nov 07, 2021
# @author: Sara Brambilla

import math

import numpy as np
import pylab
import imageio
from matplotlib.colors import Normalize
from misc import *
from matplotlib import pyplot as plt
import matplotlib.cm as cm


def generate_greys_colorbar():
    mycbar = [
        [1.00000, 0.00000, 0.00000],
        [0.76190, 0.76190, 0.76190],
        [0.74603, 0.74603, 0.74603],
        [0.73016, 0.73016, 0.73016],
        [0.71429, 0.71429, 0.71429],
        [0.69841, 0.69841, 0.69841],
        [0.68254, 0.68254, 0.68254],
        [0.66667, 0.66667, 0.66667],
        [0.65079, 0.65079, 0.65079],
        [0.63492, 0.63492, 0.63492],
        [0.61905, 0.61905, 0.61905],
        [0.60317, 0.60317, 0.60317],
        [0.58730, 0.58730, 0.58730],
        [0.57143, 0.57143, 0.57143],
        [0.55556, 0.55556, 0.55556],
        [0.53968, 0.53968, 0.53968],
        [0.52381, 0.52381, 0.52381],
        [0.50794, 0.50794, 0.50794],
        [0.49206, 0.49206, 0.49206],
        [0.47619, 0.47619, 0.47619],
        [0.46032, 0.46032, 0.46032],
        [0.44444, 0.44444, 0.44444],
        [0.42857, 0.42857, 0.42857],
        [0.41270, 0.41270, 0.41270],
        [0.39683, 0.39683, 0.39683],
        [0.38095, 0.38095, 0.38095],
        [0.36508, 0.36508, 0.36508],
        [0.34921, 0.34921, 0.34921],
        [0.33333, 0.33333, 0.33333],
        [0.31746, 0.31746, 0.31746],
        [0.30159, 0.30159, 0.30159],
        [0.28571, 0.28571, 0.28571],
        [0.26984, 0.26984, 0.26984],
        [0.25397, 0.25397, 0.25397],
        [0.23810, 0.23810, 0.23810],
        [0.22222, 0.22222, 0.22222],
        [0.20635, 0.20635, 0.20635],
        [0.19048, 0.19048, 0.19048],
        [0.17460, 0.17460, 0.17460],
        [0.15873, 0.15873, 0.15873],
        [0.14286, 0.14286, 0.14286],
        [0.12698, 0.12698, 0.12698],
        [0.11111, 0.11111, 0.11111],
        [0.09524, 0.09524, 0.09524],
        [0.07937, 0.07937, 0.07937],
        [0.06349, 0.06349, 0.06349],
        [0.04762, 0.04762, 0.04762],
        [0.03175, 0.03175, 0.03175],
        [0.01587, 0.01587, 0.01587],
        [0.00000, 0.00000, 0.00000]]

    # mycbar = np.array(mycbar, dtype=np.float32) * 255.
    # mycbar = np.round(mycbar, 0)
    # pl_grey = []
    # sh = np.shape(mycbar)
    #
    # val = np.linspace(0., 1., sh[0])
    # for i in range(0, sh[0]):
    #     rgbstr = 'rgb(%d, %d, %d)' % (mycbar[i, 1], mycbar[i, 1], mycbar[i, 2])
    #     pl_grey.append([val[i], rgbstr])

    return mycbar


def generate_jet_colorbar(m: int):
    n = int(math.ceil(float(m) / 4.))
    u = np.concatenate((np.arange(1, n + 1) / n, np.ones(n - 1), np.arange(n, 0, -1) / n))
    g = math.ceil(n * 0.5) - ((m % 4.) == 1) + np.arange(1, len(u) + 1)
    r = g + n
    b = g - n

    iremove = np.where(g > m)
    iremove = iremove[0]
    g = np.delete(g, iremove, None)
    g = g.astype(int) - 1

    iremove = np.where(r > m)
    iremove = iremove[0]
    r = np.delete(r, iremove, None)
    r = r.astype(int) - 1

    iremove = np.where(b < 1)
    iremove = iremove[0]
    b = np.delete(b, iremove, None)
    b = b.astype(int) - 1

    j = np.zeros((int(m), 3), dtype=np.float32)
    for i in range(0, len(r)):
        j[r[i], 0] = u[i]
    for i in range(0, len(g)):
        j[g[i], 1] = u[i]
    for i in range(0, len(b)):
        j[b[i], 2] = u[len(u) - len(b) + i]

    return j


def plot_fuelheight(qf: GridClass, ground_level_fuel_height: np.array, img_specs: ImgClass):

    myvmax = np.max(ground_level_fuel_height)
    myvmin = -myvmax/64. - 1e-6

    my_cmap = generate_jet_colorbar(65)
    my_cmap[0][::1] = 1.
    my_cmap = pylab.matplotlib.colors.ListedColormap(my_cmap, 'my_colormap', N=None)

    fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
    ax = fig.add_subplot(111)

    ground_level_fuel_height[np.where(ground_level_fuel_height == 0)] = myvmin
    pylab.imshow(ground_level_fuel_height,
                 cmap=my_cmap,
                 interpolation='none',
                 origin='lower',
                 extent=qf.horizontal_extent,
                 vmin=myvmin,
                 vmax=myvmax)
    cbar = pylab.colorbar()
    cbar.set_label("Fuel height (ground level) [m]",
                   size=img_specs.axis_font["size"],
                   fontname=img_specs.axis_font["fontname"])
    cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])
    pylab.xlabel('X [m]', **img_specs.axis_font)
    pylab.ylabel('Y [m]', **img_specs.axis_font)
    set_ticks_font(img_specs.axis_font, ax)
    pylab.savefig(os.path.join(img_specs.save_dir, 'fuel_height_ground_level.png'))
    pylab.close()


def set_colormap_massburnt(ncol: int):

    # Init
    usr_colormap = list()
    myvmin = np.zeros((2, 1))
    myvmax = np.zeros((2, 1))

    # Colormap #1 - Percentage mass burnt
    my_cmap1 = generate_jet_colorbar(ncol)
    my_cmap1[0][::1] = 1.
    my_cmap1 = pylab.matplotlib.colors.ListedColormap(my_cmap1, 'my_colormap', N=None)
    my_cmap1.set_bad(color='none')
    usr_colormap.append(my_cmap1)

    myvmin[0] = -100. / (float(ncol) - 1) - 1e-6
    myvmax[0] = 100.

    # Colormap #2 - Burnt/Unburnt
    my_cmap2 = np.zeros((3, 3), dtype=np.float32)
    for i in range(0, 3):
        my_cmap2[0, i] = 1.
    my_cmap2[2, 0] = 1.
    my_cmap2[2, 1] = 0.6
    my_cmap2[2, 2] = 0.6
    my_cmap2 = pylab.matplotlib.colors.ListedColormap(my_cmap2, 'my_colormap', N=None)
    my_cmap2.set_bad(color='none')
    usr_colormap.append(my_cmap2)

    myvmin[1] = 0
    myvmax[1] = 3

    return usr_colormap, myvmin, myvmax


def assign_vals(k_loc, currval: np.array, val: float):
    if len(k_loc) > 0:
        i_loc = k_loc[1]
        j_loc = k_loc[0]
        currval[tuple([j_loc, i_loc])] = val


def get_mass_burnt(fuel_dens_idx: np.ndarray, icolor_scheme: int, currval0: np.array, plotvar: np.array):
    # Create copy
    currval = copy.deepcopy(currval0)

    if icolor_scheme == 1:
        # Find unburnt fuel
        k_loc = np.where(plotvar == 0.)
        assign_vals(k_loc, currval, 2.5)

        # Find burnt fuel
        k_loc = np.where(plotvar > 0.)
        assign_vals(k_loc, currval, 1.5)

        # No fuel (may have been overwritten by unburnt)
        currval[fuel_dens_idx] = np.nan
    else:
        k_loc = np.where(plotvar > 0.)
        if len(k_loc) > 0:
            i_loc = k_loc[1]
            j_loc = k_loc[0]
            currval[tuple([j_loc, i_loc])] = plotvar[tuple([j_loc, i_loc])]

    return currval


def plot_percmassburnt(qf: GridClass, plotvar: list, fuel_dens_idx: np.ndarray,
                       img_specs: ImgClass, flags: FlagsClass):
    ncol = 64

    # Nan where there is no fuel
    currval0 = np.zeros((qf.ny, qf.nx), dtype=np.float32)
    currval0[fuel_dens_idx] = np.nan

    # Colormap scheme
    [usr_colormap, myvmin, myvmax] = set_colormap_massburnt(ncol)

    colorbar_label = ["Mass burnt (vertically-integ.) [%]", ""]
    savestr = ['perc_mass_burnt', 'bw_perc_mass_burnt']

    # 2D plot
    for icolor_scheme in range(0, 2):
        file_list = []

        for i in range(0, qf.ntimes):
            print("     * time %d/%d" % (i + 1, qf.ntimes))

            currval = get_mass_burnt(fuel_dens_idx, icolor_scheme, currval0, plotvar[i].squeeze())

            fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
            ax = fig.add_subplot(111)

            pylab.imshow(currval,
                         cmap=usr_colormap[icolor_scheme],
                         interpolation='none',
                         origin='lower',
                         extent=qf.horizontal_extent,
                         vmin=myvmin[icolor_scheme],
                         vmax=myvmax[icolor_scheme])
            cbar = pylab.colorbar()
            cbar.set_label(colorbar_label[icolor_scheme],
                           size=img_specs.axis_font["size"],
                           fontname=img_specs.axis_font["fontname"])
            if icolor_scheme == 1:
                cbar.set_ticks([0.5, 1.5, 2.5])
                cbar.set_ticklabels(['No Fuel', 'Burnt', 'Unburnt'])
            cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])
            pylab.xlabel('X [m]', **img_specs.axis_font)
            pylab.ylabel('Y [m]', **img_specs.axis_font)
            pylab.title('Time = %s s' % qf.time[i], **img_specs.title_font)
            set_ticks_font(img_specs.axis_font, ax)
            fname = '%s_Time_%d_s.png' % (savestr[icolor_scheme], qf.time[i])
            fname = os.path.join(img_specs.save_dir, fname)
            pylab.savefig(fname)
            pylab.close()
            del currval

            if img_specs.gen_gif == 1:
                file_list.append(fname)

        if img_specs.gen_gif == 1:
            fname_gif = '%s.gif' % savestr
            fname_gif = os.path.join(img_specs.gif_dir, fname_gif)
            make_gif(fname_gif, file_list)

    # 3D plot on terrain
    if flags.topo > 0:
        # m = cm.ScalarMappable(cmap='Greys')
        greys_map_array = generate_greys_colorbar()
        n = np.shape(greys_map_array)
        ncol = n[0]
        greys_map = pylab.matplotlib.colors.ListedColormap(greys_map_array, 'my_colormap', N=None)
        greys_map.set_bad(color='none')
        file_list = []
        myvmax = np.max(qf.terrain_elevation) + 1.e-6
        myvmin = np.min(qf.terrain_elevation) - 1.e-6
        delta = (myvmax - myvmin) / (ncol - 1)
        myvmin -= delta

        val = np.linspace(myvmin, myvmax, ncol + 1)

        x = np.linspace(qf.dx * 0.5, qf.Lx - qf.dx * 0.5, qf.nx)
        y = np.linspace(qf.dy * 0.5, qf.Ly - qf.dy * 0.5, qf.ny)
        x, y = np.meshgrid(x, y)

        # color by terrain elevation
        currval0 = np.ones((qf.ny, qf.nx, 4))
        for ival in range(0, ncol):
            ii, jj = np.where((val[ival] <= qf.terrain_elevation) & (qf.terrain_elevation < val[ival + 1]))
            for m in range(0, len(ii)):
                currval0[jj[m], ii[m], 0:-1] = greys_map_array[ival]

        for i in range(1, qf.ntimes):
            print("     * time (3d) %d/%d" % (i + 1, qf.ntimes))

            currval = copy.deepcopy(currval0)
            loc_var = plotvar[i].squeeze()
            k_loc = np.where(loc_var > 0.)
            if len(k_loc) > 0:
                i_loc = k_loc[1]
                j_loc = k_loc[0]
                for m in range(0, len(i_loc)):
                    for icol in range(0, 3):
                        currval[j_loc[m], i_loc[m], icol] = greys_map_array[0][icol]
                    currval[j_loc[m], i_loc[m], 3] = 1

            fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
            ax = fig.add_subplot(111, projection="3d")

            surf = ax.plot_surface(x, y, np.transpose(qf.terrain_elevation),
                                   facecolors=currval,
                                   vmin=myvmin,
                                   vmax=myvmax,
                                   linewidth=0,
                                   cmap=greys_map,
                                   antialiased=True,
                                   shade=True,
                                   edgecolors='none',
                                   color='none',
                                   rcount=max(qf.nx,qf.ny),
                                   ccount=max(qf.nx,qf.ny))

            cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
            cbar.set_label('Terrain elevation [m]', size=img_specs.axis_font["size"], fontname=img_specs.axis_font["fontname"])
            cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])

            pylab.xlabel('X [m]', **img_specs.axis_font)
            pylab.ylabel('Y [m]', **img_specs.axis_font)
            pylab.title('Time = %s s' % qf.time[i], **img_specs.title_font)
            set_ticks_font(img_specs.axis_font, ax)
            ax.set_xlim3d([0, qf.Lx])
            ax.set_ylim3d([0, qf.Ly])
            fname = '%s_Time_%d_s.png' % (savestr, qf.time[i])
            fname = os.path.join(img_specs.save_dir, fname)
            pylab.savefig(fname)
            pylab.close()
            del currval
            del loc_var
            if img_specs.gen_gif == 1:
                file_list.append(fname)

        if img_specs.gen_gif == 1:
            fname_gif = '%s.gif' % savestr
            fname_gif = os.path.join(img_specs.gif_dir, fname_gif)
            make_gif(fname_gif, file_list)




def make_gif(fname_gif: str, file_list: list):
    print("     **** making gif")
    with imageio.get_writer(fname_gif, mode='I', duration=0.25) as writer:
        for f in file_list:
            writer.append_data(imageio.imread(f))


def get_minmax(ntimes: int, plane: int, plane_dir: str, cblim, plotvar: list, no_fuel_idx, ncol_cmap: int):
    if not cblim:
        myvmin = 1e8
        myvmax = -1e8
        for i in range(0, ntimes):
            if plane >= 0:
                if plane_dir == 'xy':
                    currval = plotvar[i][::1, ::1, plane - 1]
                elif plane_dir == 'xz':
                    currval = plotvar[i][plane - 1, ::1, ::1]
                else:
                    print('Invalid plane %s\n' % plane_dir)
                    sys.exit(1)
            else:
                currval = plotvar[i]

            myvmin = min(myvmin, np.min(currval))
            myvmax = max(myvmax, np.max(currval))

        check_equal_cbar_limits(myvmin, myvmax)

    else:
        myvmin = cblim[0]
        myvmax = cblim[1]

    if no_fuel_idx:
        dcol = (myvmax - myvmin) / float(ncol_cmap - 1)
        myvmin -= dcol*1.00001

    return myvmin, myvmax


def check_equal_cbar_limits(myvmin: float, myvmax: float):
    if myvmin == myvmax:
        if myvmin == 0:
            myvmin = -1.
            myvmax = +1.
        else:
            myvmin *= 0.5
            myvmax *= 2.


def get_plane_str(plane: int, plane_dir: str):
    if plane:
        plane_str = '_Plane_%s_%d' % (plane_dir, plane)
    else:
        plane_str = ''

    return plane_str


def get_var2plot(q: GridClass, plotvar: np.array, plane: int, plane_dir: str, no_fuel_idx,
                 myvmin: float, flags: FlagsClass):
    if plane:
        if plane_dir == 'xy':
            currval = plotvar[::1, ::1, plane - 1]
            x = np.linspace(q.dx * 0.5, q.Lx - q.dx * 0.5, q.nx)
            y = np.linspace(q.dy * 0.5, q.Ly - q.dy * 0.5, q.ny)
        elif plane_dir == 'xz':
            currval = plotvar[plane - 1, ::1, 1::1]
            if flags.topo == 0:
                x = np.linspace(q.dx * 0.5, q.Lx - q.dx * 0.5, q.nx)
                x = np.tile(x, (q.nz, 1))
                x = x.T
                y = q.zm[1:-1]
                y = np.tile(y, (q.nx, 1))
            else:
                x = np.linspace(q.dx * 0.5, q.Lx - q.dx * 0.5, q.nx)
                x = np.tile(x, (q.nz, 1))
                y = copy.deepcopy(q.zm_topo[:, plane, 1:-1])
                y = np.squeeze(y)
                for k in range(0, q.nz):
                    y[:, k] = y[:, k] + q.terrain_elevation[:, plane]
                x = x.T
    else:
        x = []
        y = []
        currval = plotvar

    currval = currval.squeeze()

    if no_fuel_idx:
        currval[no_fuel_idx] = myvmin

    return x, y, currval


def get_colormap(ncol_cmap: int, no_fuel_idx):
    my_cmap = generate_jet_colorbar(ncol_cmap)
    if no_fuel_idx:
        my_cmap[0][::1] = 1.
    my_cmap = pylab.matplotlib.colors.ListedColormap(my_cmap, 'my_colormap', N=None)

    return my_cmap


def plot_2d_field(is_ave_time: bool, q: GridClass, plane: int, plane_dir: str, plotvar: list, ystr: str,
                  savestr: str, cblim, img_specs: ImgClass, no_fuel_idx, flags: FlagsClass):

    ncol_cmap = 65
    ntimes, times = get_times(is_ave_time, q)
    myvmin, myvmax = get_minmax(ntimes, plane, plane_dir, cblim, plotvar, no_fuel_idx, ncol_cmap)
    my_cmap = get_colormap(ncol_cmap, no_fuel_idx)

    plane_str = get_plane_str(plane, plane_dir)
    file_list = []
    for i in range(0, ntimes):
        print("     * time %d/%d" % (i + 1, ntimes))

        [_, _, currval] = get_var2plot(q, plotvar[i], plane, plane_dir, no_fuel_idx, myvmin, flags)

        fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
        ax = fig.add_subplot(111)

        pylab.imshow(currval,
                     cmap=my_cmap,
                     interpolation='none',
                     origin='lower',
                     extent=q.horizontal_extent,
                     vmin=myvmin,
                     vmax=myvmax)
        cbar = pylab.colorbar()
        cbar.set_label(ystr, size=img_specs.axis_font["size"], fontname=img_specs.axis_font["fontname"])
        cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])
        pylab.xlabel('X [m]', **img_specs.axis_font)
        pylab.ylabel('Y [m]', **img_specs.axis_font)
        pylab.title('Time = %s s' % times[i], **img_specs.title_font)
        set_ticks_font(img_specs.axis_font, ax)
        fname = '%s_Time_%d_s%s.png' % (savestr, times[i], plane_str)
        fname = os.path.join(img_specs.save_dir, fname)
        pylab.savefig(fname)
        pylab.close()
        if img_specs.gen_gif == 1:
            file_list.append(fname)

    if img_specs.gen_gif == 1:
        fname_gif = '%s%s.gif' % (savestr, plane_str)
        fname_gif = os.path.join(img_specs.gif_dir, fname_gif)
        make_gif(fname_gif, file_list)


def plot_2dvert_field(is_ave_time: bool, q: GridClass, plane: int, plane_dir: str, plotvar: list, ystr: str,
                      savestr: str, cblim, img_specs: ImgClass, no_fuel_idx, flags: FlagsClass):

    ncol_cmap = 65
    ntimes, times = get_times(is_ave_time, q)
    myvmin, myvmax = get_minmax(ntimes, plane, plane_dir, cblim, plotvar, no_fuel_idx, ncol_cmap)
    my_cmap = get_colormap(ncol_cmap, no_fuel_idx)

    plane_str = get_plane_str(plane, plane_dir)
    file_list = []
    for i in range(0, ntimes):
        print("     * time %d/%d" % (i + 1, ntimes))

        [x, y, currval] = get_var2plot(q, plotvar[i], plane, plane_dir, no_fuel_idx, myvmin, flags)

        fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
        ax = fig.add_subplot(111)

        phandle = ax.pcolor(x, y, currval,
                            cmap=my_cmap,
                            vmin=myvmin,
                            vmax=myvmax)

        cbar = fig.colorbar(phandle, ax=ax)
        # cbar = pylab.colorbar()
        cbar.set_label(ystr, size=img_specs.axis_font["size"], fontname=img_specs.axis_font["fontname"])
        cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])
        pylab.xlabel('X [m]', **img_specs.axis_font)
        pylab.ylabel('Z [m]', **img_specs.axis_font)
        pylab.title('Time = %s s' % times[i], **img_specs.title_font)
        set_ticks_font(img_specs.axis_font, ax)
        fname = '%s_Time_%d_s%s.png' % (savestr, times[i], plane_str)
        fname = os.path.join(img_specs.save_dir, fname)
        pylab.savefig(fname)
        pylab.close()
        if img_specs.gen_gif == 1:
            file_list.append(fname)

    if img_specs.gen_gif == 1:
        fname_gif = '%s%s.gif' % (savestr, plane_str)
        fname_gif = os.path.join(img_specs.gif_dir, fname_gif)
        make_gif(fname_gif, file_list)


def set_ticks_font(axis_font: dict, ax):
    # https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(axis_font["fontname"])
        label.set_fontsize(axis_font["size"])

    try:
        for label in ax.get_zticklabels():
            label.set_fontname(axis_font["fontname"])
            label.set_fontsize(axis_font["size"])
    except:
        return


def set_image_specifications(img_specs: ImgClass):
    # https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
    img_specs.figure_size = np.array([12, 8.5])
    fs = 14
    fs_str = str(fs)
    img_specs.axis_font = {'fontname': 'Arial', 'size': fs_str}
    fs_str = str(fs + 2)
    img_specs.title_font = {'fontname': 'Arial', 'size': fs_str, 'fontweight': 'bold'}
    fs_str = str(fs - 2)
    img_specs.colorbar_font = {'fontname': 'Arial', 'size': fs_str}


def get_log_minmax(qf: GridClass, var: list):
    minval = +1e8
    maxval = -1e8
    for it in range(0, qf.ntimes_ave):
        var[it] = np.log10(var[it], where=(var[it] != 0))
        temp = var[it][var[it] != 0]
        if np.size(temp) > 0:
            minval = min(minval, np.min(temp))
        maxval = max(maxval, np.max(var[it]))
    minval = math.floor(minval)
    maxval = math.ceil(maxval)

    return minval, maxval


def plot_firebrands(fuel_dens: list, ignitions: np.array, qf: GridClass,
                    fb: FirebrandClass, img_specs: ImgClass):
    # Define colormap
    # http://matplotlib.org/api/colors_api.html
    mycol = [
        [1., 1., 1.],  # white = no fuel
        [0.765, 0.765, 0.765],  # gray = fuel
        [0.6, 0.8, 1.],  # light blue = initial ignitions
        [0., 1., 0.],  # green = fb on cells already on fire
        [1., 0., 0.],  # red = fb on cells not on fire
        [0., 0., 0.]]  # black = fb on cells without fuel
    my_cmap = pylab.matplotlib.colors.ListedColormap(mycol, 'my_colormap', N=None)

    f0 = np.sum(fuel_dens[0], axis=2)
    currval0 = f0
    currval0[np.where(currval0 > 0)] = 1

    currval0[np.where(ignitions > 0)] = 2
    currval = np.zeros((qf.ny, qf.nx), dtype=np.float32)

    for it in range(0, qf.ntimes - 1):
        print("     * time %d/%d" % (it + 1, qf.ntimes))

        np.copyto(currval, currval0)

        # Firebrands launched during this time perios
        kt = np.where(np.logical_and(fb.time > qf.time[it], fb.time <= qf.time[it + 1]))
        kt = kt[0]

        ii = fb.i[kt]
        jj = fb.j[kt]
        kk = fb.k[kt]

        fb.state = fb.state[kt]

        m = ii * qf.ny + jj
        mu, index = np.unique(m, return_index=True)

        nnew = 0

        for i in range(0, len(mu)):
            j = np.where(m == mu[i])
            j = j[0]

            im = ii[j]
            jm = jj[j]
            km = kk[j]

            if len(fuel_dens) == 1:
                itm = 0
            else:
                itm = it + 1

            elem1 = np.where((fb.state[j] == 0) & (fuel_dens[itm][[jm, im, km]] > 0))
            elem2 = np.where((fb.state[j] == 1) | (fb.state[j] == 2))

            if len(elem1[0]) > 0:
                val_assign = 4
                nnew += 1
            elif len(elem2[0]) > 0:
                val_assign = 3
            else:
                val_assign = 5

            currval[jm[0], im[0]] = val_assign

        fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
        ax = fig.add_subplot(111)

        pylab.imshow(currval, cmap=my_cmap, interpolation='none', origin='lower',
                     extent=qf.horizontal_extent, vmin=-0.5, vmax=5.5)
        cbar = pylab.colorbar(ticks=[0, 1, 2, 3, 4, 5])
        cbar.ax.set_yticklabels(['No fuel', 'Fuel', 'Init. ign.', 'FB exist. fire', 'FB no fire', 'FB no fuel'])
        cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])
        pylab.xlabel('X [m]', **img_specs.axis_font)
        pylab.ylabel('Y [m]', **img_specs.axis_font)
        pylab.title('Time = %s-%s s - # new fires = %d' % (qf.time[it], qf.time[it+1], nnew), **img_specs.title_font)
        time_str = '_Time_%d_s' % (qf.time[it+1])
        set_ticks_font(img_specs.axis_font, ax)
        fname = 'FirebrandsOnFuel' + time_str + '.png'
        pylab.savefig(os.path.join(img_specs.save_dir, fname))
        # pylab.show()
        pylab.close()


def plot_terrain(qu: GridClass, img_specs: ImgClass):
    # 2D terrain plot
    my_cmap = generate_jet_colorbar(65)
    my_cmap = pylab.matplotlib.colors.ListedColormap(my_cmap, 'my_colormap', N=None)

    myvmin = np.min(qu.terrain_elevation)
    myvmax = np.max(qu.terrain_elevation)
    check_equal_cbar_limits(myvmin, myvmax)

    fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
    ax = fig.add_subplot(111)
    pylab.imshow(np.transpose(qu.terrain_elevation),
                 cmap=my_cmap,
                 interpolation='none',
                 origin='lower',
                 extent=qu.horizontal_extent,
                 vmin=myvmin,
                 vmax=myvmax)
    cbar = pylab.colorbar()
    cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])

    pylab.xlabel('X [m]', **img_specs.axis_font)
    pylab.ylabel('Y [m]', **img_specs.axis_font)
    cbar.set_label('Terrain elevaltion [m]', **img_specs.axis_font)

    set_ticks_font(img_specs.axis_font, ax)
    pylab.savefig(os.path.join(img_specs.save_dir, 'TerrainElevation.png'))
    pylab.close()

    # 3D terrain plot
    fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
    ax = fig.add_subplot(111, projection="3d")
    x = np.arange(qu.dx * 0.5, qu.Lx, qu.dx)
    y = np.arange(qu.dy * 0.5, qu.Ly, qu.dy)
    x, y = np.meshgrid(x, y)
    surf_handle = ax.plot_surface(x, y,
                                  np.transpose(qu.terrain_elevation),
                                  linewidth=0,
                                  antialiased=False,
                                  cmap=my_cmap,
                                  vmin=myvmin,
                                  vmax=myvmax)

    ax.set_xlim3d([0., qu.Lx])
    ax.set_ylim3d([0., qu.Ly])
    minh = np.min(qu.terrain_elevation)
    maxh = np.max(qu.terrain_elevation)
    delta = (maxh - minh) * 0.1
    ax.set_zlim3d([minh, maxh + delta])

    cbar = fig.colorbar(surf_handle, ax=ax, pad=0.2)
    cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])
    cbar.set_label('Terrain elevaltion [m]', **img_specs.axis_font)

    ax.set_xlabel('X [m]', **img_specs.axis_font)
    ax.set_ylabel('Y [m]', **img_specs.axis_font)
    ax.set_zlabel('Z [m]', **img_specs.axis_font)
    # pylab.title('Terrain elevation', **img_specs.title_font)
    set_ticks_font(img_specs.axis_font, ax)
    ax.xaxis.labelpad = 15
    ax.yaxis.labelpad = 15
    ax.zaxis.labelpad = 15
    # Ticks overlapping on z
    if (maxh - minh) / max(qu.Lx, qu.Ly) > 1:
        tickval = np.array([5., 10., 100., 125., 250., 300., 400., 500.])
        ntickval = len(tickval)
        n = np.zeros((ntickval,))
        for i in range(0, ntickval):
            n[i] = math.ceil((maxh - minh) / tickval[i])
        nlim = 5
        k = np.where(n <= nlim)
        k = k[0][0]

        vs = math.ceil(minh / tickval[k]) * tickval[k]
        ve = math.ceil(maxh / tickval[k]) * tickval[k]
        zticks = np.linspace(vs, ve, math.ceil((ve - vs) / tickval[k]))
    else:
        if minh > 0:
            odg = np.floor(np.log10(minh))
            vs = np.ceil(minh / 10 ** (odg - 1)) * 10 ** (odg - 1)
        else:
            vs = 0.
        odg = np.floor(np.log10(maxh))
        ve = np.ceil(maxh / 10**(odg-1)) *10**(odg-1)
        zticks = np.array([vs, (ve+vs)*0.5, ve])

    ax.set_zticks(zticks)
    # Aspect ratio 3d
    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(qu.terrain_elevation)))

    pylab.savefig(os.path.join(img_specs.save_dir, 'TerrainElevation3d.png'))
    pylab.close()


def plot_ignitions(qf: GridClass, fuel_dens_idx: np.array, ignitions: np.array, myextent: list,
                   img_specs: ImgClass):
    # Define colormap
    # http://matplotlib.org/api/colors_api.html
    mycol = [[1., 1., 1.], [0.765, 0.765, 0.765], [1., 0., 0.]]
    my_cmap = pylab.matplotlib.colors.ListedColormap(mycol, 'my_colormap', N=None)

    currval = np.zeros((qf.ny, qf.nx))
    currval[fuel_dens_idx] = 1
    inds = np.where(ignitions > 0)
    currval[inds] = 2

    fig = pylab.figure(figsize=(img_specs.figure_size[0], img_specs.figure_size[1]))
    ax = fig.add_subplot(111)

    pylab.imshow(currval,
                 cmap=my_cmap,
                 interpolation='none',
                 origin='lower',
                 extent=myextent,
                 vmin=-0.5,
                 vmax=2.5)
    cbar = pylab.colorbar(ticks=[0, 1, 2])
    cbar.ax.set_yticklabels(['No fuel', 'Fuel', 'Ignitions'])
    cbar.ax.tick_params(labelsize=img_specs.colorbar_font["size"])

    pylab.xlabel('X [m]', **img_specs.axis_font)
    pylab.ylabel('Y [m]', **img_specs.axis_font)
    pylab.title('Selected ignitions # %d' % len(inds[0]), **img_specs.title_font)

    set_ticks_font(img_specs.axis_font, ax)

    pylab.savefig(os.path.join(img_specs.save_dir, 'InitialIgnitions.png'))
    pylab.close()
