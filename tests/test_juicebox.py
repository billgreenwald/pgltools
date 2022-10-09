import sys
sys.path.append('../Module/PyGLtools/')
from juicebox import juicebox
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(name="baseline", N=0,C=0,expected_results_file = str(ASSET_DIR/"fixtures/juicebox/juicebox_expected_results.txt"))
@Parametrization.case(name="baseline", N=7,C=0,expected_results_file = str(ASSET_DIR/"fixtures/juicebox/juicebox_expected_results.N7.txt"))
@Parametrization.case(name="baseline", N=0,C=7,expected_results_file = str(ASSET_DIR/"fixtures/juicebox/juicebox_expected_results.C7.txt"))
def test_juicebox(N,C,expected_results_file):

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"))

    args={
        "N":N,
        "C":C,
    }

    results = juicebox(A,args)
    results=results.split("\n")

    expected_results = [line.strip() for line in open(expected_results_file)]

    for res,e_res in zip(results,expected_results):
        assert res==e_res