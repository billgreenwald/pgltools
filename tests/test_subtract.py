import sys
sys.path.append('../Module/PyGLtools/')
from subtract import subtract2D
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(name="subtract_b_from_a", a_pgl_file=str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"),
                      b_pgl_file=str(ASSET_DIR/"fixtures/file.B.sorted.annotated.pgl"),
                      expected_results_file = str(ASSET_DIR/"fixtures/subtract/subtract_expected_results.sub_b_from_a.pgl"))
@Parametrization.case(name="subtract_a_from_b", a_pgl_file=str(ASSET_DIR/"fixtures/file.B.sorted.annotated.pgl"),
                      b_pgl_file=str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"),
                      expected_results_file = str(ASSET_DIR/"fixtures/subtract/subtract_expected_results.sub_a_from_b.pgl"))
def test_intersect_2d(a_pgl_file,b_pgl_file,expected_results_file):

    #get files
    headerA,A=processFile(a_pgl_file)

    _,B=processFile(b_pgl_file)

    args={}

    results = subtract2D(A,B,args,headerA)
    results = sorted(results)

    new_header,expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results,expected_results)

    assert test_results
