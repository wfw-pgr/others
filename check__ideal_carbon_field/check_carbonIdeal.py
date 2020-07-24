import sys
import numpy                      as np
import nkUtilities.LoadConfig     as lcf
import nkUtilities.cMapTri        as cmt
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  check__carbonIdeal                               === #
# ========================================================= #
def check__carbonIdeal( datFile=None, pngFile=None, config=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( config   is None ): config   = lcf.LoadConfig()
    if ( datFile1 is None ): datFile1 = "dat/bfield_from_aoki.dat"
    if ( pngFile1 is None ): pngFile1 = "png/bfield_from_aoki.png"
    if ( datFile2 is None ): datFile2 = "dat/bfield_ideal_acoord.dat"
    if ( pngFile2 is None ): pngFile2 = "png/bfield_ideal_acoord.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    with open( datFile1, "r" ) as f:
        Data1 = np.loadtxt( f )
    xAxis1 = Data1[:,0]
    yAxis1 = Data1[:,1]
    zAxis1 = Data1[:,2]
    
    with open( datFile2, "r" ) as f:
        Data2 = np.loadtxt( f )
    xAxis2 = Data2[:,0]
    yAxis2 = Data2[:,1]
    zAxis2 = Data2[:,2]

    pngFile3 = "png/bfield_error.png"
    xAxis3 = np.copy( xAxis2 )
    yAxis3 = np.copy( yAxis2 )
    zAxis3 = np.copy( zAxis2 ) - np.copy( zAxis1 )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="cMap_def", config=config )
    config["FigSize"]        = (5,5)
    config["cmp_position"]   = [0.16,0.12,0.97,0.88]
    config["xTitle"]         = "X"
    config["yTitle"]         = "Y"
    config["cmp_xAutoRange"] = True
    config["cmp_yAutoRange"] = True
    config["cmp_xRange"]     = [-5.0,+5.0]
    config["cmp_yRange"]     = [-5.0,+5.0]

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    cmt.cMapTri( xAxis=xAxis1, yAxis=yAxis1, cMap=zAxis1, pngFile=pngFile1, config=config )
    cmt.cMapTri( xAxis=xAxis2, yAxis=yAxis2, cMap=zAxis2, pngFile=pngFile2, config=config )
    cmt.cMapTri( xAxis=xAxis3, yAxis=yAxis3, cMap=zAxis3, pngFile=pngFile3, config=config )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    check__carbonIdeal()

