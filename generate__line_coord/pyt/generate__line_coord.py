import numpy as np

# ========================================================= #
# ===  generate__line_coord                             === #
# ========================================================= #

def generate__line_coord():

    # ------------------------------------------------- #
    # --- [1] load parameter                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    const = lcn.load__constants( inpFile="dat/parameter.conf" )

    # ------------------------------------------------- #
    # --- [2] generate radial line                  --- #
    # ------------------------------------------------- #
    rval  = np.linspace( const["r1"], const["r2"], const["nData"] )
    angle = const["theta"] / 360.0 * 2.0 * np.pi
    xg    = np.cos( angle ) * rval
    yg    = np.sin( angle ) * rval
    zg    = np.zeros( ( const["nData"], ) )

    Data  = np.concatenate( [ arr[:,np.newaxis] for arr in (xg,yg,zg) ], axis=-1 )

    # ------------------------------------------------- #
    # --- [3] save in file                          --- #
    # ------------------------------------------------- #
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/out.dat"
    spf.save__pointFile( outFile=outFile, Data=Data )
    
    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    generate__line_coord()
