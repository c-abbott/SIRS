from SIRS import SIRS
import numpy as np
import sys
import matplotlib.pyplot as plt
def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments.")
        print("Usage: " + sys.argv[0] + " <parameters file>")
        quit()
    else:
        infile_parameters = sys.argv[1]

    # Open input file and assinging parameters.
    with open(infile_parameters, "r") as input_file:
        # Read the lines of the input data file.
        line = input_file.readline()
        items = line.split(", ")
        lattice_size = (int(items[0]), int(items[0]))  # Lattice size.
        ini_cond = str(items[1])   # Initial conditions.
        p2 = float(items[2])       # P(I --> R).
        p_step = float(items[3])   # Probability steps.
        eqm_sweeps = int(items[4]) # Equilibrium sweeps.
        sweeps = int(items[5])     # No. of sweeps.

    # Initialising probability domains.
    p1s = np.arange(0.0, 1.0+p_step, p_step)
    p3s = np.arange(0.0, 1.0+p_step, p_step)
    # Initialising phase matrix.
    phase_matrix = np.zeros((p1s.size, p3s.size))

    # Simulation begins.
    for p1 in p1s:
        print(p1)
        # Data storage.
        psi_per_p1 = []
        for p3 in p3s:
            simulation = SIRS(size=lattice_size,
                                ini=ini_cond, p1=p1, p2=p2, p3=p3)
            psi_per_p3 = []
            # Sweep over lattice.
            for sweep in range(sweeps):
                for j in range(simulation.size[0]*simulation.size[1]):
                    simulation.update_SIRS()
                if sweep >= eqm_sweeps:
                    psi_per_p3.append(simulation.get_infected_frac())
            # Data collection.
            psi_per_p1.append(simulation.get_avg_obs(psi_per_p3))
        # Update matrix columns.
        phase_matrix[:, int(p1*p1s.size)] = psi_per_p1[::-1]
    # Plotting.
    simulation.plot_phase_diagram(phase_matrix, p1s.size)
    # Writing to file.
    np.savetxt("phase_data.dat", phase_matrix, fmt='%1.5f', delimiter=' ')
main()


        
