import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class SIRS(object):
    def __init__(self, size, ini, p1, p2, p3):
        """
            SIRS Model class object

            Attributes:
            size = size (tuple), dimensions of SIRS simulation.
            initial_state = ini (str), initial state of lattice
        """
        self.size = size
        self.ini = ini
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.build_lattice()

    def build_lattice(self):
        """
            Creates an ndarray of lattice sites, each site is
            occupied by either an alive or dead cell.
        """
        # Random config.
        if self.ini == "random":
            self.lattice = np.random.choice(a=[-1, 0, 1], size=self.size)

    def pbc(self, indices):
        """
            Applies periodic boundary conditions (pbc) to a
            2D lattice.
        """
        return(indices[0] % self.size[0], indices[1] % self.size[1])

    def get_random(self):
        return (np.random.uniform(0, 1))

    def check_infected(self, indices):
        i, j = indices
        n_n = self.lattice[(i - 1) % self.size[0], j]
        n_e = self.lattice[i, (j + 1) % self.size[1]]
        n_s = self.lattice[(i + 1) % self.size[0], j]
        n_w = self.lattice[i, (j - 1) % self.size[1]]
        neighbours = [n_n, n_e, n_s, n_w]

        if 0 in neighbours:
            r = self.get_random()
            if r <= self.p1:
                return True
            else:
                return False
        else:
            return False

    def update_SIRS(self):
        indices = (np.random.randint(0, self.size[0]),
                   np.random.randint(0, self.size[1]))

        if self.lattice[indices] == -1:
            outcome = self.check_infected(indices)
            if outcome == True:
                self.lattice[indices] = 0

        elif self.lattice[indices] == 0:
            r_2 = self.get_random()
            if r_2 <= self.p2:
                self.lattice[indices] = 1

        elif self.lattice[indices] == 1:
            r_3 = self.get_random()
            if r_3 <= self.p3:
                self.lattice[indices] = -1

    def animate(self, *args):
        """
            Creates, saves and returns image of the current state of
            SIRS lattice for the FuncAnimation class.
        """
        for i in range(self.it_per_sweep):
            self.update_SIRS()
        self.image.set_array(self.lattice)
        return self.image,

    def run_animation(self, sweeps, it_per_sweep):
        """
            Used in partnership with the tester file
            to run the simulation.
        """
        self.it_per_sweep = it_per_sweep
        self.figure = plt.figure()
        self.image = plt.imshow(self.lattice, cmap='jet', animated=True)
        self.animation = animation.FuncAnimation(self.figure, self.animate, repeat=False, frames=sweeps, interval=50, blit=True)
        plt.colorbar(ticks=np.linspace(-1,1,3))
        plt.show()
