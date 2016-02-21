from libcloud_api import libcloud_api
import logging


def main(args):
    if (args.debug is not None):
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

    api = libcloud_api()
    api.build_controllers()

if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    main(args)
