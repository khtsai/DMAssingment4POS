'''
Created on Dec 21, 2017

@author: Chuck
'''
def viterbi(obs, states, start_p, trans_p, obs_p):
    V = [{}]

    for st in states:
        V[0][st] = {"prob": start_p[st] * obs_p[st][obs[0]], "prev": None}

    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)

            for prev_st in states:
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * obs_p[st][obs[t]]
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
        
#inputSTR = "I wish you merry christmas" #P V P A N
#inputSTR = "Happy Christmas to the one I love" #A N S S S P V
inputSTR = "Have a joyful Christmas full of love" #V S A N A S N

obs = inputSTR.lower().split(" ")
states = ('P', 'V', 'S', 'A', 'N')
start_p = {'P': 0.2, 'V': 0.2, 'S':0.2, 'A':0.2, 'N':0.2}
trans_p = {\
    'A': {'A': 0, 'N': 0.529411765, 'P': 0.058823529, 'V': 0.058823529, 'S': 0.352941176},
    'N': {'A': 0.125, 'N': 0.208333333, 'P': 0.041666667, 'V': 0.5, 'S': 0.125},
    'P': {'A': 0.076923077, 'N': 0, 'P': 0, 'V': 0.461538462, 'S': 0.461538462},
    'V': {'A': 0.071428571, 'N': 0.571428571, 'P': 0.357142857, 'V': 0.0625, 'S': 0.357142857},
    'S': {'A': 0.208333333, 'N': 0.458333333, 'P': 0.0625, 'V': 0.020833333, 'S': 0.25}}

# Love christmas forever => P=0 ,V=0.077 , S=0 , A=0 , N=0.1

obs_p = {'P': {'you':0.67,'i':0.33}, \
         'V': {'wish':0.38,'let':0.077,'surround':0.077,'have':0.15,'come':0.077,'love':0.077,'bless':0.077,'bring':0.077}, \
         'S': {'a':0.083,'and':0.125,'all':0.041,'to':0.041,'your':0.041,'this':0.083,'be':0.041,'of':0.1,'may':0.062,'with':0.062,'the':0.0625,'for':0.04,'me':0.02,'my':0.06,'one':0.02,'always':0.02,'much':0.02,'ever':0.02,'so':0.02,'is':0.02}, \
         'A': {'happy':0.176,'full':0.176,'beautiful':0.058,'merry':0.117,'best':0.235,'overflowing':0.058,'joyful':0.058,'true':0.058,'great':0.058}, \
         'N': {'christmas':0.0394,'family':0.026,'joy':0.1,'love':0.1,'time':0.05,'moments':0.026,'memories':0.026,'cheer':0.05,'happiness':0.05,'greetings':0.026,'god':0.026,'laughter':0.026,'dreams':0.026,'year':0.026,'wishes':0.026}}

for ob in obs:
    for state in states:
        if not ob in obs_p[state]:
            obs_p[state][ob] = 0

#print(obs_p)
viterbi(obs,states,start_p,trans_p,obs_p)
