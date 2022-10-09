import sys
sys.path.append('../Module/PyGLtools/')
from window import window
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(name="window1", window1="chr10:550000-570000", window2="%#$",expected_results_file = str(ASSET_DIR/"fixtures/window/window_expected_results.window1_chr10_550000_570000.pgl"))
@Parametrization.case(name="window2", window1="%#$", window2="chr10",expected_results_file = str(ASSET_DIR/"fixtures/window/window_expected_results.window2_chr10.pgl"))
@Parametrization.case(name="both_windows", window1="chr10:550000-570000", window2="chr10",expected_results_file = str(ASSET_DIR/"fixtures/window/window_expected_results.window1_chr10_550000_570000.window2_chr10.pgl"))
def test_closest_2d(window1,window2,expected_results_file):

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"))

    args={
        "window1":window1,
        "window2":window2
    }

    results = window(A,args)
    results = sorted(results)

    new_header,expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results,expected_results)

    assert test_results
