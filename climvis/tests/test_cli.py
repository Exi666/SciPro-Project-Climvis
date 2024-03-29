# Testing command line interfaces is hard. But we'll try
# At least we separated our actual program from the I/O part so that we
# can test that
import climvis
from climvis.cli import cruvis_io


def test_help(capsys):

    # Check that with empty arguments we return the help
    cruvis_io([])
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out
    print(captured.out)

    cruvis_io(['-h'])
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out

    cruvis_io(['--help'])
    captured = capsys.readouterr()
    assert 'Usage:' in captured.out


def test_version(capsys):

    cruvis_io(['-v'])
    captured = capsys.readouterr()
    assert climvis.__version__ in captured.out


def test_print_html(capsys):

    cruvis_io(['-l', '12.1', '47.3', '--no-browser'])
    captured = capsys.readouterr()
    assert 'File successfully generated at:' in captured.out

    cruvis_io(['-c', 'InnsBruck', '--no-browser'])
    captured = capsys.readouterr()
    assert 'File successfully generated at:' in captured.out

    cruvis_io(['-m', 'innsbruck', '7', '--no-browser'])
    captured = capsys.readouterr()
    assert 'File successfully generated at:' in captured.out


def test_error(capsys):

    cruvis_io(['-l', '12.1'])
    captured = capsys.readouterr()
    string = 'cruvis --loc needs lon and lat parameters!'
    assert string in captured.out

    cruvis_io(['-c'])
    captured = capsys.readouterr()
    string = 'cruvis --city needs a city name!'
    assert string in captured.out

    cruvis_io(['-m', 'xxx'])
    captured = capsys.readouterr()
    string = 'cruvis --meteo needs station and duration parameters'
    assert string in captured.out
