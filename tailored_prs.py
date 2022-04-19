import random as rd
import numpy as np
from create_transition_matrix import ctm as ctm


def prs(p, d, k, t, fs, rand_seed):
    rd.seed(rand_seed)  # set the seed of prs
    N = int(t * fs)  # 

    pseudorandom_sequence = np.zeros(N)

    transition_probabilities = ctm(p, d, k)

    starting_value = 0
    chain_length = N
    chain = np.zeros(chain_length)
    chain[0] = starting_value

    for i in range(1, chain_length):
        this_step_distribution = transition_probabilities[int(chain[i - 1]), :]
        cumulative_distribution = np.cumsum(this_step_distribution)
        r = rd.random()
        chain[i] = np.argmax(cumulative_distribution > r)  # This is how you copy the find(x>r,1) in MATLAB

    u_chain = np.unique(chain)
    pseudorandom_sequence[chain <= np.floor(np.median(u_chain))] = 1
    pseudorandom_sequence[chain > np.floor(np.median(u_chain))] = -1

    return pseudorandom_sequence
