import matplotlib.pyplot as plt
import base64
from io import BytesIO

import numpy as np
from matplotlib import style


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(labels, sis, lcps):
    x = np.arange(len(labels))
    width = 0.35
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, sis, width, label='Search Index')
    rects2 = ax.bar(x + width / 2, lcps, width, label='Largest Contentful Paint')
    ax.set_ylabel('Time [ms]')
    ax.set_title('Chart of SI and LCP times for the given URLs')
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    graph = get_graph()
    return graph
