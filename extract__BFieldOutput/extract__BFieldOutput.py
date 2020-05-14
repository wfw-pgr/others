import os, sys, re
import numpy as np

# ========================================================= #
# ===  extract b_integ field from EMSolution .out file  === #
# ========================================================= #

def extract__BFieldOutput( mode=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #

    if ( mode is None ): sys.exit( "[extract__BFieldOutput] mode = ??? " )
    
    inpFile = "out/ems_{0}.out"  .format( mode )
    outFile = "out/ems_{0}.field".format( mode )

    # ------------------------------------------------- #
    # --- [2] search by regular expression          --- #
    # ------------------------------------------------- #
    
    with open( inpFile, "r" ) as f:
        lines = f.readlines()

    pattern = r"B by v_element integration"

    for iL, line in enumerate( lines ):
        research = re.search( pattern, line )
        if ( research ): break

    # ------------------------------------------------- #
    # --- [3] write Data in outFile :: middle File  --- #
    # ------------------------------------------------- #

    lines = lines[(iL+4):]
    with open( outFile, "w" ) as f:
        f.write( "# " + lines[0] )
        for line in lines[1:]:
            if ( len( line.split() ) == 8 ):
                f.write( line )
            else:
                break
        print( "[extract__BFieldOutput] output :: {0}".format( outFile ) )
            
    # ------------------------------------------------- #
    # --- [4] write Data without index & abs value  --- #
    # ------------------------------------------------- #

    with open( outFile, "r" ) as f:
        Data = np.loadtxt( f )
        
    import nkUtilities.save__pointFile as spf
    spf.save__pointFile( outFile=outFile, Data=Data )

        
# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    import nkUtilities.genArgs as gar
    args = gar.genArgs()
    
    extract__BFieldOutput( mode=args["mode"] )
