from Lightpath import lightpath
import simpy
import Interface
import numpy as np

class split(lightpath):

    def __init__(self, env, cod, mode, source, destination, traffic, net, service_type, metric, IA, controller, error_type):
        self.id = cod
        self.nodes = []
        self.mode = mode
        self.channel_size = 0
        self.source = source
        self.destination = destination
        self.conf = []
        self.env = env
        self.report = []
        self.traffic = traffic
        self.connection = False
        ## parameters of ilp
        self.links_candidates = []
        self.links_ids = []
        self.links_costs = []
        self.links_ref = []
        self.slices = []
        self.net = net
        self.traffic_predicted = 0 ## depois mudar isso
        self.path = 0 # defined by ILP solution
        self.modulation = 0 # defined by ILP solution
        self.slots = []
        self.latencia_required = 0
        self.IA = IA
        self.metric = metric
        self.service_type = service_type
        self.ia_data_input = []
        self.controller = controller
        self.controller.set_lightpaths(self)
        self.flag_update = False
        self.granted = 0
        self.connection_control = simpy.Store(env,capacity=simpy.core.Infinity)
        self.connection_nodes = simpy.Store(env,capacity=simpy.core.Infinity)
        self.connection_lightpath = simpy.Store(env,capacity=simpy.core.Infinity)
        self.interval_data = []
        self.error_type = error_type
        self.time_factor = 600
        self.interval = 2
        self.current_traffic = self.traffic[0]
        self.data_intervals = []
        self.interruptions = 0
        self.slices_backup = []
        self.path_backup = 0
        self.current_time_decision = 0
        self.modulation_backup = 0
        self.action = self.env.process(self.run())
        

    def run(self):
        counter = 0
        while True:
            try:
                msg = yield self.connection_lightpath.get()
                if msg != None:
                    traffic = msg[0]
                    counter += 1
                    if self.flag_update:
                        indices = super().get_conf_indices()
                        super().set_conf(indices)
                        if len(self.slices_backup) > 0:
                            if super().get_interruptions_count(self.slices[self.path][self.modulation], self.slices_backup[self.path_backup][self.modulation_backup]):
                                self.interruptions += 1
                            self.flag_update = False
                    self.env.process(super().sending_traffic(traffic))
                    self.interval_data.append(traffic)
                    yield self.env.timeout(1)
            except simpy.Interrupt:
                self.flag_update = True
                counter -= 1
            if counter == self.time_factor:
                if msg != None:
                    self.current_traffic = np.random.poisson(self.traffic[msg[1]],1)[0]
                self.data_intervals.append(1)
                self.run_predictions()
                counter = 0
                   

    def run_predictions(self):  
        flag = super().setup_predictions()
        if flag:
            self.granted = Interface.get_bandwidth(self.slots[self.modulation], self.modulation, self.net)
            self.data_intervals.pop(0)
        self.env.process(super().send_msg_control(flag))

    


