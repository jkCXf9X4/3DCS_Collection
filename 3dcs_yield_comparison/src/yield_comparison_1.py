import scipy.integrate as integrate
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
 
 
def bell(x, mean, std):
    value = scipy.stats.norm.pdf(x, mean, std)
    return value
    # return 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean)**2 / (2 * std**2))
 
 
def integrate_bell(start, end, mean, std):
    proportion, error = integrate.quad(bell, start, end, args=(mean, std))
    return proportion
 
 
def plot_bell(start, end, mean, std):
    ptx = np.linspace(start, end, 100)
    pty = scipy.stats.norm.pdf(ptx, mean, std)
 
    plt.plot(ptx, pty, color='gray')
    plt.show()
 
 
def calculate_yield(std, limit, shift=0, plot=False):
    """ Return
        deviation, proportion
    """
    deviation = limit/std
    if plot:
        plot_bell(-deviation, deviation, mean=shift, std=1)
 
    proportion = integrate_bell(-deviation, deviation, mean=shift, std=1)
 
    key_values = calculate_key_values(proportion)
 
    key_values['deviation'] = deviation
    key_values['shift'] = shift
 
    return key_values
 
 
def calculate_key_values(proportion):
    small = 0.000000000000000001
    proportion_out = 1 - proportion
    data = {
        'proportion_in': proportion,
        'proportion_out': proportion_out,
        'ppm_in':  1000000 * proportion,
        'ppm_out':  1000000 * proportion_out,
        'percent_in': 100 * proportion,
        'percent_out': 100 * proportion_out,
        'one_in':  1/(proportion_out+small)
        }
    return data
 
 
# reference sigma shift
# without:          5σ  99.9999426697%  0.0000573303%  0.57ppm  1/1744278
# with 1.5 shift:   5σ  99.97670%  ppm 233
 
# Input
normal_pins = [0.133, 0.136, 0.1]
normal_PI = [0.175, 0.178, 0.124]
 
uniform_pins = [0.192, 0.187, 0.174]
uniform_PI = [0.223, 0.219, 0.188]
 
std = uniform_PI
five_std_limit = 1
 
 
# Calculations
 
print("Without shift")
 
ppm_sum = 0
ppm_shift_sum = 0
 
for i in std:
    print("-------------------------Input------------------------")
    print("Std: " + str(i))
    print("Limit: " + str(five_std_limit))
 
    keys = calculate_yield(i, five_std_limit, 0)
    keys_shifted = calculate_yield(i, five_std_limit, 1.5)
 
    print(keys)
    print(keys_shifted)
 
    ppm_sum += keys["ppm_out"]
    ppm_shift_sum += keys_shifted["ppm_out"]
 
print(f"ppm: {ppm_sum}")
print(f"ppm_shifted: {ppm_shift_sum}")