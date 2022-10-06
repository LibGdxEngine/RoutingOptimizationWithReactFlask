import pandas as pd
from scipy.spatial import distance_matrix

data = [
    # Enter Points          Exit Points
    [24.433461, 54.432755], [24.427946, 54.437588],
    [24.489013, 54.356993], [24.488262, 54.356039],
    [24.490922, 54.359676], [24.491713, 54.356108],
    [24.472605, 54.341227], [24.468474, 54.338513],
    [24.478917, 54.354531], [24.482262, 54.353828],
    [24.465393, 54.352466], [24.472863, 54.350427],
]


def generate_distance_matrix(points):
    ctys = ['E40'] * len(points)
    df = pd.DataFrame(points, columns=['xcord', 'ycord'], index=ctys)
    dm = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)
    dm = dm * 1000
    dm = pd.DataFrame(dm).astype(int).to_numpy()
    return dm


print(generate_distance_matrix(data))
