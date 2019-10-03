import numpy as np
import h5py
import pandas as pd
import sys
import matplotlib.pyplot as plt
plt.style.use('style.mplstyle')

def main():

    spectrum()
    #incident_hits_KE()
    #fluo_spectrum()


def spectrum():

    """
    Run postprocesshdf5.py (function process()) on g4simple output file to get desired files for the dataframes defined below.
    """ 

    if(len(sys.argv) != 3):
        print('Usage: spectrum.py [input .hdf5 file (with extension)] [maximum energy value for x axis of plot in keV]')
        sys.exit()

    df =  pd.read_hdf("{}".format(sys.argv[1]), key="procdf")

    m = list(df['energy'])
    p = list(x*1000 for x in m)

    plt.hist(p, np.arange(0,int(sys.argv[2]),0.1), histtype='step', color = 'black', label='1 million primaries, {} counts'.format(len(p)))
    plt.xlim(0,int(sys.argv[2]))
    #plt.ylim(0,plt.ylim()[1])
    plt.xlabel('Energy (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Energy Spectrum (90Sr Source (no 90Y) + 100 micron Au foil)')
    plt.legend(frameon=True, loc='upper right', fontsize='small')
    plt.tight_layout()
    plt.semilogy()
    #plt.semilogx()
    plt.show()


def incident_hits_KE():
    """
    Run postprocesshdf5.py (function process_initial_hits()) on g4simple output file to get desired files for the dataframes defined below
    """ 

    if(len(sys.argv) != 3):
        print('Usage: spectrum.py [input .hdf5 file (with extension)] [maximum energy value for x axis of plot in keV]')
        sys.exit()

    df =  pd.read_hdf("{}".format(sys.argv[1]), key="procdf")
    df['incident_KE'] = df['KE']+df['Edep']
    df_electrons = df.loc[(df.pid==11)&(df.incident_KE>0)]
    df_gammas = df.loc[(df.pid==22)&(df.incident_KE>0)]

    ke_electrons = list(df_electrons['incident_KE'])
    ke_electrons = list(x*1000 for x in ke_electrons)
    ke_gammas = list(df_gammas['incident_KE'])
    ke_gammas = list(x*1000 for x in ke_gammas)

    plt.hist(ke_electrons, np.arange(0,int(sys.argv[2]),1), histtype='step', color = 'red', label='electron hits, {} entries'.format(len(ke_electrons)))
    plt.hist(ke_gammas, np.arange(0,int(sys.argv[2]),1), histtype='step', color = 'green', label='gamma hits, {} entries'.format(len(ke_gammas)))
    plt.xlim(0,int(sys.argv[2]))
    #plt.ylim(0,plt.ylim()[1])
    plt.xlabel('Kinetic Energy (keV)', ha='right', x=1.0)
    plt.ylabel('Counts', ha='right', y=1.0)
    plt.title('Incident KE by Particle Type (90Sr (no 90Y) + 100 micron Au foil)')
    plt.legend(frameon=True, loc='upper right', fontsize='small')
    plt.tight_layout()
    plt.semilogy()
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
    #plt.ylim(0,plt.ylim()[1])
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

