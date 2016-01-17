import numpy as np
import scipy.sparse as sparse
import scipy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib.animation as animation
try:
    from JSAnimation import IPython_display
except:
    pass
import os
import error_handling


class propagation():
    def __init__(self, lat):
        '''
        Get lattice time evolution. Time dependent Schrodinger equation solved by
        Crank-Nicolson method.

        :param lat: **lattice** class instance.
        '''
        error_handling.lat(lat)
        self.lat = lat
        self.prop = np.array([], 'c16')

    def get_propagation(self, ham, psi_init, steps, dz, norm=False):
        '''
        Get the time evolution.

        :param ham: sparse.csr_matrix. Tight-Binding Hamilonian.
        :param psi_init: np.ndarray. Initial state.
        :param steps: Positive Integer. Number of steps.
        :param dz: Positive number. Step.
        :param norm: Boolean. Default value True. Normalize the norm to 1 at each step.
        '''
        error_handling.empty_ham(ham)
        error_handling.ndarray(psi_init, 'psi_init', self.lat.sites)
        error_handling.positive_int(steps, 'steps')
        error_handling.positive_real(dz, 'dz')
        error_handling.boolean(norm, 'norm')
        self.steps = steps
        self.dz = dz
        self.prop = np.empty((self.lat.sites, self.steps), 'c16')
        self.prop[:, 0] = psi_init
        diag = 1j*np.ones(self.lat.sites, 'c16')
        A = (sparse.diags(diag, 0) - 0.5 * self.dz * ham).toarray()
        B = (sparse.diags(diag, 0) + 0.5 * self.dz * ham).toarray()
        mat = (np.dot(LA.inv(A), B))
        for i in range(1, self.steps):
            self.prop[:, i] = np.dot(mat, self.prop[:, i-1])
            if norm:
                self.prop[:, i] /= np.abs(self.prop[:, i]).sum()

    def get_propagation_nonlin(self, ham, psi_init, steps, dz, nu=0, norm=True):
        '''
        Get the time evolution.

        :param ham: Tight-Binding Hamilonian.
        :param psi_init: np.ndarray. Initial state.
        :param steps: Positive Integer. Number of steps.
        :param dz: Positive number. Step value.
        :param nu: Real number. Nonlinearity strength.
        :param norm: Boolean. Default value True. Normalize the norm to 1 at each step.
        '''
        self.steps = steps
        self.dz = dz
        from scipy.integrate import odeint
        sites = self.lat.sites
        N = 2 * sites

        def eq_motion(y, t, H, nu):
            non_lin = y ** 2
            non_lin = nu *(non_lin[:sites] + non_lin[sites:])
            T = np.copy(H)
            T[range(sites), range(sites, N)] += non_lin
            T[range(sites, N), range(sites)] -= non_lin
            dy = np.dot(T, y)
            return dy

        ham = ham.toarray()
        H = np.zeros((N, N))
        H[:sites, :sites] = ham.imag
        H[:sites, sites:] = ham.real
        H[sites:, :sites] = - ham.real
        H[sites:, sites:] = ham.imag
        y0 = np.zeros(N)
        y0[:sites] = psi_init.real
        y0[sites:] = psi_init.imag
        t = np.arange(0., self.dz*self.steps, self.dz)
        param= (H, nu)
        y = odeint(eq_motion, y0, t, args=param)
        self.prop = y[:, :sites].T +1j * y[:, sites:].T

    def get_pumping(self, hams, psi_init, steps, dz, norm=True):
        '''
        Get the time evolution under adiabatic pumpings.

        :param hams: List of sparse.csr_matrices. Tight-Binding Hamilonians.
        :param psi_init: np.ndarray. Initial state.
        :param steps: Positive integer. Number of steps.
        :param dz: Positive number. Step.
        :param norm: Boolean. Default value True. Normalize the norm to 1 at each step.
        '''
        error_handling.get_pump(hams)
        error_handling.ndarray(psi_init, 'psi_init', self.lat.sites)
        error_handling.positive_int(step, 'step')
        error_handling.positive_real(dz, 'dz')
        error_handling.boolean(norm, 'norm')
        self.steps = steps
        self.dz = dz
        no = len(hams)
        self.prop = np.empty((self.lat.sites, self.steps), 'c16')
        self.prop[:, 0] = psi_init
        diag = 1j * np.ones(self.lat.sites, 'c16')
        delta = self.steps // (1 + no)
        A = (sparse.diags(diag, 0) - 0.5 * self.dz * hams[0]).toarray()
        B = (sparse.diags(diag, 0) + 0.5 * self.dz * hams[0]).toarray()
        mat = (np.dot(LA.inv(A), B))
        # before pumping
        for i in range(1, delta):
           self.prop[:, i] = np.dot(mat, self.prop[:, i-1])
           if norm:
               self.prop[:, i] /= np.abs(self.prop[:, i]).sum()
      # pumping
        c = np.linspace(0, 1, delta)
        for j in range(0, no-1):
            for i in range(0, delta):
                ham = (1-c[i])*hams[j]+c[i]*hams[j+1]
                A = (sparse.diags(diag, 0) - 0.5 * self.dz * ham).toarray()
                B = (sparse.diags(diag, 0) + 0.5 * self.dz * ham).toarray()
                mat = (np.dot(LA.inv(A), B))
                self.prop[:, (j+1)*delta+i] = np.dot(mat, self.prop[:,  (j+1)*delta+i-1])
                if norm:
                    self.prop[:,  (j+1)*delta+i] /= \
                        np.abs(self.prop[:,  (j+1)*delta+i]).sum() 
      # after pumping
        j = no
        for i in range(0, self.steps - no*delta):
            self.prop[:,  no*delta+i] = np.dot(mat, self.prop[:,  no*delta+i-1])
            if norm:
                self.prop[:,  no*delta+i] /= np.abs(self.prop[:,  no*delta+i]).sum()

    def plt_propagation_1d(self, fs=20):
        '''
        Plot time evolution for 1D systems. 

        :param fs: Default value 20. Fontsize.
        '''
        if not self.prop.any():
            raise Exception('\n\nRun method get_prop() or get_pump() first.\n')
        fig, ax = plt.subplots(figsize=(8, 6))
        prop = np.abs(self.prop[::-1, :]) **2
        color = self.prop_smooth_1d(prop)
        plt.title('$|\psi(z)|^2$', fontsize=fs)
        plt.ylabel('n', fontsize=fs)
        plt.xlabel('z', fontsize=fs)
        vmin, vmax = 0., np.max(color[:, 0: self.lat.sites])
        extent = (0, self.steps*self.dz, 
                       -self.lat.sites//2+0.5, self.lat.sites-self.lat.sites//2+0.5)
        aspect = 'auto'
        interpolation = 'nearest'
        im = plt.imshow(color, cmap=plt.cm.hot, aspect=aspect,
                                  interpolation=interpolation, extent=extent,
                                  vmin=vmin, vmax=vmax)
        cbar = plt.colorbar(im, ticks=[vmin, vmax])
        cbar.ax.set_yticklabels(['0', 'max'], fontsize=fs)
        ya = ax.get_yaxis()
        ya.set_major_locator(plt.MaxNLocator(integer=True))
        return fig

    def prop_smooth_1d(self, prop, a=14., no=40):
        r'''
        Private function. Used in *plt_propagation_1d*.
        Smooth propagation for 1D systems ().
        Perform Gaussian interpolation :math:`e^{-a(x-x_i)^2}`,

        :param prop: Propagation.
        :param a: Default value 10. Gaussian Parameter.
        :param no: Default value 40. Number of points of each Gaussians.

        :returns:
           * **smooth** -- Smoothed propagation.
        '''
        x = np.linspace(-0.5, 0.5, no)
        smooth = np.empty((self.lat.sites * no, self.steps))
        for iz in range(0, self.steps):
            for i in range(self.lat.sites):
                smooth[i*no: (i+1)*no, iz] = prop[i, iz] * np.exp(-a * x ** 2)
        return smooth

    def get_animation(self, s=300., fs=20., ani_type='real', figsize=None):
        '''
        Get time evolution animation.

        :param s: Default value 300. Circle size.
        :param fs: Default value 20. Fontsize.
        :param figsize: Tuple. Default value None. Figsize.
        :param ani_type: Default value None. Figsize.

        :returns:
          * **ani** -- Animation.
        '''
        error_handling.empty_ndarray(self.prop, 'get_propagation or get_pumping')
        error_handling.positive_real(s, 's')
        error_handling.positive_real(fs, 'fs')
        error_handling.ani_type(ani_type)
        error_handling.tuple_2elem(figsize, 'figsize')
        if os.name == 'posix':
            blit = False
        else:
            blit = True
        if ani_type == 'real':
            color = self.prop.real
            max_val = max(np.max(color), -np.min(color))
            ticks = [-max_val, max_val]
            cmap = 'seismic'
        elif ani_type == 'imag':
            color = self.prop.imag
            max_val = max(np.max(color), -np.min(color))
            ticks = [-max_val, max_val]
            cmap = 'seismic'
        else:
            color = np.abs(self.prop) ** 2
            ticks = [0., np.max(color)]
            cmap = 'Reds'
        fig, ax = plt.subplots(figsize=figsize)
        plt.xlim([self.lat.coor['x'][0]-1., self.lat.coor['x'][-1]+1.])
        plt.ylim([self.lat.coor['y'][0]-1., self.lat.coor['y'][-1]+1.])
        scat = plt.scatter(self.lat.coor['x'], self.lat.coor['y'], c=color[:, 0],
                                   s=s, vmin=ticks[0], vmax=ticks[1],
                                   cmap=plt.get_cmap(cmap))
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])
        ax.set_aspect('equal')
        if ani_type == 'norm':
            cbar = fig.colorbar(scat, ticks=[0, ticks[1]])
            cbar.ax.set_yticklabels(['0','max'])
        else:
            cbar = fig.colorbar(scat, ticks=[ticks[0], 0, ticks[1]])
            cbar.ax.set_yticklabels(['min', '0','max'])

        def update(i, color, scat):
            scat.set_array(color[:, i])
            return scat,

        ani = animation.FuncAnimation(fig, update, frames=self.steps,
                                                  fargs=(color, scat), blit=blit, repeat=False)
        return ani

    def get_animation_nb(self, s=300., fs=20., ani_type='real', figsize=None):
        '''
        Get time evolution animation for iPython notebooks.

        :param s: Default value 300. Circle shape.
        :param fs: Default value 20. Fontsize.

        :returns:
           * **ani** -- Animation.
        '''
        '''
        Get time evolution animation.

        :param s: Default value 300. Circle size.
        :param fs: Default value 20. Fontsize.
        :param figsize: Tuple. Default value None. Figsize.
        :param ani_type: Default value None. Figsize.

        :returns:
          * **ani** -- Animation.
        '''
        error_handling.empty_ndarray(self.prop, 'get_propagation or get_pumping')
        error_handling.positive_real(s, 's')
        error_handling.positive_real(fs, 'fs')
        error_handling.ani_type(ani_type)
        error_handling.tuple_2elem(figsize, 'figsize')
        if ani_type == 'real':
            color = self.prop.real
            max_val = max(np.max(color), -np.min(color))
            ticks = [-max_val, max_val]
            cmap = 'seismic'
        elif ani_type == 'imag':
            color = self.prop.imag
            max_val = max(np.max(color), -np.min(color))
            ticks = [-max_val, max_val]
            cmap = 'seismic'
        else:
            color = np.abs(self.prop) ** 2
            ticks = [0., np.max(color)]
            cmap = 'Reds'
        fig = plt.figure()
        ## TO CHANGE
        scat = plt.scatter(self.lat.coor['x'], self.lat.coor['y'], c=color[:, 0],
                                    s=s, vmin=ticks[0], vmax=ticks[1],
                                    cmap=cmap)
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])
        if ani_type == 'norm':
            cbar = fig.colorbar(scat, ticks=[0, ticks[1]])
            cbar.ax.set_yticklabels(['0','max'])
        else:
            cbar = fig.colorbar(scat, ticks=[ticks[0], 0, ticks[1]])
            cbar.ax.set_yticklabels(['min', '0','max'])

        def init():
            scat.set_array(color[:, 0])
            print('IIIIIII')
            return scat,

        def animate(i):
            print(i)
            scat.set_array(color[:, i])
            return scat,

        return animation.FuncAnimation(fig, animate, init_func=init,
                                                           frames=self.steps, interval=120)

    def plt_prop_dimer(self, lw=5, fs=20):
        '''
        Plot time evolution for dimers.
        
        :param lw: Default value 5. Linewidth.
        :param fs: Default value 20. Fontsize.

        :returns:
           * **fig** -- Figure.
        '''
        if not self.prop.any():
            raise Exception('\n\nRun method get_prop() or get_pump() first.\n')
        color = ['b', 'r']
        fig, ax = plt.subplots()
        z = self.dz * np.arange(self.steps)
        for i, c in zip([0, 1], color):
            plt.plot(z, np.abs(self.prop[i, :])**2, c, lw=lw)
        plt.title('Intensity', fontsize=fs)
        plt.xlabel('$z$', fontsize=fs)
        plt.ylabel('$|\psi_j|^2$', fontsize=fs)
        plt.xlim([0, z[-1]])
        return fig

