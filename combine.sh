python postprocesshdf5.py Sim_1.hdf5 Processed_1.hdf5
python postprocesshdf5.py Sim_2.hdf5 Processed_2.hdf5
python postprocesshdf5.py Sim_3.hdf5 Processed_3.hdf5
python postprocesshdf5.py Sim_4.hdf5 Processed_4.hdf5
python postprocesshdf5.py Sim_5.hdf5 Processed_5.hdf5
python combine_hdf5.py Processed 1 5
rm Processed_1.hdf5
rm Processed_2.hdf5
rm Processed_3.hdf5
rm Processed_4.hdf5
rm Processed_5.hdf5
mv Processed.hdf5 Tc_Au_Gadget5_Processed_1.hdf5
