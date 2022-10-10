![pgltools logo](/Images/logo.png?raw=true)

Pgltools is a genomic arithmetic software suite designed for working with paired-loci genomic data, such as contacts from a Hi-C or ChIA-PET experiment, and utilizes the PGL file format. Pgltools is available both as a tool suite for the UNIX command line, and as a python module.

If you wish to contribute and need to install the required dependencies for tests, you can use poetry and run `poetry install` in the root of the repo to install all the needed deps.  Or, just `pip install pytest-parameterized` for the only needed package.

## Citation

Please cite the following paper when citing pgltools:  

<b>Pgltools: a genomic arithmetic tool suite for
manipulation of Hi-C peak and other chromatin interaction data</b>

https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1621-0

## Table of Contents
1. [Software Dependencies](#software-dependencies)
2. [Installation](#installation)
3. [The PGL File Format](#the-pgl-file-format)
4. [The PyGLtools Module](#the-pygltools-module)
5. [Formatting Operations](#file-formatting-and-converting-operations)
6. [2D Operations](#2d-operations)
7. [1D Operations](#1d-operations)
8. [Example Pipelines](#example-pipelines)
9. [Useful Parameter Combinations](#useful-parameter-combinations)

## Software Dependencies

pgltools is written in Python 3.10, and does not require any external packages.  As such, all operations, except for coverage, have been tested in pypy.  Pypy is an alternative python compiler, and is recommended for use with this tool suite.  Pypy is available on most linux distributions, and can be installed via "apt-get" or "yum".  <b>By utilizing pypy, pgltools sees a 5-7x speed up on all operations, and about a 25% decrease in the amount of RAM utilized</b>.

The UNIX version of pgltools will automatically detect if pypy is installed, and will run through pypy if so.  Otherwise, it will default to python.

## Installation:

The pgltools tool suite is designed to be used through the bash interface.  A few commands (mainly sorting commands) are not written in python, but are rather written in bash.  <b>To ensure pgltools runs with the proper functionality, please utilize the pgltools/sh folder, rather than the direct python scripts in the pgltools/Module/PyGLtools folder</b>.  Following the Unix installation directions immediately below will ensure that the /sh folder is used.

### UNIX:
To install pgltools, clone the directory to the desired location, and add the /sh folder to your system PATH variable.  Methods can then be called with pgltools [command].  To view the avaiable commands, or the available arguments for a command, call pgltools with no command, or call pgltools [command] with no arguments.

### Python Module:
The python module version of pgltools, PyGLtools, is avaiable for installation both from this repository, and on PyPI.

#### PyPI
To install PyGLtools from PyPI, simply run: 
```
pip install PyGLtools
```

#### From github
cd into the "Module" subdirectory and run:
```
python setup.py install
```

## The PGL file format:

The PGL file format is a 1-based file consisting of 6 columns, plus any additional annotations.  The six required columns are locus A chromosome, locus A start, locus A end, locus B chromosome, locus B start, locus B end.  After these six columns, any additional columns may be included as annotations.  These columns will be perserved by pgltools, and can be manipulated with pgltools merge.  As annotations are arbitrary, header lines may be indcluded in pgl files by starting a line with "#" and will be carried over from the "A" file when using pgltools methods.  **In addition to the six required columns, pgl files are formatted such that each locus A comes before its partner locus B.**  The included **formatbedpe** operation will fix any loci violating this rule in addition to sorting the file.  Example pgl files are provided below:

<b>Proper Formatting</b>:
```
#some header information
#some more header information
chr10 1    100   chr10 1000 10000 Annotation1 Annotation2
chr10 1000 10000 chr11 1    100   Annotation1 Annotation2
chr11 100  1000  chr11 2000 2200  Annotation1 Annotation2
...
```

<b>Improprer Formatting</b> (locus A comes after locus B):
```
chr10 1000 10000 chr10 1 100 Annotation1 Annotation2
...
```

## The PyGLtools Module:
Most method names in PyGLtools are the same as the UNIX tool suite (2D methods that have a 1D analog are explicitly named in the python module).  Command line arguments are instead function arguments, and can be viewed as one would view the docstring of a particular function (usually through tab completion), and inputs and outputs can be viewed in the docstring.  All arguments, their format, and what they do, is discussed below in the Methods section of this readme.  All functions take at least one PyGL object as an input.

### The PyGL and PyGL-bed objects:

The PyGLtools module utilizes two dimensional lists to house PGL information, and a dict of lists to house Bed information.  These types are the underlying structure to the pgltools .py files utilized by the command line interface.  These objects will work with any PyGLtools function that requires their input, and are loaded via the read_PGL and read_BED functions.  These functions return two arguments, first the header of the file, and second the PyGL or PyGL_BED object.  The explicit format of the objects are:

PyGL
```
[[chrA,startA,stopA,chrB,startB,stopB,[list of annotations]],[...]]
```
PyGL-bed
```
{chr:[start,stop,[list of annotations],[...]]
 ...
}
```

### Recommended Usage

The PyGLtools package utilizes helper functions that are hidden to its namespace; it is therefore recommended to import the module and define its namespace.  As an example, to import the module, read two files, intersect them, and save their output into a new PyGL object, one would use the following:

```
import PyGLtools as pygl
headerA,pglA=pygl.read_PGL(someFilePath)
headerB,pglB=pygl.read_PGL(someOtherFilePath)
intersected=pygl.intersect2D(pglA,pglB)
```

## Methods:

## File Formatting and Converting Operations:

### formatbedpe:

Converts a bedpe (as defined by bedtools) or similarly formated file to a sorted pgl file:
```
pgltools formatbedpe [FILE]
```
Example, storing output to output.pgl:
```
pgltools formatbedpe myFile.bedpe > output.pgl
```

### formatTripSparse:

Converts a set of Triplet Sparse Matrix files to a pgl file:
```
pgltools formatTripSparse [options]
```
options:
```
-ts [FILE]:  Triplet Sparse Matrix file.  
-an [FILE]:  Annotation file accompanying Triplet Sparse Matrix File.
```
Example, storing output to output.pgl:
```
pgltools formatTripSparse -ts myFile.tripSparse -an myFile.annotations > output.pgl
```

### browser:

Formats a pgl file for viewing in the UCSC Genome Browser.  Columns are 1 indexed:
```
pgltools browser [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-N [COLUMN_NUMBER]:  Specify column for naming entry.  If not given, entries are named Contact_#
-S [COLUMN_NUMBER]:  Specify column for scoring entry.  If not given, entries are scored uniformly
-R [COLUMN_NUMBER]:  Specify column for coloring entry.  If not given, entries are all colored black
-P [COLUMN_NUMBER]:  Specify column for pValue of entry.  If not given, pValue is ignored
-Q [COLUMN_NUMBER]:  Specify column for qValue of entry.  If not given, qValue is ignored
-tN [COLUMN_NUMBER]: Track name. If not given, track is named "pgl_track"
```
Example, storing output to output.bed:
```
pgltools browser myFile.pgl > output.bed
```

### conveRt:

Formats a pgl file for use with the GenomicInteractions R package.  Use the "chiapet.tool" format while importing. Columns are 1 indexed:
```
pgltools conveRt [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-N [COLUMN_NUMBER]:  Specify column for read counts.  If not given, counts are set to 0
-P [COLUMN_NUMBER]:  Specify column for scoring entry.  If not given, pValues are set to 0
-Q [COLUMN_NUMBER]:  Specify column for coloring entry.  If not given, q Values are set to 0
```
Example, storing output to output.pgl:
```
pgltools conveRt myFile.pgl > output.chiapetTool
```

### juicebox:

Formats a pgl file for use visualization with JuiceBox.  Columns are 1 indexed:
```
pgltools juicebox [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-N [COLUMN_NUMBER]:  Specify column for entry name .  If not given, names are "Contact_[Line #]"
-C [COLUMN_NUMBER]:  Specify column for entry color.  If not given, colors are set to black
```
Example, storing output to output.pgl:
```
pgltools juicebox -a myFile.pgl -N 7 > output.chiapetTool
```
### findLoops:

Outputs regions from anchor to anchor for each PGL entry as a BED file.  Intra-chromosomal PGLs will have one entry of col1, col2, col6.  Inter-chromosomal regions will have two entries, one for each anchor:
```
pgltools findLoops [FILE]
```
Example, storing output to output.pgl:
```
pgltools findLoops myFile.pgl > output.bed
```

### condense:

Outputs a two BED entries per PGL, one for each anchor.  Annotations will be written for both entries.:
```
pgltools condense [FILE]
```
Example, storing output to output.pgl:
```
pgltools condense myFile.pgl > output.bed
```

### sort:
Sorts a pgl file.  A sorted pgl file is sorted by columns 1-6 in order with columns 1 and 4 treated as strings.  The sort2D file will not flip paired-loci that have locus B occuring before locus A as a pgl file is required to follow this format.  If a file does not follow this formatting, use the "formatbedpe" operation.  Most commands below require sorted files.  <b> Note that the PyGLtools command for sort is named pyglSort to avoid collisions when importing * </b>.  Syntax:
```
pgltools sort [FILE]
```
Example, storing output to output.pgl:
```
pgltools sort myFile.pgl > output.pgl
```

## 2D Operations:

![pgltools merge](/Images/Merge.PNG?raw=true)
Merges adjacent loci within a pgl file.  Requires sorted input. All operations can only utilize the annotation columns.  If no annotations are present in the file, one can quickly add a dummy column to use for count via:
```
awk '{print $0 "\t."}' myFile.pgl > myNewFile.pgl
```
If annotations are present, use any annotation column (7 or higher).  A header will be automatically generated for the resulting file unless -noH is used.  Syntax:
```
pgltools merge [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-c [COLUMN_NUMBER]:  perform an operation on the given column when merged
-o [OPERATION]:  perform the specified operation when merging.  operations listed below
-delim: change the delimeter for -o collapse and -o distinct.  Default is ","
-d: Distance allowed between loci for merging.  default 0
-noH: Do not create a header for the output file.
```
operations (*NOTE* that the program assumes you have passed columns with correct types for the desired operations).  A comma separated list may be given (ie -c 10,10,11,12 -o sum,min,sum,collapse):  
* sum -- sum the values from the specified column.  *Numeric*
* min -- find the minimum value from the specified column.  *Numeric*
* max -- find the maximum value from the specified column.  *Numeric*
* absmin -- find the minimum magintude value and report the signed value (ie [-1,-7,9] will report -1). *Numeric*
* absmax -- find the maximum magintude value and report the signed value (ie [-1,-7,9] will report 9).  *Numeric*
* mean -- find the mean of the values from the specified column.  *Numeric*
* median -- find the median of the values from the specified column. *Numeric*
* collapse -- combine the annotations from the column as a comma separated list. *String*
* distinct -- combine the unique annotations from the column as a comma separated list. *String*
* count -- Return the number of merged loci.  *NA*
* count_distinct -- Return the number of unique annotations from the specified column. *String*

Example, storing output to output.pgl:
```
pgltools merge -a myFile.pgl -c 10,10,11,12 -o min,max,count,collapse -d 200 > output.pgl
```
Example, storing output to output.pgl, reading input from stdin:
```
[some command] | pgltools merge -stdInA myFile.pgl > output.pgl
```

![pgltools intersect](/Images/Intersect.PNG?raw=true)
Finds the overlapping loci of two pgl files.  If using -m or -mc, the seventh column will contain the id of the file the locus came from.  Requires sorted inputs.  Syntax:
```
pgltools intersect [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
-d:  Distance to allow for intersections.  Default 0
-v:  Returns entries in A that do not overlap any entries in B
-m:  Returns the union of loci instead of the intersection of loci
-mc:  Returns only unions of loci where an overlap between files occurred
-wa: Returns the original loci from A if an overlap occurs.
-wb: Returns the original loci from B if an overlap occurs.
-wo: Returns the original loci from A and B if an overlap occurs, as well as the number of bases overlapping per anchor
-u: Report an overlap happened.  An entry will be generated per overlap.
-bA:  Keep the annotations from file B instead of file A
-allA:  Keep the annotations from both files.  Annotations from A will come first.
```
Example, storing output to output.pgl:
```
pgltools intersect -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

![pgltools windowpgl](/Images/Window.PNG?raw=true)
Finds the loci with locus A fully contained in window1 and locus B fully contained window2.  Alternatively, only 1 window can be provided.  Syntax:
```
pgltools intersect [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-window1 [chr:start-stop]
-window2 [chr:start-stop]
```
Example, storing output to output.pgl:
```
pgltools windowpgl -a myFile.pgl -window1 chr1:1-10000 -window2 chr10:1000-100000 > output.pgl
```

![pgltools subtract](/Images/Subtract.PNG?raw=true)
Finds the parts of loci from file A that do not overlap loci from file B.  Requires sorted input. Syntax:
```
pgltools subtract [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools subtract -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

![pgltools closest](/Images/Closest.PNG?raw=true)
Finds the closest loci in file B for each loci in file A.  Locus A chromosomes must match, and locus B chromosomes must match to be considered for distance.  If no loci share the same chromosomal composition, the paired-loci from file A will not be matched with a paired-loci from file B.  The output fil will have 13 columns, with annotations overwritten: the six columns from file A followed by the six columns from file B if a paired-loci was found, followed by the distance between the two PGLs, else 7 ".".  Syntax:
```
pgltools closest [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools closest -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

![pgltools coverage](/Images/Coverage.PNG?raw=true)
Finds the coverage of file B on file A.  Loci from file B must be fully contained to be counted in coverage calculation.  Syntax:
```
pgltools coverage [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
-z: Report entries that have 0 coverage
```
Example, storing output to output.pgl:
```
pgltools coverage -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

### sam2pgl:
Converts a sam file to a pgl file.  A single paired end sam file must be used where paired end reads have the same name, or have the same name leading up to a delimeter which can be specified.  File must be sorted on the read name column (first column).  Reads with two alignments will be transformed into paired-loci.  Reads with greater than two alignments (which can occur in Hi-C from multiple contacts) will use the furthest end points on both chromosomes.  If all reads align to the same chromosomes, the specified insert size will be used to split apart loci ends.  If all read alignments are within the insert size, no paired-loci entry will be generated in the resulting pgl file.  Single alignment reads will be ignored.  As of now, soft-clipped reads are not supported. The sam file Syntax:
```
pgltools sam2pgl [options]
```
options:
```
-a [FILE]:  convert [FILE] to a pgl file.  
-stdInA:  convert the sam file piped from stdin to a pgl file.
-delim [DELIM]:  specify the delimeter in the read name
-ins [INT] : specify the insert size for multiple alignments to a single chromosome.  Default 1000
```
Example, storing output to output.pgl:
```
pgltools sam2pgl -a myFile.sam > output.pgl
```
Example, storing output to output.pgl, using BAM and samtools with a pipe:
```
samtools view myFile.sam | pgltools sam2pgl -stdInA > output.pgl
```

### expand:
Expands the start and end of both loci for each loci by the provided distance.  A genome file can be provided to prevent invalid positions from occuring within the file.  Syntax:
```
pgltools expand [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-d [INT]:  size to expand by.  
-g [FILE]:  genome file formatted as below.
```
Genome file formatting:
```
chr1 endPosition
chr2 endPosition
chr3 endPosition
...
```
Example, storing output to output.pgl:
```
pgltools expand -a myFile.pgl -d 200 -g myGenomeFile > output.pgl
```

## 1D Operations:

All 1D operations will internally convert bed entries to 1-based start and stop entries so that they can be compared properly to PGL files.  As bed files have redundancy in single base pair long entries (chr1  10  10   is equivalent to   chr1  9   10), these entries types of entries will both be converted to the same entry in pgltools (in this case, chr1  10  10). 

![pgltools intersect1D](/Images/Intersect1D.PNG?raw=true)
Finds the intersection of loci from a pgl file and a standard bed file.  Following the standard 6 columns, the seventh column holds the locus (A, B, or AB) the bed region overlapped. If a single PGL entry overlaps multiple BED entries, a resulting entry will be generated for each intersection event.  Requires a sorted pgl file. Note that when using -d, it is possible to have the resulting entry have the end position before the start position if the two entries do not overlap; it is recommended to use -d in conjunction with -wa and/or -wb. Syntax:
```
pgltools intersect1D [options]
```
options:
```
-a [bed2dFILE]:  use [bed2dFILE] as input.  
-stdInA:  use stdin as input file.
-b [bedFILE]:  use [bedFILE] as input.  
-stdInB:  use stdin as input file.
-bA:  Keep annotations from the bed file rather than the pgl file
-allA:  Keep the annotation from both files.  Will output annotations from pgl followed by bed
-wa:  Prints the original loci from A upon finding overlapping region rather than the intersection
-wb:  Prints the 1-based bed entry as an annotation in the final pgl output file.
-v:  Print the entries in file A that do not overlap regions from file B
-d [INT]:  Adds [INT] to end of each loci and subtracts [INT] from start of loci when performing intersection checks.
```
Example, storing output to output.pgl:
```
pgltools intersect1D -a myFile.pgl -b myOtherFile.bed > output.pgl
```

![pgltools subtract1D](/Images/Subtract1D.PNG?raw=true)
Finds the parts of loci from file A that do not overlap regions from file B.  Requires a sorted pgl file.  Syntax:
```
pgltools subtract [options]
```
options:
```
-a [bed2dFILE]:  use [bed2dFILE] as input.  
-stdInA:  use stdin as input file.
-b [bedFILE]:  use [bedFILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools subtract1D -a myFile.pgl -b myOtherFile.bed > output.pgl
```

![pgltools closest1D](/Images/Closest1D.PNG?raw=true)
Finds the closest region in bed file B for each PGL in file A.  Returns either 10 or 14 columns, depending on the -ba option.  A header will automatically be generated.  The first 6 columns are the PGL, the next 3 are the closest entry from bed file B, and the 10th is the distance.  If -ba is given, two entries are reported, one for each anchor.  The Syntax:
```
pgltools closest [options]
```
options:
```
-a [bed2dFILE]:  use [bed2dFILE] as input.  
-stdInA:  use stdin as input file.
-b [bedFILE]:  use [bedFILE] as input.  
-stdInB:  use stdin as input file.
-ba:  Report the closest bed entry for both anchor.
```
Example, storing output to output.pgl:
```
pgltools closest1D -a myFile.pgl -b myOtherFile.bed > output.pgl
```

## Example Pipelines:

### Determining Enhancer Promoter Interactions.
It is easy to find all PGLs from a PGL file in which a promoter anchor is interacting with an enhancer anchor.  Assuming we have an annotation BED file with annotations in column 7, we could do the following:
```
pgltools intersect1D -a myPGL.pgl -b annotations.BED -bA -aL > annotatedPGLs.pgl
pgltools merge -a annotatedPGLs.pgl -o collapse,distinct -c 7,8 > annotatedPGLs.merged.pgl
```
or in a pipe
```
pgltools intersect1D -a myPGL.pgl -b annotations.BED -bA -aL | pgltools merge -stdInA -o collapse,distinct -c 7,8 > annotatedPGLs.merged.pgl
```
we could then filter this file to where column 7 contained "A,B" and where column 8 contained our annotations of interest.  

### Determining if an eQTL and its eGene are in a Hi-C Interaction.
We can also quickly find if any eQTLs are in a chromatin interaction with their partnered eGene.  Assuming we have three files, eQTL.bed, eGene.bed, and interactions.pgl, we first make a PGL file consisting of each eQTL with its corresponding eGenes (either through paste or join).  We can then perform an intersection on this PGL file with the interactions.pgl file to get the eQTLs that are interacting with their eGene.  The full pipe would look as follows:
```
paste eQTL.bed eGene.bed > combinedQTL.bedpe
pgltools formatbedpe combinedQTL.bedpe > combinedQTL.pgl
pgltools intersect -a combinedQTL.pgl -b interactions.pgl > QTLeGeneInInteractions.pgl
```
or in a pipe:
```
paste eQTL.bed eGene.bed | pgltools formatbedpe | pgltools intersect -stdInA -b interactions.pgl >   QTLeGeneInInteractions.pgl
```

## Useful Parameter Combinations
It is possible to intersect 2 PGL files, keep the annotations from file B, and the original entries from file A, via:
```
pgltools intersect -a fileA.pgl -b fileB.pgl -wa -bA > output.pgl
```

Similarly, it is possible to intersect 2 PGL files, keep all the annotations when an intersection occurs, report the original entry from A when an intersection occurs, and report all PGL entries from both files via:
```
pgltools intersect -a fileA.pgl -b fileB.pgl -wa -m -allA > output.pgl
```

To report the original entries from file B instead, simply change -wa to -wb, yeliding:
```
pgltools intersect -a fileA.pgl -b fileB.pgl -wb -m -allA > output.pgl
```
