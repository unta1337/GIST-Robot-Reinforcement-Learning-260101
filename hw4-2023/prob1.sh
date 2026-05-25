#!/bin/bash

python cs285/scripts/run_hw4.py -cfg experiments/mpc/halfcheetah_0_iter/orig.yaml
python cs285/scripts/run_hw4.py -cfg experiments/mpc/halfcheetah_0_iter/layer_more.yaml
python cs285/scripts/run_hw4.py -cfg experiments/mpc/halfcheetah_0_iter/hidden_more.yaml
