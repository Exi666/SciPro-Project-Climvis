import webbrowser
import sys
import climvis
from climvis import plot_acinn

HELP = """cruvis: CRU data visualization at a selected location.

Usage:
   -h, --help            : print the help
   -v, --version         : print the installed version
   -l, --loc [LON] [LAT] : the location at which the climate data must be
                           extracted
   -c, --city [City]     : the location at which the climate data must be
                           extracted
   -m, --meteo [station] [duration]:
                           load meteorological data from ACINN,
                               stations: innsbruck, sattelberg, obergurgl,
                                         ellboegen
                               durations: 1, 3, 7 (days)
   --no-browser          : the default behavior is to open a browser with the
                           newly generated visualisation. Set to ignore
                           and print the path to the html file instead
"""


def cruvis_io(args):
    """The actual command line tool.

    Parameters
    ----------
    args: list
        output of sys.args[1:]
    """

    if len(args) == 0:
        print(HELP)
    elif args[0] in ['-h', '--help']:
        print(HELP)
    elif args[0] in ['-v', '--version']:
        print('cruvis: ' + climvis.__version__)
        print('License: public domain')
        print('cruvis is provided "as is", without warranty of any kind')
    elif args[0] in ['-l', '--loc']:
        if len(args) < 3:
            print('cruvis --loc needs lon and lat parameters!')
        elif len(args) >= 3:
            lon, lat = float(args[1]), float(args[2])
            html_path = climvis.write_html(lon, lat)
            if '--no-browser' in args:
                print('File successfully generated at: ' + html_path)
            else:
                webbrowser.get().open_new_tab(html_path)
    elif args[0] in ['-c', '--city']:
        if len(args) < 2:
            print('cruvis --city needs a city name!')
        elif len(args) >= 2:
                lat, lon, elevation = climvis.core.city_coord(args[1])
                html_path = climvis.write_html(lon, lat)
                if '--no-browser' in args:
                    print('File successfully generated at: ' + html_path)
                else:
                    webbrowser.get().open_new_tab(html_path)
    elif args[0] in ['-m', '--meteo']:
        if len(args) < 3:
            print('cruvis --meteo needs station and duration parameters')
            return
        if len(args) >= 3:
            station = args[1]
            duration = args[2]
            html_path = plot_acinn.plot_both(station, duration)
            if '--no-browser' in args:
                print('File successfully generated at: ' + html_path)
            else:
                webbrowser.get().open_new_tab(html_path)
    else:
        print('cruvis: command not understood. '
              'Type "cruvis --help" for usage options.')


def cruvis():
    """Entry point for the cruvis application script"""

    # Minimal code because we don't want to test for sys.argv
    # (we could, but this is too complicated for now)
    cruvis_io(sys.argv[1:])
