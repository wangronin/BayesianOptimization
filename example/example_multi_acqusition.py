import numpy as np
import sys, os
sys.path.insert(0, '../')

from BayesOpt import ContinuousSpace, OrdinalSpace, NominalSpace, RandomForest
from BayesOpt.Extension import MultiAcquisitionBO

dim_r = 2  # dimension of the real values
def obj_fun(x):
    x_r = np.array([x['continuous_%d'%i] for i in range(dim_r)])
    x_i = x['ordinal']
    x_d = x['nominal']
    _ = 0 if x_d == 'OK' else 1
    return np.sum(x_r ** 2) + abs(x_i - 10) / 123. + _ * 2

search_space = ContinuousSpace([-5, 5], var_name='continuous') * dim_r + \
    OrdinalSpace([5, 15], var_name='ordinal') + \
    NominalSpace(['OK', 'A', 'B', 'C', 'D', 'E', 'F', 'G'], var_name='nominal')
model = RandomForest(levels=search_space.levels)

opt = MultiAcquisitionBO(
    search_space=search_space, 
    obj_fun=obj_fun, 
    model=model, 
    max_FEs=40, 
    DoE_size=4,    # the initial DoE size
    eval_type='dict',
    n_job=4,       # number of processes
    n_point=4,     # number of the candidate solution proposed in each iteration
    verbose=True   # turn this off, if you prefer no output
)

xopt, fopt, stop_dict = opt.run()
print('xopt: {}'.format(xopt))
print('fopt: {}'.format(fopt))
print('stop criteria: {}'.format(stop_dict))