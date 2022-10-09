import sys
sys.path.append('../Module/PyGLtools/')
from browser import browser
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(name="baseline", N=0,S=0,P=0,Q=0,C=0,tN="pgl_track",expected_results_file = str(ASSET_DIR/"fixtures/browser/browser_expected_results.bed"))
@Parametrization.case(name="Use_N", N=7,S=0,P=0,Q=0,C=0,tN="pgl_track",expected_results_file = str(ASSET_DIR/"fixtures/browser/browser_expected_results.N7.bed"))
@Parametrization.case(name="Use_S", N=0,S=7,P=0,Q=0,C=0,tN="pgl_track",expected_results_file = str(ASSET_DIR/"fixtures/browser/browser_expected_results.S7.bed"))
@Parametrization.case(name="Use_P", N=0,S=0,P=7,Q=0,C=0,tN="pgl_track",expected_results_file = str(ASSET_DIR/"fixtures/browser/browser_expected_results.P7.bed"))
@Parametrization.case(name="Use_Q", N=0,S=0,P=0,Q=7,C=0,tN="pgl_track",expected_results_file = str(ASSET_DIR/"fixtures/browser/browser_expected_results.Q7.bed"))
@Parametrization.case(name="Use_C", N=0,S=0,P=0,Q=0,C=7,tN="pgl_track",expected_results_file = str(ASSET_DIR/"fixtures/browser/browser_expected_results.C7.bed"))
@Parametrization.case(name="Use_tN", N=0,S=0,P=0,Q=0,C=0,tN="some_other_name",expected_results_file = str(ASSET_DIR/"fixtures/browser/browser_expected_results.tN.bed"))
def test_browser(N,S,P,Q,C,tN,expected_results_file):

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"))

    results = browser(A,N=N,S=S,P=P,Q=Q,C=C,tN=tN)
    results=results.split("\n")

    expected_results = [line.strip() for line in open(expected_results_file)]

    for res,e_res in zip(results,expected_results):
        assert res==e_res