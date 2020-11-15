import os, sys
import numpy                    as np
import scipy.interpolate        as itp
import nkUtilities.load__config as lcf
import nkUtilities.plot1D       as pl1
import nkUtilities.save__pointFile as spf

# ========================================================= #
# ===  draw__basicshape                                 === #
# ========================================================= #

class draw__basishape():

    # ------------------------------------------------- #
    # --- [1] initialize                            --- #
    # ------------------------------------------------- #

    def __init__( self ):

        self.lines          = []
        self.DataCollection = []
        self.line           = None
        self.pngFile        = "png/line.png"
        self.outFile        = "dat/line.dat"
        self.config         = lcf.load__config()
        self.eps            = 1.e-8


    # ------------------------------------------------- #
    # --- [2] draw straight line                    --- #
    # ------------------------------------------------- #

    def draw__straightline( self, xpt1, xpt2, nDiv ):

        x_,y_,z_ = 0, 1, 2

        # -- [2-1] line generation     -- #
        line       = np.zeros( ( nDiv, 3 ) )
        line[:,x_] = np.linspace( xpt1[x_], xpt2[x_], nDiv )
        line[:,y_] = np.linspace( xpt1[y_], xpt2[y_], nDiv )
        line[:,z_] = np.linspace( xpt1[z_], xpt2[z_], nDiv )
        
        # -- [2-2] append to the lines -- #
        self.lines.append( line )

        # -- [2-3] xpt1, xpt2 => store -- #
        data = np.concatenate( ( np.reshape( xpt1, (1,3) ), \
                                 np.reshape( xpt2, (1,3) ) ), axis=0 )
        self.DataCollection.append( data )

        
    # ------------------------------------------------- #
    # --- [3] draw arc line                         --- #
    # ------------------------------------------------- #
    # -------------------------------- #
    # -- for xy plane :: theta = 90 -- #
    # -- for yz plane :: phi   = 90 -- #
    # -- for xz plane :: phi   =  0 -- #
    # -------------------------------- #
    def draw__arcline( self, xcnt, radius, th1, th2, ph1, ph2, nDiv ):

        x_,y_,z_ = 0, 1, 2

        # -- [3-1] line generation     -- #
        line       = np.zeros( ( nDiv, 3 ) )
        theta      = np.linspace( th1, th2, nDiv ) * np.pi / 180.0
        phi        = np.linspace( ph1, ph2, nDiv ) * np.pi / 180.0
        line[:,x_] = xcnt[x_] + radius*np.sin( theta )*np.cos( phi )
        line[:,y_] = xcnt[y_] + radius*np.sin( theta )*np.sin( phi )
        line[:,z_] = xcnt[z_] + radius*np.cos( theta )
        
        # -- [3-2] append to the lines -- #
        self.lines.append( line )

        # -- [3-3] End point  => store -- #
        data = np.concatenate( ( np.reshape( line[ 0,:], (1,3) ), \
                                 np.reshape( line[-1,:], (1,3) ) ), axis=0 )
        self.DataCollection.append( data )

        
    # ------------------------------------------------- #
    # --- [4] draw spline series                    --- #
    # ------------------------------------------------- #

    def draw__spline( self, Data, nDiv, close=False ):

        x_,y_,z_  = 0, 1, 2
        Data      = np.array( Data )
        tied      = False
        self.DataCollection.append( np.copy( Data ) )

        # ------------------------------------------------ #
        # -- Data :: xyz position   : [nData,3]
        # -- nDiv :: new resolution : integer
        # ------------------------------------------------ #
        
        # -- [4-1] check data size        -- #
        if ( Data.shape[1] != 3 ):
            sys.exit( "[draw__spline] Data shape ???    :: {0} ".format( Data.shape ) )
        if ( Data.shape[0] <  3 ):
            sys.exit( "[draw__spline] Data is too small :: {0} ".format( Data.shape ) )

        # -- [4-2] close & tied detection -- #
        if ( np.sqrt( np.sum( ( Data[0,:] - Data[-1,:] )**2 ) ) < self.eps ):
            close = True
            tied  = True
        if ( close is True ):
            if   ( tied is True  ):
                Data_ = np.concatenate( ( Data, Data[1:] ), axis=0 )
            elif ( tied is False ):
                Data_ = np.concatenate( ( Data, Data     ), axis=0 )
        else:
            Data_ = np.copy( Data )    

        # -- [4-3] prepare variables      -- #
        xAxis = Data_[:,x_]
        yAxis = Data_[:,y_]
        zAxis = Data_[:,z_]
        dpar  = np.cumsum( np.sqrt( np.sum( np.diff( Data_, axis=0 )**2, axis=1 ) ) )
        dpar  = np.insert( dpar, 0, 0 ) / dpar[-1]
        if ( close is True ):
            lpar  = np.linspace( 0.25, 0.75, nDiv )
        else:
            lpar  = np.linspace( 0.0 , 1.0 , nDiv ) 
            
        # -- [4-4] interpolation         -- #
        xfunc = itp.interp1d( dpar, xAxis, kind="cubic" )
        yfunc = itp.interp1d( dpar, yAxis, kind="cubic" )
        zfunc = itp.interp1d( dpar, zAxis, kind="cubic" )
        xret  = xfunc( lpar )
        yret  = yfunc( lpar )
        zret  = zfunc( lpar )
        if ( close is True ):
            xret  = np.append( xret, xret[0] )
            yret  = np.append( yret, yret[0] )
            zret  = np.append( zret, zret[0] )
        line  = np.concatenate( ( xret[:,np.newaxis], yret[:,np.newaxis], \
                                  zret[:,np.newaxis] ), axis=1 )
        # -- [4-5] add line to lines     -- #
        self.lines.append( line )


    # ------------------------------------------------- #
    # --- [5] merge line                            --- #
    # ------------------------------------------------- #
    def merge__line( self ):

        # -- [5-1] concatenate lines -- #
        tline = np.zeros( (0,3) )
        for hline in self.lines:
            tline = np.concatenate( ( tline, hline ), axis=0 )

        # -- [5-2] remove duplicates -- #
        tied = False
        if ( np.sqrt( np.sum( ( tline[0,:] - tline[-1,:] )**2 ) ) < self.eps ):
            tied = True
        dist  = np.sqrt( np.sum( np.diff( tline, axis=0 )**2, axis=1 ) )
        tline = tline[ np.where( dist > self.eps ) ]
        if ( tied is True ):
            print( tline.shape, tline[0,:].shape )
            tline = np.concatenate( ( tline, np.reshape( tline[0,:], (1,3) ) ), axis=0 )

        # -- [5-3] data collection   -- #
        self.endPoints = np.concatenate( self.DataCollection, axis=0 )
        
        # -- [5-4] store total line  -- #
        self.line = tline
            
    # ------------------------------------------------- #
    # --- [6] display line                          --- #
    # ------------------------------------------------- #

    def display__line( self ):
        x_, y_, z_ = 0, 1, 2

        # -- xy plane -- #
        fig    = pl1.plot1D( pngFile=self.pngFile, config=self.config )
        fig.add__plot( xAxis=self.line[:,x_]     , yAxis=self.line[:,y_]     , linewidth=0.8 )
        fig.add__plot( xAxis=self.endPoints[:,x_], yAxis=self.endPoints[:,y_], linewidth=0.0, \
                       marker="o" )
        fig.set__axis()
        fig.save__figure()


    # ------------------------------------------------- #
    # --- [7] save in file                          --- #
    # ------------------------------------------------- #

    def save__line( self ):
        spf.save__pointFile( outFile=self.outFile, Data=self.line )


    # ------------------------------------------------- #
    # --- [8] save as vtk file                      --- #
    # ------------------------------------------------- #

    def save__vtkFile( self ):
        

    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    drawer = draw__basishape()

    # -- parameters -- #
    xpt1   = np.array( [ 0.0, 0.0, 0.0 ] )
    xpt2   = np.array( [ 1.0, 1.0, 1.0 ] )
    nDiv   = 101

    xcnt   = np.array( [ 0.0, 0.0, 0.0] )
    radius = 1.0
    th1    = 90.0
    th2    = 90.0
    ph1    = 0.0
    ph2    = 360.0

    Data   = [ [ 0.0, 0.0, 0.0 ], \
               [ 0.3, 0.1, 0.0 ], \
               [ 0.5, 0.2, 0.0 ], \
               [ 0.4, 0.4, 0.0 ], \
               [ 0.3, 0.3, 0.0 ], \
               [ 0.2, 0.3, 0.0 ], \
               [ 0.1, 0.2, 0.0 ], \
               [ 0.0, 0.1, 0.0 ], \
               [ 0.0, 0.0, 0.0 ]  \
    ]

    # -- draw lines -- #

    # drawer.draw__arcline( xcnt, radius, th1, th2, ph1, ph2, nDiv )
    # drawer.draw__straightline( xpt1, xpt2, nDiv )
    drawer.draw__spline( Data, nDiv, close=True )
    
    drawer.merge__line()
    drawer.display__line()
    drawer.save__line()
