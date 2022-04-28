import os

import matplotlib.pyplot as plt
import pandas as pd

import populate_database
from config import subject, researchers_file, build_dir


def boxplot(df, subject, metrics, file, legends=None, vert=True, rows=1):
    """metrics should be a 2D matrix"""
    if not legends:
        legends = metrics

    plots_last_col = len(metrics) % rows
    cols = (len(metrics) // rows) + (1 if plots_last_col else 0)

    width = 2.5  # boxplot width
    height = 5  # boxplot height
    if not vert:
        width, height = height, width
    width *= cols  # figure width
    height *= rows  # figure height

    with plt.xkcd():
        plt.close('all')
        fig = plt.figure(figsize=(width, height))
        for i in range(len(metrics)):
            metric = metrics[i]
            ax = plt.subplot2grid((rows * 2, cols), (
            (i % rows) * 2 + (0 if i < len(metrics) - plots_last_col else rows - plots_last_col), i // rows), rowspan=2)
            df.boxplot(column=metric, ax=ax, widths=0.7, vert=vert)

            if vert:
                ax.set_xticklabels([legends[i]])
            else:
                ax.set_yticklabels([legends[i]])

            # data points
            for j, row in df.iterrows():
                x = 1
                y = row[metric]
                if not vert:
                    x, y = y, x
                ax.plot(x, y, 'ko', ms=4, alpha=0.2, zorder=3)

            # subject point
            if metric in subject:
                x = 1
                y = subject[metric]
                if not vert:
                    x, y = y, x
                ax.plot(x, y, 'ro', ms=8, zorder=4)

    plt.tight_layout()
    plt.savefig(build_dir + os.sep + file)
    print('Boxplot saved in file ' + file)


def main():
    # Comment the line bellow to remove the red dot indicating the performance of the subject in the following boxplot
    # subject.update(populate.all(subject['ID Lattes'], subject['ID Scholar']))
    # print('Red dot representing', subject["Nome"])

    df = pd.read_excel(researchers_file, dtype={'ID Lattes': object})

    # Métricas referentes a toda a carreira
    legends = [
        'Projetos',
        'Projetos\nCoordenados',
        'Orientações',
        'Orientações\nde Doutorado',
        'Bancas',
        'Bancas\nde Doutorado',
        'Publicações',
        'Publicações\nem Periódicos',
        'Publicações\nJCR',
        'Citações',
        'H-Index'
    ]
    metrics = [e.replace('\n', ' ') + ' (total)' for e in legends]
    boxplot(df, subject, metrics, 'fig-carreira.png', legends, rows=2)

    # Métricas referentes ao horizonte previamente configurado
    legends = [
        'Projetos',
        'Projetos\nCoordenados',
        'Orientações',
        'Orientações\nde Doutorado',
        'Bancas',
        'Bancas\nde Doutorado',
        'Publicações',
        'Publicações\nem Periódicos',
        'Citações',
        'Publicações\nJCR'
    ]
    metrics = [e.replace('\n', ' ') for e in legends]
    boxplot(df, subject, metrics, 'fig-horizonte.png', legends, rows=2)

    legends = [
        'Idade\nAcadêmica',
        'H-Index'
    ]
    metrics = [
        'Idade Acadêmica',
        'H-Index (total)'
    ]
    boxplot(df, subject, metrics, 'fig-idade.png', legends, vert=False)

    # Métricas normalizadas (anualizadas) referentes a toda a carreira
    legends = [
        'Projetos',
        'Projetos\nCoordenados',
        'Orientações',
        'Orientações\nde Doutorado',
        'Bancas',
        'Bancas\nde Doutorado',
        'Publicações',
        'Publicações\nem Periódicos',
        'Citações',
        'Publicações\nJCR',
        'H-Index'
    ]
    metrics = [e.replace('\n', ' ') + ' (anual)' for e in legends]
    boxplot(df, subject, metrics, 'fig-anual.png', legends, rows=2)

if __name__ == "__main__":
   main()