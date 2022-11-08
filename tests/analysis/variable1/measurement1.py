import numpy as np
import matplotlib.pyplot as plt
from tidypath import savedata, savefig

@savedata("x+z+kwargs") # alternative: @savedata("all-y")
def slow_computation(x, y, *args, z=1, **kwargs):
    """
    Function you want to compute once and store keeping your folders tidy. Save time and record your results in memory with optimal compression.
    You will always know which function created the data by looking at the file path: 
            data/subpackages/module/function_name/file
    In this example:
            data/variable1/measurement1/slow_computation/file.lzma
    """
    return np.random.normal(size=int(1e4))

@savefig("kwargs")
def plot_slow_computation(*args, **kwargs):
    """
    Figure you want to automatically save, keeping your folders tidy. 
    You will always know which function created the figure by looking at the image path:
        figs/subpackages/module/function_name/image
    In this example:
        figs/variable1/measurement1/plot_slow_computation/image.png
    """
    X = slow_computation(*args, **kwargs)
    _ = plt.hist(X, bins=100, density=1)
    plt.xlabel("X")
    plt.ylabel("Probability density")
    return plt.gcf()
