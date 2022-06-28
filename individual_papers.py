
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import publication_settings
from numpy.random import Generator, PCG64
from matplotlib.patches import Ellipse

matplotlib.rcParams.update(publication_settings.params)

fontsize = 12

t_mar, b_mar, l_mar, r_mar = (1.5, 0, 3, 2)
h_paper, w_paper = (1., 1.)
h_pad, w_pad = 0.5, 0.25
w_space = 3

max_authors = 6
num_papers = 18

h_total = t_mar + h_paper*num_papers + h_pad*(num_papers) + b_mar
w_total = l_mar + 2*w_space + (w_paper + w_pad)*(3*max_authors) + r_mar

width = 7.1
scale = width/w_total

fig = plt.figure(1, figsize=(scale * w_total,
                             scale * h_total))


#ax = fig.add_axes([0.1, 0.1, scale*w_total, scale*h_total])
plot_axes = []
for i in range(3):
    left = (l_mar + i*(w_space + (w_paper + w_pad)*max_authors) ) / w_total
    bottom = b_mar / h_total
    width = (w_paper+w_pad)*max_authors / w_total
    height = (h_paper + h_pad)*num_papers / h_total
    plot_axes.append(fig.add_axes([left, bottom, width, height]))

for ax in plot_axes:
    ax.set_xlim([0, max_authors+1])
    ax.set_ylim([0, num_papers+1])
    ax.set_axis_off()

#ax.plot([-w_total/2+l_mar, w_total/2-r_mar], [h_total-t_mar, h_total-t_mar], color='k')
#ax.plot([0, 0], [0, h_total], color='k')

num_authors =  np.array([4, 2, 3, 2, 2, 2, 5, 5, 2, 4, 6, 2, 1, 3, 1, 1, 3, 1])
tot_authors =  np.array([4, 1, 2, 2, 2, 2, 5, 5, 2, 4, 6, 2, 1, 3, 1, 1, 3, 1])
first_author = np.array([1, 0, 0,-1,-1, 1, 1, 1, 1, 1, 1, 1,-1, 1, 1, 1, 1, 1])
num_male =     np.array([4, 1, 1, 0, 1, 1, 3, 5, 2, 4, 4, 2, 0, 3, 1, 1, 3, 1])
index = np.arange(18) + 1

order = np.argsort(-num_authors)
num_authors = num_authors[order]
tot_authors = tot_authors[order]
first_author = first_author[order]
index = index[order]
num_male = num_male[order]
num_coauthor_male = np.copy(num_male)
num_coauthor_male[first_author==1] -= 1

def xy(i, j):
    # i is paper number, j is author number
    x = j + 1
    y = num_papers + 1 - i - 1
    return (x, y)

gender = {1:'#56B8B6', 0:'w', -1:'#B856A1'}

male_only = '#178583'
female_only = '#EDC2CE'

rng = Generator(PCG64(42))

w = w_paper/(w_paper+w_pad)
h = h_paper/(h_paper+h_pad)

dh = 1/32
dw = dh/h*w

title = ['Actual\nAuthors', 'Random\nAuthors', 'Random\nCoauthors']

for k, ax in enumerate(plot_axes):
    if k == 0:
        ax.text(0, 19.2, 'paper\nnum.', fontsize=12, horizontalalignment='right', verticalalignment='center')
    ax.text((max_authors+1)/2, 19.2, title[k], fontsize=12, horizontalalignment='center', verticalalignment='center')
    ax.plot([0, 0], [0.5, 18.5], linewidth=2, color='k')
    for i in range(num_papers):
        # real
        if k == 0:
            if num_male[i] == num_authors[i] or (first_author[i] == 0 and num_male[i] == num_authors[i]-1):
                x, y = xy(i, 0)
                ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=male_only))
            elif num_male[i] == 0:
                x, y = xy(i, 0)
                ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=female_only))
            ax.add_patch(Ellipse(xy(i, 0), width=w, height=h, facecolor=gender[first_author[i]], edgecolor='k'))
            for j in range(1, num_authors[i]):
                if j < num_coauthor_male[i]+1:
                    ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[1], edgecolor='k'))
                else:
                    ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[-1], edgecolor='k'))

        # random authors
        elif k == 1:
            authors = tot_authors[i]            
            nums = rng.uniform(size=authors)
            n_male = np.sum(nums > 17/45)

            if n_male == authors:
                x, y = xy(i, 0)
                ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=male_only))
            elif n_male == 0:
                x, y = xy(i, 0)
                ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=female_only))
            if first_author[i] == 0:
                ax.add_patch(Ellipse(xy(i, 0), width=w, height=h, facecolor=gender[first_author[i]], edgecolor='k'))
                for j in range(1, authors+1):
                    if j < n_male+1:
                        ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[1], edgecolor='k'))
                    else:
                        ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[-1], edgecolor='k'))
            else:
                for j in range(0, authors):
                    if j < n_male:
                        ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[1], edgecolor='k'))
                    else:
                        ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[-1], edgecolor='k'))

        # random co-authors
        elif k == 2:
            extra_authors = num_authors[i] - 1
            if first_author[i] == 1:
                n_male = 1
            else:
                n_male = 0
            if extra_authors > 0:
                nums = rng.uniform(size=extra_authors)
                extra_male = np.sum(nums > 17/45)
                n_male += extra_male

            if n_male == num_authors[i] or (first_author[i] == 0 and n_male == num_authors[i]-1):
                x, y = xy(i, 0)
                ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=male_only))
            elif n_male == 0:
                x, y = xy(i, 0)
                ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=female_only))
            ax.add_patch(Ellipse(xy(i, 0), width=w, height=h, facecolor=gender[first_author[i]], edgecolor='k'))
            for j in range(1, num_authors[i]):
                if j < extra_male+1:
                    ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[1], edgecolor='k'))
                else:
                    ax.add_patch(Ellipse(xy(i, j), width=w, height=h, facecolor=gender[-1], edgecolor='k'))

        ax.text(-0.75, num_papers - i - h/8, '%i' %(i+1), fontsize=12, horizontalalignment='center', verticalalignment='center')


# Legend
ax = plot_axes[0]
x, y = xy(15, 6)
ax.add_patch(Ellipse((x, y), width=w, height=h, facecolor=gender[1], edgecolor='k', clip_on=False))
ax.text(x-0.75, y, 'male', fontsize=12, horizontalalignment='right', verticalalignment='center')
x, y = xy(16, 6)
ax.add_patch(Ellipse((x, y), width=w, height=h, facecolor=gender[-1], edgecolor='k', clip_on=False))
ax.text(x-0.75, y, 'female', fontsize=12, horizontalalignment='right', verticalalignment='center')
x, y = xy(17, 6)
ax.add_patch(Ellipse((x, y), width=w, height=h, facecolor=gender[0], edgecolor='k', clip_on=False))
ax.text(x-0.75, y, 'non-KITP', fontsize=12, horizontalalignment='right', verticalalignment='center')

ax = plot_axes[2]
x, y = xy(16, 7)
ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=male_only, clip_on=False))
ax.text(x-0.75, y, 'male-only', fontsize=12, horizontalalignment='right', verticalalignment='center')
x, y = xy(17, 7)
ax.add_patch(plt.Rectangle((x-1/2-w/4+dw, y-1/2+dh), num_authors[i]+w/2-2*dw, 1-2*dh, lw=0, color=female_only, clip_on=False))
ax.text(x-0.75, y, 'female-only', fontsize=12, horizontalalignment='right', verticalalignment='center')

plt.savefig('papers.pdf')

