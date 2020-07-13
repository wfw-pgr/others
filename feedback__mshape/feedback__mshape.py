import sys
import numpy as np
import nkUtilities.genArgs as gar

# ------------------------------------------------- #
# --- [1] Arguments                             --- #
# ------------------------------------------------- #
args     = gar.genArgs()
num      = args["integer"]

if ( num is None ):
    print( "[feedback__mshape] num == ???  ( --integer xxx ) " )
    sys.exit()

# ------------------------------------------------- #
# --- [2] Load input Files                      --- #
# ------------------------------------------------- #
inpFile  = "out/mshape_{0:04}.dat".format( num )
outFile  = "dat/mshape_feedback.dat"

import nkUtilities.load__pointFile as lpf
Data     = lpf.load__pointFile( inpFile=inpFile, returnType="structured" )
LJ       = Data.shape[0]
LI       = Data.shape[1]

# ------------------------------------------------- #
# --- [3] extrapolate peripheral region         --- #
# ------------------------------------------------- #

for j in range( LJ ):
    for i in range( LI ):
        if ( Data[j,i,5] == 0.0 ):
            avg = 0.0
            num = 0
            if ( i >= 1    ):
                if ( round( Data[j,i-1,5] ) == 1 ):
                    avg = avg + Data[j,i-1,2]
                    num = num + 1
            if ( i <= LI-2 ):
                if ( round( Data[j,i+1,5] ) == 1 ):
                    avg = avg + Data[j,i+1,2]
                    num = num + 1
            if ( j >= 1    ):
                if ( round( Data[j-1,i,5] ) == 1 ):
                    avg = avg + Data[j-1,i,2]
                    num = num + 1
            if ( j <= LJ-2 ):
                if ( round( Data[j+1,i,5] ) == 1 ):
                    avg = avg + Data[j+1,i,2]
                    num = num + 1
            if ( num != 0 ):
                Data[j,i,2] = avg / float( num )

        
# ------------------------------------------------- #
# --- [4] save as point File                    --- #
# ------------------------------------------------- #
wData = Data[:,:,0:3]
wData = np.reshape( wData, (1,LJ,LI,3) )

import nkUtilities.save__pointFile as spf
spf.save__pointFile( outFile=outFile, Data=wData )
