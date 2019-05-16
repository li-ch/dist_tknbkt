import numpy as np

SimTime = 10000
NumServer = 16

class Server(object):
    def __init__(self, depth, rate):
        self.max_depth = depth
        self.rate = rate
        self.cur_depth = depth
        self.num_overflow = 0
        self.dropped_traffic = 0
    
    def update_cur_depth_and_overflow(self):
        diff = self.cur_depth - self.max_depth
        if diff > 0:
            self.cur_depth = self.max_depth
            self.num_overflow = diff
    
    def gen(self):
        self.cur_depth += self.rate
        self.update_cur_depth_and_overflow()
    
    def recv(self, num_tk):
        self.cur_depth += num_tk
        self.update_cur_depth_and_overflow()
    
    def cosume(self, demand):
        diff = demand - self.cur_depth
        if diff > 0:
            self.dropped_traffic = diff
            self.curr_depth = 0
        else:
            self.cur_depth -= demand
            
    def send(self):
        # reset local overflow
        self.num_overflow = 0


# simulation environment
class Env(object):
    def __init__(self, num_server, sim_time, depth, rate):
        self.num_server = num_server
        self.sim_time = sim_time
        # each server has a timeline
        # each timeline is a dictionary of tick# -> [event]
        self.event_slots = [{}]*self.num_server
        self.servers = []
        for i in range(self.num_server):
            s = Server(depth, rate)
            self.servers.append(s)
    
    def gen_traffic(self):
        return np.random.random()*100

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