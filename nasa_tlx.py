def calculate_tlx_score(scores, weights=None):
    """
    Calculate the NASA TLX score based on the given dimension scores and weights.
    
    :param scores: Dictionary containing scores for each TLX dimension
    :param weights: Dictionary containing weights for each TLX dimension (optional)
    :return: Overall TLX score
    """
    if weights is None:
        # If no weights are provided, use equal weights for all dimensions
        weights = {dim: 1 for dim in scores.keys()}
    
    weighted_scores = [scores[dim] * weights[dim] for dim in scores.keys()]
    total_weight = sum(weights.values())
    
    return sum(weighted_scores) / total_weight

def get_dimension_impact(scores, weights=None):
    """
    Determine which dimensions have the highest impact on the overall score.
    
    :param scores: Dictionary containing scores for each TLX dimension
    :param weights: Dictionary containing weights for each TLX dimension (optional)
    :return: List of tuples (dimension, weighted_score) sorted by impact (highest first)
    """
    if weights is None:
        # If no weights are provided, use equal weights for all dimensions
        weights = {dim: 1 for dim in scores.keys()}
    
    weighted_scores = [(dim, scores[dim] * weights[dim]) for dim in scores.keys()]
    return sorted(weighted_scores, key=lambda x: x[1], reverse=True)
