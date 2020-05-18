import os, sys, subprocess
import numpy as np

# ========================================================= #
# === make .inp file for EMSolution execution           === #
# ========================================================= #

def make__emsInpFile( mode=None ):

    # ------------------------------------------------- #
    # --- [1] Check Arguments                       --- #
    # ------------------------------------------------- #
    if ( mode is None ): sys.exit( "[make__emsInpFile] mode == ???" )

    # ------------------------------------------------- #
    # --- [2] copy refference slv input File        --- #
    # ------------------------------------------------- #

    if ( mode in ["slv"] ):
        cmd = "cp ref/ems_slv.inp inp/ems_slv.inp"
        print( cmd )
        subprocess.call( cmd.split() )
        return()
    
    # ------------------------------------------------- #
    # --- [3] Load File for post                    --- #
    # ------------------------------------------------- #

    targetFile  = "ref/ems_{0}.inp"  .format( mode )
    coordFile   = "dat/ems_{0}.coord".format( mode )

    with open( targetFile, "r" ) as f:
        contents = f.read()
    with open( coordFile , "r" ) as f:
        coord    = np.loadtxt( f )
        nLine    = coord.shape[0]
    with open( coordFile , "r" ) as f:
        coord    = f.read()
    
    # ------------------------------------------------- #
    # --- [4] save File                             --- #
    # ------------------------------------------------- #

    outFile   = "inp/ems_{0}.inp".format( mode )
    contents_ = contents.format( nLine, coord )

    with open( outFile, "w" ) as f:
        f.write( contents_ )
    

# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    import nkUtilities.genArgs as gar
    args = gar.genArgs()
    mode = args["mode"]
    
    make__emsInpFile( mode=mode )
