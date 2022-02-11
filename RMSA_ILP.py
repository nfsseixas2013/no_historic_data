from docplex.mp.model import Model

class rmsa_ilp:
    def __init__(self,qtd_demanda,qtd_links,qtd_path,qtd_channel,qtd_frequency_slot,qtd_modulacao):
        self.qtd_demanda = qtd_demanda
        self.qtd_links = qtd_links
        self.qtd_path = qtd_path
        self.qtd_channel = qtd_channel
        self.qtd_frequency_slot = qtd_frequency_slot
        self.qtd_modulacao = qtd_modulacao
        self.sigma = dict()
        self.gama = dict()
        self.dpm = dict()
        self.mdl = Model("RMSA")
        self.Min = self.mdl.binary_var_dict([(d,p,c,m) for d in range(0,self.qtd_demanda) for p in 
                                        range(0, self.qtd_path) for c in range(0, self.qtd_channel) for m in range(0,self.qtd_modulacao)])
        self.inicia_sigma()
        self.inicia_gama()
        self.inicia_dpm()
        self.latencia = [0 for x in range(0,qtd_demanda)]
        self.ldp = dict()
        self.inicia_ldp()
        
     
    def inicia_sigma(self): ## Inicializa os valores com zero
        indices = [(e,d,p) for e in range(0,self.qtd_links) for d in range(0,self.qtd_demanda) for p in range(0,self.qtd_path)]
        values = [0 for x in range(0, len(indices))]
        self.sigma = dict(zip(indices,values))
    
    def set_links(self,link): 
        self.sigma[link] = 1
        
    def inicia_gama(self): ## Inicializa os valores com zero
        indices = [(d,p,c,m,s) for d in range(0,self.qtd_demanda) for p in range(0,self.qtd_path)
        for c in range(0,self.qtd_channel) for m in range(0,self.qtd_modulacao) for s in range(0,self.qtd_frequency_slot)]
        values = [0 for x in range(0,len(indices))]
        self.gama = dict(zip(indices,values))
        
    def set_slices(self,gama):
        self.gama[gama] = 1
        
    def inicia_dpm(self):
        indices = [(d,p,m) for d in range(0,self.qtd_demanda) for p in range(0,self.qtd_path) for m in range(0,self.qtd_modulacao)]
        values = [10000 for x in range(0,len(indices))]
        self.dpm = dict(zip(indices,values))
        
    def set_dpm(self,indice, value):
        self.dpm[indice] = value
        
    def inicia_ldp(self):
        indices = [(d,p) for d in range(0,self.qtd_demanda) for p in range(0,self.qtd_path)]
        values = [0 for x in range(0,len(indices))]
        self.ldp = dict(zip(indices,values))
        
    def inicia_latencia(self,latencies):
        self.latencia = latencies
        
    def set_constraint1(self):
        print(self.mdl.add_constraints(self.mdl.sum(self.Min[(d,p,c,m)] for p in range(0,self.qtd_path) for c in range(0, self.qtd_channel)
        for m in range(0,self.qtd_modulacao)) == 1 for d in range(0,self.qtd_demanda)))
        
    def set_constraint2(self):
        print(self.mdl.add_constraints(self.mdl.sum(self.gama[(d,p,c,m,s)] * self.sigma[(e,d,p)] * self.Min[(d,p,c,m)] for d in range(0,self.qtd_demanda) for p in range(0,self.qtd_path)
                                  for c in range(0,self.qtd_channel) for m in range(0,self.qtd_modulacao)) <= 1 for e in range(0,self.qtd_links) for s in range(0,self.qtd_frequency_slot)))
    
    def set_constraint3(self):
        print(self.mdl.add_constraints(self.mdl.sum(self.Min[d,p,c,m] * self.ldp[d,p] for p in range(0,self.qtd_path) for c in range(0,self.qtd_channel) 
                           for m in range(0,self.qtd_modulacao)) <= self.latencia[d] for d in range(0,self.qtd_demanda)))
        
    def set_min(self):
        print(self.mdl.minimize(self.mdl.sum(self.Min[(d,p,c,m)] * self.dpm[(d,p,m)] for d in range(0,self.qtd_demanda) for p in range(self.qtd_path)
        for c in range(0,self.qtd_channel) for m in range(0,self.qtd_modulacao))))
    
    def set_ldp(self,indice,value):
        self.ldp[indice] = value
        
    def set_latencias(self, lista):
        self.latencia = lista
        
    def solver(self):
        self.set_min()
        self.set_constraint1()
        self.set_constraint2()
        self.set_constraint3()
        solution = self.mdl.solve()
        conf = []
        if solution != None:
            solution.display()
            S = solution.get_value_dict(self.Min)
            for i in S.keys():
                if S[i] == 1:
                    print("Indice :{}".format(i))
                    conf.append(i)
            return conf
                
        else:
            return None
        
    def reset_ILP(self):
        self.inicia_sigma()
        self.inicia_gama()
        self.inicia_dpm()
        self.inicia_ldp()
    
    def print_gama(self,indice):
        for i in self.gama.keys():
            if i[0] == indice:
                print("{} : {}".format(i,self.gama[i]))
                    