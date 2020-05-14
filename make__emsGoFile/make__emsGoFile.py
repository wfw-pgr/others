import os, sys
import nkUtilities.genArgs as gar

# ------------------------------------------------- #
# --- [1] prepare Arguments                     --- #
# ------------------------------------------------- #
# :: use  --mode & --job :: #
args = gar.genArgs()
mode = args["mode"]
job  = args["job"]
if ( mode is None ): sys.exit( "[make_goFile] --mode is None [ERROR]" )
if ( job  is None ): sys.exit( "[make_goFile] --job  is None [ERROR]" )

# ------------------------------------------------- #
# --- [2] Load File                             --- #
# ------------------------------------------------- #
if   ( mode in ["slv"            ] ):
    inpFile = "ref/ems_slv.go"
elif ( mode in ["pst","shm","lin"] ):
    inpFile = "ref/ems_pst.go"

with open( inpFile, "r" ) as f:
    goContents = f.read()

# ------------------------------------------------- #
# --- [3] modify file contents                  --- #
# ------------------------------------------------- #
goContents_ = goContents.format( job, mode )

# ------------------------------------------------- #
# --- [4] write out contents                    --- #
# ------------------------------------------------- #

outFile = "./ems_{0}.go".format( mode )

with open( outFile, "w" ) as f:
    f.write( goContents_ )


