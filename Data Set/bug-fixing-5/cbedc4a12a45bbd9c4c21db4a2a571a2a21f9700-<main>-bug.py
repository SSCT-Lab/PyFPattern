def main():
    if (not HAS_AZURE):
        sys.exit("The Azure python sdk is not installed (try 'pip install azure>=2.0.0rc5') - {0}".format(HAS_AZURE_EXC))
    if (LooseVersion(azure_compute_version) < LooseVersion(AZURE_MIN_VERSION)):
        sys.exit('Expecting azure.mgmt.compute.__version__ to be {0}. Found version {1} Do you have Azure >= 2.0.0rc5 installed?'.format(AZURE_MIN_VERSION, azure_compute_version))
    AzureInventory()