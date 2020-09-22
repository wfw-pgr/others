import numpy as np

# ========================================================= #
# ===  generate__axisymm_coord.py                       === #
# ========================================================= #

def generate__axisymm_coord():

    cnfFile     = "dat/parameter.conf"
    outFile     = "dat/axisymm_coord.dat"
    
    import nkUtilities.load__constants as lcn
    const       = lcn.load__constants( inpFile=cnfFile )
    
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ const["rMin"], const["rMax"], const["LI"] ]
    x2MinMaxNum = [ 0.0, 0.0,  1 ]
    x3MinMaxNum = [ const["zMin"], const["zMax"], const["LK"] ]
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )

    # ------------------------------------------------- #
    # --- [3] save in file                          --- #
    # ------------------------------------------------- #
    
    with open( outFile, "w" ) as f:
        np.savetxt( f, ret )
    
    return()



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    generate__axisymm_coord()
