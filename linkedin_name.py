import matplotlib.pyplot as plt

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 4))

# Set background color
fig.patch.set_facecolor('#2B2B2B')
ax.set_facecolor('#2B2B2B')

# Hide axes
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# Add code text
code_text = "linkedin > lanin.py\nfrom lanin import data_analysis_skills\n# Aspiring Data Analyst / Content Creator"
ax.text(0.02, 0.7, code_text, color='#FFFFFF', fontsize=14, fontfamily='monospace')

# Add code-like box at the top
ax.text(0.02, 0.95, "mochen.py   x", color='#B0B0B0', fontsize=12, fontfamily='monospace', alpha=0.9)

# Add title bar like UI
ax.text(0.02, 1.0, "1", color='#00FF00', fontsize=12, fontfamily='monospace')
ax.text(0.02, 0.85, "2", color='#00FF00', fontsize=12, fontfamily='monospace')

# Remove axes spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Save the image
plt.savefig("linkedin_background.png", facecolor=fig.get_facecolor())
plt.show()