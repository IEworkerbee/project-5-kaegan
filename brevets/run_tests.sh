#!/bin/bash

for t in tests/*.py
do
    nosetests $t
    sleep 10m
done
