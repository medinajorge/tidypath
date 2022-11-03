# PhD-utils

For people that have to compute and store a large variety of data and/or perform statistical inference.

## Keep your files tidy!

Don't spend time creating directories, deciding filenames, etc. Decorators `savefig` & `savedata` will do it for you.

- `savedata` computes output and stores it in the first function call. Future calls reads it from memory. Default LZMA compression
- `savefig`  saves output figure.

### savedata
Example function `slow_computation` in module `package.subpackages.module`
```
@savedata("x+z")
def slow_computation(x, y, *args, z=1, **kwargs):
    ...
    return result
```
1. Apply to function (result of any type).
2. Choose the variables to record in the filenames.
3. Optionally, choose file extension and other specifications.
4. Result will be saved at `data/subpackages/module/slow_computation/x-'x'_z-'z'_.lzma` ('x' = value of x passed to `slow_computation` during call)
5. If you want to recompute and overwrite, you can pass `overwrite=True` to `slow_computation`. The decorator adds the arguments: `save`, `overwrite` and `keys`.

### savefig
```
@savefig("kwargs")
def plot_results(*args, **kwargs):
    ...
    return figure
```
- Same steps as  `savedata`.
- Only difference is the output.
- Decorator adds the same arguments as `savedata` plus `return_fig` (`bool`).

## Estimate confidence intervals
The subpackage `utils.stats.rtopy.resample` allows calls to the `resample` [R package](https://cran.r-project.org/web/packages/resample/resample.pdf).
- Provides CI and permutation tests.
- CIs can account narrowness bias, skewness and other errors in CI estimation, as indicated in the [article](https://arxiv.org/abs/1411.5279)

## Numba-accelerated permutation tests
Subpackage `utils.stats.tests.permutation`. 
- Faster permutation tests for the means and medians. Includes paired case.
- Scheme for adding other statistics in a numba-compatible way (`_permutation_test_2sample_paired` and `_permutation_test_2sample_not_paired` functions)

## Example
Please check `Example.ipynb`
