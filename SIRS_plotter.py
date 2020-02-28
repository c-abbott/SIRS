from SIRS import SIRS
import numpy as np
import sys
import matplotlib.pyplot as plt
import math

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
        # Lattice size.
        lattice_size = (int(items[0]), int(items[0]))
        desired_plot = str(items[1]) # Desired plot.
        ini_cond = str(items[2])     # Initial conditions.
        p2 = float(items[3])         # P(I --> R).
        p_step = float(items[4])     # Probability steps.
        eqm_sweeps = int(items[5])   # Equilibrium sweeps.
        sweeps = int(items[6])       # No. of sweeps.

    if desired_plot == 'heatmap':
        # Initialising probability domains.
        p1s = np.arange(0.0, 1.0 + p_step, p_step)
        #print(p1s.size)
        p3s = np.arange(0.0, 1.0 + p_step, p_step)
        # Initialising phase matrix.
        phase_matrix = np.zeros((p1s.size, p3s.size))
        var_matrix = np.zeros((p1s.size, p3s.size))

        # Simulation begins.
        for p1 in p1s:
            print(p1)
            # Data storage.
            psi_per_p1 = []
            var_data = []
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
                        #psi = simulation.get_infected_frac()
                        #if psi != 0:
                        #    psi_per_p3.append(psi)
                        #else:
                        #    break
                # Data collection.
                psi_per_p1.append(simulation.get_avg_obs(
                    psi_per_p3) / (simulation.size[0]*simulation.size[1]))
                var_data.append(simulation.get_infected_var(
                    psi_per_p3) / (simulation.size[0]*simulation.size[1]))
            # Update matrix columns.
            phase_matrix[:, int(p1*(p1s.size-1))] = psi_per_p1
            var_matrix[:, int(p1*(p1s.size-1))] = var_data

        # Plotting.
        simulation.plot_phase_diagram(phase_matrix, p_step)
        simulation.plot_variance_contour(var_matrix, p_step)

        # Writing to file.
        np.savetxt("phase_data.dat", phase_matrix, fmt='%1.5f', delimiter=' ')
        np.savetxt("var_data.dat", var_matrix, fmt='%1.5f', delimiter=' ')

    elif desired_plot == 'variance_plot':
        # Initialising probability domains.
        p1s = np.arange(0.2, 0.51, 0.01)
        p3 = 0.5
        # Data storage.
        var_array = np.zeros(p1s.size)
        error_array = np.zeros(p1s.size)
        # Simulation begins.
        for i in range(p1s.size):
            print(p1s[i])
            # Data storage.
            psis = []
            # New simulation.
            simulation = SIRS(size=lattice_size,
                              ini=ini_cond, p1=p1s[i], p2=p2, p3=p3)
            # Sweeping.
            for sweep in range(10000):
                for j in range(simulation.size[0]*simulation.size[1]):
                        simulation.update_SIRS()
                if sweep >= eqm_sweeps:
                        psis.append(simulation.get_infected_frac())
            # Update arrays.
            var_array[i] = simulation.get_infected_var(psis) / \
                (simulation.size[0] * simulation.size[1])
            error_array[i] = simulation.bootstrap(psis, 100) / \
                (simulation.size[0] * simulation.size[1])
        # Plotting.
        simulation.plot_figure(p1s, var_array, error_array)

        # Writing to a file.
        with open("var_cut.dat", "w+") as f:
            f.writelines(map("{}, {}, {}\n".format, p1s, var_array, error_array))

    elif desired_plot == 'immunity':
        # Initialising probabilities.
        p1 = 0.5
        p3 = 0.5
        # Initialising x domain.
        im_fracs = np.arange(0.0, 0.505, 0.05)
        # Data storage.
        overall_psis = []
        errors = []
        for k in range(5):
            print(len(overall_psis))
            # Data storage.
            psi_per_k = []
            # New simulation.
            for frac in im_fracs:
                psi_per_frac = []
                simulation = SIRS(size=lattice_size,
                                  ini=ini_cond, p1=p1, p2=p2, p3=p3)
                # Creating immune sites.
                for i in range(int(simulation.size[0]*simulation.size[1]*frac)):
                    indices = (np.random.randint(0, simulation.size[0]),
                               np.random.randint(0, simulation.size[1]))
                    simulation.lattice[indices] = 2
                # Sweeping.
                for sweep in range(sweeps * 10):
                    for j in range(simulation.size[0]*simulation.size[1]):
                            simulation.update_SIRS()
                    if sweep >= eqm_sweeps:
                            psi_per_frac.append(simulation.get_infected_frac() / (simulation.size[0] * simulation.size[1]))
                psi_per_k.append(simulation.get_avg_obs(psi_per_frac))
            overall_psis.append(psi_per_k)
        for vals in np.array(overall_psis).T:
            errors.append(np.std(vals)/math.sqrt(len(vals)))
        y_data = np.mean(overall_psis, axis = 0)

        plt.title('Infected Sites vs. Immune Fraction')
        plt.xlabel('Immune Fraction')
        plt.ylabel('Infected Fraction')
        plt.errorbar(im_fracs, y_data, yerr = errors)
        plt.show()
main()
