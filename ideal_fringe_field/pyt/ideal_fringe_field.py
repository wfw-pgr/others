import os, sys
import numpy as np


# ========================================================= #
# ===  ideal_fringe_field                               === #
# ========================================================= #

def ideal_fringe_field():

    # ------------------------------------------------- #
    # --- [1] parameter settings                    --- #
    # ------------------------------------------------- #
    #  -- [1-1] Load parameter file                 --  #
    import nkUtilities.load__constants as lcn
    inpFile = "dat/parameter.conf"
    params  = lcn.load__constants( inpFile=inpFile )
    
    # ------------------------------------------------- #
    # --- [2] grid making                           --- #
    # ------------------------------------------------- #

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ params["xMin"], params["xMax"], params["LI"] ]
    x2MinMaxNum = [ params["yMin"], params["yMax"], params["LJ"] ]
    x3MinMaxNum = [            0.0,            0.0,            1 ]
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    radii       = np.sqrt( ret[:,0]**2 + ret[:,1]**2 )
    xg          = np.copy( ret[:,0] )
    yg          = np.copy( ret[:,1] )
    zg          = np.copy( ret[:,2] )
    bz          = np.copy( ret[:,2] ) * 0.0
    
    # ------------------------------------------------- #
    # --- [3] ideal aoki main field                 --- #
    # ------------------------------------------------- #
    index       = np.where( radii <= params["r_main"] )
    radii_h     = radii[index]
    bz[index]   = mainAokiField( radii_h, params=params )
    
    # ------------------------------------------------- #
    # --- [4] buffer field                          --- #
    # ------------------------------------------------- #
    index       = np.where( ( radii > params["r_main"] ) & ( radii < params["r_fringe"] ) )
    rh          = radii[index]
    xh          = xg[index]
    yh          = yg[index]
    nBuff       = xh.shape[0]
    theta       = np.arctan2( yh, xh )
    r1, r2, r3  = params["r_main"], params["r_main"] - params["r_delta"], params["r_main"] - 2.0*params["r_delta"]
    xp1, yp1    = r1*np.cos( theta ), r1*np.sin( theta )
    xp2, yp2    = r2*np.cos( theta ), r2*np.sin( theta )
    xp3, yp3    = r3*np.cos( theta ), r3*np.sin( theta )
    bp1         = mainAokiField( np.sqrt( xp1**2 + yp1**2 ), params=params )
    bp2         = mainAokiField( np.sqrt( xp2**2 + yp2**2 ), params=params )
    bp3         = mainAokiField( np.sqrt( xp3**2 + yp3**2 ), params=params )
    dbdr_main   = ( bp1 - bp3 ) / params["r_delta"]
    dbdr_fringe = params["fringe_grad"] * np.ones( (nBuff,) )
    b_fringe_edge = np.ones( (nBuff) ) * params["fringe_fixed"]

    rhat          = ( rh - r2 ) / ( params["r_fringe"] - r2 )
    delta_main    =   rh - r2
    delta_fringe  =   rh - params["r_fringe"]
    
    approx_main   = linear_approx( delta_main  , dbdr_main  , bp2           )
    approx_fringe = linear_approx( delta_fringe, dbdr_fringe, b_fringe_edge )
    rate_main     = rateFunc_main  ( rhat )
    rate_fringe   = rateFunc_fringe( rhat )

    
    bz_buffer     = rate_main * approx_main + rate_fringe * approx_fringe
    bz[index]     = np.copy( bz_buffer )

    
    # ------------------------------------------------- #
    # --- [5] main fringe field                     --- #
    # ------------------------------------------------- #
    index       = np.where( radii >= params["r_fringe"] )
    radii_h     = radii[index]
    bz[index]   = mainFringeField( radii_h, params=params ) 

    # ------------------------------------------------- #
    # --- [6] output field                          --- #
    # ------------------------------------------------- #
    #  -- [6-1] save in file                        --  #
    ret         = np.zeros( (bz.shape[0],4) )
    ret[:,0]    = np.copy( xg )
    ret[:,1]    = np.copy( yg )
    ret[:,2]    = np.copy( zg )
    ret[:,3]    = np.copy( bz )
    shape       = ( params["LJ"], params["LI"], 4 )
    ret_        = np.reshape( ret, shape )
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/extended_idealField.dat"
    spf.save__pointFile( outFile=outFile, Data=ret_, shape=shape )

    #  -- [6-2] 2d color map                        --  #
    import nkUtilities.cMapTri as cmt
    cmt.cMapTri( xAxis=ret[:,0], yAxis=ret[:,1], cMap=ret[:,3], pngFile="png/out.png" )

    import nkBasicAlgs.extract__data_onAxis as ext
    onXAxis = ext.extract__data_onAxis( Data=ret, axis="y" )
    onYAxis = ext.extract__data_onAxis( Data=ret, axis="x" )
    
    import nkUtilities.plot1D     as pl1
    import nkUtilities.LoadConfig as lcf
    config  = lcf.LoadConfig()
    config["plt_linewidth"] = 0.0
    config["plt_marker"]    = "x"
    
    #  -- [6-3] 1d plot (x)                         --  #
    xAxis   = onXAxis[:,0]
    bAxis   = onXAxis[:,3]
    xAxis1  = xAxis[ np.where( np.abs( xAxis ) <= params["r_main"] ) ]
    bAxis1  = bAxis[ np.where( np.abs( xAxis ) <= params["r_main"] ) ]
    xAxis2  = xAxis[ np.where( ( np.abs( xAxis ) > params["r_main"] )  & ( np.abs( xAxis ) < params["r_fringe"] ) ) ]
    bAxis2  = bAxis[ np.where( ( np.abs( xAxis ) > params["r_main"] )  & ( np.abs( xAxis ) < params["r_fringe"] ) ) ]
    xAxis3  = xAxis[ np.where( np.abs( xAxis ) >= params["r_fringe"] ) ]
    bAxis3  = bAxis[ np.where( np.abs( xAxis ) >= params["r_fringe"] ) ]
    
    pngFile = "png/onXAxis.png"
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=xAxis1, yAxis=bAxis1, label="main"   )
    fig.add__plot( xAxis=xAxis2, yAxis=bAxis2, label="buffer" )
    fig.add__plot( xAxis=xAxis3, yAxis=bAxis3, label="fringe" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    #  -- [6-4] 1d plot (y)                         --  #
    yAxis   = onYAxis[:,1]
    bAxis   = onYAxis[:,3]
    yAxis1  = yAxis[ np.where( np.abs( yAxis ) <= params["r_main"] ) ]
    bAxis1  = bAxis[ np.where( np.abs( yAxis ) <= params["r_main"] ) ]
    yAxis2  = yAxis[ np.where( ( np.abs( yAxis ) > params["r_main"] )  & ( np.abs( yAxis ) < params["r_fringe"] ) ) ]
    bAxis2  = bAxis[ np.where( ( np.abs( yAxis ) > params["r_main"] )  & ( np.abs( yAxis ) < params["r_fringe"] ) ) ]
    yAxis3  = yAxis[ np.where( np.abs( yAxis ) >= params["r_fringe"] ) ]
    bAxis3  = bAxis[ np.where( np.abs( yAxis ) >= params["r_fringe"] ) ]

    pngFile = "png/onYAxis.png"
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=yAxis1, yAxis=bAxis1, label="main"   )
    fig.add__plot( xAxis=yAxis2, yAxis=bAxis2, label="buffer" )
    fig.add__plot( xAxis=yAxis3, yAxis=bAxis3, label="fringe" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()

    return()



# ========================================================= #
# ===  mainFringeField                                  === #
# ========================================================= #

def mainFringeField( radii, params=None ):
    ret = ( radii - params["r_fringe"] ) * params["fringe_grad"] + params["fringe_fixed"]
    return( ret )


# ========================================================= #
# ===  mainFringeField                                  === #
# ========================================================= #

def mainAokiField( radii, params=None ):
    Bcent = - 4.00
    Bedge = - 3.95
    rcent =   0.00
    redge = params["r_main"]
    
    rhat  = ( radii - rcent ) / ( redge - rcent )
    ret   = ( Bcent - Bedge ) * np.cos( rhat * np.pi*0.5 )**2 + Bedge
    return( ret )


# ========================================================= #
# ===  rate Function for main                           === #
# ========================================================= #

def rateFunc_main( rhat ):
    ret = np.cos( rhat * 0.5 * np.pi )**2
    return( ret )


# ========================================================= #
# ===  rate Function for fringe                         === #
# ========================================================= #

def rateFunc_fringe( rhat ):
    ret = np.sin( rhat * 0.5 * np.pi )**2
    return( ret )


# ========================================================= #
# ===  linear approximation                             === #
# ========================================================= #

def linear_approx( delta, dydx, y0 ):
    ret = dydx * delta + y0
    return( ret )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    ideal_fringe_field()
