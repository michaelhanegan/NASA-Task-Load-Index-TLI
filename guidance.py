from nasa_tlx import get_dimension_impact

def generate_guidance(scores, desired_change, project_context, selected_model):
    """
    Generate guidance for workload adjustment based on current scores, desired change, project context, and selected AI model.
    
    :param scores: Dictionary containing scores for each TLX dimension
    :param desired_change: Desired change in overall TLX score (-100 to +100)
    :param project_context: String containing project context information
    :param selected_model: String representing the selected AI model
    :return: String containing guidance for workload adjustment
    """
    impact_order = get_dimension_impact(scores)
    guidance = f"Using {selected_model} for analysis:\n\n"

    # Analyze project context
    context_factors = analyze_context(project_context)

    if desired_change > 0:
        guidance += f"To increase the overall workload by approximately {desired_change} points, consider the following:\n\n"
        for dimension, score in impact_order:
            if score < 80:  # Room for increase
                guidance += f"- Increase the {dimension.lower()} of the task. "
                guidance += get_dimension_advice(dimension, "increase", context_factors)
                guidance += "\n"
    elif desired_change < 0:
        guidance += f"To decrease the overall workload by approximately {abs(desired_change)} points, consider the following:\n\n"
        for dimension, score in reversed(impact_order):
            if score > 20:  # Room for decrease
                guidance += f"- Decrease the {dimension.lower()} of the task. "
                guidance += get_dimension_advice(dimension, "decrease", context_factors)
                guidance += "\n"
    else:
        guidance = f"{selected_model} analysis: No change in workload is desired. The current task design seems appropriate."

    return guidance

def analyze_context(project_context):
    """
    Analyze the project context to extract relevant factors for guidance generation.
    
    :param project_context: String containing project context information
    :return: Dictionary containing extracted context factors
    """
    # This is a simple implementation. In a more advanced version, you could use
    # natural language processing techniques to extract more detailed information.
    context_factors = {
        "audience": "general",
        "duration": "medium",
        "complexity": "moderate"
    }

    if "beginner" in project_context.lower() or "novice" in project_context.lower():
        context_factors["audience"] = "novice"
    elif "expert" in project_context.lower() or "advanced" in project_context.lower():
        context_factors["audience"] = "expert"

    if "short" in project_context.lower() or "quick" in project_context.lower():
        context_factors["duration"] = "short"
    elif "long" in project_context.lower() or "extended" in project_context.lower():
        context_factors["duration"] = "long"

    if "simple" in project_context.lower() or "easy" in project_context.lower():
        context_factors["complexity"] = "low"
    elif "complex" in project_context.lower() or "difficult" in project_context.lower():
        context_factors["complexity"] = "high"

    return context_factors

def get_dimension_advice(dimension, direction, context_factors):
    """
    Provide specific advice for each dimension based on the desired direction of change and project context.
    
    :param dimension: TLX dimension
    :param direction: 'increase' or 'decrease'
    :param context_factors: Dictionary containing extracted context factors
    :return: String containing specific advice
    """
    advice = {
        "Mental Demand": {
            "increase": {
                "novice": "Gradually introduce more complex problem-solving elements, providing scaffolding for learning.",
                "expert": "Introduce advanced cognitive challenges or multitasking elements to the task.",
                "general": "Introduce more complex problem-solving elements or increase the cognitive load of the task."
            },
            "decrease": {
                "novice": "Simplify the task, provide step-by-step instructions, or offer more frequent guidance.",
                "expert": "Streamline decision-making processes or provide automated cognitive support for routine aspects.",
                "general": "Simplify the task, provide clearer instructions, or offer decision-making support."
            }
        },
        "Physical Demand": {
            "increase": "Add more physical elements to the task or increase the duration of physical activities.",
            "decrease": "Reduce physical requirements, provide ergonomic support, or automate physical aspects of the task."
        },
        "Temporal Demand": {
            "increase": {
                "short": "Introduce tighter deadlines within the limited timeframe.",
                "long": "Increase the frequency of milestones or deliverables throughout the project duration.",
                "general": "Introduce tighter deadlines or increase the pace of task progression."
            },
            "decrease": {
                "short": "Extend the timeframe if possible, or prioritize essential subtasks.",
                "long": "Introduce more flexible deadlines or longer intervals between milestones.",
                "general": "Allow more time for task completion or introduce breaks between sub-tasks."
            }
        },
        "Performance": {
            "increase": {
                "low": "Set gradually increasing performance standards to encourage improvement.",
                "high": "Introduce stretch goals or additional performance metrics to track.",
                "general": "Set higher performance standards or introduce more challenging success criteria."
            },
            "decrease": {
                "low": "Adjust performance expectations to be more achievable, focusing on key outcomes.",
                "high": "Prioritize quality over quantity, allowing for a more focused approach on critical aspects.",
                "general": "Adjust performance expectations or provide additional resources to support task completion."
            }
        },
        "Effort": {
            "increase": "Introduce additional sub-tasks or increase the complexity of existing elements.",
            "decrease": "Streamline processes, provide shortcuts, or offer more efficient tools for task completion."
        },
        "Frustration": {
            "increase": "Introduce more challenging obstacles or reduce available resources.",
            "decrease": {
                "novice": "Improve user interface, provide more frequent positive feedback, and offer readily available support.",
                "expert": "Minimize unnecessary obstacles, provide advanced troubleshooting tools, and allow for greater autonomy.",
                "general": "Improve user interface, provide clearer feedback, or offer more support during task execution."
            }
        }
    }
    
    if isinstance(advice[dimension][direction], dict):
        return advice[dimension][direction][context_factors["audience"]]
    else:
        return advice[dimension][direction]
