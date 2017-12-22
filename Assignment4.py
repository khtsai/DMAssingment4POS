'''
Created on Dec 21, 2017

@author: Chuck
'''
def viterbi(obs, states, start_p, trans_p, emit_p):

    V = [{}]

    for st in states:

        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}

    # Run Viterbi when t > 0

    for t in range(1, len(obs)):

        V.append({})

        for st in states:

            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)

            for prev_st in states:

                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:

                    max_prob = max_tr_prob * emit_p[st][obs[t]]

                    V[t][st] = {"prob": max_prob, "prev": prev_st}

                    break

    for line in dptable(V):

        print(line)

    opt = []

    # The highest probability

    max_prob = max(value["prob"] for value in V[-1].values())

    previous = None

    # Get most probable state and its backtrack

    for st, data in V[-1].items():

        if data["prob"] == max_prob:

            opt.append(st)

            previous = st

            break

    # Follow the backtrack till the first observation

    for t in range(len(V) - 2, -1, -1):

        opt.insert(0, V[t + 1][previous]["prev"])

        previous = V[t + 1][previous]["prev"]


    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)


def dptable(V):

    # Print a table of steps from dictionary

    yield " ".join(("%12d" % i) for i in range(len(V)))

    for state in V[0]:

        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)
        
obs = ('normal', 'cold', 'dizzy')
states = ('Healthy', 'Fever')
start_p = {'Healthy': 0.6, 'Fever': 0.4}
trans_p = {
    'A': {'A': 0, 'N': 0.529411765, 'P': 0.058823529, 'V': 0.058823529, 'S': 0.352941176},
    'N': {'A': 0.125, 'N': 0.208333333, 'P': 0.041666667, 'V': 0.5, 'S': 0.125},
    'P': {'A': 0.076923077, 'N': 0, 'P': 0, 'V': 0.461538462, 'S': 0.461538462},
    'V': {'A': 0.071428571, 'N': 0.571428571, 'P': 0.357142857, 'V': 0.0625, 'S': 0.357142857},
    'S': {'A': 0.208333333, 'N': 0.458333333, 'P': 0.0625, 'V': 0.020833333, 'S': 0.25},
   }
emit_p = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
   }

viterbi(obs,states,start_p,trans_p,emit_p)