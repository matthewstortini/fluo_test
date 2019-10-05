import numpy as np
import h5py
import pandas as pd
import sys
import matplotlib.pyplot as plt
plt.style.use('style.mplstyle')

def main():

    #spectrum()
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

    df =  pd.read_hdf("{}".format(sys.argv[1]), key="procdf")

    m = list(df['energy'])
    p = list(x*1000 for x in m)

    plt.hist(p, np.arange(0,int(sys.argv[2]),1), histtype='step', color = 'black', label='1 million primaries, {} counts'.format(len(p)))
    plt.xlim(0,int(sys.argv[2]))
    plt.ylim(0,plt.ylim()[1])
    plt.xlabel('Energy (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Energy Spectrum (90Sr Source (no 90Y) + 10 micron Au foil)')
    plt.legend(frameon=True, loc='upper right', fontsize='small')
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

    df = pd.read_hdf("{}".format(sys.argv[1]), key="procdf")
    df_electrons = df.loc[(df.fp==11)]
    df_gammas = df.loc[(df.fp==22)]

    electrons_spectrum = list(df_electrons['energy'])
    electrons_spectrum = list(x*1000 for x in electrons_spectrum)
    gammas_spectrum = list(df_gammas['energy'])
    gammas_spectrum = list(x*1000 for x in gammas_spectrum)

    plt.hist(electrons_spectrum, np.arange(0,int(sys.argv[2]),1), histtype='step', color = 'red', label='electron triggered event, {} entries'.format(len(electrons_spectrum)))
    plt.hist(gammas_spectrum, np.arange(0,int(sys.argv[2]),1), histtype='step', color = 'green', label='gamma triggered event, {} entries'.format(len(gammas_spectrum)))
    plt.xlim(0,int(sys.argv[2]))
    plt.ylim(0,plt.ylim()[1])
    plt.xlabel('Energy (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Energy Spectrum (90Sr (no 90Y) + 10 micron Au foil)')
    plt.legend(frameon=True, loc='upper right', fontsize='small')
    plt.tight_layout()
    #plt.semilogy()
    #plt.semilogx()
    plt.show()


def fluo_spectrum():
    """
    Run postprocesshdf5.py on g4simple output file to get desired files for the dataframes defined below.
    """

    if(len(sys.argv) != 2):
        print('Usage: spectrum.py [maximum energy value for x axis of plot in keV] [Source]')
        sys.exit()

    df =  pd.read_hdf("alpha_gold_sim_processed.hdf5", key="procdf")
    m = list(df['KE'])
    p = list(x*1000 for x in m)

    df1 =  pd.read_hdf("gamma_gold_sim_processed.hdf5", key="procdf")
    m1 = list(df1['KE'])
    p1 = list(x*1000 for x in m1)

    df2 =  pd.read_hdf("electron_gold_sim_processed.hdf5", key="procdf")
    m2 = list(df2['KE'])
    p2 = list(x*1000 for x in m2)

    plt.hist(p1, np.arange(0,int(sys.argv[1]),0.5), histtype='step', color = 'blue', label='100 keV gamma sim, {} entries'.format(len(p1)))
    plt.hist(p2, np.arange(0,int(sys.argv[1]),0.5), histtype='step', color = 'red', label='300 keV beta sim, {} entries'.format(len(p2)))
    plt.hist(p, np.arange(0,int(sys.argv[1]),0.5), histtype='step', color = 'black', label='5.48 Mev alpha sim, {} entries'.format(len(p)))
    plt.xlim(0,int(sys.argv[1]))
    plt.ylim(0,plt.ylim()[1])
    plt.xlabel('KE (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Fluorescence Production (10 million primaries, 10 micron Au foil)')
    plt.legend(frameon=True, loc='best', fontsize='small')
    plt.tight_layout()
    #plt.semilogy()
    #plt.semilogx()
    plt.show()


if __name__ == '__main__':
	main()

