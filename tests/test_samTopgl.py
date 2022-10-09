import sys
sys.path.append('../Module/PyGLtools/')
from samTopgl import samTopgl, formatContacts
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

def test_samTopgl():

    #get files
    input_file = str(ASSET_DIR/"fixtures/test_sam.sam")
    expected_results_file = str(ASSET_DIR/"fixtures/samToPgl/samToPgl_expected_results.pgl")

    header, res = samTopgl(input_file, "\t", 1000)
    results = [line.split() for line in formatContacts(res)]
    results = sorted(results, key=lambda x: (x[0], int(x[1]), int(x[2]), x[3], int(x[4]), int(x[5])))

    #compare to real results
    expected_results = [line.strip().split() for line in open(expected_results_file)]

    test_results = compare_test_outputs(results,expected_results)

    assert test_results
