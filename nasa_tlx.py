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

def pair_wise_comparison(dimensions):
    """
    Generate pair-wise comparison questions for TLX dimensions.
    
    :param dimensions: List of TLX dimensions
    :return: List of tuples representing pair-wise comparisons
    """
    comparisons = []
    for i, dim1 in enumerate(dimensions):
        for dim2 in dimensions[i+1:]:
            comparisons.append((dim1, dim2))
    return comparisons

def calculate_weights(pair_wise_results):
    """
    Calculate dimension weights based on pair-wise comparison results.
    
    :param pair_wise_results: Dictionary with (dim1, dim2) tuples as keys and selected dimension as values
    :return: Dictionary of dimension weights
    """
    weights = {dim: 0 for dim in set(dim for pair in pair_wise_results.keys() for dim in pair)}
    for (dim1, dim2), selected in pair_wise_results.items():
        weights[selected] += 1
    return weights
