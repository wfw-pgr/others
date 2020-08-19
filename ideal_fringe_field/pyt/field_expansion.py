import numpy as np

# ========================================================= #
# ===  field_expansion                                  === #
# ========================================================= #

def field_expansion():

    # ------------------------------------------------- #
    # --- [1] load data                             --- #
    # ------------------------------------------------- #
    #  -- [1-1] Load parameter file                 --  #
    import nkUtilities.load__constants as lcn
    inpFile = "dat/parameter.conf"
    params  = lcn.load__constants( inpFile=inpFile )
    
    #  -- [1-2] Load field file                     --  #
    import nkUtilities.load__pointFile as lpf
    inpFile = "dat/extended_idealField.dat"
    data2d  = lpf.load__pointFile( inpFile=inpFile, returnType="structured" )
    bz      = np.copy( data2d[:,:,3] )

    # ------------------------------------------------- #
    # --- [2] calculate derivative                  --- #
    # ------------------------------------------------- #
    
    dx      = ( ( params["xMax"] - params["xMin"] ) / float( params["LI"]-1 ) )
    dy      = ( ( params["yMax"] - params["yMin"] ) / float( params["LJ"]-1 ) )
    dz      = ( ( params["zMax"] - params["zMin"] ) / float( params["LK"]-1 ) )
    dxInv   = 1.0 / dx
    dyInv   = 1.0 / dy
    dzInv   = 1.0 / dz
    
    dbzdx   = ( np.roll( bz, +1, axis=1 ) - np.roll( bz,-1,axis=1 )          ) * dxInv * 0.5
    dbzdy   = ( np.roll( bz, +1, axis=0 ) - np.roll( bz,-1,axis=0 )          ) * dyInv * 0.5
    d2bzdx2 = ( np.roll( bz, +1, axis=1 ) + np.roll( bz,-1,axis=1 ) - 2.0*bz ) * dxInv**2
    d2bzdy2 = ( np.roll( bz, +1, axis=0 ) + np.roll( bz,-1,axis=0 ) - 2.0*bz ) * dyInv**2
    d2bzdz2 = - d2bzdx2 - d2bzdy2
    
    # ------------------------------------------------- #
    # --- [3] euler integral                        --- #
    # ------------------------------------------------- #

    x_,y_,z_ = 0, 1, 2
    b3d      = np.zeros( (params["LK"],params["LJ"],params["LI"],3) )
    n_kplus  = int( ( params["LK"]-1 ) / 2 )
    kmid     = int( ( params["LK"]-1 ) / 2 )
    
    b3d[kmid,:,:,x_] = 0.0
    b3d[kmid,:,:,y_] = 0.0
    b3d[kmid,:,:,z_] = bz

    for ik in range( 1, n_kplus+1 ):
        b3d[kmid+ik,:,:,x_] =            dbzdx   *   float(ik)*dz
        b3d[kmid+ik,:,:,y_] =            dbzdy   *   float(ik)*dz
        b3d[kmid+ik,:,:,z_] = bz + 0.5 * d2bzdz2 * ( float(ik)*dz )**2
    for ik in range( 1, n_kplus+1 ):
        b3d[kmid-ik,:,:,x_] = - b3d[kmid+ik,:,:,x_]
        b3d[kmid-ik,:,:,y_] = - b3d[kmid+ik,:,:,y_]
        b3d[kmid-ik,:,:,z_] = + b3d[kmid+ik,:,:,z_]

    # ------------------------------------------------- #
    # --- [4] edge care                             --- #
    # ------------------------------------------------- #
    #  -- [4-1] copy edge                           --  #
    b3d[:, 0, :,:] = b3d[:, 1, :,:]
    b3d[:,-1, :,:] = b3d[:,-2, :,:]
    b3d[:, :, 0,:] = b3d[:, :, 1,:]
    b3d[:, :,-1,:] = b3d[:, :,-2,:]
    
    # ------------------------------------------------- #
    # --- [5] save in file                          --- #
    # ------------------------------------------------- #
    
    #  -- [5-1]  save as .dat file                  --  #
    x_,y_,z_,bx_,by_,bz_ = 0, 1, 2, 3, 4, 5
    Data                 = np.zeros( (params["LK"],params["LJ"],params["LI"],6) )

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ params["xMin"], params["xMax"], params["LI"] ]
    x2MinMaxNum = [ params["yMin"], params["yMax"], params["LJ"]  ]
    x3MinMaxNum = [ params["zMin"], params["zMax"], params["LK"]  ]
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    Data[:,:,:, x_]       = ret[:,:,:,x_]
    Data[:,:,:, y_]       = ret[:,:,:,y_]
    Data[:,:,:, z_]       = ret[:,:,:,z_]
    Data[:,:,:,bx_]       = b3d[:,:,:,x_]
    Data[:,:,:,by_]       = b3d[:,:,:,y_]
    Data[:,:,:,bz_]       = b3d[:,:,:,z_]
    
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/out.dat"
    names     = ["xp","yp","zp","bx","by","bz"]
    spf.save__pointFile( outFile=outFile, Data=Data, shape=Data.shape, names=names )
    
    #  -- [5-2]  save as .png file                  --  #
    import nkUtilities.cMapTri as cmt
    for ik in range( params["LK"] ):
        hData = np.reshape( Data[ik,:,:,:], ( -1,6 ) )
        cmt.cMapTri( xAxis=hData[:,x_], yAxis=hData[:,y_], cMap=hData[:,bx_], \
                     pngFile="png/bx_k={0}.png".format( ik ) )
        cmt.cMapTri( xAxis=hData[:,x_], yAxis=hData[:,y_], cMap=hData[:,by_], \
                     pngFile="png/by_k={0}.png".format( ik ) )
        cmt.cMapTri( xAxis=hData[:,x_], yAxis=hData[:,y_], cMap=hData[:,bz_], \
                     pngFile="png/bz_k={0}.png".format( ik ) )
    

    
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    field_expansion()
