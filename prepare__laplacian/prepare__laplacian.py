import sys, os
import numpy as np


# ========================================================= #
# ===  prepare__laplacian                               === #
# ========================================================= #
def prepare__laplacian( xCnt=0.0, yCnt=0.0, x1MinMaxNum=None, x2MinMaxNum=None ):

    # ------------------------------------------------- #
    # --- [1] parameters                            --- #
    # ------------------------------------------------- #
    r1   = 0.2
    r2   = 0.4
    c1   = 1.e-9
    c2   = 3.e-6
    xCnt =   0.00
    yCnt = - 0.60

    # ------------------------------------------------- #
    # --- [2] grid making                           --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    if ( x1MinMaxNum is None ): x1MinMaxNum = [  0.0, +1.8, 121 ]
    if ( x2MinMaxNum is None ): x2MinMaxNum = [ -1.8, +1.8, 241 ]
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     returnType = "structured" )
    xg          = np.ravel( ret[:,:,0] )
    yg          = np.ravel( ret[:,:,1] )
    LI          = ret.shape[1]
    LJ          = ret.shape[0]
    radii       = np.sqrt( ( xg-xCnt )**2 + ( yg-yCnt )**2 )

    # ------------------------------------------------- #
    # --- [3] distribution                          --- #
    # ------------------------------------------------- #
    ret         = rFunc( radii=radii, c1=c1, c2=c2, r1=r1, r2=r2 )
    print( ret.shape )

    # ------------------------------------------------- #
    # --- [4] output results                        --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "out.dat"
    print( ret.shape )
    shape     = (LJ,LI,1)
    Data      = np.reshape( ret, shape )
    spf.save__pointFile( outFile=outFile, Data=Data, shape=shape )

    import nkUtilities.cMapTri as cmt
    pngFile   = "out.png"
    import nkUtilities.LoadConfig as lcf
    config    = lcf.LoadConfig()
    config["cmp_AutoLevel"] = False
    config["cmp_MaxMin"]    = [ 1.e-10, 5.e-6 ]
    cmt.cMapTri( xAxis=xg, yAxis=yg, cMap=ret, pngFile=pngFile, config=config  )


# ========================================================= #
# ===  rFunc :: distribution                            === #
# ========================================================= #
def rFunc( radii=None, c1=1.e-9, c2=3.e-6, r1=0.2, r2=0.4 ):
    ret                            = np.zeros( radii.shape )
    ret[ np.where( radii <= r1 ) ] = c1
    ret[ np.where( radii >= r2 ) ] = c2
    rest                           = np.where( ( radii >= r1 ) & ( radii <= r2 ) ) 
    ret[ rest ] = ( ( c2-c1 ) / ( r2-r1 ) ) * ( radii[rest] - r1 ) + c1
    return( ret )
    
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    prepare__laplacian()
    
