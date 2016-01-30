#!/bin/bash

echo "Dump features to the csv file."
psql -d $1 -U $2 -f dump.sql

