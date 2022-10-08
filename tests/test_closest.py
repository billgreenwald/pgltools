import sys
sys.path.append('../Module/PyGLtools/')
from closest import closest2D
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

# @Parametrization.autodetect_parameters()
# @Parametrization.case(name="testA", op='plus', value=3)
def test_closest_2d():

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.sorted.pgl"))

    headerB,B=processFile(str(ASSET_DIR/"fixtures/file.B.sorted.pgl"))

    results = closest2D(A,B,headerA,headerB,False,False)

    new_header,expected_results = processFile(str(ASSET_DIR/"fixtures/closest/closest_expected_results.pgl"))

    assert compare_test_outputs(results,expected_results)
