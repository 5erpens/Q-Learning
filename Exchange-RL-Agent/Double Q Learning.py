import datetime
from random import randint, uniform, choice

import math

from libs.fileio import fileio
from Raw_input import STF, RM, QM, OPG, QFINAL


def display_matrix(list):
    for lst in list:
        print(lst)


def optimum_states(state):
    return len(OPG[state]) - 1


def optimum_rewards(cord1, cord2):
    return QFINAL[cord1][cord2]


def write_for_graph(graph_input, filename):
    fileio().set_File_Name(fileio().root_path("/data/{}.DAT".format(filename)))
    print("{},{},{},{},{}".format(graph_input["episode"], graph_input["steps"], graph_input["cumulative_rewards"],
                                  graph_input["epsilon"], graph_input["initial_state"]))
    fileio().write_file(
        "{},{},{},{},{}\n".format(graph_input["episode"], graph_input["steps"], graph_input["cumulative_rewards"],
                                  graph_input["epsilon"], graph_input["initial_state"]))


def write_cache(graph_input):
    fileio().set_File_Name(fileio().root_path("/tool/{}".format("graph.cache")))
    fileio().write_file(
        "{},{},{},{},{}\n".format(graph_input["episode"], graph_input["steps"], graph_input["cumulative_rewards"],
                                  graph_input["epsilon"], graph_input["initial_state"]))


def flush_cache():
    fileio().set_File_Name(fileio().root_path("/tool/{}".format("graph.cache")))
    fileio().file_flush()


def get_states(state, QMatrix):
    state_val = []
    for action in STF[state]:
        state_val.insert(len(state_val), [action, QMatrix[state][action]])
    return state_val


def maximum_reward_state_val(state_val):
    val = 0
    state = choice(state_val)[0]
    for couple in state_val:
        if val < couple[1]:
            val = couple[1]
            state = couple[0]

    return [state, val]


def random_state_val(state_val):
    lst = []
    for state in state_val:
        lst.insert(len(lst), state[0])
    return choice(lst)


def random_state(ranges):
    for i in range(ranges):
        state = randint(0, 12)
        yield state


def step(config):

    # Initialization ------------------------------------------------------------------------------------------
    epsilon = config["epsilon"]
    learning_rate = config["learning_rate"]
    gamma = config["gamma"]
    current_state = config["state"]
    switch = uniform(0.0, 1.0)

    # Explore VS Exploit ---------------------------------------------------------------------------------------
    if uniform(0.0, 1.0) >= epsilon:
        # Exploit
        if switch <= 0.5:
            next_state = maximum_reward_state_val(get_states(current_state, config["QM1"]))[0]
        else:
            next_state = maximum_reward_state_val(get_states(current_state, config["QM2"]))[0]
    else:
        # Explore
        next_state = random_state_val(get_states(current_state, config["QM1"]))

    # Double Q Learning Algorithm -------------------------------------------------------------------------------
    if switch <= 0.5:
        # Q1[s,a] = Q1[s,a] + ALPHA * (reward + GAMMA * Q2[s_,a_] - Q1[s,a])
        config["QM1"][current_state][next_state] += learning_rate * (
                (config["RM"][current_state][next_state] + gamma * config["QM2"][next_state][
                 maximum_reward_state_val(get_states(next_state, config["QM1"]))[0]]
                 ) - config["QM1"][current_state][next_state])
    else:
        # Q2[s,a] = Q2[s,a] + ALPHA * (reward + GAMMA * Q1[s_,a_] - Q2[s,a])
        config["QM2"][current_state][next_state] += learning_rate * (
                (config["RM"][current_state][next_state] + gamma * config["QM1"][next_state][
                 maximum_reward_state_val(get_states(next_state, config["QM2"]))[0]]
                 ) - config["QM2"][current_state][next_state])

    # Epsilon Variation ---------------------------------------------------------------------------------------
    if config["epsilon"] <= 0.5:
        config["epsilon"] *= 0.99999
    else:
        config["epsilon"] *= 0.9999

    # ---------------------------------------------------------------------------------------------------------
    config["state"] = next_state
    if switch <= 0.5:
        normalised_reward = config["QM1"][current_state][next_state] / optimum_rewards(current_state, next_state)
    else:
        normalised_reward = config["QM2"][current_state][next_state] / optimum_rewards(current_state, next_state)
    # ---------------------------------------------------------------------------------------------------------

    return config, normalised_reward


def episode(Config):
    rewards = 0
    steps = 0
    initial_state = Config["state"]
    while Config["state"] != Config["goal"]:
        results = step(Config)
        steps = steps + 1
        rewards = rewards + results[1]
        Config = results[0]
    return Config, ((steps - optimum_states(initial_state)) + 1), rewards / steps, initial_state


if __name__ == '__main__':

    flush_cache()
    filename = str(datetime.datetime.now()).replace(":", ".")

    config = {
        "epsilon": 0.9,
        "learning_rate": 0.3,
        "gamma": 0.75,
        "state": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "goal": 6,
        "QM1": QM,
        "QM2": QM,
        "RM": RM
    }

    graph = {
        "steps": 0,
        "cumulative_rewards": 0,
        "episode": 0,
        "epsilon": 0,
        "initial_state": 0
    }

    Episode = 200000
    episode_count = 0
    for state in random_state(Episode):
        episode_count = episode_count + 1
        if state != config["goal"]:
            config["state"] = state
            results = episode(config)
            config = results[0]

            if results[1] != 0 and results[2] != 0:
                graph["steps"] = results[1]
                graph["cumulative_rewards"] = results[2]
                graph["episode"] = episode_count
                graph["epsilon"] = config["epsilon"]
                graph["initial_state"] = results[3]

                write_for_graph(graph, filename)
                write_cache(graph)

    print()
    display_matrix(config["QM1"])
    print()
    display_matrix(config["QM2"])
