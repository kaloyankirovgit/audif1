import os
import fastf1
import matplotlib.pyplot as plt

# Enable cache to improve performance and avoid repeated downloads
cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fastf1_cache')
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

# Session identifiers: 'FP1', 'FP2', 'FP3', 'Q' (Qualifying),
# 'S' (Sprint), 'SQ' (Sprint Qualifying), or 'R' (Race).

session = fastf1.get_session(2026, 'Hungary', 'R')

# Timing, telemetry, weather, ...
session.load()

# For plots
compounds = {'SOFT': 'red', 'MEDIUM': 'gold', 'HARD': 'grey'}
linestyles = {1: 'solid', 9: 'dashed', 19: 'dotted'}

positions = [1, 9, 19]
drivers = [
    session.results.loc[session.results['Position'] == pos, 'Abbreviation'].iloc[0]
    for pos in positions
]

fig, ax = plt.subplots(figsize=(12, 7))

for drv, pos in zip(drivers, positions):
    laps = session.laps.pick_drivers(drv)
    linestyle = linestyles[pos]
    for _, stint in laps.groupby('Stint'):
        compound = stint['Compound'].iloc[0]
        ax.plot(
            stint['LapNumber'],
            stint['LapTime'].dt.total_seconds(),
            color=compounds.get(compound, 'black'),
            linestyle=linestyle,
            marker='o',
            markersize=3,
        )

ax.set_xlabel('Lap number')
ax.set_ylabel('Lap time / s')
ax.set_title('Lap times by tyre compound')
ax.grid(True, alpha=0.3)

# Legend for tyre compound (line color)
compound_handles = [
    plt.Line2D([0], [0], color=color, lw=2, label=compound)
    for compound, color in compounds.items()
]
compound_legend = ax.legend(handles=compound_handles, title='Tyre', loc='upper right')
ax.add_artist(compound_legend)

# Legend for driver (line style)
driver_handles = [
    plt.Line2D([0], [0], color='black', lw=2, linestyle=linestyles[pos], label=f'P{pos} - {drv}')
    for drv, pos in zip(drivers, positions)
]
ax.legend(handles=driver_handles, title='Driver', loc='upper left')

fig.tight_layout()
plt.show()
