import subprocess
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent
PYTHON_FILE_DIR = ASSET_DIR / "../Module/PyGLtools/"

##can parameterize this in a sec

@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="browser",
    script = PYTHON_FILE_DIR / "browser.py",
    input_file_1 = ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2 = "",
)
@Parametrization.case(
    name="closest",
    script = PYTHON_FILE_DIR / "closest.py",
    input_file_1 = ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2 = ASSET_DIR / "fixtures/file.B.sorted.pgl",
)
@Parametrization.case(
    name="closest1D",
    script = PYTHON_FILE_DIR / "closest1D.py",
    input_file_1 = ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2 = ASSET_DIR / "fixtures/file.B.bed",
)
@Parametrization.case(
    name="formatbedpe",
    script = PYTHON_FILE_DIR / "column_flip.py",
    input_file_1 = ASSET_DIR / "fixtures/file.A.pgl",
    input_file_2 = "",
)
@Parametrization.case(
    name="condense",
    script = PYTHON_FILE_DIR / "condense.py",
    input_file_1 = ASSET_DIR / "fixtures/file.A.pgl",
    input_file_2 = "",
)
@Parametrization.case(
    name="conveRt",
    script = PYTHON_FILE_DIR / "conveRt.py",
    input_file_1 = ASSET_DIR / "fixtures/file.A.pgl",
    input_file_2 = "",
)
@Parametrization.case(
    name="coverage",
    script = PYTHON_FILE_DIR / "coverage.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2=ASSET_DIR / "fixtures/file.B.sorted.pgl",
)
@Parametrization.case(
    name="expand",
    script = PYTHON_FILE_DIR / "expand.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
input_file_2 = "",
)
@Parametrization.case(
    name="findLoops",
    script = PYTHON_FILE_DIR / "findLoops.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
input_file_2 = "",
)
@Parametrization.case(
    name="intersect",
    script = PYTHON_FILE_DIR / "intersect.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2=ASSET_DIR / "fixtures/file.B.sorted.pgl",
)
@Parametrization.case(
    name="intersect1D",
    script = PYTHON_FILE_DIR / "intersect1D.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2=ASSET_DIR / "fixtures/file.B.bed",
)
@Parametrization.case(
    name="juicebox",
    script = PYTHON_FILE_DIR / "juicebox.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2 = "",
)
@Parametrization.case(
    name="merge",
    script = PYTHON_FILE_DIR / "merge.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2 = "",
)
@Parametrization.case(
    name="samTopgl",
    script = PYTHON_FILE_DIR / "samTopgl.py",
    input_file_1=ASSET_DIR / "fixtures/test_sam.sam",
    input_file_2 = "",
)
@Parametrization.case(
    name="subtract",
    script = PYTHON_FILE_DIR / "subtract.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2=ASSET_DIR / "fixtures/file.B.sorted.pgl",
)
@Parametrization.case(
    name="subtract1D",
    script = PYTHON_FILE_DIR / "subtract1D.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2=ASSET_DIR / "fixtures/file.B.bed",
)
@Parametrization.case(
    name="window",
    script = PYTHON_FILE_DIR / "window.py",
    input_file_1=ASSET_DIR / "fixtures/file.A.sorted.pgl",
    input_file_2 = "",
)
def test_command_line(script,input_file_1,input_file_2):

    if input_file_2=="":
        res = subprocess.run(["python", script, "-a", input_file_1])
    else:
        res = subprocess.run(["python", script, "-a", input_file_1, "-b", input_file_2])

    res.check_returncode()