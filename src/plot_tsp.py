from plotnine import (
    ggplot,
    aes,
    geom_point,
    labs,
    geom_path,
    annotate,
    geom_segment,
    theme,
)
import pandas as pd
import numpy as np
import os
import re
from PIL import Image
from src.lns_tsp import TSPSolver, dist
from itertools import combinations
from datetime import datetime

# initialize and solve


def random_distances(cities=10):
    """Create random cities on a map"""
    coords = list(
        zip(
            [0] + np.random.randint(1, 1000, size=cities).tolist(),
            [0] + np.random.randint(1, 1000, size=cities).tolist(),
        )
    )
    dist_m = {}
    for i, j in combinations(range(cities), 2):
        dist_m[(i, j)] = dist(*coords[i], *coords[j])
    return coords, dist_m


np.random.seed(3)
coords, distances = random_distances(20)
tsp = TSPSolver(distances)
tsp.lns(rounds=5000, neighborhood_size=5)

print(
    "Runtime:",
    datetime.fromisoformat(tsp.best_sol_log[-1]["t"])
    - datetime.fromisoformat(tsp.best_sol_log[0]["t"]),
)

# Convert the list of tuples to a DataFrame
df = pd.DataFrame(coords, columns=["x", "y"])

os.system("rm -rf tsp_plot")
os.makedirs("tsp_plot", exist_ok=True)

for i, analytics in enumerate(tsp.best_sol_log):
    step = str(i).rjust(2, "0")
    plot = (
        ggplot(
            df.iloc[analytics["x"]].assign(n=lambda x: x.index.isin(analytics["n"])),
            aes(x="x", y="y", shape="n"),
        )
        + geom_point(size=4, fill="none")
        + geom_path(aes(shape=None))
        + labs(x="", y="")
        + geom_segment(
            x=df.iloc[analytics["x"]].iloc[-1]["x"],
            y=df.iloc[analytics["x"]].iloc[-1]["y"],
            xend=df.iloc[analytics["x"]].iloc[0]["x"],
            yend=df.iloc[analytics["x"]].iloc[0]["y"],
            size=0.2,
        )
        + annotate(
            "text",
            label=f"Step: {step}\n Best: {round(analytics['y'], 1)}",
            x=df["x"].max(),
            y=df["y"].min(),
            ha="right",
            va="bottom",
        )
        + theme(legend_position="none")
    )

    # Save the plot to a file
    plot.save("tsp_plot/" + re.sub(r":|\.|-", "", analytics["t"]) + f"_{step}" + ".png")

# Get all PNG files in the folder
images = [img for img in os.listdir("tsp_plot") if img.endswith(".png")]

# Sort images by name to maintain order
images.sort()

# Load images
frames = [Image.open(os.path.join("tsp_plot", img)) for img in images]

# Save as GIF
frames[0].save(
    "tsp_plot/tsp_plot.gif",
    save_all=True,
    append_images=frames[1:] + frames[-1:] * 40,
    duration=50,  # Duration in milliseconds
    loop=None,  # Loop forever
)
