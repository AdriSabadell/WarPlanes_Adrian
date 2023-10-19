#!/bin/bash

for file in ./*.png
do
  convert $file +level-colors black,#aaaaaa $(basename $file .png)dark.png
done


