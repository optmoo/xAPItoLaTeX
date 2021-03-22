#!/bin/bash
IFS=$(echo -en "\n\b")

root_dir='/home/user'

qp_files=$(find $root_dir -name *_P0*.xml)
for f in $qp_files; do
	dirname=$(dirname $f)
	filename=$(basename $f)
	if python2 parse_questionpool.py -f $f -o tmp/$filename.tex; then
		if pdflatex -halt-on-error -output-directory pdf tmp/$filename.tex > /dev/null; then
			echo "$dirname/$filename.pdf"
			rm pdf/$filename.aux pdf/$filename.log
			rm tmp/$filename.tex
			mv pdf/$filename.pdf $dirname
		else
			echo "[ERROR] tmp/$filename.tex"
			rm pdf/$filename.aux pdf/$filename.log
		fi
	else
		echo "[ERROR] $f"
	fi
done

cs_files=$(find $root_dir -name *_C0*.xml)
for f in $cs_files; do
	dirname=$(dirname $f)
	filename=$(basename $f)
	if python2 parse_casestudy.py -f $f -o tmp/$filename.tex; then
		if pdflatex -halt-on-error -output-directory pdf tmp/$filename.tex > /dev/null; then
			echo "$dirname/$filename.pdf"
			rm pdf/$filename.aux pdf/$filename.log
			rm tmp/$filename.tex
			mv pdf/$filename.pdf $dirname
		else
			echo "[ERROR] tmp/$filename.tex"
			rm pdf/$filename.aux pdf/$filename.log
		fi
	else
		echo "[ERROR] $f"
	fi
done
