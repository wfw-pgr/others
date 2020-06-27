import numpy as np
import os, sys, subprocess


# ========================================================= #
# ===  prepare__pole_mcoord                             === #
# ========================================================= #

def prepare__pole_mcoord():

    # ------------------------------------------------- #
    # --- [1] File copying                          --- #
    # ------------------------------------------------- #
    mdtRoot  = "/mnt/f/kent/mdt2/"
    path     = "biaAnalysis/generate__ideal_mainField/dat/"
    FileName = "bia_coordinates_mcoord.dat"
    cooFile  = mdtRoot + path + FileName

    cmd      = "cp {0} dat/".format( cooFile )
    print( cmd )
    subprocess.call( cmd.split() )

    # ------------------------------------------------- #
    # --- [2] File extraction                       --- #
    # ------------------------------------------------- #

    inpFile  = "dat/{0}".format( FileName )
    with open( inpFile, "r" ) as f:
        Data = np.loadtxt( f )

    outFile  = "dat/ems_pst.coord"
    with open( outFile, "w" ) as f:
        np.savetxt( f, Data, fmt="%15.8e" )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    prepare__pole_mcoord()
