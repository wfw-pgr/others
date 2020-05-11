import numpy as np


# ========================================================= #
# ===  generate__discrete_shimShape                     === #
# ========================================================= #

def generate__discrete_shimShape():

    # ------------------------------------------------- #
    # --- [1] parameters                            --- #
    # ------------------------------------------------- #
    
    rMin_  = 0.60
    rMax_  = 0.70
    nDiv_  = 10
    zMin_  = 0.010
    zMax_  = 0.060
    nr_    = 1
    nz_    = 10
    Mz_    = 2.07
    ul_    = 1.0
    idx_   = 0.4

    # ------------------------------------------------- #
    # --- [2] make Fe Data                          --- #
    # ------------------------------------------------- #
    
    rNode  = np.linspace( rMin_, rMax_, nDiv_+1 )

    FeList = []
    for ik in range( nDiv_ ):
        unit = {}
        unit["rMin"] = rNode[ik  ]
        unit["rMax"] = rNode[ik+1]
        rhat         = ( 0.5 * ( unit["rMin"] + unit["rMax"] ) - rMin_ ) / ( rMax_ - rMin_ )
        unit["zMin"] = ( zMin_-zMax_ ) * rFunc( rhat ) + zMax_
        unit["zMax"] = zMax_
        unit["nr"]   = nr_
        unit["nz"]   = nz_
        unit["Mz"]   = Mz_
        unit["ul"]   = ul_
        unit["idx"]  = idx_
        FeList.append( unit )

    # ------------------------------------------------- #
    # --- [3] save in file                          --- #
    # ------------------------------------------------- #
        
    keys    = ["rMin","rMax","zMin","zMax","nr","nz","Mz","ul","idx"]
    outFile = "FeList.dat"
    with open( outFile, "w" ) as f:
        for ik,unit in enumerate( FeList ):
            f.write( "# ife == {0}\n".format( ik ) )
            for key in keys:
                f.write( "{0:<20}   {1:5}\n".format( unit[key], key ) )
        
    print( "[generate__discrete_shimShape] output :: {0} ".format( outFile ) )


    
# ========================================================= #
# ===  Function of r ( R(r) )                           === #
# ========================================================= #
def rFunc( rhat ):
    ret  = ( np.sin( rhat*np.pi ) )**2
    return( ret )
    

# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    generate__discrete_shimShape()
