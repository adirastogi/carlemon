#!/bin/bash

fnr()
{
  if [ "$#" -lt 2 ]
  then
    echo "Usage: fnr <Word to replace> <New word> <Directory/File Names(Optional)>"
  elif [ "$#" -eq 2 ]
  then
    grep -lr --exclude-dir=".svn" -e "$1" . | xargs sed -i "s/"$1"/"$2"/g"
  else
    FIRST_WORD="$1"
    SECOND_WORD="$2"
    shift 2
    echo -e "Files to be modified:\t" "$@" "\n"
    for filename in "$@"
    do
      if [[ -d "$filename" ]]
      then
        grep -lr --exclude-dir=".svn" -e "$FIRST_WORD" "$filename" | xargs sed -i "s/"$FIRST_WORD"/"$SECOND_WORD"/g"
      elif [[ -f "$filename" ]]
      then
        sed -i "s/"$FIRST_WORD"/"$SECOND_WORD"/g" "$filename"
      fi
    done
  fi
}

fnr 0.0 0 result.txt
fnr 1.0 1 result.txt 
paste --delimiters="," ref_ids.txt result.txt > prediction.txt
