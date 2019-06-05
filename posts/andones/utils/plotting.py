from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.pyplot as plt
import seaborn as sb

import urllib
import pandas as pd


def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    '''
    Draws a half-court
    Shamelessly adapted from http://savvastjortjoglou.com/nba-shot-sharts.html 
    (and rotated to landscape...)
    '''

    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    outer_box = Rectangle((-470, -80), 190, 160, linewidth=lw, color=color, fill=False)

    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((-417.5, 0), 80, 80, theta1=270, theta2=90, linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-470, 220), 140, 0, linewidth=lw, color=color)
    corner_three_b = Rectangle((-470, -220), 140, 0, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the threes
    three_arc = Arc((-417.5, 0), 475, 475, theta1=292, theta2=68, linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [outer_box, restricted, corner_three_a, corner_three_b, three_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax



def plot_results(pickteam: str, andoneplayer: pd.DataFrame, numberofgames: int):
    '''
    Plots results of counting the and-one plays.
    '''

    plt.figure(figsize=(7,7.45))

    # Unique category labels: 'D', 'F', 'G', ...
    color_labels = andoneplayer['ID'].unique()
    name_labels = andoneplayer['last2'].unique()

    # List of RGB triplets
    rgb_values = sb.color_palette("Set1", 17)

    # Map label to RGB
    color_map = dict(zip(color_labels, rgb_values))

    # Count the total number.
    numandones = andoneplayer.shape[0]
    labels = [andoneplayer['last2'][i] for i in range(numandones)]

    # We'll map the scatter by player
    for i in range(andoneplayer['last2'].unique().shape[0]):
        andonesforhim = andoneplayer.loc[ (andoneplayer['last2'] == name_labels[i]) , : ]
        scatter = plt.scatter(andonesforhim.fg_loc_x, andonesforhim.fg_loc_y, 
                        c=andonesforhim['ID'].map(color_map), 
                        alpha=0.6, s=40, edgecolors='none', label= name_labels[i])

    draw_court(outer_lines=False)

    plt.xlim(-470,0)
    plt.ylim(-250,250)

    # I think these are the only two weird cases.
    if pickteam == "OKL":
        teamname = "OKC"
    elif pickteam == "BRO":
        teamname = "BKN"
    else:
        teamname = pickteam

    # let's rip some logos from the internet (sorry espn and yahoo)
    imgurl = "http://a.espncdn.com/i/teamlogos/nba/500/{}.png".format(teamname)
    img2   = "http://l.yimg.com/xe/i/us/sp/v/nba/teams/83/70x70/{}.png".format(teamname.lower())

    f = urllib.request.urlopen(imgurl)
    # currently yahoo is not letting us grab these alternate images.
    g = urllib.request.urlopen(imgurl)

    # plot them on our half court.
    a = plt.imread(f)
    b = plt.imread(g)
    plt.imshow(a, zorder=0, extent=[-120, 120, -120, 120])
    plt.imshow(b, origin = 'lower', zorder=0, extent=[-420, -360, -120, -180])

    # Clean up the axes.
    plt.tick_params(
        axis='both',       # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        left=False,
        labelleft=False,
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    leg = plt.legend(fontsize=8, frameon=True)
    frame = leg.get_frame()
    frame.set_facecolor('white')

    plt.suptitle("And Ones in 2018-2019 Season", fontsize = 18)
    plt.title("Team: " + pickteam.upper() + ", Number of Games: " + str(numberofgames))

    # Plot
    # plt.show()
    plt.savefig( pickteam + "_" + str(numberofgames) + "games.png")