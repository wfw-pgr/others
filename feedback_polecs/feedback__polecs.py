import sys
import numpy as np


# ========================================================= #
# ===  feedback__polecs                                 === #
# ========================================================= #

def feedback__polecs():

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #

    datFile = "dat/bfield_xAxis.dat"
    pcsFile = "dat/pole_cs.dat"
    outFile = "dat/pole_cs_fb.dat"
    pngFile = "png/pole_cs_fb.png"
    

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #

    with open( datFile, "r" ) as f:
        Data = np.loadtxt( f )
    xAxis = Data[:,3]
    yAxis = Data[:,8]

    with open( pcsFile, "r" ) as f:
        Data = np.loadtxt( f )
    rAxis = Data[:,0]
    zAxis = Data[:,2]
    
    index = np.argsort( xAxis )
    xAxis = xAxis[index]
    yAxis = yAxis[index]

    # ------------------------------------------------- #
    # --- [3] interpolation                         --- #
    # ------------------------------------------------- #

    import nkInterpolator.LinearInterp1D as li1
    ret = li1.LinterInterp1D( xa=xAxis, fa=yAxis, xp=rAxis )

    # ------------------------------------------------- #
    # --- [4] feedback shape                        --- #
    # ------------------------------------------------- #

    bia        = 4.60
    wData      = np.zeros( (rAxis.shape[0],3) )
    wData[:,0] = rAxis
    
    coef       = ( np.copy( ret ) - bia      ) / bia
    addS       = ( Height - np.copy( zAxis ) ) * coef
    wData[:,2] = np.copy( zAxis ) + addS
    
    # ------------------------------------------------- #
    # --- [4] save feedback pole's cross section    --- #
    # ------------------------------------------------- #

    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=outFile, Data=wData )



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    feedback__polecs()
