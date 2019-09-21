#!/usr/bin/env bash
sudo service postgresql start
python wikimovies_main.py do_all
