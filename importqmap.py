"""
Script to import a QMAP into OCL. A QMAP is a JSON representation of a mapping between
a point of service system (POS) and a FHIR Questionnaire.

python importqmap.py -dmAtches4 --env=staging -t="your-token-here" --testmode -v1
    qmap-questionnaires/HIV_example_map_with_constants.json
"""
import json
import argparse
import datim.qmap


# Script constants
APP_VERSION = '0.1.0'
OCL_ENVIRONMENTS = {
    'qa': 'https://api.qa.openconceptlab.org',
    'staging': 'https://api.staging.openconceptlab.org',
    'production': 'https://api.openconceptlab.org',
    'demo': 'https://api.demo.openconceptlab.org',
}


# Argument parser validation functions
def ocl_environment(string):
    if string not in OCL_ENVIRONMENTS:
        raise argparse.ArgumentTypeError('Argument "env" must be %s' % ', '.join(OCL_ENVIRONMENTS.keys()))
    return OCL_ENVIRONMENTS[string]


# Script argument parser
parser = argparse.ArgumentParser("qmap", description="Import a QMAP into OCL")
parser.add_argument('-d', '--domain', help='ID of the QMAP domain', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--env', help='Name of the OCL API environment', type=ocl_environment)
group.add_argument('--envurl', help='URL of the OCL API environment')
parser.add_argument('-t', '--token', help='OCL API token', required=True)
parser.add_argument('--testmode', action="store_true", help='Enable test mode', default=False)
parser.add_argument(
    '-v', '--verbosity', help='Verbosity level: 0 (default), 1, or 2', default=0, type=int)
parser.add_argument('--version', action='version', version='%(prog)s v' + APP_VERSION)
parser.add_argument('file', type=argparse.FileType('r'), help='QMAP JSON document')
args = parser.parse_args()
with args.file as qmap_file:
    qmap_json = json.load(qmap_file)
    qmap = datim.qmap.Qmap(qmap_json=qmap_json)
ocl_env_url = args.env if args.env else args.envurl

# Display debug output
if args.verbosity > 1:
    import pprint
    print args
    pprint.pprint(json.loads(str(qmap)))

# Process the qmap import
bulk_import_task_id = qmap.import_qmap(
    domain=args.domain, ocl_env_url=ocl_env_url, ocl_api_token=args.token,
    test_mode=args.testmode, verbosity=args.verbosity)

if bulk_import_task_id:
    print 'Bulk import task ID:', bulk_import_task_id
