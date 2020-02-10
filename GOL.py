import numpy as np
import matplot.pyplot as plt

class GOL(object):
    def __init__(self, size, ini):
        """
            Game of life class object

            Attributes:
            size = size (tuple), dimensions of Game of Life.
            initial_state = ini (str), initial state of lattice
        """
        self.size = size
        self.ini = ini
        self.build_lattice()

    def build_lattice(self):
        """
            Creates an ndarray of lattice sites, each site is
            occupied by either an alive or dead cell.
        """
        # Random config.
        if self.ini == "random":
            self.lattice = np.random.choice(a=[0, 1], size=self.size)
        if self.ini == "oscillator":
            self.lattice = np.zeros(self.size)
            self.lattice[25:28, 25] = self.create_oscillator
        if self.ini == "glider":
            self.lattice = np.zeros(self.size)
            self.lattice[0:3, 0:3] = self.create_glider
        if self.ini == "beehive":
            self.lattice = np.zeros(self.size) 
            self.lattice[25:29, 24:27] = self.create_beehive
        if self.ini == "square":
            self.lattice = np.zeros(self.size)
            self.lattice[25:27, 25] = self.create_square 

    def pbc(self, indices):
        """
            Applies periodic boundary conditions (pbc) to a
            2D lattice.
        """
        return(indices[0] % self.size[0], indices[1] % self.size[1])
    
    def create_glider(self):
        glider = np.zeros((3,3))
        glider[2:] = 1
        glider[1, 2] = 1
        glider[0, 1] = 1
        return glider
    
    def create_oscillator(self):
        oscillator = np.ones((1,3))
        return oscillator
    
    def create_beehive(self):
        beehive = np.zeros((4,3))
        beehive[0, 1] = 1
        beehive[3, 1] = 1
        beehive[2, 0] = 1
        beehive[1, 0] = 1
        beehive[2, 2] = 1
        beehive[1, 2] = 1
        return beehive

    def create_square(self):
        square = np.ones((2, 2))
        return square

    def count_nn(self, indices):
        i, j = indices
        nn = np.sum(self.lattice[((i-1) % self.size[0]):((i+1) % self.size[0])],
                    self.lattice[((j-1) % self.size[1]):((j+1) % self.size[1])]) - self.lattice(i, j)
        return nn
    
    def evolve_state():
       new_state = np.zeros(self.size)
       for i in range(self.size[0]):
           for j in range(self.size[1]):
               


    def animate(self, *args):
        """
            Creates, saves and returns image of the current state of
            lattice for the FuncAnimation class.
        """
        for i in range(self.it_per_sweep):
            if self.dynamics == "glauber":
                self.glauber()
            elif self.dynamics == "kawasaki":
                self.kawasaki()
            elif self.dynamics == "kawasaki_2":
                self.kawasaki_2()
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
        self.animation = animation.FuncAnimation(
            self.figure, self.animate, repeat=False, frames=sweeps, interval=50, blit=True)
        plt.colorbar(ticks=np.linspace(-1, 1, 2))
        plt.show()


