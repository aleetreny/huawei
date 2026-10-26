"""SynthCareer: a synthetic career game with known ground truth for validating the lab.

The mechanics are invented (see ``game``'s docstring); only the public structure
and the MCP tool interface mirror the official game.
"""

from careerlab.synthetic.game import (DEFAULT_CONFIG, EpisodeOutcome, SynthConfig, SynthGame, Truth, fast_episode,
                                      throughput, truth)
from careerlab.synthetic.policy import (ACTORS, DESIGNED, FAMILIES, THETA_SPACE, ActorModel, ParamPolicy, PolicyActor,
                                        complexity, crossover, make_agent, mutate, random_theta, view_from_obs)

__all__ = ["ACTORS", "DEFAULT_CONFIG", "DESIGNED", "FAMILIES", "THETA_SPACE", "ActorModel", "EpisodeOutcome",
           "ParamPolicy", "PolicyActor", "SynthConfig", "SynthGame", "Truth", "complexity", "crossover",
           "fast_episode", "make_agent", "mutate", "random_theta", "throughput", "truth", "view_from_obs"]
