#!/bin/bash

echo "Load data into the database."
psql -d $1 -U $2 -f load.sql

echo "Extract features from the dataset."
psql -d $1 -U $2 -f features.sql
psql -d $1 -U $2 -f day_by_day_features.sql

