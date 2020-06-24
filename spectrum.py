import numpy as np
import h5py
import pandas as pd
import sys
import matplotlib.pyplot as plt
plt.style.use('style.mplstyle')

def main():

    spectrum()
    spectrum_by_incident_particle()
    #fluo_spectrum()


def spectrum():
    """
    This function simply plots an energy histogram. Run postprocesshdf5.py (function process()) on g4simple output file to get desired files 
    for the dataframes defined below.
    """ 

    if(len(sys.argv) != 3):
        print('Usage: spectrum.py [input .hdf5 file (with extension)] [maximum energy value for x axis of plot in keV]')
        sys.exit()

    # read in pandas dataframe, and pull out data of interest
    df =  pd.read_hdf("{}".format(sys.argv[1]), key="procdf")

    # set up data to plot, and perform any necessary unit conversion
    m = list(df['energy'])
    p = list(x*1000 for x in m)

    # I put here x-ray data from http://xdb.lbl.gov/Section1/Table_1-2.pdf, assign each line its type (i.e. ka1) and a color for plotting
    expected_fluo_peaks = [16.615,16.521,18.623]
    fluo_peaks_label = ['ka1', 'ka2', 'kb1']
    fluo_peaks_colors = ['red', 'aqua', 'black']
 
    # plot simulation data
    plt.hist(p, np.arange(0,int(sys.argv[2]),0.05), histtype='step', color = 'black', label='10 million primaries, {} counts'.format(len(p)))
    
    # plot expected x-ray lines
    for i in range(len(expected_fluo_peaks)):
        plt.axvline(x=expected_fluo_peaks[i], ymin=0, ymax=30, color='{}'.format(fluo_peaks_colors[i]), linestyle='--', lw=0.8, zorder=1, label='{}, E={} keV'.format(fluo_peaks_label[i],expected_fluo_peaks[i]))

    # set plot aesthetics
    plt.xlim(0,int(sys.argv[2]))
    plt.ylim(0,plt.ylim()[1])
    plt.xlabel('Energy (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Energy Spectrum ($^{99}$Tc + 100 micron Nb foil in gadget)')
    plt.legend(frameon=True, loc='best', fontsize='x-small')
    plt.tight_layout()
    #plt.semilogy()
    #plt.semilogx()
    plt.show()


def spectrum_by_incident_particle():
    """
    This function plots an energy histogram just like spectrum(), but it breaks the spectrum into parts showing the particle type that initially
    triggers the detector for a given event. Run postprocesshdf5.py (function process()) on g4simple output file to get desired files for the 
    dataframes defined below.
    """ 

    if(len(sys.argv) != 3):
        print('Usage: spectrum.py [input .hdf5 file (with extension)] [maximum energy value for x axis of plot in keV]')
        sys.exit()

    # read in pandas dataframe, and pull out data of interest
    df = pd.read_hdf("{}".format(sys.argv[1]), key="procdf")
    df_electrons = df.loc[(df.fp==11)]
    df_gammas = df.loc[(df.fp==22)]

    # set up data to plot, and perform any necessary unit conversion
    electrons_spectrum = list(df_electrons['energy'])
    electrons_spectrum = list(x*1000 for x in electrons_spectrum)
    gammas_spectrum = list(df_gammas['energy'])
    gammas_spectrum = list(x*1000 for x in gammas_spectrum)

    # I put here x-ray data from http://xdb.lbl.gov/Section1/Table_1-2.pdf, assign each line its type (i.e. ka1) and a color for plotting
    expected_fluo_peaks = [16.615,16.521,18.623]
    fluo_peaks_label = ['ka1', 'ka2', 'kb1']
    fluo_peaks_colors = ['red', 'aqua', 'black']

    # plot simulation data
    plt.hist(electrons_spectrum, np.arange(0,int(sys.argv[2]),0.05), histtype='step', color = 'red', label='electron triggered event, {} entries'.format(len(electrons_spectrum)))
    plt.hist(gammas_spectrum, np.arange(0,int(sys.argv[2]),0.05), histtype='step', color = 'green', label='gamma triggered event, {} entries'.format(len(gammas_spectrum)))

    # plot expected x-ray lines
    for i in range(len(expected_fluo_peaks)):
        plt.axvline(x=expected_fluo_peaks[i], ymin=0, ymax=30, color='{}'.format(fluo_peaks_colors[i]), linestyle='--', lw=0.8, zorder=1, label='{}, E={} keV'.format(fluo_peaks_label[i],expected_fluo_peaks[i]))

    # set plot aesthetics
    plt.xlim(0,int(sys.argv[2]))
    plt.ylim(0,plt.ylim()[1])
    plt.xlabel('Energy (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Energy Spectrum ($^{99}$Tc + 100 micron Nb foil in gadget)')
    plt.legend(frameon=True, loc='upper right', fontsize='x-small')
    plt.tight_layout()
    #plt.semilogy()
    #plt.semilogx()
    plt.show()


def fluo_spectrum():
    """
    Run postprocesshdf5.py on g4simple output file to get desired files for the dataframes defined below.
    """

    if(len(sys.argv) != 3):
        print('Usage: spectrum.py [input .hdf5 file (with extension)] [maximum energy value for x axis of plot in keV]')
        sys.exit()

    # read in pandas dataframe, and pull out data of interest
    df = pd.read_hdf("{}".format(sys.argv[1]), key="procdf")

    # set up data to plot, and perform any necessary unit conversion
    m = list(df['KE'])
    p = list(x*1000 for x in m)
  
    # I put here data from http://xdb.lbl.gov/Section1/Table_1-2.pdf, assign each line its type (i.e. ka1) and a color for plotting
    expected_fluo_peaks = [1.487, 1.486, 1.557]
    fluo_peaks_label = ['ka1', 'ka2', 'kb1']
    fluo_peaks_colors = ['red', 'aqua', 'black']

    # plot simulation data
    plt.hist(p, np.arange(0,int(sys.argv[2]),0.005), histtype='step', color = 'green', label='1 million primaries w/ Bearden, {} counts'.format(len(p)))
 
    # plot expected x-ray lines
    for i in range(len(expected_fluo_peaks)):
        plt.axvline(x=expected_fluo_peaks[i], ymin=0, ymax=30, color='{}'.format(fluo_peaks_colors[i]), linestyle='--', lw=0.8, zorder=1, label='{}, E={} keV'.format(fluo_peaks_label[i],expected_fluo_peaks[i]))

    # set plot aesthetics
    plt.xlim(1,int(sys.argv[2]))
    plt.ylim(0,plt.ylim()[1])
    plt.xlabel('KE (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Fluorescence Production (63Ni + 10 mm Al foil)')
    plt.legend(frameon=True, loc='best', fontsize='x-small')
    plt.tight_layout()
    #plt.semilogy()
    #plt.semilogx()
    plt.show()


if __name__ == '__main__':
	main()

