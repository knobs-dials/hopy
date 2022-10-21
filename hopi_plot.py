import matplotlib
from matplotlib import pyplot

import hopy


if __name__ == '__main__':
    try:
        import serial
    except ImportError as ie:
        print("Error importing pyserial.  You may want to do:  pip3 install pyserial")

    fig = pyplot.figure( figsize=(14, 8) )  # decent chunk of a modern screen

    simple = False # TODO: put on parameter

    if simple:
        axis_power          = fig.add_subplot(3,1, 1)  
        axis_current        = fig.add_subplot(3,1, 2)  
        axis_pf             = fig.add_subplot(3,1, 3)  
    else:
        axis_power          = fig.add_subplot(3,2, 1)  
        axis_current        = fig.add_subplot(3,2, 2)  
        axis_pf             = fig.add_subplot(3,2, 3)  
        axis_volts          = fig.add_subplot(3,2, 5)
        axis_freq           = fig.add_subplot(3,2, 6)  

    all_axes = [axis_current, axis_pf, axis_power]
    if not simple:
        all_axes.extend( [axis_volts, axis_freq] )

    fig.canvas.manager.set_window_title('HOPI readout')

    stop = False
    def stop_soon(_):
        global stop
        stop = True
    fig.canvas.mpl_connect('close_event', stop_soon) # roughly to ensure we close the program (and don't hold up the serial port)

    first = True

    pyplot.ion()
    pyplot.show()

    data_time  = []
    data_current, data_volts, data_pf, data_freq, data_power = [], [], [], [], []

    hopi = hopy.Hopi(verbose=False) # defaults to look for CH340s
    while not stop:
        hopi.read_all()
        #print(hopi.regs)

        last_points = 300 # approx 5 mins

        data_current.append( hopi.regs[1] )
        data_current = data_current[-last_points:]
        axis_current.cla()
        axis_current.plot( data_current )
        axis_current.title.set_text('Current')
        axis_current.set_ylabel('A')
        axis_current.set_ylim( 0, max(0.1, 1.1*max(data_current)) )  # TODO: adaptive
        axis_current.text( x=len(data_current)-1,  y=data_current[-1],  s='%.1f mA'%(1000.*data_current[-1]),  fontdict={'size':16} )

        data_pf.append( hopi.regs[4])
        data_pf = data_pf[-last_points:]
        axis_pf.cla()
        axis_pf.plot( data_pf )
        axis_pf.title.set_text('Power factor')
        axis_pf.set_ylim( 0, 1.05 )
        axis_pf.text( x=len(data_pf)-1,  y=data_pf[-1],  s='%.2f'%data_pf[-1],  fontdict={'size':16}  )

        data_power.append( hopi.regs[0] )
        data_power = data_power[-last_points:]
        axis_power.cla()
        axis_power.plot( data_power)
        axis_power.title.set_text('Real power')
        axis_power.set_ylabel('W')
        axis_power.set_ylim( 0, max(25, 1.1* max(data_power)) )  # TODO: adaptive
        axis_power.text( x=len(data_power)-1,  y=data_power[-1],  s='%.1f W'%data_power[-1],  fontdict={'size':16}  )

        if not simple:
            data_volts.append( hopi.regs[2])
            data_volts = data_volts[-last_points:]
            axis_volts.cla()
            axis_volts.plot( data_volts )
            axis_volts.title.set_text('Mains voltage')
            axis_volts.set_ylabel('V')
            axis_volts.set_ylim( 215, 250 ) 
            #axis_volts.set_ylim( max(220, min(data_volts)),  min(250, max(data_volts)), ) 
            axis_volts.text( x=len(data_volts)-1,  y=data_volts[-1],  s='%.1f V'%data_volts[-1],  fontdict={'size':16}  )

            data_freq.append( hopi.regs[3])
            data_freq = data_freq[-last_points:]
            axis_freq.cla()
            axis_freq.plot( data_freq )
            axis_freq.title.set_text('Mains frequency')
            axis_freq.set_ylabel('Hz')
            axis_freq.set_ylim( 49.9, 50.1 ) 
            axis_freq.text( x=len(data_freq)-1,  y=data_freq[-1],  s='%.3f Hz'%data_freq[-1],  fontdict={'size':16}  )


        for ax in all_axes:
            ax.get_xaxis().set_visible(False) # TODO: meaningful time on that axis
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        if first:
            if simple:
                fig.subplots_adjust(left=0.05, bottom=0.05, right=0.92, top=0.95,  wspace=0.15, hspace=0.15)
            else:
                fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95,  wspace=0.21, hspace=0.15)

            first = False

        pyplot.pause( 0.99 )

    hopi.port.close()

