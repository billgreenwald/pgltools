import sys
sys.path.append('../Module/PyGLtools/')
from closest import closest2D
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(name="no_annots", aAnnots=False, bAnnots=False,expected_results_file = str(ASSET_DIR/"fixtures/closest/closest_expected_results.pgl"))
@Parametrization.case(name="aAnnots", aAnnots=True, bAnnots=False,expected_results_file = str(ASSET_DIR/"fixtures/closest/closest_expected_results.aA.pgl"))
@Parametrization.case(name="bAnnots", aAnnots=False, bAnnots=True,expected_results_file = str(ASSET_DIR/"fixtures/closest/closest_expected_results.bA.pgl"))
@Parametrization.case(name="bothAnnots", aAnnots=True, bAnnots=True,expected_results_file = str(ASSET_DIR/"fixtures/closest/closest_expected_results.aA.bA.pgl"))
def test_closest_2d(aAnnots,bAnnots,expected_results_file):

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"))

    headerB,B=processFile(str(ASSET_DIR/"fixtures/file.B.sorted.annotated.pgl"))

    results = closest2D(A,B,headerA,headerB,aAnnots,bAnnots)
    results = sorted(results)

    new_header,expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results,expected_results)

    assert test_results
