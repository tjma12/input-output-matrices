# input-output-matrices
This code is used to determine feedback paths in the LIGO interferometers based on a parsing of the input/output matrices

Written by TJ Massinger for LVC use

This code is shipped with a list of EPICs channels that comprise the LSC input/output matrices.

There are a series of python dictionaries defined in the query_matrices.py that allow for the EPICs channels to be parsed and assigned to photodiodes/degrees of freedom/optics.

The output will be a simple text dump that tells you which photodiodes are being piped into physical degrees of freedom and which optics are being used to actuate on those degrees of freedom.

The executables should be run in the directory they sit in with the only arg being a GPS time. 

Example command:

python query_matrices.py 1115899216

Returns:

Fetching a bunch of data from frames
Mapping of PD error signals to physical DOFs:

POP_A_RF45_Q -> MICH

POP_A_RF9_I -> PRCL

POP_A_RF9_I -> SRCL

POP_A_RF45_I -> SRCL

REFL_SERVO_SLOW -> MCL

TR_REFL9 -> REFLBIAS

OMC_DC -> DARM

Mapping of physical DOF control signals to optics:

DARM -> ETMX

DARM -> ETMY

OSC3 -> ETMX

OSC3 -> ETMY

SRCL FF -> ETMY

MICH FF -> ITMY

PRCL -> PRM

SRCL -> SRM

MICH -> BS

MCL -> MC2

