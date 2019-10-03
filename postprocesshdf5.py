import numpy as np
import h5py
import pandas as pd
import sys
import time
from numba import jit
from tqdm import tqdm
#np.set_printoptions(threshold=sys.maxsize)

def main():

    #process()
    process_initial_hits()
    #fluo_creations_process()


def process():

    if(len(sys.argv) != 3):
        print('Usage: postprocesshdf5.py [input filename.hdf5 (with extension)] [output filename.hdf5 (with extension)]')
        sys.exit()

    start = time.time()
    print('In Progress...')
 
    pd.options.mode.chained_assignment = None

    g4sfile = h5py.File(sys.argv[1], 'r')
    g4sntuple = g4sfile['default_ntuples']['g4sntuple']
    
    ##taking data from g4sntuple and organizing it into a frame. the groups for which there is data is given by print(n).
    g4sdf = pd.DataFrame(np.array(g4sntuple['event']['pages']), columns=['event'])
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['step']['pages']), columns=['step']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['Edep']['pages']), columns=['Edep']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['volID']['pages']),
                       columns=['volID']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['pid']['pages']),
                       columns=['pid']), lsuffix = '_caller', rsuffix = '_other')

    detector_hits = g4sdf.loc[(g4sdf.Edep>0)&(g4sdf.volID==1)]

    procdf= pd.DataFrame(detector_hits.groupby(['event','volID'], as_index=False)['Edep'].sum())

    procdf = procdf.rename(columns={'Edep':'energy'})

    procdf.to_hdf('{}'.format(sys.argv[2]), key='procdf', mode='w')
    
    end = time.time()
    print('Done --- processed file has been output!')
    print('Run time = {:.0f} seconds'.format(end-start))


def process_initial_hits():

    if(len(sys.argv) != 3):
        print('Usage: postprocesshdf5.py [input filename.hdf5 (with extension)] [output filename.hdf5 (with extension)]')
        sys.exit()

    start = time.time()
    print('In Progress...')

    pd.options.mode.chained_assignment = None

    g4sfile = h5py.File(sys.argv[1], 'r')
    g4sntuple = g4sfile['default_ntuples']['g4sntuple']

    ##taking data from g4sntuple and organizing it into a frame. the groups for which there is data is given by print(n).
    g4sdf = pd.DataFrame(np.array(g4sntuple['event']['pages']), columns=['event'])
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['step']['pages']), columns=['step']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['Edep']['pages']), columns=['Edep']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['KE']['pages']), columns=['KE']),
                       lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['volID']['pages']),
                       columns=['volID']), lsuffix = '_caller', rsuffix = '_other')
    g4sdf = g4sdf.join(pd.DataFrame(np.array(g4sntuple['pid']['pages']),
                       columns=['pid']), lsuffix = '_caller', rsuffix = '_other')


    df = g4sdf.loc[(g4sdf.volID==1)]

    event = df['event'].values
    nothing = np.zeros(len(df), dtype=np.float64)

    @jit(nopython=True)
    def initial_hits_loop(array1, array_cutter):
        for i in range(0, len(array_cutter)-1):
            a = int(i)+1
            if array1[i]==array1[a]:
                array_cutter[a] = 1
        return array_cutter

    initial_hits_loop(event, nothing)

    df['nothing'] = nothing

    procdf = df.loc[(df.nothing<1)&(df.volID==1)]
    del procdf['nothing']

    procdf.to_hdf('{}'.format(sys.argv[2]), key='procdf', mode='w')

    end = time.time()
    print('Done --- processed file has been output!')
    print('Run time = {:.0f} seconds'.format(end-start))


def fluo_creations_process():

    if(len(sys.argv) != 3):
        print('Usage: postprocesshdf5.py [input filename.hdf5 (with extension)] [output filename.hdf5 (with extension)]')
        sys.exit()

    start = time.time()
    print('In Progress...')

    pd.options.mode.chained_assignment = None

    g4sfile = h5py.File(sys.argv[1], 'r')
    g4sntuple = g4sfile['default_ntuples']['g4sntuple']

    ##taking data from g4sntuple and organizing it into a frame. the groups for which there is data is given by print(n).
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


    procdf = g4sdf.loc[(g4sdf.step==0)&(g4sdf.pid==22)]

    procdf.to_hdf('{}'.format(sys.argv[2]), key='procdf', mode='w')

    end = time.time()
    print('Done --- processed file has been output!')
    print('Run time = {:.0f} seconds'.format(end-start))


if __name__ == '__main__':
        main()

