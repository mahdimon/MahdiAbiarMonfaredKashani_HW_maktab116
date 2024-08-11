#!/bin/bash
FILE="log.txt"
read -rp "enter download link: " link
wget "$link" >> $FILE 2>&1

