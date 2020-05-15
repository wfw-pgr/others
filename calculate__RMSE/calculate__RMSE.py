import numpy as np

# ========================================================= #
# ===  calculate RMSE and other statistics              === #
# ========================================================= #

def calculate__RMSE( num=None ):

    # ------------------------------------------------- #
    # --- [1] preparation                           --- #
    # ------------------------------------------------- #
    wData   = np.zeros( (num,2) )
    inpFile = "out/b_on_fov_{0:02}.out"
    outFile = "dat/rmse.dat"
    
    for ik in range( num ):
        with open( inpFile.format(ik+1), "r" ) as f:
            Data = np.loadtxt( f )
        error = Data[:,2] - Data[:,4]
        RMSE  = np.sqrt( np.mean( error**2 ) )

        wData[ik,:] = np.array( [ik+1,RMSE] )
        
    with open( outFile, "w" ) as f:
        np.savetxt( f, wData )

    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):
    import nkUtilities.genArgs as gar
    args    = gar.genArgs()
    calculate__RMSE( num=args["integer"] )
