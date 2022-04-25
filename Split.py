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
        self.eMBB_factor = 300.5
        self.mMTC_factor = 2.50
        self.URLLC_factor = 1.40
        self.interval_data = []
        self.error_type = error_type
        self.time_factor = 600
        self.action = self.env.process(self.run())
        

    def run(self):
        while True:
            msg = yield self.connection_lightpath.get()
            if msg != None:
                traffic = msg[0]
                try:
                    if self.flag_update:
                        indices = super().get_conf_indices()
                        super().set_conf(indices)
                    self.env.process(super().sending_traffic(traffic))
                    self.interval_data.append(traffic)
                    yield self.env.timeout(1)
                except simpy.Interrupt:
                    self.flag_update = True
                if self.metric == 'median':
                    self.ia_data_input.append(np.median(self.interval_data))
                elif self.metric == 'quantile3':
                    self.ia_data_input.append(np.quantile(self.interval_data,0.75))
                else:
                    self.ia_data_input.append(np.amax(self.interval_data))
                if self.env.now % self.time_factor == 0:
                    self.run_predictions()
        

    def run_predictions(self):  
        flag = super().setup_predictions()
        if flag:
            self.granted = Interface.get_bandwidth(self.slots[self.modulation], self.modulation, self.net)
        self.env.process(super().send_msg_control(flag))

    


