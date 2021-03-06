"""
Script to present DATIM MOH metadata -
NOTE This only shows the global PEPFAR DATIM MOH Alignment indicators, without mapping to country indicators.
To view country mappings, use the IMAP export script and mediator.

Supported Formats: html, xml, csv, json
OpenHIM Mediator Request Format: /datim-moh?period=____&format=____

This script fetches an export from OCL for the latest released version of the specified
collection. If it seems like you're looking at old data, check the collection version first.
"""
import argparse
import datim.datimshow
import datim.datimshowmoh
import common


# Script argument parser
parser = argparse.ArgumentParser("moh", description="Export MOH data from OCL")
parser.add_argument('-f', '--format', help='Format of Export', default='csv')
parser.add_argument('-p', '--period', help='Period of MOH Export', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--env', help='Name of the OCL API environment', type=common.ocl_environment)
group.add_argument('--envurl', help='URL of the OCL API environment')
parser.add_argument('-t', '--token', help='OCL API token', required=False)
parser.add_argument(
    '-v', '--verbosity', help='Verbosity level: 0 (default), 1, or 2', default=0, type=int)
parser.add_argument('--version', action='version', version='%(prog)s v' + common.APP_VERSION)
args = parser.parse_args()
ocl_env_url = args.env if args.env else args.env_url

# Create Show object and run
datim_show = datim.datimshowmoh.DatimShowMoh(
    oclenv=ocl_env_url, oclapitoken=args.token, verbosity=args.verbosity)
datim_show.get(period=args.period, export_format=args.format)
