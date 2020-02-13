import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
        self.eqm = False
        self.build_lattice()


    def build_lattice(self):
        """
            Creates an ndarray of lattice sites, each site is
            occupied by either an alive or dead cell.
        """
        # Random config.
        if self.ini == "random":
            self.lattice = np.random.choice(a=[0, 1], size=self.size)
        # Oscillator config.
        if self.ini == "oscillator":
            self.lattice = np.zeros(self.size)
            self.lattice[25:28, 25] = self.create_oscillator()
        # Glider config.
        if self.ini == "glider":
            self.lattice = np.zeros(self.size)
            self.lattice[0:3, 0:3] = self.create_glider()
        # Beehive config.
        if self.ini == "beehive":
            self.lattice = np.zeros(self.size) 
            self.lattice[25:29, 24:27] = self.create_beehive()
        # Square config.
        if self.ini == "square":
            self.lattice = np.zeros(self.size)
            self.lattice[25:27, 25] = self.create_square()

    def pbc(self, indices):
        """
            Applies periodic boundary conditions (pbc) to a
            2D lattice.
        """
        return(indices[0] % self.size[0], indices[1] % self.size[1])
    
    def create_glider(self):
        """
            Creates an array in the shape
            of a GOL glider.
        """
        glider = np.zeros((3,3))
        glider[2:] = 1
        glider[1, 2] = 1
        glider[0, 1] = 1
        return glider
    
    def create_oscillator(self):
        """
            Creates an array in the shape
            of a GOL blinker.
        """
        oscillator = np.ones((1,3))
        return oscillator
    
    def create_beehive(self):
        """
            Creates an array in the shape
            of a GOL beehive.
        """
        beehive = np.zeros((4,3))
        beehive[0, 1] = 1
        beehive[3, 1] = 1
        beehive[2, 0] = 1
        beehive[1, 0] = 1
        beehive[2, 2] = 1
        beehive[1, 2] = 1
        return beehive

    def create_square(self):
        """
            Creates an array in the shape
            of a GOL square.
        """
        square = np.ones((2, 2))
        return square

    def count_nn(self, site):
        #i, j = indices
        #nn = np.sum(self.lattice[(i-1) % self.size[0]:(j+1) % self.size[0],
        #                         (j-1) % self.size[0]:(i+1) % self.size[0]]) - self.lattice[i, j]
        #return nn
        nearestNeighbours = 0

        neighbourNorth = self.lattice[(site[0] - 1) % self.size[0], site[1]]
        neighbourNorthEast = self.lattice[(
            site[0] - 1) % self.size[0], (site[1] + 1) % self.size[0]]
        neighbourEast = self.lattice[site[0], (site[1] + 1) % self.size[0]]
        neighbourSouthEast = self.lattice[(
            site[0] + 1) % self.size[0], (site[1] + 1) % self.size[0]]
        neighbourSouth = self.lattice[(site[0] + 1) % self.size[0], site[1]]
        neighbourSouthWest = self.lattice[(
            site[0] + 1) % self.size[0], (site[1] - 1) % self.size[0]]
        neighbourWest = self.lattice[site[0], (site[1] - 1) % self.size[0]]
        neighbourNorthWest = self.lattice[(
            site[0] - 1) % self.size[0], (site[1] - 1) % self.size[0]]

        if neighbourNorth == 1:
            nearestNeighbours += 1
        if neighbourNorthEast == 1:
            nearestNeighbours += 1
        if neighbourEast == 1:
            nearestNeighbours += 1
        if neighbourSouthEast == 1:
            nearestNeighbours += 1
        if neighbourSouth == 1:
            nearestNeighbours += 1
        if neighbourSouthWest == 1:
            nearestNeighbours += 1
        if neighbourWest == 1:
            nearestNeighbours += 1
        if neighbourNorthWest == 1:
            nearestNeighbours += 1

        return(nearestNeighbours)
    
    def evolve_state(self):
        """
            Parallel updating scheme for the GOL.
        """
        new_state = np.zeros(self.size)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                indices = [i, j]
                if self.lattice[i, j] == 1:
                    if self.count_nn(indices) < 2:
                        new_state[i, j] = 0
                    elif self.count_nn(indices) > 3:
                        new_state[i, j] = 0
                    else:
                        new_state[i, j] = 1
                    
                elif self.lattice[i, j] == 0:
                    if self.count_nn(indices) == 3:
                        new_state[i, j] = 1
                    else:
                        new_state[i, j] = 0

        self.lattice = new_state
    
    def count_live(self):
        """
            Returns the total number of live cells
            on the lattice.
        """
        return np.sum(self.lattice)
    
    def get_com(self):
        """
            Determines the centre of mass of live cells
            based on a 2D lattice of 1s and 0s.
        """
        # Determining locations of live cells.
        x_indices = np.where(self.lattice == 1)[0]
        y_indices = np.where(self.lattice == 1)[1]
        # Computing COM based off live cell positions.
        com_x = 1 / self.count_live() * np.sum(x_indices)
        com_y = 1 / self.count_live() * np.sum(y_indices)
        return np.array([com_x, com_y])
    
    def plot_hist(self, data, num_bins):
        """
            Histogram plotter for 
            steady state times.
        """
        plt.grid()
        plt.title("Histogram of GOL EQM Times")
        plt.xlabel("Time (Sweeps)")
        plt.ylabel("Frequency") 
        plt.hist(data, num_bins, facecolor='blue')
        plt.show()
    
    def plot_traj(self, x_data, y_data):
        """
            Scatter plotter for glider 
            trajectory.
        """
        plt.grid()
        plt.title("GOL Glider trajectory")
        plt.ylabel("x(t)")
        plt.xlabel("Time (Sweeps)")
        plt.scatter(x_data, y_data)
        plt.show()

    def animate(self, *args):
        """
            Creates, saves and returns image of the current state of
            lattice for the FuncAnimation class.
        """
        for i in range(self.it_per_sweep):
            self.evolve_state()
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
            self.figure, self.animate, repeat=False, frames=sweeps, interval=25, blit=True)
        plt.show()


