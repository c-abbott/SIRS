from GOL import GOL
import numpy as np
import sys


def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + " <parameters file>")
        quit()
    else:
        infile_parameters = sys.argv[1]

     # open input file and assinging parameters
    with open(infile_parameters, "r") as input_file:
        # read the lines of the input data file
        line = input_file.readline()
        items = line.split(", ")

        simulations = int(items[0])  # No. of simulations.
        ini_cond = str(items[1])    # Initial conditions.
        lattice_size = (int(items[2]), int(items[2]))  # Lattice size.

    game = GOL(size=lattice_size, ini=ini_cond)

    # Simulation for GOL steady state determination.
    if game.ini == 'random':
        eqm_times = []
        # Simulation begins.
        for i in range(simulations):
            live_cells = []
            game = GOL(size=lattice_size, ini=ini_cond)
            while game.eqm == False:
                game.evolve_state()
                # Count number of live cells in state.
                live_cells.append(game.count_live())
                # Steady state determination.
                game.check_eqm(live_cells)
            # Minus 3 to account for check_eqm.
            eqm_times.append(len(live_cells) - 3)
            print (eqm_times[i])
        # Plotting.
        game.plot_hist(eqm_times, np.arange(0, 2500, 100))

    elif game.ini == 'glider':
        # Initialising data storage.
        x_pos = []
        y_pos = []
        times = []
        plot_all = False
        # Simulation begins.
        for i in range(simulations):
            for j in range(10):
                game.evolve_state()
            # Find live cells of glider.
            xs = game.get_glider_pos()[0]
            ys = game.get_glider_pos()[1]
            # Check if at lattice boundary.
            x_checker, y_checker = game.boundary_checker(xs, ys)
            # Store COM pos if not at lattice boundary.
            if x_checker == False and y_checker == False:
                times.append(i)
                x_pos.append(game.get_com(xs, ys)[0])
                y_pos.append(game.get_com(xs, ys)[1])

        # Printing glider velocity.
        vel = game.plot_traj(times, x_pos, all=plot_all)
        if plot_all == False:
            print("The velocity of the glider is " + str(vel) + " cells / sweep")


main()
