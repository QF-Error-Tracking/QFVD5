# -*- coding: utf-8 -*-
# Version date: Nov 07, 2021
# @author: Sara Brambilla

class FirebrandClass:
    def __init__(self):
        self.i = None
        self.j = None
        self.k = None
        self.state = None
        self.time = None


class ImgClass:
    def __init__(self, gen_gif=0):
        self.figure_size = None
        self.axis_font = None
        self.title_font = None
        self.colorbar_font = None
        self.gen_gif = gen_gif
        self.gif_dir = None
        self.save_dir = None


class LinIndexClass:
    def __init__(self):
        self.ijk = None
        self.num_cells = None


class FlagsClass:
    def __init__(self):
        # Use defaults for pyvista script
        self.firebrands = 0
        self.en2atm = 0
        self.perc_mass_burnt = 0
        self.fuel_density = 0
        self.emissions = 0
        self.thermal_rad = 0
        self.qf_winds = 0
        self.qu_qwinds_inst = 0
        self.qu_qwinds_ave = 0
        self.react_rate = 0
        self.moisture = 0
        self.topo = 0
        self.isfire = 0


class IgnitionClass:
    def __init__(self):
        self.hor_plane = None
        self.flag = None


class GridClass:
    def __init__(self):
        self.nx = None
        self.ny = None
        self.nz = None
        self.nz_en2atmos = None
        self.dx = None
        self.dy = None
        self.dz = None
        self.z = None
        self.z_en2atmos = None
        self.zm = None
        self.z_tot_topo = None
        self.zm_topo = None
        self.Lx = None
        self.Ly = None
        self.sim_time = None
        self.ntimes = None
        self.time = None
        self.ntimes_ave = None
        self.time_ave = None
        self.dt = None
        self.dt_print = None
        self.dt_print_ave = None
        self.horizontal_extent = None
        self.indexing = LinIndexClass()
        self.terrain_elevation = None # Only points inside the grid
        self.terrain_elevation_full = None # Also border cells
        self.topo_grid = None
        self.domain_rotation = None
        self.utmx = None
        self.utmy = None
        self.utm_zone = None
        self.utm_letter = None
