import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from nasa_tlx import calculate_tlx_score, get_dimension_impact, pair_wise_comparison, calculate_weights
from guidance import generate_guidance
from visualizations import create_radar_chart, create_bar_chart
from styles import set_page_style

# Check if the app is running in embedded mode
embedded = st.query_params.get("embedded", "false").lower() == "true"

def generate_unique_id():
    return str(uuid.uuid4())

def save_assessment(name: str, task_description: str, scores: dict, weights: dict, overall_score: float):
    if 'assessments' not in st.session_state:
        st.session_state.assessments = {}
    
    assessment_id = generate_unique_id()
    assessment = {
        'id': assessment_id,
        'name': name,
        'task_description': task_description,
        'scores': scores,
        'weights': weights,
        'overall_score': overall_score,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.assessments[assessment_id] = assessment
    return assessment_id

def get_assessment(assessment_id: str):
    return st.session_state.assessments.get(assessment_id)

def get_assessments():
    return list(st.session_state.assessments.values())

def main():
    global embedded
    if embedded:
        st.set_page_config(page_title="NASA TLX", layout="centered")
    else:
        st.set_page_config(page_title="NASA Task Load Index", layout="wide")

    if not embedded:
        theme = set_page_style()
    
    if embedded:
        st.markdown("""
        <style>
        .main > div {
            padding-top: 0;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    if not embedded:
        st.title("NASA Task Load Index (TLX) Assessment")
        
        # Generate unique URL for the current assessment
        current_url = st.query_params
        assessment_id = current_url.get("id")
        
        if assessment_id:
            assessment = get_assessment(assessment_id)
            if assessment:
                permalink = f"https://nasa-task-load-index-tli.streamlit.app/?id={assessment_id}"
                embed_link = f"<iframe src='{permalink}&embedded=true' width='100%' height='600px'></iframe>"
                
                st.markdown(f"[Permalink]({permalink})")
                st.markdown("Embed this assessment:")
                st.code(embed_link, language="html")
                
                # Display the assessment details
                st.header("Assessment Details")
                st.write(f"Name: {assessment['name']}")
                st.write(f"Task Description: {assessment['task_description']}")
                st.write(f"Overall Score: {assessment['overall_score']:.2f}")
                
                col1, col2 = st.columns(2)
                with col1:
                    radar_fig = create_radar_chart(assessment['scores'])
                    st.plotly_chart(radar_fig, use_container_width=True)
                with col2:
                    bar_fig = create_bar_chart(assessment['scores'])
                    st.plotly_chart(bar_fig, use_container_width=True)
                
                return  # End the function here to avoid showing the creation form
    else:
        st.header("NASA TLX Assessment")

    if not embedded:
        st.header("Your Assessments")
        assessments = get_assessments()
        if assessments:
            selected_assessment = st.selectbox("Select an assessment", [f"{a['name']} (Score: {a['overall_score']:.2f})" for a in assessments])
            selected_assessment = [a for a in assessments if f"{a['name']} (Score: {a['overall_score']:.2f})" == selected_assessment][0]
            
            st.write("Selected Assessment Details:")
            st.write(f"Name: {selected_assessment['name']}")
            st.write(f"Task Description: {selected_assessment['task_description']}")
            st.write(f"Overall Score: {selected_assessment['overall_score']:.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                radar_fig = create_radar_chart(selected_assessment['scores'])
                st.plotly_chart(radar_fig, use_container_width=True)
            with col2:
                bar_fig = create_bar_chart(selected_assessment['scores'])
                st.plotly_chart(bar_fig, use_container_width=True)
        else:
            st.write("You haven't created any assessments yet.")

    st.header("Create New Assessment")
    new_assessment_name = st.text_input("Your Name")
    task_description = st.text_area("Task Description", "Describe the task you're assessing...")

    tlx_dimensions = {
        "Mental Demand": "How much mental and perceptual activity was required?",
        "Physical Demand": "How much physical activity was required?",
        "Temporal Demand": "How much time pressure did you feel due to the pace of the task?",
        "Performance": "How successful were you in performing the task?",
        "Effort": "How hard did you have to work to accomplish your level of performance?",
        "Frustration": "How irritated, stressed, and annoyed did you feel during the task?"
    }

    scores = {dim: 50 for dim in tlx_dimensions.keys()}

    st.subheader("Task Load Assessment")
    st.write("Use the sliders to rate each dimension from 0 to 100.")
    
    for dimension, description in tlx_dimensions.items():
        with st.expander(f"{dimension} - Click to expand"):
            st.write(description)
            scores[dimension] = st.slider(f"{dimension} Rating", 0, 100, 50, key=f"score_{dimension}")

    st.subheader("Dimension Importance Comparison")
    st.write("For each pair, select the dimension that was more important to your experience of workload in the task.")
    
    comparisons = pair_wise_comparison(list(tlx_dimensions.keys()))
    pair_wise_results = {}
    
    for dim1, dim2 in comparisons:
        selected = st.radio(f"Which was more important: {dim1} or {dim2}?", [dim1, dim2], key=f"compare_{dim1}_{dim2}")
        pair_wise_results[(dim1, dim2)] = selected

    weights = calculate_weights(pair_wise_results)
    tlx_score = calculate_tlx_score(scores, weights)

    st.header("Assessment Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Task Information")
        st.write(f"Name: {new_assessment_name}")
        st.write(f"Task Description: {task_description}")
        st.write(f"Overall Task Load Index Score: {tlx_score:.2f}")

        results_df = pd.DataFrame({
            "Dimension": list(scores.keys()),
            "Score": list(scores.values()),
            "Weight": [weights[dim] for dim in scores.keys()]
        })
        st.dataframe(results_df)

    with col2:
        st.subheader("Visualizations")
        radar_fig = create_radar_chart(scores)
        st.plotly_chart(radar_fig, use_container_width=True)
        bar_fig = create_bar_chart(scores)
        st.plotly_chart(bar_fig, use_container_width=True)

    if st.button("Save Assessment"):
        if new_assessment_name and task_description:
            assessment_id = save_assessment(new_assessment_name, task_description, scores, weights, tlx_score)
            permalink = f"https://nasa-task-load-index-tli.streamlit.app/?id={assessment_id}"
            st.success(f"Assessment saved successfully! [Permalink]({permalink})")
        else:
            st.error("Please provide your name and task description")

if __name__ == "__main__":
    main()
