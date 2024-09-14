import streamlit as st
import pandas as pd
import plotly.express as px
from nasa_tlx import calculate_tlx_score, get_dimension_impact
from guidance import generate_guidance
from visualizations import create_radar_chart, create_bar_chart
from styles import set_page_style

st.set_page_config(page_title="NASA Task Load Index", layout="wide")

def main():
    theme = set_page_style()
    st.title("NASA Task Load Index (TLX) Assessment")

    # Introduction
    st.header("Introduction")
    st.write("""
    The NASA Task Load Index (TLX) is a widely used, subjective assessment tool that allows users to perform subjective workload assessments on operators working with various human-machine interface systems. NASA TLX is a multi-dimensional rating procedure that derives an overall workload score based on a weighted average of ratings on six subscales: Mental Demand, Physical Demand, Temporal Demand, Performance, Effort, and Frustration.
    
    This application helps you assess and analyze task load using the NASA TLX methodology. You can input scores for each dimension, assign weights, and receive guidance on workload adjustment based on your results.
    
    For more information, please refer to the following resources:
    - [NASA TLX Paper](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20000021488.pdf)
    - [NASA TLX Website](https://humansystems.arc.nasa.gov/groups/tlx/)
    """)

    # Project Context
    st.header("Project Context")
    st.write("""
    Please provide context about your project to help generate more accurate guidance. 
    Consider including information such as:
    - Nature of the task or project
    - Target audience or users
    - Expected duration or timeline
    - Complexity level
    - Goals or objectives
    """)
    
    if 'context_submitted' not in st.session_state:
        st.session_state.context_submitted = False
        st.session_state.submitted_context = ""

    if not st.session_state.context_submitted:
        project_context = st.text_area("Project Context:", value=st.session_state.submitted_context, height=150, key="project_context")
        if st.button("Submit Context"):
            st.session_state.submitted_context = project_context
            st.session_state.context_submitted = True
            st.rerun()
    else:
        st.write("Submitted Context:")
        st.write(st.session_state.submitted_context)
        if st.button("Edit Project Context"):
            st.session_state.context_submitted = False
            st.rerun()
        
    st.markdown('''
    <style>
    .stTextArea textarea {
        background-color: white !important;
        border: 1px solid black !important;
    }
    </style>
    ''', unsafe_allow_html=True)

    # Input for TLX dimensions
    st.header("Task Load Assessment")
    st.write("Use the sliders to rate each dimension from 0 to 100.")
    
    dimensions = ["Mental Demand", "Physical Demand", "Temporal Demand", "Performance", "Effort", "Frustration"]
    dimension_descriptions = {
        "Mental Demand": "How much mental and perceptual activity was required?",
        "Physical Demand": "How much physical activity was required?",
        "Temporal Demand": "How much time pressure did you feel due to the pace at which tasks or task elements occurred?",
        "Performance": "How successful were you in performing the task?",
        "Effort": "How hard did you have to work to accomplish your level of performance?",
        "Frustration": "How irritated, stressed, and annoyed versus content, relaxed, and complacent did you feel during the task?"
    }
    
    scores = {}
    weights = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Scores")
        for dim in dimensions:
            with st.expander(f"{dim} - {dimension_descriptions[dim]}", expanded=True):
                scores[dim] = st.slider(f"{dim} Score", 0, 100, 50, key=f"score_{dim}")

    with col2:
        st.subheader("Weights")
        st.write("""
        Assign relative importance to each dimension (1-5).
        1: Not important | 3: Moderately important | 5: Very important
        """)
        for dim in dimensions:
            weights[dim] = st.slider(f"{dim} Weight", 1, 5, 3, key=f"weight_{dim}")
        
        total_weight = sum(weights.values())
        for dim in dimensions:
            weights[dim] /= total_weight

    # Calculate TLX score
    tlx_score = calculate_tlx_score(scores, weights)

    # Display results
    st.header("Results")
    st.write("""
    This section displays the overall Task Load Index score and visualizations of your assessment.
    The radar chart shows the scores for each dimension, while the bar chart compares the dimensions side by side.
    """)
    st.subheader(f"Overall Task Load Index Score: {tlx_score:.2f}")

    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        radar_fig = create_radar_chart(scores)
        st.plotly_chart(radar_fig)

    with col2:
        bar_fig = create_bar_chart(scores)
        st.plotly_chart(bar_fig)

    # Display dimension impact
    st.subheader("Dimension Impact")
    st.write("""
    The Dimension Impact table shows how each dimension contributes to the overall score.
    Higher values indicate a greater impact on the total workload.
    """)
    impact = get_dimension_impact(scores, weights)
    for dim, weighted_score in impact:
        st.write(f"{dim}: {weighted_score:.2f}")

    # Desired changes
    st.header("Workload Adjustment")
    st.write("""
    Use this section to explore potential adjustments to the task or work environment.
    Indicate how much you'd like to change the overall workload, and the system will provide tailored guidance
    based on your current scores, desired change, and project context.
    """)
    col_minus, col_slider, col_plus = st.columns([1, 10, 1])
    with col_minus:
        st.markdown('<div class="slider-icon">-</div>', unsafe_allow_html=True)
    with col_slider:
        desired_change = st.slider("Desired change in overall TLX score", -100, 100, 0)
    with col_plus:
        st.markdown('<div class="slider-icon">+</div>', unsafe_allow_html=True)
    
    # AI Model Selection
    ai_models = ["GPT-3.5", "GPT-4", "BERT"]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_model = st.selectbox("Select Your Model", ai_models)
    with col2:
        if st.button("Generate Guidance"):
            if st.session_state.context_submitted:
                guidance = generate_guidance(scores, desired_change, st.session_state.submitted_context, selected_model)
                st.subheader("Guidance for Workload Adjustment")
                st.write(guidance)
            else:
                st.warning("Please submit the project context before generating guidance.")

if __name__ == "__main__":
    main()
