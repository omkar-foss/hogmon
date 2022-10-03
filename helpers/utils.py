"""
    Utility functions used in this project.
"""


# pylint: disable=consider-using-f-string
def convert_bytes(num):
    """ Converts RAM usage to humand readable format. """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, sym in enumerate(symbols):
        prefix[sym] = 1 << (i + 1) * 10
    for sym in reversed(symbols):
        if num >= prefix[sym]:
            value = float(num) / prefix[sym]
            return '%.1f%s' % (value, sym)
    return "%sB" % num
