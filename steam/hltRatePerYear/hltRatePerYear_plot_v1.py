#!/usr/bin/env python3
import matplotlib.pyplot as plt

# Existing Data
data = [
  [2012, 0.50,  420.0,  400.0,   996.0],
  [2015, 0.25,  992.5,   98.8,  1057.1],
  [2016, 0.91, 1005.8,  514.5,  4467.8],
  [2017, 1.01,  976.0,  409.7,  4635.0],
  [2018, 1.18, 1046.4, 2918.7,  4855.6],
  [2022, 1.45, 1776.7, 2438.3, 22296.7],
  [2023, 1.66, 1683.8, 2660.2, 17114.2],
]

years = [foo[0] for foo in data]
luminosity = [foo[1] for foo in data]
prompt_rates = [foo[2]/1e3 for foo in data]
parking_rates = [foo[3]/1e3 for foo in data]
scouting_rates = [foo[4]/1e3 for foo in data]

total_rates = [sum(x) for x in zip(prompt_rates, parking_rates)]
elegant_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
scaled_luminosity = [l for l in luminosity]  # Scaling for plotting

# Plot Setup
plt.figure(figsize=(18, 11))
ax1 = plt.gca()

# Plotting Rates
ax1.plot(years, prompt_rates, 'o--', color='black', label='Prompt', linewidth=2.5, markersize=12)
ax1.plot(years, parking_rates, 's--', color=elegant_palette[1], label='Parking', linewidth=2.5, markersize=12)
ax1.plot(years, total_rates, '^--', color=elegant_palette[2], label='Prompt + Parking', linewidth=2.5, markersize=12)

# Axes labels and ticks
ax1.set_xlabel('Year', fontsize=30)
ax1.set_ylabel('HLT Rate (Prompt and Parking) [kHz]', fontsize=30, color='black', labelpad=20)
ax1.tick_params(axis='y', labelsize=24, labelcolor='black', pad=10)
ax1.tick_params(axis='x', labelsize=24, pad=10)
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
ax1.set_xticks(years)

# Plotting Scouting rate in blue
ax2 = ax1.twinx()
ax2.plot(years, scouting_rates, 'x--', color=elegant_palette[0], label='Scouting', linewidth=2.5, markersize=12)
ax2.set_ylabel('HLT-Scouting Rate [kHz]', color=elegant_palette[0], fontsize=30, labelpad=25)
ax2.tick_params(axis='y', labelcolor=elegant_palette[0], labelsize=24, pad=10)

# Plotting Instantaneous Luminosity in a different style
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 160))  # Increasing the gap between ax2 and ax3
ax3.plot(years, scaled_luminosity, 'p-.', color='magenta', label='Inst. Luminosity', linewidth=2.5, markersize=12)
ax3.set_ylabel('Inst. Luminosity [$10^{34}$ cm$^{-2}$ s$^{-1}$]', color='magenta', fontsize=30, labelpad=20)
ax3.tick_params(axis='y', labelcolor='magenta', labelsize=24, pad=20)

# Legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc=2, fontsize=25, frameon=True, edgecolor='black', facecolor='white')

# CMS label with more space between them
plt.text(0.01, 1.035, 'CMS', ha='left', va='center', transform=ax1.transAxes, fontsize=36, fontweight='bold')
plt.text(0.12, 1.035, '', ha='left', va='center', transform=ax1.transAxes, fontsize=34, style='italic')

plt.text(0.01, 0.600, 'HLT rates and instantaneous luminosity\naveraged over one typical Fill\nof a given data-taking year', ha='left', va='center', transform=ax1.transAxes, fontsize=20)

ax1.set_ylim([0, 5.0])
ax2.set_ylim([0, 25])

#plt.text(0.01, 0.60, 'Average HLT rates ', ha='left', va='center', fontsize=22) 
#plt.text(-5, 60, 'Average HLT rates and instantaneous luminosity over one typical Fill of a given data-taking year', fontsize = 22) 

# Layout and Save
plt.tight_layout()
plt.savefig("231218_TypicalHLTRates_Suggestion01.png", bbox_inches='tight', dpi=600)
plt.savefig("231218_TypicalHLTRates_Suggestion01.pdf", bbox_inches='tight', dpi=600)
#plt.show()
