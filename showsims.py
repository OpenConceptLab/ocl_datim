"""
Script to present DATIM SIMS metadata using the DatimShowSims class

Supported Formats: html, xml, csv, json
Supported Collections:
    sims3_facility, sims3_community, sims3_above_site
    sims2_facility, sims2_community, sims2_above_site
    sims_option_sets
OpenHIM Endpoint Request Format: /datim-sims?collection=____&format=____
"""
import sys
import settings
import datim.datimshow
import datim.datimshowsims


# Default Script Settings
verbosity = 0  # 0=none, 1=some, 2=all
run_ocl_offline = False  # Set to true to use local copies of ocl exports
export_format = datim.datimshow.DatimShow.DATIM_FORMAT_JSON
repo_id = 'SIMS3-Above-Site'

# OCL Settings - JetStream Staging user=datim-admin
oclenv = settings.oclenv
oclapitoken = settings.oclapitoken

# Optionally set arguments from the command line
if sys.argv and len(sys.argv) > 1:
    export_format = datim.datimshow.DatimShow.get_format_from_string(sys.argv[1])
    repo_id = sys.argv[2]

# Create Show object and run
datim_show = datim.datimshowsims.DatimShowSims(
    oclenv=oclenv, oclapitoken=oclapitoken, run_ocl_offline=run_ocl_offline, verbosity=verbosity)
datim_show.get(repo_id=repo_id, export_format=export_format)
