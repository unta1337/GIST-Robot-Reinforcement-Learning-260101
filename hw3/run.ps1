# 2.4
uv run src/scripts/run_dqn.py -cfg experiments/dqn/cartpole.yaml --eval_interval 2500

# 2.5
uv run src/scripts/run_dqn.py -cfg experiments/dqn/lunarlander.yaml
uv run src/scripts/run_dqn.py -cfg experiments/dqn/mspacman.yaml

# 2.6
# Learning Rate
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_lr_1e-2.yaml
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_lr_5e-4.yaml
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_lr_1e-4.yaml

# Architecture
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_arch_128x2.yaml
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_arch_512x2.yaml
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_arch_256x3.yaml

# Target Freq
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_target_500.yaml
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_target_5000.yaml
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_target_10000.yaml

# Exploration Schedule
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_steps_250k.yaml
uv run src/scripts/run_dqn.py -cfg parameters/lunarlander_steps_1M.yaml

# 3.2 3.3
uv run src/scripts/run_sac.py -cfg experiments/sac/sanity_invertedpendulum.yaml

# 3.4
uv run src/scripts/run_sac.py -cfg experiments/sac/halfcheetah.yaml

# 3.5
uv run src/scripts/run_sac.py -cfg experiments/sac/sanity_invertedpendulum_autotune.yaml
uv run src/scripts/run_sac.py -cfg experiments/sac/halfcheetah_autotune.yaml

# Bonus Task
uv run src/scripts/run_sac.py -cfg parameters/halfcheetah_temp_0.01.yaml
uv run src/scripts/run_sac.py -cfg parameters/halfcheetah_temp_0.05.yaml
uv run src/scripts/run_sac.py -cfg parameters/halfcheetah_temp_0.5.yaml
uv run src/scripts/run_sac.py -cfg parameters/halfcheetah_temp_1.0.yaml

# 3.6
uv run src/scripts/run_sac.py -cfg experiments/sac/hopper_singleq.yaml
uv run src/scripts/run_sac.py -cfg experiments/sac/hopper_clipq.yaml
