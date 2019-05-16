# rate limiting server
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