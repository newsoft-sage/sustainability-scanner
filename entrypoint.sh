#!/bin/bash
FILES=$(ls $1/*.template $1/*.yaml)
echo Found the following files: $FILES
cd $1
susscanner $FILES
