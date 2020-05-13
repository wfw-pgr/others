import numpy as np

# ========================================================= #
# ===  correct__coordinate                              === #
# ========================================================= #

def correct__coordinate( inpFile=None, outFile=None, delta=0.0 ):

    if ( inpFile is None ): sys.exit( "[correct__coordinate] inpFile == ???" )
    if ( outFile is None ): sys.exit( "[correct__coordinate] outFile == ???" )

    with open( inpFile, "r" ) as f:
        Data = np.loadtxt( f )

    Data[:,1] = Data[:,1] + delta

    with open( outFile, "w" ) as f:
        np.loadtxt( f, Data )
    print( "[correct__coordinate] output :: {0} ".format( outFile ) )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    inpFile = "miyata_sample.dat"
    outFile = "miyata_sample_.dat"
    delta   = + 0.493138773 - 0.444941274
    
    correct__coordinate( inpFile=inpFile, outFile=outFile, delta=delta )
