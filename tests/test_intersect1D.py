import sys
sys.path.append('../Module/PyGLtools/')
from intersect1D import intersect1D
from pgltools_library import  processFile, processBedFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(name="baseline", allA=False, bA=False, wa=False, wb=False, v=False, u=False,
                      d=0, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.pgl"))
@Parametrization.case(name="all_annotations", allA=True, bA=False, wa=False, wb=False, v=False, u=False,
                      d=0, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.allA.pgl"))
@Parametrization.case(name="b_annotations", allA=False, bA=True, wa=False, wb=False, v=False, u=False,
                      d=0, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.bA.pgl"))
@Parametrization.case(name="dashWa", allA=False, bA=False, wa=True, wb=False, v=False, u=False,
                      d=0, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.wa.pgl"))
@Parametrization.case(name="dashWb", allA=False, bA=False, wa=False, wb=True, v=False, u=False,
                      d=0, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.wb.pgl"))
@Parametrization.case(name="dashV", allA=False, bA=False, wa=False, wb=False, v=True, u=False,
                      d=0, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.v.pgl"))
@Parametrization.case(name="dashU", allA=False, bA=False, wa=False, wb=False, v=False, u=True,
                      d=0, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.u.pgl"))
@Parametrization.case(name="Distance_5,000", allA=False, bA=False, wa=False, wb=False, v=False, u=False,
                      d=5000, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.d5000.pgl"))
@Parametrization.case(name="Distance_500,000", allA=False, bA=False, wa=False, wb=False, v=False, u=False,
                      d=500000, anchA="Intersected_Anchor", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.d500000.pgl"))
@Parametrization.case(name="anchorIntersectColumnName", allA=False, bA=False, wa=False, wb=False, v=False, u=False,
                      d=0, anchA="some_arbitrary_name", expected_results_file = str(ASSET_DIR/"fixtures/intersect1D/intersect1D_expected_results.anchA.pgl"))
def test_intersect_1d(allA,bA,wa,wb,v,u,d,anchA,expected_results_file):

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.sorted.annotated.pgl"))

    headerB,B=processBedFile(str(ASSET_DIR/"fixtures/file.B.annotated.bed"))

    args={
        "allA":allA,
        "bA":bA,
        "wa":wa,
        "wb":wb,
        "v":v,
        "u":u,
        "d":d,
        "anchA":anchA,
    }

    results = intersect1D(A,B,args,headerA,headerB)
    results = sorted(results)

    new_header,expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results,expected_results)

    assert test_results
