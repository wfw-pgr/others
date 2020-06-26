import sys
import numpy as np
import nkUtilities.genArgs as gar

args    = gar.genArgs()
num     = args["integer"]

if ( num is None ):
    print( "[feedback__mshape] num == ???  ( --integer xxx ) " )
    sys.exit()

inpFile   = "out/mshape_{0:04}.dat".format( num )
outFile   = "dat/mshape_feedback.dat"

import nkUtilities.load__pointFile as lpf
Data  = lpf.load__pointFile( inpFile=inpFile, returnType="structured" )
wData = Data[:,:,0:3]
LJ    = wData.shape[0]
LI    = wData.shape[1]
wData = np.reshape( wData, (1,LJ,LI,3) )

import nkUtilities.save__pointFile as spf
spf.save__pointFile( outFile=outFile, Data=wData )
