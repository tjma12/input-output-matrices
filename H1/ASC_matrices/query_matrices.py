from gwpy.timeseries import TimeSeriesDict
from glue import datafind
import numpy as np
import sys

# input/output matrix values are 16Hz EPICs channels
# the data grab is only (1/16)s long because we only need to test one sample

start_gps = float(sys.argv[1])
end_gps = start_gps + 1.0/16
ifo = 'H'
frames = 'H1_R'
connection = datafind.GWDataFindHTTPConnection()
cache = connection.find_frame_urls(ifo, frames, start_gps, end_gps, urltype='file')

# dictionary defining the enumeration of the input PD signals
# PDs that feed into DARM from the OMC model use a different input matrix
# Those specific channels are stored in the AS_inputs dictionary

PD_inputs = {1: 'AS_A_RF45_I',
2: 'AS_A_RF45_Q',
3: 'AS_A_RF36_I',
4: 'AS_A_RF36_Q',
5: 'AS_B_RF45_I',
6: 'AS_B_RF45_Q',
7: 'AS_B_RF36_I',
8: 'AS_B_RF36_Q',
9: 'REFL_A_RF9_I',
10: 'REFL_A_RF9_Q',
11: 'REFL_A_RF45_I',
12: 'REFL_A_RF45_Q',
13: 'REFL_B_RF9_I',
14: 'REFL_B_RF9_Q',
15: 'REFL_B_RF45_I',
16: 'REFL_B_RF45_Q',
17: 'REFL_A_DC',
18: 'REFL_B_DC',
19: 'AS_A_DC',
20: 'AS_B_DC',
21: 'POP_A_DC',
22: 'POP_B_DC',
23: 'TR_X_A',
24: 'TR_X_B',
25: 'TR_Y_A',
26: 'TR_Y_B',
27: 'AS_C_DC'}

# the PD signals are mapped onto the alignment degrees of freedom

alignment_DOFs = {1: 'INP1',
2: 'INP2',
3: 'PRC1',
4: 'PRC2',
5: 'MICH',
6: 'SRC1',
7: 'SRC2',
8: 'DHARD',
9: 'DSOFT',
10: 'CHARD',
11: 'CSOFT',
12: 'DC1',
13: 'DC2',
14: 'DC3',
15: 'DC4',
16: 'DC5'}

DOF_outputs = {1: 'INP1',
2: 'INP2',
3: 'PRC1',
4: 'PRC2',
5: 'MICH',
6: 'SRC1',
7: 'SRC2',
8: 'DHARD',
9: 'DSOFT',
10: 'CHARD',
11: 'CSOFT',
12: 'DC1',
13: 'DC2',
14: 'DC3',
15: 'DC4',
16: 'DC5',
17: 'ALSX1',
18: 'ALSX2',
19: 'ALSX3',
20: 'ALSY1',
21: 'ALSY2',
22: 'ALSY3',
23: 'OSC1',
24: 'OSC2',
25: 'OSC3',
26: 'OSC4'}
# output matrix maps DOF control signals to specific optics

optics = {1: 'PRM',
2: 'PR2',
3: 'PR3',
4: 'BS',
5: 'ITMX',
6: 'ITMY',
7: 'ETMX',
8: 'ETMY',
9: 'SRM',
10: 'SR2',
11: 'SR3',
12: 'IM1',
13: 'IM2',
14: 'IM3',
15: 'IM4',
16: 'RM1',
17: 'RM2',
18: 'OM1',
19: 'OM2',
20: 'OM3',
21: 'TMSX',
22: 'TMSY'}

# read in channel lists to populate each input matrix

INMATRIX_chans_PIT=np.loadtxt('ASC_INMATRIX_P_chans.txt',dtype=str)
INMATRIX_chans_YAW=np.loadtxt('ASC_INMATRIX_Y_chans.txt',dtype=str)
OUTMATRIX_chans_PIT=np.loadtxt('ASC_OUTMATRIX_P_chans.txt',dtype=str)
OUTMATRIX_chans_YAW=np.loadtxt('ASC_OUTMATRIX_Y_chans.txt',dtype=str)

# make a timeseries dictionary for each input matrix
print 'Fetching a bunch of data from frames'

INMATRIX_PIT_data = TimeSeriesDict.read(cache,INMATRIX_chans_PIT,start=start_gps,end=end_gps)
INMATRIX_YAW_data = TimeSeriesDict.read(cache,INMATRIX_chans_YAW,start=start_gps,end=end_gps)
OUTMATRIX_PIT_data = TimeSeriesDict.read(cache,OUTMATRIX_chans_PIT,start=start_gps,end=end_gps)
OUTMATRIX_YAW_data = TimeSeriesDict.read(cache,OUTMATRIX_chans_YAW,start=start_gps,end=end_gps)

# main workhorse function of this script
#
# requires a dictionary containing matrix element time series and two dictionaries
# that map these matrix elements to IO channels
#
# grab the first sample of each channel - if it's non-zero, add it to the list of active channels
# 
# process the active channels and return a set of tuples indicating the matrix entries
# 
# send through a search function that lines up the inputs and outputs
# uses the set of tuples generated from active channels a dictionary maps them to PDs and DOFs
def find_mappings(data_dict,input_dict,output_dict):
	active_chans = [chan for chan,data in data_dict.iteritems() if data.value[0] != 0]
	active_tuples = []
	for channel in active_chans:
		active_tuples.append(channel.split("_")[-2:])
	for entry in active_tuples:
		print input_dict[int(entry[1])] + " -> " + output_dict[int(entry[0])]


# input matrix pointing PDs -> DOFs
print 'Mapping of WFS error signals to PITCH DOFs:\n'

find_mappings(INMATRIX_PIT_data,PD_inputs,alignment_DOFs)

print '\nMapping of PITCH DOF control signals to optics:\n'

find_mappings(OUTMATRIX_PIT_data,DOF_outputs,optics)

print 'Mapping of WFS error signals to YAW DOFs:\n'

find_mappings(INMATRIX_YAW_data,PD_inputs,alignment_DOFs)

print '\nMapping of YAW DOF control signals to optics:\n'

find_mappings(OUTMATRIX_YAW_data,DOF_outputs,optics)

