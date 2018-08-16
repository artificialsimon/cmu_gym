#ACT-R
This uses custom ACT-R9
Run run-act-r.command


# gym-gridworld

Basic implementation of gridworld game 
for reinforcement learning research. 

## Install gym-gridworld

install virtual environment for gridworld

    cd gym-gridworld
    conda env create -f environment.yml
    source gridworld
    pip install -e .

## Use gym-gridworld
    
    import gym
    import gym_gridworld
    env = gym.make('gridworld-v0')
    _ = env.reset()
    _ = env.step(env.action_space.sample())
    
## Visualize gym-gridworld
In order to visualize the gridworld, you need to set `env.verbose` to `True`

    env.verbose = True
    _ = env.reset()
