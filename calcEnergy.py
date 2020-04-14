import numpy as np

# ========================================================= #
# ===  calcEnergy                                       === #
# ========================================================= #
def calcEnergy():

    # ------------------------------------------------- #
    # --- [1] input parameter                       --- #
    # ------------------------------------------------- #

    inpFile = "dat/slotRegionBField.dat"
    outFile = "result.dat"
    LI      = 25
    LJ      = 66
    mu0     = 4.0 * np.pi * 1.e-7
    
    # ------------------------------------------------- #
    # --- [2] summation                             --- #
    # ------------------------------------------------- #
    
    #  -- [2-1] Load Data                           --  #
    with open( inpFile, "r" ) as f:
        Data = np.loadtxt( f )
    xAxis = np.reshape( Data[:,1], (LJ,LI) )
    yAxis = np.reshape( Data[:,2], (LJ,LI) )
    zAxis = np.reshape( Data[:,3], (LJ,LI) )
    bx    = np.reshape( Data[:,4], (LJ,LI) )
    by    = np.reshape( Data[:,5], (LJ,LI) )
    bz    = np.reshape( Data[:,6], (LJ,LI) )
    
    #  -- [2-2] rAxis                               --  #
    rAx_  = np.sqrt( xAxis**2 + yAxis**2 )
    rAxis = 
    dr    = rAxis[0,1] - rAxis[0,0]
    dz    = zAxis[1,0] - zAxis[0,0]
    dvol  = 2.0 * np.pi * rAxis * dr * dz
    coef  = 1.0 / ( 2.0*mu0 )
    Uem   = np.sqrt( bx**2 + by**2 + bz**2 ) * coef * dvol

    

# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    calcEnergy()
