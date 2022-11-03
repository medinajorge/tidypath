import numpy as np
import matplotlib.pyplot as plt
from utils import savedata, savefig

@savedata("x+z+kwargs")
def slow_computation(x, y, *args, z=1, **kwargs):
    """
    Function you want to compute once and store keeping your folders tidy => save time and record your results in memory. 
    You will always know which function created the data.
    """
    return np.random.normal(size=int(1e4))

@savefig("kwargs")
def plot_slow_computation(*args, **kwargs):
    """
    Figure you want to automatically save, keeping your folders tidy. 
    You will always know which function created the figure.
    """
    X = slow_computation(*args, **kwargs)
    _ = plt.hist(X, bins=100, density=1)
    plt.xlabel("X")
    plt.ylabel("Probability density")
    return plt.gcf()