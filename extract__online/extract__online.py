import numpy as np
import nkUtilities.load__pointFile as lpf


# ========================================================= #
# ===  extract__online                                  === #
# ========================================================= #

def extract__online():

    inpFile1 = "grid.dat"
    inpFile2 = "line.dat"

    grid_    = lpf.load__pointFile( inpFile=inpFile1, returnType="structured" )
    line     = lpf.load__pointFile( inpFile=inpFile2, returnType="point"      )

    grid        = np.zeros( ( grid.shape[0],grid.shape[1],3 ) )
    grid[:,:,0] = grid_[:,:,0]
    grid[:,:,1] = grid_[:,:,1]
    grid[:,:,2] = grid_[:,:,5]
    
    import nkInterpolator.LinearInterp2D as li2
    Data = li2.LinearInterp2D( gridData=grid, pointData=line )

    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    extract__online()
