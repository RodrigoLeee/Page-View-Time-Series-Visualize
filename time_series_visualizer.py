import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
# Filtra DIAS em que as VISUALIZAÇÕES estão fora do intervalo de 2.5% e 97.5%
# DIAS QUE VISUALIZAÇÕES == abaixo de 2.5%, TCHAU TCHAU
# DIAS QUE VISUALIZAÇÕES == acima de 97.5%, TCHAU TCHAU
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    # Cria line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    # df.index no EIXO X (series data)
    # df['value'] no EIXO Y
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    # TITULO do gráfico
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    # eixo X = Data (dia)
    ax.set_xlabel('Date')
    # eixo Y = VISUALIZAÇÕES (número de visualizações)
    ax.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Prepare data for bar plot
    # Cria uma cópia do dataframe em df_bar
    df_bar = df.copy()
    
    # EXTRAI ANOS a partir do index
    df_bar['year'] = df_bar.index.year
    # EXTRAI mes a partir do index
    df_bar['month'] = df_bar.index.month_name()

    # Group by year and month, then calculate the mean
    # Agrupa por ANO e MÊS
    # Calcula a média das VISUALIZAÇÕES
    # .unstack() = Cria um NOVO DATAFRAME
    # .unstack() novo datframe é baseado no ANO e no MES
    # .unstack() = cada ANO É LINHA, e MES É COLUNA
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Reorder the months
    # Ordena os meses
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # ORGANIZA AS COLUNAS/MESES DO DATAFRAME
    df_bar = df_bar[month_order]

    # Draw bar plot
    # Cria bar plot
    fig = df_bar.plot(kind='bar', figsize=(12, 6)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.title('Average Daily Page Views per Month')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    # cria um copia do dataframe em df_box
    df_box = df.copy()
    # RESETA O INDEX de df_box
    # inplace significa que altera o dataframe df_box 
    df_box.reset_index(inplace=True)

    # Cria uma coluna ANO a partir da coluna DATE
    df_box['year'] = [d.year for d in df_box.date]
    # Cria uma coluna MÊS a partir da coluna DATE
    # Formata cada mês para 3 letras
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
