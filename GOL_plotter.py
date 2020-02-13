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

        simulations = int(items[0]) # No. of simulations.
        ini_cond = str(items[1])    # Initial conditions.
        lattice_size = (int(items[2]), int(items[2]))  # Lattice size.
        num_bins = int(items[3])

    game = GOL(size=lattice_size, ini=ini_cond)

    if game.ini == 'random':
        eqm_times = []
        for i in range(simulations):
            #print(i)
            live_cells = []
            game = GOL(size=lattice_size, ini=ini_cond)
            while game.eqm == False:
                game.evolve_state()
                live_cells.append(game.count_live())
                if len(live_cells) > 3:
                    if live_cells[len(live_cells)-1] == live_cells[len(live_cells)-2] and live_cells[len(live_cells)-2] == live_cells[len(live_cells)-3]:
                        game.eqm = True
            eqm_times.append(len(live_cells) - 3)
        game.plot_hist(eqm_times,num_bins)
    
    elif game.ini == 'glider':
        x_pos = []
        y_pos = []
        for i in range(simulations):
            for j in range(10):
                game.evolve_state()
            x_pos.append(game.get_com()[0])
            y_pos.append(game.get_com()[1])
        game.plot_traj(np.arange(0,simulations,1), x_pos)

main()
