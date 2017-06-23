### pscp -r Desktop\serial_write.py pi@10.21.113.171:/home/pi/Desktop

import time
import simpy
import serial
import sys

ser = serial.Serial(port='/dev/ttyAMA0',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                    )

class systemHeat():
    def __init__(self, env):
        self.algae_heat = simpy.Container(env, init=5866.8) ### Internal energy of the algae water at 35 degrees (Table).
        self.algae_temp = self.algae_heat.level/167.42 ### Temperature of the algae water (Energy/m*c).
        self.pump_energy = simpy.Container(env, init = 0) ### Total energy supplied by the pump.
        self.wall_temp = simpy.Container(env,init = 25)
        env.process(self.monitor_bottle(env))
        
    def monitor_bottle(self, env):
        while True:
            self.algae_temp = self.algae_heat.level/167.42 ### Temperature of the algae water (Energy/m*c).
            yield env.timeout(1) ### Update temperature every 1 second.

def solarRad(env,systemHeat):
    while True:
        Qsol = 3 ### Solar constant = 3W
        yield env.timeout(1) ### Update energy every 1 second.
        yield systemHeat.algae_heat.put(Qsol) ### Add Qsol to the energy of the algae water.
        print '+%sJ from Solar Radiation'%(round(Qsol,2))

def pumpConv(env,systemHeat):
    while True:
        yield env.timeout(1) ### Update energy every 1 second.
        Qpump = 0.14*0.0047124*((systemHeat.algae_temp-25)/0.002) ### Qpump to the tube = k*A*(dT/dx).
        Epump = 1.5 ### Work on the water from the pump = 1.5W = 1.5J/s.
        yield systemHeat.algae_heat.get(Qpump) ### Subtract Qpump from the energy of the algae water.
        yield systemHeat.pump_energy.put(Epump)
        print str(systemHeat.pump_energy.level)
        print '-%sJ from Pump Convection'%(round(Qpump,2))+'\n'
        minutes,seconds = divmod(env.now, 60)
        print 'Time elapsed: '+str(minutes)+' minutes '+str(seconds)+' seconds'
        print 'Temperature of algae bottle: '+str(systemHeat.algae_temp)+'\n'
        b.write(str(env.now)+' '+
                str(systemHeat.algae_temp)+' '+
                str(systemHeat.algae_heat.level)+'\n')

def wallCond(env,systemHeat):
    while True:
        yield env.timeout(1) ### Update energy every 1 second.
        Qwall = 0.19*0.012896*(systemHeat.algae_temp-25)/0.0015 ### Qwall to the plexiglass wall = lambda*(delta T).
        if Qwall <= 0:
            Qwall = 0.000000001
        yield systemHeat.algae_heat.get(Qwall) ### Subtract Qwall from the energy of the algae water.
        print '-%sJ from Wall Conduction'%(round(Qwall,2))
        
def stat():
    stat = raw_input('Return the value for temp, power, or heat? ')
    statlist = ['temp','power','heat']
    x=True
    while x==True:
        if stat in statlist:
            if stat == statlist[0]:
                print 'Equilibrium Temperature: '+str(s.algae_temp)+'K'
            elif stat == statlist[1]:
                runtime = raw_input('Specify running time in seconds: ')
                print 'Total Power Consumption for %s second(s): '%(runtime)+str(1.5*float(runtime))+'W'
            elif stat == statlist[2]:
                print 'Equilibrium Heat: '+str(s.algae_heat.level)+'J'
            x=False
        else:
            stat = raw_input('Invalid input. Return the value for temp, power or heat? ')
            x=True
        
    

init = raw_input('Choose which simulation to run (day or night): ')


env = simpy.rt.RealtimeEnvironment(factor=1) ### Run a real time simulation with time factor 0.01.
s = systemHeat(env) ### Create an environment s.
env.process(wallCond(env,s)) ### Create the wallCond process that runs in s.
if init == 'day':
    env.process(solarRad(env,s)) ### Create the solarRad process that runs in s.
env.process(pumpConv(env,s)) ### Create the pumpConv process that runs in s.
env.run(10) ### Run the simulation.

orig_stdout = sys.stdout
b = open('simulation_data.txt','w')
sys.stdout = b


try: 
    pass
except KeyboardInterrupt:
    print 'exit'
finally:
    ser.close()
    sys.stdout = orig_stdout
    b.close()
