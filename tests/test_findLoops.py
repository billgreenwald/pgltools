import sys
sys.path.append('../Module/PyGLtools/')
from findLoops import findLoops
from pgltools_library import  processFile, processBedFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(name="baseline", expected_results_file = str(ASSET_DIR/"fixtures/findLoops/findLoops_expected_results.bed"))
def test_findLoops(expected_results_file):

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"))

    results = findLoops(A)
    results = sorted(results)

    new_header,expected_results = processBedFile(expected_results_file)

    test_results = compare_test_outputs(results,expected_results)

    assert test_results
