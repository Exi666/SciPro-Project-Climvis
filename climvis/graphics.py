import matplotlib.pyplot as plt


def plot_annual_cycle(df, filepath=None):

    z = df.grid_point_elevation
    df = df.loc['1981':'2010']
    df = df.groupby(df.index.month).mean()
    df.index = list('JFMAMJJASOND')

    f, ax = plt.subplots(figsize=(6, 4))

    df['pre'].plot(ax=ax, kind='bar', color='C0', label='Precipitation', rot=0)
    ax.set_ylabel('Precipitation (mm mth$^{-1}$)', color='C0')
    ax.tick_params('y', colors='C0')
    ax.set_xlabel('Month')
    ax = ax.twinx()
    df['tmp'].plot(ax=ax, color='C3', label='Temperature')
    ax.set_ylabel('Temperature (\u00b0C)', color='C3')
    ax.tick_params('y', colors='C3')
    title = 'Climate diagram at location ({}\u00b0, {}\u00b0)\nElevation: {} m a.s.l'
    plt.title(title.format(df.lon[0], df.lat[0], int(z)),
              loc='left')
    plt.tight_layout()

    if filepath is not None:
        plt.savefig(filepath, dpi=150)
        plt.close()

    return f

# Plot time series of temperature and linear trend
def plot_time_line(df, filepath=None):

    z = df.grid_point_elevation
    dfy = df.groupby(df.index.year).mean()

    years=dfy.index
    temp_slope, temp_intercept, temp_rvalue, temp_pvalue, temp_stderr = stats.linregress(years, dfy['tmp'])

    f, ax = plt.subplots(figsize=(6, 4))

    plt.plot(years, dfy['tmp'], 'b', label='annual mean')
    plt.plot(years, temp_intercept + temp_slope * years, 'r', label='linear trend')

    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature (\u00b0C)')
    title = 'Temperature time series at location ({}\u00b0, {}\u00b0)\nElevation: {} m a.s.l'
    plt.title(title.format(df.lon[0], df.lat[0], int(z)), loc='left')
    plt.legend(loc='best')

    if filepath is not None:
        plt.savefig(filepath, dpi=150)
        plt.close()

    return f

