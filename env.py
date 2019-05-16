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