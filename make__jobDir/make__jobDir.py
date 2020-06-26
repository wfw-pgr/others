import os, sys, subprocess

# ========================================================= #
# ===  make__jobDir                                     === #
# ========================================================= #

def make__jobDir( job=None ):
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( job     is None ): sys.exit( "[make__jobDir] job     == ???" )

    # ------------------------------------------------- #
    # --- [2] make directories                      --- #
    # ------------------------------------------------- #

    mkdir_cmd = "mkdir -p {0}"
    mdtRoot   = "/mnt/f/kent/mdt2/"
    jobDir    = mdtRoot + "job/" + job + "/"
    
    cmd1      = mkdir_cmd.format( jobDir         )
    cmd2      = mkdir_cmd.format( jobDir + "cnf" )
    cmd3      = mkdir_cmd.format( jobDir + "dat" )
    cmd4      = mkdir_cmd.format( jobDir + "ems" )
    cmd5      = mkdir_cmd.format( jobDir + "png" )
    cmd6      = mkdir_cmd.format( jobDir + "msh" )
    print( cmd1 ) 
    print( cmd2 ) 
    print( cmd3 ) 
    print( cmd4 ) 
    print( cmd5 ) 
    print( cmd6 )
    subprocess.call( cmd1.split()  )
    subprocess.call( cmd2.split()  )
    subprocess.call( cmd3.split()  )
    subprocess.call( cmd4.split()  )
    subprocess.call( cmd5.split()  )
    subprocess.call( cmd6.split()  )

    print( "[make__jobDir] job directories is made..." )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    import nkUtilities.genArgs as gar
    args    = gar.genArgs()
    make__jobDir( job=args["job"] )
