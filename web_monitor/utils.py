import matplotlib.pyplot as plt
import base64
from io import BytesIO
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


def get_plot(x, y, z):
    plt.switch_backend('AGG')
    plt.style.use('seaborn-whitegrid')
    plt.figure(figsize=(10, 5))
    plt.title('Wykres czasów LCP i SI dla podanego URL')
    plt.scatter(x, y, cmap='C1', label='Search Index')
    plt.scatter(x, z, cmap='C2', label='Largest Contentful Paint')
    plt.xticks(rotation=45)
    plt.xlabel('Data i godzina wykonania testu')
    plt.ylabel('Czas [ms]')
    plt.tight_layout()
    graph = get_graph()
    return graph
