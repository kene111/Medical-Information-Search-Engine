def calc_mean_score(results):
    "calculates the mean score of the returned n_results."
    mean_val = 0
    sum_ = 0

    for score in results:
        sum_ +=  score["score"]
    
    if len(results) == 0:
        return 0
        
    mean_val =  sum_/ len(results)

    return mean_val
        