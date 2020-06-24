import numpy as np
import matplotlib.pyplot as plt
plt.style.use('style.mplstyle')

# set up two figures for plot
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

# counting rates plot
t = [100,110,120,130,140,150,160,170,180]
counts = [0.0003515,0.0003338,0.0003079,0.0002883,0.0002664,0.0002591,0.0002579,0.0002382,0.0002187]
color = 'tab:red'
ax1.set_xlabel('thickness (microns)', ha='right', x=1.0)
ax1.set_ylabel('counts/decay', ha='right', y=1.0, color=color)
ax1.scatter(t, counts, s=9, color=color)
ax1.set_ylim(0.0002, 0.0004)
ax1.set_title('$^{99}$Tc + Nd Foil')
#ax1.semilogy()
#ax1.tick_params(axis='y', labelcolor=color)

# percentage of counts in ka1 x-ray peak
percentages = [11.1,11.3,12.1,10.9,12.7,12.1,13.0,12.2,11.9]
color = 'tab:blue'
ax2.set_ylabel('% of total in ka1 peak', ha='right', y=1.0, color=color)
ax2.scatter(t, percentages, s=9, color=color)
#ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
