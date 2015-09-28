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

PD_inputs = {1: 'POP_A_RF9_I',
2: 'POP_A_RF9_Q',
3: 'POP_A_RF45_I',
4: 'POP_A_RF45_Q',
5: 'REFL_AF9_I',
6: 'REFL_A_RF9_Q',
7: 'REFL_A_RF45_I',
8: 'REFL_A_RF45_Q',
9: 'POPAIR_A_RF9_I',
10: 'POPAIR_A_RF9_Q',
11: 'POPAIR_A_RF45_I',
12: 'POPAIR_A_RF45_Q',
13: 'REFLAIR_A_RF9_I',
14: 'REFLAIR_A_RF9_Q',
15: 'REFLAIR_A_RF45_I',
16: 'REFLAIR_A_RF45_Q',
17: 'REFLAIR_B_RF27_I',
18: 'REFLAIR_B_RF27_Q',
19: 'REFLAIR_B_RF135_I',
20: 'REFLAIR_B_RF135_Q',
21: 'TR_X',
22: 'TR_Y',
23: 'REFL_SERVO_SLOW',
24: 'ALS_COMM_RF',
25: 'ASAIR_A_LF',
26: 'TR_CARM',
27: 'TR_REFL9',
28: 'REFL_DC',
29: 'OMC DC',
30: 'ASAIR_A_RF45_I',
31: 'ASAIR_A_RF45_Q'}

AS_inputs = {1: 'OMC_DC',
2: 'ASAIR_A_RF45_I',
3: 'ASAIR_A_RF45_Q',
4: 'ALS_DIFF',
5: 'REFL_SERVO'}

# the PD signals are mapped onto the length degrees of freedom

length_DOFs = {1: 'DARM',
2: 'CARM',
3: 'MICH',
4: 'PRCL',
5: 'SRCL',
6: 'MCL',
7: 'XARM',
8: 'YARM',
9: 'REFLBIAS'}

# the outputs of the DARM and CARM loops use a different output matrix
# for this reason, they're separated into their own dictionary

AS_outputs = {1: 'DARM',
2: 'CARM'}

DOF_outputs = {1: 'MICH',
2: 'PRCL',
3: 'SRCL', 
4: 'MCL',
5: 'XARM',
6: 'YARM',
7: 'OSC1',
8: 'OSC2',
9: 'OSC3',
10: 'MICH FF',
11: 'SRCL FF',
12: 'CPS FF'}

# output matrix maps DOF control signals to specific optics

optics = {1: 'ETMX',
2: 'ETMY',
3: 'ITMX',
4: 'ITMY',
5: 'PRM',
6: 'SRM',
7: 'BS',
8: 'PR2',
9: 'SR2',
10: 'MC2'}

# read in channel lists to populate each input matrix

PD_DOF_chans=np.loadtxt('PD_DOF_MTRX_chans',dtype=str)
ARM_INPUT_chans=np.loadtxt('ARM_INPUT_MTRX_chans',dtype=str)
OUTPUT_chans=np.loadtxt('OUTPUT_MTRX_chans',dtype=str)
ARM_OUTPUT_chans=np.loadtxt('ARM_OUTPUT_MTRX_chans',dtype=str)

# make a timeseries dictionary for each input matrix
print 'Fetching a bunch of data from frames'

PD_DOF_data = TimeSeriesDict.read(cache,PD_DOF_chans,start=start_gps,end=end_gps)
ARM_INPUT_data = TimeSeriesDict.read(cache,ARM_INPUT_chans,start=start_gps,end=end_gps)
OUTPUT_data = TimeSeriesDict.read(cache,OUTPUT_chans,start=start_gps,end=end_gps)
ARM_OUTPUT_data = TimeSeriesDict.read(cache,ARM_OUTPUT_chans,start=start_gps,end=end_gps)

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
print 'Mapping of PD error signals to physical DOFs:\n'

find_mappings(PD_DOF_data,PD_inputs,length_DOFs)
find_mappings(ARM_INPUT_data,AS_inputs,length_DOFs)

print '\nMapping of physical DOF control signals to optics:\n'

find_mappings(ARM_OUTPUT_data,AS_outputs,optics)
find_mappings(OUTPUT_data,DOF_outputs,optics)

