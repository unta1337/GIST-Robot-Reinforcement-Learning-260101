#!/bin/bash

python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_ablations/orig.yaml

python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_ablations/ensemble_less.yaml
python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_ablations/ensemble_more.yaml

python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_ablations/action_seq_less.yaml
python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_ablations/action_seq_more.yaml

python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_ablations/horizon_less.yaml
python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_ablations/horizon_more.yaml
