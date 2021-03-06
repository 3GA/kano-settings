#
# about.py
#
# Copyright (C) 2014, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Contains the about screen backend functions


from kano.utils.shell import run_cmd
from kano.utils.hardware import get_board_property, get_rpi_model


def _split_helper(os, devstage, number="?", name="?", *args):
    if args:
        print "DEV ERROR: Too many values in version string!"
    return os, devstage, number, name


def get_current_version():
    with open('/etc/kanux_version', 'r') as f:
        output = f.read().strip()
        dummy1, dummy2, number, name = _split_helper(*output.split("-"))
    return number, name


def get_space_available():
    out, err, rc = run_cmd('df -h / | tail -1')
    device, size, used, free, percent, mp = out.split()

    info = {
        'used': '',
        'total': ''
    }

    if not err:
        info['used'] = used
        info['total'] = size

    return info


def get_temperature():
    temperature = None
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        output = f.read().strip()
        temperature = int(output) / 1000.0
    return temperature


def get_model_name():
    model = get_rpi_model()
    model_name = get_board_property(model, 'name')

    return model_name
