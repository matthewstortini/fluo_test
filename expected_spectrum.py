import numpy as np
import h5py
import pandas as pd
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm
from numba import jit
plt.style.use('style.mplstyle')

if(len(sys.argv) != 2):
    print('Usage: expected_spectrum.py [input .hdf5 file (with extension)]')
    sys.exit()

#def resolution(E, a=1.17083, b=0.04221, c=0.00100):
    #return np.sqrt(a**2+b**2*E+c**2*E**2)

@jit(nopython=True)
def apply_resolution(sim_array,loop_length, a, b, c):
    ''' This function takes in simulation data and parameters of a resolution function to apply resolution to simulation data. The bigger
    the loop_length, the less stats you lose from applying resolution. Make sure when histogramming the output that you weight your histogram 
    values by 1/loop_length, so that simulation counting statistics can be accurate. '''
    output_array = np.zeros(len(sim_array)*loop_length)
    for i in range(len(sim_array)):
        for j in range(0,loop_length):
            output_array[int(i*loop_length+j)] = sim_array[i] + np.random.normal(0,np.sqrt(a**2+b**2*sim_array[i]+c**2*sim_array[i]**2),1)[0]
    output_array
    return output_array

# import mj60 background data and calibrate it
df = pd.read_hdf('t2_run994.h5')
df['e_cal'] = df['e_ftp']*0.42273-0.03475

# read in pandas dataframe, and pull out data of interest
df2 = pd.read_hdf("{}".format(sys.argv[1]), key="procdf")
# set up data to plot, and perform any necessary unit conversion
df2['energy'] = df2['energy']*1000
m = np.array(df2['energy'])

loop_length = 50000
sim_energies = apply_resolution(m,loop_length=loop_length,a=3.17083, b=0.04221, c=0.00100)

# specify relevant values, plot simulation data and mj60 data
source_activity=100000
sim_primaries=5000000
mj60_runtime=1800
sim_hist, bins = np.histogram(sim_energies,bins=np.arange(0,5000,0.5),weights=np.repeat(1,len(sim_energies))*mj60_runtime*source_activity*0.8/(sim_primaries*loop_length))
data_hist, bins = np.histogram(df['e_cal'],bins=np.arange(0,5000,0.5))
hist = sim_hist + data_hist
bins = bins + (bins[1]-bins[0])

bkgcts = round(np.sum(data_hist)/mj60_runtime,1)
totcts = round(np.sum(hist)/mj60_runtime,1)

plt.plot(bins[0:-1],hist,ds='steps',color='black',label="simulation + background : {} counts/second".format(totcts))
plt.hist(df['e_cal'],np.arange(0,1500,0.5),color='red',label='background : {} counts/second'.format(bkgcts))

# plot expected x-ray lines
expected_fluo_peaks = [68.804,66.990,77.984]
fluo_peaks_label = ['ka1', 'ka2', 'kb1']
fluo_peaks_colors = ['green', 'aqua', 'black']
for i in range(len(expected_fluo_peaks)):
    plt.axvline(x=expected_fluo_peaks[i], ymin=0, ymax=30, color='{}'.format(fluo_peaks_colors[i]), linestyle='--', lw=0.8, zorder=1, label='{}, E={} keV'.format(fluo_peaks_label[i],expected_fluo_peaks[i]))

# set plot aesthetics
plt.xlim(0,300)
plt.ylim(0,plt.ylim()[1])
plt.xlabel('Energy (keV)', ha='right', x=1.0)
plt.ylabel('Counts', ha='right', y=1.0)
plt.title('$^{99}$Tc, 250 micron Au foil, 100 kBq source, Aluminum Source Holder')
plt.legend(frameon=True, loc='best', fontsize='small')
plt.tight_layout()
#plt.semilogy()
#plt.semilogx()
plt.show()
