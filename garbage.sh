#!/bin/tcsh -f
# Author: Kory Kozlowski
# if the garbage directory exists:
if(-d ~/.garbage) then
    # set positional index to 1
    set filePos=1
    while ($filePos <= $#argv)
	#if argument is -cleanup
	if("$argv[$filePos]" == "-cleanup") then
	    set fileSet = `ls ~/.garbage`
	    set garb = 1
	    while($garb <= $#fileSet)
		set file = $fileSet[$garb]
		echo "$file delete/restore/skip? (d/r/s) "
		set drs = $<
		if($drs == "d") then
		    echo "$file deleted!"
		    rm ~/.garbage/$file
		else
		    if($drs == "r") then
			echo "$file restored!"
			mv ~/.garbage/$file ~/$file
		    else
			if($drs == "s") then
			    echo "$file skipped!"
			endif
		    endif
		endif
		@ garb++
	    end
	else

	    # if argument is file, move to garbage
	    if(-f $argv[$filePos]) then
		mv $argv[$filePos] ~/.garbage
		echo "$argv[$filePos] thrown in garbage"
	    endif
	endif
       	@ filePos++
    end
    # output garbage directory size
    echo "Size of garbage in bytes: "
    du ~/.garbage
else
    # if garbage directory does not exist:
    echo ".garbage directory being made..."
    mkdir ~/.garbage
endif
