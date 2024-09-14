import streamlit as st
import pandas as pd
import plotly.express as px
from nasa_tlx import calculate_tlx_score, get_dimension_impact, pair_wise_comparison, calculate_weights
from guidance import generate_guidance
from visualizations import create_radar_chart, create_bar_chart
from styles import set_page_style

st.set_page_config(page_title="NASA Task Load Index", layout="wide")

def save_assessment(name: str, scores: dict, weights: dict, overall_score: float):
    if 'assessments' not in st.session_state:
        st.session_state.assessments = []
    
    assessment = {
        'name': name,
        'scores': scores,
        'weights': weights,
        'overall_score': overall_score
    }
    st.session_state.assessments.append(assessment)

def get_assessments():
    return st.session_state.get('assessments', [])

def main():
    theme = set_page_style()
    st.title("NASA Task Load Index (TLX) Assessment")

    st.header("Your Assessments")
    assessments = get_assessments()
    if assessments:
        selected_assessment = st.selectbox("Select an assessment", [f"{a['name']} (Score: {a['overall_score']:.2f})" for a in assessments])
        selected_assessment = assessments[[f"{a['name']} (Score: {a['overall_score']:.2f})" for a in assessments].index(selected_assessment)]
        
        st.write("Selected Assessment Details:")
        st.write(f"Name: {selected_assessment['name']}")
        st.write(f"Overall Score: {selected_assessment['overall_score']:.2f}")
        
        # Display visualizations for the selected assessment
        col1, col2 = st.columns(2)
        with col1:
            radar_fig = create_radar_chart(selected_assessment['scores'])
            st.plotly_chart(radar_fig)
        with col2:
            bar_fig = create_bar_chart(selected_assessment['scores'])
            st.plotly_chart(bar_fig)
    else:
        st.write("You haven't created any assessments yet.")

    st.header("Create New Assessment")
    new_assessment_name = st.text_input("Assessment Name")

    # NASA TLX dimensions with descriptions
    tlx_dimensions = {
        "Mental Demand": "How much mental and perceptual activity was required? Was the task easy or demanding, simple or complex?",
        "Physical Demand": "How much physical activity was required? Was the task easy or demanding, slack or strenuous?",
        "Temporal Demand": "How much time pressure did you feel due to the pace at which the tasks or task elements occurred?",
        "Performance": "How successful were you in performing the task? How satisfied were you with your performance?",
        "Effort": "How hard did you have to work (mentally and physically) to accomplish your level of performance?",
        "Frustration": "How irritated, stressed, and annoyed versus content, relaxed, and complacent did you feel during the task?"
    }

    # Initialize scores dictionary with default values
    scores = {dim: 50 for dim in tlx_dimensions.keys()}

    # Add input fields for each TLX dimension
    st.subheader("Task Load Assessment")
    st.write("Use the sliders to rate each dimension from 0 to 100.")
    
    for dimension, description in tlx_dimensions.items():
        with st.expander(f"{dimension} - Click to expand"):
            st.write(description)
            scores[dimension] = st.slider(f"{dimension} Rating", 0, 100, 50, key=f"score_{dimension}")

    # Pair-wise comparison for weight calculation
    st.subheader("Dimension Importance Comparison")
    st.write("For each pair, select the dimension that was more important to your experience of workload in the task.")
    
    comparisons = pair_wise_comparison(list(tlx_dimensions.keys()))
    pair_wise_results = {}
    
    for dim1, dim2 in comparisons:
        selected = st.radio(f"Which was more important: {dim1} or {dim2}?", [dim1, dim2], key=f"compare_{dim1}_{dim2}")
        pair_wise_results[(dim1, dim2)] = selected

    # Calculate weights
    weights = calculate_weights(pair_wise_results)

    # Calculate TLX score
    tlx_score = calculate_tlx_score(scores, weights)

    # Display results
    st.subheader("Results")
    st.write(f"Overall Task Load Index Score: {tlx_score:.2f}")

    # Display individual dimension scores and weights
    st.write("Individual Dimension Scores and Weights:")
    results_df = pd.DataFrame({
        "Dimension": list(scores.keys()),
        "Score": list(scores.values()),
        "Weight": [weights[dim] for dim in scores.keys()]
    })
    st.dataframe(results_df)

    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        radar_fig = create_radar_chart(scores)
        st.plotly_chart(radar_fig)
    with col2:
        bar_fig = create_bar_chart(scores)
        st.plotly_chart(bar_fig)

    # Save assessment
    if st.button("Save Assessment"):
        if new_assessment_name:
            save_assessment(new_assessment_name, scores, weights, tlx_score)
            st.success("Assessment saved successfully!")
        else:
            st.error("Please provide a name for the assessment")

if __name__ == "__main__":
    main()
