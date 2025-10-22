import pandas as pd
import numpy as np
import random

final_data = pd.read_csv('final_data.csv')

def day_generator():
    """Generates random day conditions."""
    conditions = {'lighting': ['daylight', 'dim', 'night'],
                  'weather': ['rainy', 'clear', 'foggy'],
                  'time_of_day': ['afternoon', 'evening', 'morning'],
                  'holiday': [False, True],
                  'school_season': [True, False]}
    condition = {}
    for key in conditions.keys():
        condition[key] = random.choice(conditions[key])
    return condition

def create_routes(condition, day, data=final_data):
    """Generates random routes for given day conditions and """
    route_counts = 4 + int(day/7)
    filtered_df = data.copy()
    for key, value in condition.items():
        filtered_df = filtered_df[filtered_df[key] == value]
    
    intervals = filtered_df['accident_risk'].quantile(np.linspace(0, 1, route_counts + 1)).values
    routes = []
    for i in range(1, len(intervals)):
        route = filtered_df[(filtered_df['accident_risk'] <= intervals[i]) & (filtered_df['accident_risk'] >= intervals[i-1])]
        if route.shape[0] == 0:
            continue
        else:
            routes.append(route.sample())
    if len(routes) == 0:
        print("No routes found for the given condition.")
        return pd.DataFrame()
    else:
        return pd.concat(routes, axis=0).sample(frac=1).reset_index(drop=True)
    
    