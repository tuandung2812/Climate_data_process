#!/bin/usr/env bash
input_features="u10 v10 surface_pressure evaporation total_precipitation"
nc_files_dir="data/nc_files/"
csv_save_files_dir="data/csv/"
stations_data_dir="data/stations_data/"
python3 read_nc.py --features="$input_features" --nc_files_dir="$nc_files_dir" --csv_save_files_dir="$csv_save_files_dir"
python3 process_data.py --features="$input_features" --csv_save_files_dir="$csv_save_files_dir" --stations_data_dir="$stations_data_dir"