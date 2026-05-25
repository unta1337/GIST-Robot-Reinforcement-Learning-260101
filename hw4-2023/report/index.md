# HW4 - 20201068 Kim Sungnyoung

## Problem 1
### Result
|Orig|Layer More|Hidden More|
|:-:|:-:|:-:|
|![](./pics/hc_orig.png)|![](./pics/hc_layer_more.png)|![](./pics/hc_hidden_more.png)|
|0.1618|0.2861|0.117|

### Discussion
On this experiment, I compared how the model dimensions affect the result; layer and hidden.  

As a results, the model with more layers(depper model) is poor than the one with more hidden layers(wide model).
This is because with just more layers, the model tends to be fit with more time or iterations. Thus, the model with more hidden is be more fit with data in less time or iterations; its loss decreases.  

### Command Lines and Arguments
```pwsh
> python cs285/scripts/run_hw4.py -cfg experiments/mpc/halfcheetah_0_iter/orig.yaml
> python cs285/scripts/run_hw4.py -cfg experiments/mpc/halfcheetah_0_iter/layer_more.yaml
> python cs285/scripts/run_hw4.py -cfg experiments/mpc/halfcheetah_0_iter/hidden_more.yaml
```

#### Configs
`orig.yaml`
```yaml
env_name: cheetah-cs285-v0
exp_name: cheetah_0iter

base_config: mpc
num_layers: 1
hidden_size: 32

num_iters: 1
initial_batch_size: 20000
num_agent_train_steps_per_iter: 500
num_eval_trajectories: 0
```

`layer_more.yaml`
```yaml
env_name: cheetah-cs285-v0
exp_name: cheetah_0iter_layer_more

base_config: mpc
num_layers: 8
hidden_size: 32

num_iters: 1
initial_batch_size: 20000
num_agent_train_steps_per_iter: 500
num_eval_trajectories: 0
```

`hidden_more.yaml`
```yaml
env_name: cheetah-cs285-v0
exp_name: cheetah_0iter_hidden_more

base_config: mpc
num_layers: 1
hidden_size: 64

num_iters: 1
initial_batch_size: 20000
num_agent_train_steps_per_iter: 500
num_eval_trajectories: 0
```

## Problem 2
### Result
|Loss|Eval Return|
|:-:|:-:|
|![](./pics/obstacles_loss.png)|-25.41|

### Discussion
The value of -25.41 means the model is trained kind of successfully. But still the eval return is negative; there's need the breakthrough with this problem.  

Since the number of steps is just 20, this result is simply due to the lack of steps.  
And the criterial is soley based on distance; there should be more sophicticated criterial to learn.  

### Command Lines and Arguments
```pwsh
> python cs285/scripts/run_hw4.py -cfg experiments/mpc/obstacles_1_iter.yaml
```

#### Configs
`obstacles_1_iter.yaml`
```yaml
env_name: obstacles-cs285-v0
exp_name: obstacles_single

base_config: mpc
num_layers: 2
hidden_size: 250

num_iters: 1
initial_batch_size: 5000
num_agent_train_steps_per_iter: 20
num_eval_trajectories: 20
mpc_horizon: 10
mpc_strategy: random
```

## Problem 3
### Result
|Obstacles|Reacher|Halfcheetah|
|:-:|:-:|:-:|
|![](./pics/obstacles_multi_loss.png)|![](./pics/reacher_multi_loss.png)|![](./pics/hc_multi_loss.png)|
|![](./pics/obstacles_multi_eval.png)|![](./pics/reacher_multi_eval.png)|![](./pics/hc_multi_eval.png)|

### Discussion
#### On-Policy Iterative Training and Distribution Shift
The primary reason on-policy iterative training outperforms training on purely random data is the mitigation of **distribution shift**. When a dynamics model is trained only on random data, it learns the physics of the environment only in regions explored by a random policy. However, when we use this model for planning (MPC) to maximize rewards, the controller often steers the agent into high-reward regions that the random policy never visited. In these new states, the model's predictions are often inaccurate, leading to a failure in planning. 

By iteratively collecting data using the current MPC policy (Step 3) and aggregating it into the replay buffer (Step 4), we ensure that the dynamics model is trained on the exact state-action distributions it encounters during task execution. This "DAgger-like" approach for dynamics allows the model to become increasingly accurate in task-relevant regions, leading to significantly higher eval returns.

#### Improvement Patterns Across Environments
The improvement patterns differ across the three environments due to their varying complexity and horizons:
- **Obstacles**: This environment typically shows the fastest convergence. Since the task is navigation with a relatively short horizon and simple point-mass dynamics, the model quickly learns to avoid obstacles and reach the goal within a few iterations.
- **Reacher and HalfCheetah**: These environments involve continuous control of jointed robots, exhibiting more gradual improvement. The non-linear dynamics of the robotic arms and legs are harder to model accurately. HalfCheetah, in particular, requires a longer horizon (15 steps) and a very stable model to maintain a running gait without falling or stalling. As a result, we see a steady increase in evaluation returns over more iterations as the replay buffer grows and the model refines its understanding of these complex motions.

#### Model Error and Replay Buffer Growth
As the replay buffer grows with each iteration, the dynamics model is exposed to a richer and more diverse set of transitions. Initially, when the agent explores new strategies, the model error might fluctuate or temporarily increase. However, as more on-policy data is collected, the model's accuracy on the trajectories that matter for high performance improves. This synergy between the expanding dataset and the retraining process is what allows the agent to eventually master the tasks, as observed in the evaluation curves.

### Command Lines and Arguments
```pwsh
> python cs285/scripts/run_hw4.py -cfg experiments/mpc/obstacles_multi_iter.yaml
> python cs285/scripts/run_hw4.py -cfg experiments/mpc/reacher_multi_iter.yaml
> python cs285/scripts/run_hw4.py -cfg experiments/mpc/halfcheetah_multi_iter.yaml
```

#### Configs
`obstacles_multi_iter.yaml`
```yaml
env_name: obstacles-cs285-v0
exp_name: obstacles_multi

base_config: mpc
num_layers: 2
hidden_size: 250

num_iters: 12
initial_batch_size: 5000
batch_size: 1000
num_agent_train_steps_per_iter: 20
num_eval_trajectories: 20
mpc_horizon: 10
mpc_strategy: random
```

`reacher_multi_iter.yaml`
```yaml
env_name: reacher-cs285-v0
exp_name: reacher_multi

base_config: mpc
num_layers: 2
hidden_size: 250

num_iters: 15
initial_batch_size: 5000
batch_size: 5000
num_agent_train_steps_per_iter: 1000
num_eval_trajectories: 10
mpc_horizon: 10
mpc_strategy: random
```

`halfcheetah_multi_iter.yaml`
```yaml
env_name: cheetah-cs285-v0
exp_name: cheetah_multi

base_config: mpc
num_layers: 2
hidden_size: 250

num_iters: 15
initial_batch_size: 5000
batch_size: 5000
num_agent_train_steps_per_iter: 1500
num_eval_trajectories: 10
mpc_horizon: 15
mpc_strategy: random
```

## Problem 4
### Result
### Discussion
### Command Lines and Arguments
#### Configs

## Problem 5
### Result
### Discussion
### Command Lines and Arguments
#### Configs

## Problem 6
### Result
### Discussion
### Command Lines and Arguments
#### Configs
