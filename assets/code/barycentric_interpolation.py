from functools import reduce
import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Callable


def plot(f, interval, label="", linewidth=1.5, legend_loc="upper left"):
    """
    Returns a plot of `f` on `interval` with resolution 1000 points/step.
    Takes an optional label for the plotted line.
    """
    start, stop = interval
    if start > stop: start, stop = stop, start
    steps = 1000 * (stop - start)
    x_vals = np.linspace(start, stop, num=steps)
    y_vals = list(map(f, x_vals))
    plt.plot(x_vals, y_vals, label=label, linewidth=linewidth)
    plt.legend(framealpha=1, frameon=False, loc=legend_loc)
    return plt


def save(fig, file):
    """
    Saves a `fig` plot figure to `file`.
    """
    fig.savefig(file,
                transparent=True,
                dpi=600,
                bbox_inches="tight",
                pad_inches=0.25)


def barycentric_weight(i: int, x: List[float]):
    """
    Computes the `i`"th Barycentric weight
        `w_i = 1 / \prod_{j=0, j!=i}^n (x_i - x_j)`

    Params:  `i` order of Barycentric weight to compute
             `x` set `{x_0, ..., x_n}` to use in computing barycentric weight
    Returns: barycentric weight of order `i`
    """
    denominator = 1
    for j in range(len(x)):
        if j == i: continue
        denominator *= (x[i] - x[j])

    return 1 / denominator


def barycentric_formula(f: Callable[[float], float], x: List[float]):
    """
    Computes a function handle to the Barycentric formula
        `p_n(x) = {\sum_{i=0}^n \omega_i / (x - x_i) * f_i} / {\sum_{i=0}^n \omega_i / (x - x_i)}`
    interpolating the function `f` at points in `x`.

    Params:  `f` function to find interpolation Barycentric formula for,
               evaluable at every `x_i` in `x`
             `x` set `{x_0, ..., x_n}` to use in computing Barycentric Formula
    Returns: Handle to the interpolating Barycentric formula accepting one
             argument `a` and evaluating `p_n(a)`.
    """
    weights = list(map(lambda i: barycentric_weight(i, x), range(len(x))))

    def p_n(a: float):
        if a in x: return f(a)  # fast path; would cause divide-by-zero
        numerator = 0
        denominator = 0
        for i in range(len(x)):
            x_i = x[i]
            w_i = weights[i]
            numerator += w_i / (a - x_i) * f(x_i)
            denominator += w_i / (a - x_i)

        return numerator / denominator

    return p_n


f = lambda x: math.sin(4 * x * math.cos(8 * x))
interval = [-1, 1]

# Plot approximation with equidistant nodes.
fig = plt.figure()
plot(f, interval, label=f"f(x) = sin(4xcos(8x))", linewidth=3)
for h in range(1, 4 + 1):
    start, stop = interval
    N = 2**h
    x = np.linspace(start, stop, num=N)
    p_N = barycentric_formula(f, x)
    fig = plot(p_N, interval, label=f"p_{N}(x)")
save(fig, "equidistant.png")

# Plot approximation with Chebyshev nodes.
fig = plt.figure()
plot(f, interval, label=f"f(x) = sin(4xcos(8x))", linewidth=3)
for h in range(1, 4 + 1):
    start, stop = interval
    N = 2**h
    x = np.cos(np.pi * np.arange(N + 1) / N)
    p_N = barycentric_formula(f, x)
    plot(p_N, interval, label=f"p_{N}(x)")
save(fig, "chebyshev.png")

# Plot error with Chebyshev nodes.
fig = plt.figure()
for h in range(1, 4 + 1):
    start, stop = interval
    N = 2**h
    x = np.cos(np.pi * np.arange(N + 1) / N)
    p_N = barycentric_formula(f, x)
    error = lambda x: abs(f(x) - p_N(x))
    plot(error,
         interval,
         label=f"|f(x) - p_{N}(x)|",
         legend_loc="upper center")
save(fig, "error.png")

# Print L2 norm error of approximation with Chebyshev nodes.
print("Order\tL2 norm")
print("-----\t-------")
for h in range(4, 7 + 1):
    start, stop = interval
    steps = (stop - start) * 1000
    N = 2**h
    x = np.cos(np.pi * np.arange(N + 1) / N)
    p_N = barycentric_formula(f, x)
    error = lambda x: abs(f(x) - p_N(x))
    error_vals = map(error, np.linspace(start, stop, num=steps))
    norm = math.sqrt(reduce(lambda a, x: a + x**2, error_vals))
    print(f"{N}\t{norm}")

# Print max error of approximation with Chebyshev nodes.
print("Order\tMax error")
print("-----\t---------")
for h in range(1, 7 + 1):
    start, stop = interval
    steps = (stop - start) * 1000
    N = 2**h
    x = np.cos(np.pi * np.arange(N + 1) / N)
    p_N = barycentric_formula(f, x)
    error = lambda x: abs(f(x) - p_N(x))
    error_vals = map(error, np.linspace(start, stop, num=steps))
    max_error = max(error_vals)
    print(f"{N}\t{max_error}")
