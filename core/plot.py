import textwrap
from matplotlib.pyplot import Text

def format_plot(ax):
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                    box.width, box.height * 0.9])

    # wrap y axis labels
    for tick in ax.get_yticklabels():
        tick.set_wrap(True)

    # wrap title
    ax.set_title(ax.get_title(), wrap=True)

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=2)

    return ax