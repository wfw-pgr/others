import os, sys
import numpy as np

# ========================================================= #
# ===  make regenerator shape file for tsvd2d           === #
# ========================================================= #

def make__regenShapeFile():

    # ------------------------------------------------- #
    # --- [1] Load parameter File                   --- #
    # ------------------------------------------------- #
    
    import nkUtilities.load__constants as lcn
    cnfFile  = "dat/parameter.conf"
    const    = lcn.load__constants( inpFile=cnfFile )

    x_,y_,z_ = 0, 1, 2
    i_,s_,f_ = 3, 4, 5
    dx1      =  ( const["x1Max"] - const["x1Min"] ) / float( const["LI"]-1 )
    dx2      =  ( const["x2Max"] - const["x2Min"] ) / float( const["LJ"]-1 )

    # ------------------------------------------------- #
    # --- [2] Grid Generation                       --- #
    # ------------------------------------------------- #
    # -- [2-1] structured grid  -- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ const["x1Min"]+0.5*dx1, const["x1Max"]-0.5*dx1, const["LI"]-1 ]
    x2MinMaxNum = [ const["x2Min"]+0.5*dx2, const["x2Max"]-0.5*dx2, const["LJ"]-1 ]
    x3MinMaxNum = [           0.0,           0.0,    1 ]
    grid        = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    nData       = grid.shape[0]
    # -- [2-2] radius & angle   -- #
    radii       = np.sqrt( grid[:,x_]**2 + grid[:,y_]**2 )
    phi         = np.arctan2( grid[:,y_], grid[:,x_] ) / np.pi * 180.0
    phi[ np.where( phi < 0.0 ) ] = phi[ np.where( phi < 0.0 ) ] + 360.0
    # -- [2-3] normalized value -- #
    rhat        = ( radii - const["regen_r1"] ) / ( const["regen_r2"] - const["regen_r1"] )
    phat        = ( phi   - const["regen_p1"] ) / ( const["regen_p2"] - const["regen_p1"] )
    # -- [2-4] judge in/out     -- #
    idx         = np.where( ( rhat > 0.0 ) & ( rhat < 1.0 ) & ( phat > 0.0 ) & ( phat < 1.0 ) )
    flags       = np.zeros( (nData) )
    flags[idx]  = 1.0

    # ------------------------------------------------- #
    # --- [3] interpolate regen.nodes               --- #
    # ------------------------------------------------- #
    
    #  -- [3-1] load regen.nodes  -- #
    inpFile = "dat/regen.nodes"
    with open( inpFile, "r" ) as f:
        rData = np.loadtxt( f )
    nodes  = np.copy( rData[:,2:] )
    points = np.copy( grid )
    
    #  -- [3-2] barycentric__interpolation  -- #    
    import nkInterpolator.barycentric__interpolator as bry
    ret = bry.barycentric__interpolator( nodes=nodes, points=points )
    
    # ------------------------------------------------- #
    # --- [4] regen coordinates making              --- #
    # ------------------------------------------------- #
    Data        = np.zeros( (nData,6) )
    Data[:,x_]  = grid[:,x_]
    Data[:,y_]  = grid[:,y_]
    Data[:,z_]  = ret [:,z_]
    Data[:,i_]  = ret [:,z_]
    Data[:,s_]  = 0.0
    Data[:,f_]  = flags

    # ------------------------------------------------- #
    # --- [5] save in File                          --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/regen_shape.dat"
    spf.save__pointFile( outFile=outFile, Data=Data, shape=(const["LI"]-1,const["LJ"]-1,6) )

    # ------------------------------------------------- #
    # --- [6] output figure for check               --- #
    # ------------------------------------------------- #
    import nkUtilities.cMapTri as cmt
    pngFile = "png/flag.png"
    cmt.cMapTri( xAxis=Data[:,x_], yAxis=Data[:,y_], cMap=Data[:,f_], pngFile=pngFile )
    pngFile = "png/init.png"
    cmt.cMapTri( xAxis=Data[:,x_], yAxis=Data[:,y_], cMap=Data[:,i_], pngFile=pngFile )
    


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    import nkUtilities.genArgs as gar
    args    = gar.genArgs()
    make__regenShapeFile()
    
