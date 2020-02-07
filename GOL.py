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
        if self.ini == "r":
            self.lattice = np.random.choice(a=[0, 1], size=self.size)
