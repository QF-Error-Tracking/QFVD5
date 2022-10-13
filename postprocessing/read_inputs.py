# -*- coding: utf-8 -*-
# Version date: Nov 07, 2021
# @author: Sara Brambilla

import sys
import numpy as np
import copy
import os
from class_def import *
from misc import *


def get_line(fid, fun):
    # http://stackoverflow.com/questions/4289331/python-extract-numbers-from-a-string
    s = fid.readline().strip().split()
    try:
        out = fun(s[0])
    except ValueError:
        out = []
    return out


def read_ground_fuel_height(qf: GridClass, output_folder: str):
    fid = open_file(os.path.join(output_folder, "groundfuelheight.bin"), "rb")
    # Read header
    np.fromfile(fid, dtype=np.int32, count=1)
    t = np.fromfile(fid, dtype=np.float32, count=qf.nx * qf.ny)
    fuel_height = np.reshape(t, (qf.nx, qf.ny), order="F")
    fuel_height = np.transpose(fuel_height)
    fid.close()

    return fuel_height


def read_fireca_field(
    filestr: str,
    ntimes: int,
    times: list,
    qf: GridClass,
    is_3d: int,
    output_folder: str,
):
    outvar = []
    if filestr == "mburnt_integ-":
        nvert = 1
    elif filestr == "fire-energy_to_atmos-":
        nvert = qf.nz_en2atmos
    else:
        if is_3d:
            nvert = qf.nz + 1
        else:
            nvert = qf.nz

    for i in range(0, ntimes):
        fname = filestr + "%05d.bin" % (times[i])
        # Open file
        fid = open_file(os.path.join(output_folder, fname), "rb")
        temp = np.zeros((qf.ny, qf.nx, nvert), dtype=np.float32)
        # Read header
        np.fromfile(fid, dtype=np.int32, count=1)
        if is_3d == 0:
            var = np.fromfile(fid, dtype=np.float32, count=qf.indexing.num_cells)
            # http://scipy-cookbook.readthedocs.io/items/Indexing.html
            index = tuple(
                [
                    qf.indexing.ijk[::1, 1],
                    qf.indexing.ijk[::1, 0],
                    qf.indexing.ijk[::1, 2],
                ]
            )
            temp[index] = var
        else:
            for k in range(0, nvert):
                t = np.fromfile(fid, dtype=np.float32, count=qf.nx * qf.ny)
                temp[::1, ::1, k] = np.reshape(t, (qf.ny, qf.nx))
        outvar.append(temp)
        fid.close()

    return outvar


def read_vertical_grid(
    qu: GridClass, qf: GridClass, flags: FlagsClass, output_folder: str
):
    fid = open_file(os.path.join(output_folder, "grid.bin"), "rb")

    # Header
    np.fromfile(fid, dtype=np.int32, count=1)
    # Read z
    qu.z = np.fromfile(fid, dtype=np.float32, count=qu.nz + 2)

    # Header
    np.fromfile(fid, dtype=np.int32, count=2)

    # Read zm
    qu.zm = np.fromfile(fid, dtype=np.float32, count=qu.nz + 2)

    # Header
    np.fromfile(fid, dtype=np.int32, count=2)

    qu.z_tot_topo = np.zeros((qu.nx, qu.ny, qu.nz + 2), dtype=np.float32)
    if flags.topo > 0:
        # sigma
        np.fromfile(fid, dtype=np.float32, count=qu.nz + 2)
        np.fromfile(fid, dtype=np.int32, count=2)
        # sigmam
        np.fromfile(fid, dtype=np.float32, count=qu.nz + 2)
        np.fromfile(fid, dtype=np.int32, count=2)

        for k in range(0, qu.nz + 2):
            t = np.fromfile(fid, dtype=np.float32, count=qu.nx * qu.ny)
            qu.z_tot_topo[:, :, k] = np.reshape(t, (qu.nx, qu.ny), order="F")

        np.fromfile(fid, dtype=np.int32, count=2)
        qu.zm_topo = np.zeros((qu.nx, qu.ny, qu.nz + 2), dtype=np.float32)
        for k in range(0, qu.nz + 2):
            t = np.fromfile(fid, dtype=np.float32, count=qu.nx * qu.ny)
            qu.zm_topo[:, :, k] = np.reshape(t, (qu.nx, qu.ny), order="F")

        np.fromfile(fid, dtype=np.int32, count=2)
        # qugrid%cellvol_mult
        np.fromfile(fid, dtype=np.int32, count=qu.nx * qu.ny)
        np.fromfile(fid, dtype=np.int32, count=2)

    if flags.isfire == 1:
        temp = np.fromfile(fid, dtype=np.int32, count=1)
        qf.nz_en2atmos = temp[0]
        np.fromfile(fid, dtype=np.int32, count=2)
        qf.z_en2atmos = np.fromfile(fid, dtype=np.float32, count=qf.nz_en2atmos + 1)

    fid.close()


def read_qu_grid(qu: GridClass, prj_folder: str):

    # ------- QU_simparams
    fid = open_file(os.path.join(prj_folder, "QU_simparams.inp"), "r")
    fid.readline()  # header
    qu.nx = get_line(fid, int)
    qu.ny = get_line(fid, int)
    qu.nz = get_line(fid, int)
    qu.dx = get_line(fid, float)
    qu.dy = get_line(fid, float)
    qu.Lx = qu.dx * float(qu.nx)
    qu.Ly = qu.dy * float(qu.ny)

    grid_flag = get_line(fid, int)
    if grid_flag == 0:
        temp = get_line(fid, float)
        qu.dz = np.ones(qu.nz) * temp
    else:
        fid.readline()
        fid.readline()
        fid.readline()
        qu.dz = []
        for i in range(0, qu.nz):
            qu.dz.append(get_line(fid, float))

    number_of_times = get_line(fid, int)
    for useless_lines in range(15 + number_of_times):
        fid.readline()
    qu.domain_rotation = get_line(fid, float)
    qu.utmx = get_line(fid, float)
    qu.utmy = get_line(fid, float)
    qu.utm_zone = get_line(fid, int)
    qu.utm_letter = get_line(fid, int)
    fid.close()

    qu.horizontal_extent = [0.0, qu.dx * float(qu.nx), 0.0, qu.dy * float(qu.ny)]


def read_times(fid, qu: GridClass, qf: GridClass):

    # Header
    fid.readline()
    fid.readline()

    # Simulation time
    qu.sim_time = get_line(fid, int)
    qf.sim_time = qu.sim_time

    # Fire time step
    qf.dt = get_line(fid, int)

    # QU time step
    qu.dt = int(get_line(fid, int) * qf.dt)

    # Print time for FireCA variables
    qf.dt_print = int(get_line(fid, int) * qf.dt)

    # Print time for QUIC variables
    qu.dt_print = int(get_line(fid, int) * qu.dt)

    # Print time for emission and rad variables
    qf.dt_print_ave = int(get_line(fid, int) * qf.dt)

    # Print time for averaged QUIC variables
    qu.dt_print_ave = int(get_line(fid, int) * qu.dt_print)

    qf.ntimes = int(qf.sim_time / qf.dt_print + 1)
    qf.time = np.zeros((qf.ntimes,), dtype=np.int)

    qu.ntimes = int(qu.sim_time / qu.dt_print + 1)
    qu.time = np.zeros((qu.ntimes,), dtype=np.int)

    for i in range(0, qf.ntimes):
        qf.time[i] = qf.dt_print * i

    for i in range(0, qu.ntimes):
        qu.time[i] = qu.dt_print * i

    qf.ntimes_ave = int(qf.sim_time / qf.dt_print_ave)
    qf.time_ave = np.zeros((qf.ntimes_ave,), dtype=np.int)

    qu.ntimes_ave = int(qu.sim_time / qu.dt_print_ave + 1)
    qu.time_ave = np.zeros((qu.ntimes_ave,), dtype=np.int)

    for i in range(0, qf.ntimes_ave):
        qf.time_ave[i] = qf.dt_print_ave * (i + 1)

    for i in range(0, qu.ntimes_ave):
        qu.time_ave[i] = qu.dt_print_ave * i


def read_fire_grid(fid, qu: GridClass, qf: GridClass, output_folder: str):
    fid.readline()  # ! FIRE GRID
    qf.nz = get_line(fid, int)
    qf.nx = qu.nx
    qf.ny = qu.ny
    qf.dx = qu.dx
    qf.dy = qu.dy
    dz_flag = get_line(fid, int)
    if dz_flag == 0:
        dztemp = get_line(fid, float)
        qf.dz = dztemp * np.ones((qf.nz,), dtype=np.float32)
    else:
        qf.dz = np.zeros((qf.nz,), dtype=np.float32)
        for i in range(0, qf.nz):
            qf.dz[i] = get_line(fid, float)

    qf.z = np.zeros((qf.nz + 1,), dtype=np.float32)
    for k in range(1, qf.nz + 1):
        qf.z[k] = qf.z[k - 1] + qf.dz[k - 1]

    qf.zm = np.zeros((qf.nz,), dtype=np.float32)
    for k in range(0, qf.nz):
        qf.zm[k] = qf.z[k] + qf.dz[k] * 0.5

    qf.horizontal_extent = [0.0, qf.dx * float(qf.nx), 0.0, qf.dy * float(qf.ny)]

    read_fire_grid_indexing(qf, output_folder)


def read_fuel(fid):
    fid.readline()  # ! FUEL
    # - fuel density flag
    dens_flag = get_line(fid, int)
    if dens_flag == 1:
        fid.readline()  # read density

    # - moisture flag
    if get_line(fid, int) == 1:
        fid.readline()

    # - height flag
    if dens_flag == 1:
        if get_line(fid, int) == 1:
            fid.readline()


def read_ignitions(fid, qf: GridClass, ignitions: IgnitionClass, output_folder: str):
    fid.readline()  # ! IGNITION LOCATIONS
    ignitions.flag = get_line(fid, int)
    if ignitions.flag > 7:
        print("Invalid ignition flag. Program will be terminated")
        sys.exit(1)

    # Specify 2D array of ignitions
    read_selected_ignitions(qf, ignitions, output_folder)

    # Read uninteresting lines
    nlines_extra = [5, 7, 5, 0, 0, 1, 1]
    for i in range(0, nlines_extra[ignitions.flag - 1]):
        fid.readline()


def read_selected_ignitions(
    qf: GridClass, ignitions: IgnitionClass, output_folder: str
):
    sel_ign = np.zeros((qf.ny, qf.nx, qf.nz), dtype=np.float32)
    fname = os.path.join(output_folder, "ignite_selected.dat")
    nelem = int(os.path.getsize(fname) / (5 * 4))
    fid = open_file(fname, "rb")
    var = np.fromfile(fid, dtype=np.int32, count=nelem * 5)
    var = np.reshape(var, (5, nelem), order="F")
    var -= 1
    myindex = [var[2], var[1], var[3]]
    sel_ign[tuple(myindex)] = 1
    fid.close()
    ignitions.hor_plane = np.sum(sel_ign, axis=2)


def read_firebrands(output_folder: str, fb: FirebrandClass):
    fname = os.path.join(output_folder, "firebrands.bin")
    nfields = 5
    nelem = int(os.path.getsize(fname) / nfields)
    fid = open_file(fname, "rb")

    var = np.fromfile(fid, dtype=np.int32, count=nelem)
    var = np.reshape(var, ((nfields + 2), int(nelem / (nfields + 2))), order="F")
    # var[0] is the header
    fb.time = var[1]
    fb.i = var[2] - 1
    fb.j = var[3] - 1
    fb.k = var[4] - 1
    fb.state = var[5]


def read_file_flags(fid, flags: FlagsClass):
    # Firebrands
    fid.readline()  # FIREBRANDS
    flags.firebrands = get_line(fid, int)

    # Out files
    fid.readline()  # OUTPUT FILES
    flags.en2atm = get_line(fid, int)
    flags.react_rate = get_line(fid, int)
    flags.fuel_density = get_line(fid, int)
    flags.qf_winds = get_line(fid, int)
    flags.qu_qwinds_inst = get_line(fid, int)
    flags.qu_qwinds_ave = get_line(fid, int)
    fid.readline()
    flags.moisture = get_line(fid, int)
    flags.perc_mass_burnt = get_line(fid, int)
    fid.readline()
    flags.emissions = get_line(fid, int)
    flags.thermal_rad = get_line(fid, int)


def read_path(fid, qf: GridClass):
    fid.readline()  # ! PATH LABEL
    temp = fid.readline()  # ! PATH
    qf.path = temp[1:-1]
    fid.readline()  # trees file option
    fid.readline()  # trees file formats


def read_topo(
    flags: FlagsClass, qu: GridClass, qf: GridClass, prj_folder: str, output_folder: str
):
    fid = open_file(os.path.join(prj_folder, "QU_TopoInputs.inp"), "r")
    fid.readline()
    fid.readline()
    flags.topo = get_line(fid, int)
    fid.close()

    if flags.topo > 0:
        fid = open_file(os.path.join(output_folder, "QF_elevation.bin"), "r")
        np.fromfile(fid, dtype=np.int32, count=1)
        min_terrain_elevation = np.fromfile(fid, dtype=np.float32, count=1)
        np.fromfile(fid, dtype=np.int32, count=2)
        elev = np.fromfile(fid, dtype=np.float32, count=(qu.nx + 2) * (qu.ny + 2))
        qu.terrain_elevation_full = np.reshape(elev, (qu.nx + 2, qu.ny + 2), order="F")
        qu.terrain_elevation = qu.terrain_elevation_full[1:-1, 1:-1]
        qu.terrain_elevation = qu.terrain_elevation  # + min_terrain_elevation
        qu.terrain_elevation_full = qu.terrain_elevation_full  # + min_terrain_elevation
        # Fix corners (used by pyvista)
        qu.terrain_elevation_full[0, 0] = (
            qu.terrain_elevation_full[1, 0]
            + qu.terrain_elevation_full[1, 1]
            + qu.terrain_elevation_full[0, 1]
        ) / 3.0
        qu.terrain_elevation_full[-1, 0] = (
            qu.terrain_elevation_full[-2, 0]
            + qu.terrain_elevation_full[-2, 1]
            + qu.terrain_elevation_full[-1, 1]
        ) / 3.0
        qu.terrain_elevation_full[0, -1] = (
            qu.terrain_elevation_full[1, -1]
            + qu.terrain_elevation_full[1, -2]
            + qu.terrain_elevation_full[0, -2]
        ) / 3.0
        qu.terrain_elevation_full[-1, -1] = (
            qu.terrain_elevation_full[-2, -1]
            + qu.terrain_elevation_full[-2, -2]
            + qu.terrain_elevation_full[-1, -2]
        ) / 3.0
        fid.close()
    else:
        qu.terrain_elevation = np.zeros((qf.nx, qf.ny))
        qu.terrain_elevation_full = np.zeros((qf.nx + 2, qf.ny + 2))

    qf.terrain_elevation = copy.deepcopy(qu.terrain_elevation)
    qf.terrain_elevation_full = copy.deepcopy(qu.terrain_elevation_full)


def read_init_flags(fid, flags: FlagsClass):
    flags.isfire = get_line(fid, int)
    # random number generator
    fid.readline()


def read_qfire_file(
        qf: GridClass,
        qu: GridClass,
        ignitions: IgnitionClass,
        flags: FlagsClass,
        fb: FirebrandClass,
        prj_folder: str,
        output_folder: str):
    fid = open_file(os.path.join(prj_folder, "QUIC_fire.inp"), "r")

    print("\t\t* read flags")
    read_init_flags(fid, flags)
    if flags.isfire:
        qf.__dict__.update(qu.__dict__)
        print("\t\t* read times")
        read_times(fid, qu, qf)
        print("\t\t* read fire grid")
        read_fire_grid(fid, qu, qf, output_folder)
        print("\t\t* read fuel specs")
        read_path(fid, qf)
        read_fuel(fid)
        print("\t\t* read ignitions")
        read_ignitions(fid, qf, ignitions, output_folder)
        print("\t\t* read output flags")
        read_file_flags(fid, flags)
        if flags.firebrands == 1:
            try:
                read_firebrands(output_folder, fb)
            except:
                print("Firebrands will not be plotted")

    fid.close()


def read_fire_grid_indexing(qf: GridClass, output_folder: str):
    fid = open_file(os.path.join(output_folder, "fire_indexes.bin"), "rb")
    np.fromfile(fid, dtype=np.int32, count=1)
    temp = np.fromfile(fid, dtype=np.int32, count=1)
    qf.indexing.num_cells = temp[0]
    np.fromfile(fid, dtype=np.int32, count=7 + qf.indexing.num_cells)
    qf.indexing.ijk = np.zeros((qf.indexing.num_cells, 3), dtype=np.int32)
    for i in range(0, 3):
        qf.indexing.ijk[::1, i] = np.fromfile(
            fid, dtype=np.int32, count=qf.indexing.num_cells
        )

    qf.indexing.ijk = qf.indexing.ijk.astype(int)
    qf.indexing.ijk -= 1
    fid.close()
