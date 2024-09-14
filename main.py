import streamlit as st
import pandas as pd
import plotly.express as px
from nasa_tlx import calculate_tlx_score, get_dimension_impact
from guidance import generate_guidance
from visualizations import create_radar_chart, create_bar_chart
from styles import set_page_style
from database import User, Assessment, get_db
from sqlalchemy.orm import Session
import bcrypt

st.set_page_config(page_title="NASA Task Load Index", layout="wide")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(db: Session, username: str, password: str):
    hashed_password = hash_password(password)
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def save_assessment(db: Session, user_id: int, name: str, scores: dict, overall_score: float):
    assessment = Assessment(
        user_id=user_id,
        name=name,
        mental_demand=scores['Mental Demand'],
        physical_demand=scores['Physical Demand'],
        temporal_demand=scores['Temporal Demand'],
        performance=scores['Performance'],
        effort=scores['Effort'],
        frustration=scores['Frustration'],
        overall_score=overall_score
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

def get_user_assessments(db: Session, user_id: int):
    return db.query(Assessment).filter(Assessment.user_id == user_id).all()

def main():
    theme = set_page_style()
    st.title("NASA Task Load Index (TLX) Assessment")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id is None:
        st.header("Login / Register")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                db = next(get_db())
                user = get_user(db, login_username)
                if user and verify_password(login_password, user.password):
                    st.session_state.user_id = user.id
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with col2:
            st.subheader("Register")
            reg_username = st.text_input("Username", key="reg_username")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            if st.button("Register"):
                db = next(get_db())
                existing_user = get_user(db, reg_username)
                if existing_user:
                    st.error("Username already exists")
                else:
                    create_user(db, reg_username, reg_password)
                    st.success("User registered successfully! Please log in.")

    else:
        db = next(get_db())
        user = db.query(User).filter(User.id == st.session_state.user_id).first()
        st.write(f"Welcome, {user.username}!")
        if st.button("Logout"):
            st.session_state.user_id = None
            st.rerun()

        st.header("Your Assessments")
        user_assessments = get_user_assessments(db, st.session_state.user_id)
        if user_assessments:
            selected_assessment = st.selectbox("Select an assessment", [f"{a.name} (Score: {a.overall_score:.2f})" for a in user_assessments])
            selected_assessment = user_assessments[[f"{a.name} (Score: {a.overall_score:.2f})" for a in user_assessments].index(selected_assessment)]
        else:
            st.write("You haven't created any assessments yet.")

        st.header("Create New Assessment")
        new_assessment_name = st.text_input("Assessment Name")

        # Initialize scores dictionary with default values
        scores = {
            "Mental Demand": 50,
            "Physical Demand": 50,
            "Temporal Demand": 50,
            "Performance": 50,
            "Effort": 50,
            "Frustration": 50
        }

        # Add input fields for each TLX dimension
        st.subheader("Task Load Assessment")
        st.write("Use the sliders to rate each dimension from 0 to 100.")
        
        for dimension in scores.keys():
            scores[dimension] = st.slider(f"{dimension}", 0, 100, 50, key=f"score_{dimension}")

        # Calculate TLX score
        tlx_score = calculate_tlx_score(scores)

        # Display results
        st.subheader("Results")
        st.write(f"Overall Task Load Index Score: {tlx_score:.2f}")

        # Display individual dimension scores
        st.write("Individual Dimension Scores:")
        for dimension, score in scores.items():
            st.write(f"{dimension}: {score}")

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
                save_assessment(db, st.session_state.user_id, new_assessment_name, scores, tlx_score)
                st.success("Assessment saved successfully!")
            else:
                st.error("Please provide a name for the assessment")

if __name__ == "__main__":
    main()
