
from scipy import optimize
from scipy.optimize import minimize

from catia._3dcs.main import _3DCS
import numpy as np



catia_3dcs = _3DCS()
catia_3dcs.run_simulation()


catia_3dcs.collect_products()
catia_3dcs.collect_tolerances()


#initial_values = catia_3dcs.get_tolerances()

bounds = catia_3dcs.get_bounds() # format  bounds=((-1.0, 1.0), (-1.0, 1.0)),

# test
# x = [2, 2, 2, 2]
# catia_3dcs.set_tolerances(x)

def simulation(x):
    catia_3dcs.set_tolerances(x)

    results = catia_3dcs.run_simulation()

    return sum(results)


# options

# results = dict()
# results['shgo'] = optimize.shgo(simulation, bounds)

# x0 = np.array(initial_values)
# res = minimize(simulation, x0, method='nelder-mead', options={'xatol': 1e-8, 'disp': True})

# res = minimize(simulation, x0, method='BFGS', options={'disp': True})
