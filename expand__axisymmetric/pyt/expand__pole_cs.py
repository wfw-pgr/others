import numpy as np
import nkBasicAlgs.expand__axisymmetric as axi

# ========================================================= #
# ===  expand__pole_cs                                  === #
# ========================================================= #

def expand__pole_cs( inpFile=None, outFile=None ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): inpFile = "dat/pole_cs.dat"
    if ( outFile is None ): outFile = "dat/gridData.dat"
    cnsFile = "dat/expand.conf"
    import nkUtilities.load__constants as lcn
    const   = lcn.load__constants( inpFile=cnsFile )
    
    # ------------------------------------------------- #
    # --- [2] Load Settings                         --- #
    # ------------------------------------------------- #

    x1MinMaxNum = const["x1MinMaxNum"]
    x2MinMaxNum = const["x2MinMaxNum"]
    radius      = const["radius"]

    with open( inpFile, "r" ) as f:
        pole    = np.loadtxt( f )

    ra          = pole[:,0]
    fa          = pole[:,2]

    # ------------------------------------------------- #
    # --- [3] expand rz Profile >> axi-symmetric    --- #
    # ------------------------------------------------- #

    ret         = axi.expand__axisymmetric( ra=ra, fa=fa, radius=radius, \
                                            x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum )

    # ------------------------------------------------- #
    # --- [4] save result                           --- #
    # ------------------------------------------------- #

    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=outFile, Data=ret )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    sample      = np.zeros( (101,3) )
    sample[:,0] = np.linspace( 0.0, 1.0, 101 )
    sample[:,2] = np.cos( sample[:,0] * np.pi * 0.5 ) ** 2

    import nkUtilities.save__pointFile as spf
    sampleFile  = "dat/pole_cs.dat"
    gridFile    = "dat/gridData.dat"
    spf.save__pointFile( outFile=sampleFile, Data=sample )
    
    expand__pole_cs( inpFile=sampleFile, outFile=gridFile )


    with open( gridFile, "r" ) as f:
        Data = np.loadtxt( f )

    import nkUtilities.cMapTri as cmt
    print( Data )
    cmt.cMapTri( xAxis=Data[:,0], yAxis=Data[:,1], cMap=Data[:,2] )
