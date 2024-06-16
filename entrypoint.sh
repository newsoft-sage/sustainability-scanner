#!/bin/bash
FILES=$(ls $1)
echo Found the following files: $FILES
cd $1
susscanner $FILES
