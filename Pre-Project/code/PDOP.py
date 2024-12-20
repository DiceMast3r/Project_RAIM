import numpy as np

def cal(sat_position, rec_position):
    G = []
    GIN_MID = []
    for sat in sat_position:
        sat = np.array(sat)
        rec = np.array(rec_position)
        dist = np.sqrt(np.sum((sat - rec) ** 2))
        unit_vector = (sat - rec) / dist
        G.append(unit_vector)
    G = np.array(G)
    G_transpose = G.T
    GTG = np.dot(G_transpose, G)
    GIN = np.linalg.inv(GTG)
    for i in range(len(GIN)):
        GIN_MID.append(GIN[i][i])
    PDOP = np.sqrt(np.sum(GIN_MID))

    return PDOP

satellites = [[ 8532065.95452706, 14260013.67111646 ,20824389.96600079],  # Satellite 1 position (ECEF, km)
    [18563098.28901298 ,12967294.44940344 ,14116089.58051955],  
    [ -3146907.66794293 , 21345011.4069616  ,-15371693.63628407],  
    [-2050943.01571882, 21473513.16985594 ,15728950.24446666],
    [ 4927103.41617994 ,24737345.12504125 ,-8298873.53700631],
    [-10955005.67952687 , 11803466.06057115 , 20922579.19039785],
    [-16912030.54640304 , 18704883.25753407  , 6621537.18943011],
    [-14188696.27287192 , 22205510.17089337   , 371207.76784277],
    [-10095045.0414692  , 12763050.32832661 ,-21130136.08814235],
    [13053017.07709232, 21716090.20211055 ,-7196791.44883791]
    ]


receiver = [-1158298.689750454, 6087925.457297738, 1503753.4457173424]
pdop = cal(satellites, receiver)
print("Sat Number:", len(satellites))
print("Predicted PDOP:", pdop)
