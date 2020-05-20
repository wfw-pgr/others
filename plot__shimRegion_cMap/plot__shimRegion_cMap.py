import numpy                      as np
import nkUtilities.cMapTri        as cmt


# ========================================================= #
# ===  add__shimRegion_cMap                             === #
# ========================================================= #
def add__shimRegion_cMap( fig=None, r1=1.0, r2=2.0, p1=280.0, p2=320.0 ):

    # ------------------------------------------------- #
    # --- [1] Data points                           --- #
    # ------------------------------------------------- #
    p1    = p1 / 180.0 * np.pi
    p2    = p2 / 180.0 * np.pi
    t     = np.linspace( 0.0, 1.0, 2  )
    p     = np.linspace(  p1,  p2, 51 )
    x1    = np.array( [ r1*np.cos( p1 ), r1*np.sin( p1 ) ] )
    x2    = np.array( [ r2*np.cos( p1 ), r2*np.sin( p1 ) ] )
    x3    = np.array( [ r2*np.cos( p2 ), r2*np.sin( p2 ) ] )
    x4    = np.array( [ r1*np.cos( p2 ), r1*np.sin( p2 ) ] )
    l12_x = ( x2[0]-x1[0] ) * t + x1[0]
    l12_y = ( x2[1]-x1[1] ) * t + x1[1]
    l23_x = r1 * np.cos( p )
    l23_y = r1 * np.sin( p )
    l34_x = ( x4[0]-x3[0] ) * t + x3[0]
    l34_y = ( x4[1]-x3[1] ) * t + x3[1]
    l41_x = r2 * np.cos( p )
    l41_y = r2 * np.sin( p )
    
    # ------------------------------------------------- #
    # --- [2] plot lines                            --- #
    # ------------------------------------------------- #
    fig.add__plot( xAxis=l12_x, yAxis=l12_y )
    fig.add__plot( xAxis=l23_x, yAxis=l23_y )
    fig.add__plot( xAxis=l34_x, yAxis=l34_y )
    fig.add__plot( xAxis=l41_x, yAxis=l41_y )
    return( fig )
    

# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    fig = cmt.cMapTri()
    add__shimRegion_cMap( fig=fig )
    fig.save__figure()
