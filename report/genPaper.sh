#! /bin/sh

pslatex report.tex
dvips -Ppdf -G0 -t letter -o report.ps report.dvi
ps2pdf -dPDFSETTINGS=/prepress \
-dCompatibilityLevel=1.4 \
-dAutoFilterColorImages=false \
-dAutoFilterGrayImages=false \
-dColorImageFilter=/FlateEncode \
-dGrayImageFilter=/FlateEncode \
-dMonoImageFilter=/FlateEncode \
-dDownsampleColorImages=false \
-dDownsampleGrayImages=false \
report.ps report.pdf
