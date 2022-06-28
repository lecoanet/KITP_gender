
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import publication_settings

matplotlib.rcParams.update(publication_settings.params)

fontsize = 12

t_mar, b_mar, l_mar, r_mar = (0.15, 0.3, 0.3, 0.05)
h_plot, w_plot = (1., 1./publication_settings.golden_mean)

h_pad = 0.45

h_total = t_mar + 2*h_plot + h_pad + b_mar
w_total = l_mar + w_plot + r_mar

width = 3.4
scale = width/w_total

fig = plt.figure(1, figsize=(scale * w_total,
                             scale * h_total))

plot_axes = []
for i in range(2):
    left = (l_mar) / w_total
    bottom = 1 - (t_mar + h_plot + i*(h_plot + h_pad) ) / h_total
    width = w_plot / w_total
    height = h_plot / h_total
    plot_axes.append(fig.add_axes([left, bottom, width, height]))

tops = [0.375, 0.6]

for i, ax in enumerate(plot_axes):
    top = tops[i]
    ax.set_xlim([0.25-1, 14.75-1])
    ax.set_ylim([0, tops[i]])

    x_width = 14.75-0.25

papers_male_authors = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
fraction_male_authors = [0.0024, 0.011, 0.039, 0.0923, 0.1592, 0.2084, 0.201, 0.1481, 0.0851, 0.0375, 0.0121, 0.0027, 0.0012]

papers_female_authors = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
fraction_female_authors = [0.0296, 0.1365, 0.2448, 0.2629, 0.1858, 0.0988, 0.0311, 0.0082, 0.0021, 0.0002]

papers_male_coauthors = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
fraction_male_coauthors = [0.0014, 0.017, 0.0699, 0.1636, 0.2453, 0.2475, 0.1562, 0.072, 0.0226, 0.0039, 0.0006, 0.0]

papers_female_coauthors = np.array([1, 2, 3, 4, 5])
fraction_female_coauthors = [0.2081, 0.4112, 0.2874, 0.0859, 0.0074]

mean_male = [6.47, 7.566]
mean_female = [2.91, 2.282]

male_only = '#178583'
female_only = '#EDC2CE'

pm = [papers_male_authors, papers_male_coauthors]
fm = [fraction_male_authors, fraction_male_coauthors]
pf = [papers_female_authors, papers_female_coauthors]
ff = [fraction_female_authors, fraction_female_coauthors]

dy = [0.07*0.35/0.5, 0.07]
 
colors = {'m':'#56B8B6', 'f':'#F594DD'}

title = ['Random Authors', 'Random Coauthors']

for i, ax in enumerate(plot_axes):

    papers_male = pm[i]
    fraction_male = fm[i]
    papers_female = pf[i]
    fraction_female = ff[i]

    for papers in range(0, 15):
        i_f = np.where(papers_female==papers)[0]
        i_m = np.where(papers_male==papers)[0]
        frac_female = 0
        frac_male = 0
        if len(i_f) > 0:
            frac_female = fraction_female[i_f[0]]
        if len(i_m) > 0:
            frac_male = fraction_male[i_m[0]]
        if frac_female > frac_male:
            ax.add_patch(plt.Rectangle((papers-0.45, 0), 0.9, frac_female, lw=0, color=female_only))
            ax.add_patch(plt.Rectangle((papers-0.45, 0), 0.9, frac_male, lw=0, color=male_only))
        else:
            ax.add_patch(plt.Rectangle((papers-0.45, 0), 0.9, frac_male, lw=0, color=male_only))
            ax.add_patch(plt.Rectangle((papers-0.45, 0), 0.9, frac_female, lw=0, color=female_only))

    legend_x = 8.7
    legend_y = tops[i]-dy[i]
    y_height = 0.9*tops[i]/x_width/publication_settings.golden_mean
    
    ax.plot([mean_male[i], mean_male[i]], [0, legend_y-y_height*1.4], color='k', linestyle='--')
    ax.plot([mean_female[i], mean_female[i]], [0, legend_y-y_height*1.4], color='k', linestyle='--')
    
    ax.plot([2, 2], [0, legend_y-y_height*1.4], color=colors['f'], lw=2)
    ax.plot([11, 11], [0, legend_y-y_height*1.4], color=colors['m'], lw=2)

    y_height = 0.9*tops[i]/x_width/publication_settings.golden_mean
    ax.add_patch(plt.Rectangle((legend_x-0.45, legend_y), 0.9, y_height, lw=0, color=male_only))
    ax.text(legend_x+0.55, legend_y+y_height/2, "male-only", fontsize=10, horizontalalignment='left', verticalalignment='center')
    
    ax.add_patch(plt.Rectangle((legend_x-0.45, legend_y-y_height*1.2), 0.9, y_height, lw=0, color=female_only))
    ax.text(legend_x+0.55, legend_y-y_height*1.2+y_height/2, "female-only", fontsize=10, horizontalalignment='left', verticalalignment='center')

    legend_x = 0.1
    dx = 1.2
    ly = legend_y+y_height/2
    ax.plot([legend_x, legend_x+dx], [ly, ly], color='k', lw=2)
    ax.text(legend_x + dx + 0.2, ly, "data", fontsize=10, horizontalalignment='left', verticalalignment='center')

    ly = legend_y-y_height*1.2+y_height/2
    ax.plot([legend_x, legend_x+dx], [ly, ly], color='k', linestyle='--')
    ax.text(legend_x + dx + 0.2, ly, "model mean", fontsize=10, horizontalalignment='left', verticalalignment='center')

    ax.set_title(title[i])

    ax.set_ylabel('pdf')
    ax.set_xlabel('number of papers')
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    ax.set_xticklabels(['0','','2','','4','','6','','8','','10','','12',''])

plt.savefig('model.pdf')

