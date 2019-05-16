import numpy as np
from env import Env
from server import Server

SimTime = 10000
NumServer = 16

env = Env(NumServer, SimTime, 100, 50)

for t in range(SimTime):
    for s in range(NumServer):
        # 1. gen token
        env.servers[s].gen()
        
        # 2. receive token
        if t in env.event_slots[s]:
            env.servers[s].recv(env.event_slots[s][t])
        
        # 3. gen traffic
        d = env.gen_traffic()
        
        # 4. cosume token
        env.servers[s].cosume(d)
        
        # 5. send token
        if env.servers[s].num_overflow > 0:
            latency = np.random.randint(100,1000) # 100ns to 1us
            if t+latency < SimTime:
                env.event_slots[(s+1) % NumServer][t+latency] = env.servers[s].num_overflow
        
        env.servers[s].send() # reset overflow
        
        # 6. collect statistic
        # ...