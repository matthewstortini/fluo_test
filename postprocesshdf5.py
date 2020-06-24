import numpy as np
import h5py
import pandas as pd
import sys
import time
from numba import jit
from tqdm import tqdm
#np.set_printoptions(threshold=sys.maxsize)

def main():

    process()
    #fluo_creations_process()


def process():
    """
    This postprocessing script takes g4simple data, and sums up the energy depositions per event to make a dataframe.
    It also saves in the dataframe the column "fp", which denotes the particle id (pid) of the first particle of a 
    given event to strike the detector. This is so that one can distinguish what particle is responsible for triggering
    the detector. Note that "fp" does not say anything about particles that strike the detector after the first particle
    for a given event, so for events when multiple particles enter the detector, "fp" will not tell the whole story. Thus,
    "fp" is most enlightening for simulations that have low event rates, i.e. simulations in which each event usually only
    has one particle entering the detector.
    """

    if(len(sys.argv) != 3):
        print('Usage: postprocesshdf5.py [input filename.hdf5 (with extension)] [output filename.hdf5 (with extension)]')
        sys.exit()

    start = time.time()
    print('In Progress...')

    pd.options.mode.chained_assignment = None

    # Import g4simple data
    g4sfile = h5py.File(sys.argv[1], 'r')
    g4sntuple = g4sfile['default_ntuples']['g4sntuple']

    # Taking data from g4sntuple and organizing it into a pandas dataframe.
    g4sdf = pd.DataFrame(np.array(g4sntuple['event']['pages']), columns=['event'])
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['step']['pages']), columns=['step']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['Edep']['pages']), columns=['Edep']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['volID']['pages']),
                       columns=['volID']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['pid']['pages']),
                       columns=['pid']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['trackID']['pages']),
                       columns=['trackID']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['t']['pages']),
                       columns=['t']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['parentID']['pages']),
                       columns=['parentID']), lsuffix = '_caller', rsuffix = '_other')

    # Only keep data that corresponds to particles in the detector.
    df = g4sdf.loc[(g4sdf.volID==1)]

    # Numba speeds up loops, but is only capatible with numpy, so convert df columns of interest into np arrays.
    event = df['event'].values
    pid_array = df['pid'].values

    # Define function that will allow fp to be extracted from data.
    @jit(nopython=True)
    def fp(array1, array2):
        for i in range(0, len(array2)-1):
            a = int(i)+1
            if array1[i]==array1[a]:
                array2[a] = array2[i]
        return array2

    fp(event, pid_array)
    
    # Insert fp into dataframe, and sum energy depositions by event.
    df['fp'] = pid_array
    procdf= pd.DataFrame(df.groupby(['event','fp'], as_index=False)['Edep'].sum())
    procdf = procdf.rename(columns={'Edep':'energy'})
    procdf = procdf.loc[(procdf.energy>0)]

    # Save the pandas dataframe.
    procdf.to_hdf('{}'.format(sys.argv[2]), key='procdf', mode='w')

    end = time.time()
    print('Done --- processed file has been output!')
    print('Run time = {:.0f} seconds'.format(end-start))


def fluo_creations_process():
    """
    This post-processing script tracks the initial energy of gammas as they are created in some volume.
    """

    if(len(sys.argv) != 3):
        print('Usage: postprocesshdf5.py [input filename.hdf5 (with extension)] [output filename.hdf5 (with extension)]')
        sys.exit()

    start = time.time()
    print('In Progress...')

    pd.options.mode.chained_assignment = None

    # Import g4simple data.
    g4sfile = h5py.File(sys.argv[1], 'r')
    g4sntuple = g4sfile['default_ntuples']['g4sntuple']

    # Taking data from g4sntuple and organizing it into a frame. Including KE to note the energy of particles when created.
    g4sdf = pd.DataFrame(np.array(g4sntuple['event']['pages']), columns=['event'])
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['step']['pages']), columns=['step']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['Edep']['pages']), columns=['Edep']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['volID']['pages']),
                       columns=['volID']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['pid']['pages']),
                       columns=['pid']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['KE']['pages']),
                       columns=['KE']), lsuffix = '_caller', rsuffix = '_other')

    # Only keep gammas's (pid 22) first step (step 0) in the foil (volID 2) to track creations.
    procdf = g4sdf.loc[(g4sdf.volID==2)&(g4sdf.step==0)&(g4sdf.pid==22)]

    # Save the pandas dataframe
    procdf.to_hdf('{}'.format(sys.argv[2]), key='procdf', mode='w')

    end = time.time()
    print('Done --- processed file has been output!')
    print('Run time = {:.0f} seconds'.format(end-start))


if __name__ == '__main__':
        main()

