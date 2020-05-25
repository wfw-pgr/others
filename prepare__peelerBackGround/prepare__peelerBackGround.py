import numpy as np

# ========================================================= #
# ===  prepare peelerBackGround Field                   === #
# ========================================================= #

def prepare__peelerBackGround():

    # ------------------------------------------------- #
    # --- [1] Load Data                             --- #
    # ------------------------------------------------- #
    
    inpFile_wo = "out/ems_shm_wo.field"
    inpFile_wp = "out/ems_shm_wp.field"
    outFile    = "out/ems_peeler.field"
    
    with open( inpFile_wo, "r" ) as f:
        Data_wo = np.loadtxt( f )
    with open( inpFile_wp, "r" ) as f:
        Data_wp = np.loadtxt( f )

    # ------------------------------------------------- #
    # --- [2] coordinate consitency                 --- #
    # ------------------------------------------------- #
        
    eps  = 1.e-5
    dist = np.mean( np.sqrt( ( Data_wo[:,0] - Data_wp[:,0] )**2 + ( Data_wo[:,1] - Data_wp[:,1] )**2 ) )
    if ( dist > eps ):
        print( "[prepare__peelerBackGround] abnormal dist detected :: {0} :: [ERROR] ".format( dist ) )
        sys.exit()

    # ------------------------------------------------- #
    # --- [3] obtain peeler field components        --- #
    # ------------------------------------------------- #
        
    Data      = np.zeros( (Data_wp.shape[0],6) )
    Data[:,0] = Data_wp[:,0]
    Data[:,1] = Data_wp[:,1]
    Data[:,2] = Data_wp[:,2]
    Data[:,3] = Data_wp[:,3] - Data_wo[:,3]
    Data[:,4] = Data_wp[:,4] - Data_wo[:,4]
    Data[:,5] = Data_wp[:,5] - Data_wo[:,5]

    # ------------------------------------------------- #
    # --- [4] save in File                          --- #
    # ------------------------------------------------- #
    
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=outFile, Data=Data )


    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    prepare__peelerBackGround()
