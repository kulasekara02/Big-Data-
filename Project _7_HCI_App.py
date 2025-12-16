"""
=============================================================================
PROJECT 7: Human-Computer Interaction (HCI) User Interface Prototype
=============================================================================
Course: Modern Database Technologies and Big Data Analytics
Institution: Transport and Telecommunication Institute, Latvia
Academic Level: Master's Program

Description:
    This Streamlit application demonstrates advanced HCI principles through
    an interactive Employee Performance Analytics Dashboard. The prototype
    implements multiple interaction modalities including direct manipulation,
    form-based interaction, natural language queries, and visual feedback
    mechanisms following Norman's Design Principles and Nielsen's Heuristics.

Key HCI Concepts Implemented:
    1. Visibility of System Status
    2. Match Between System and Real World
    3. User Control and Freedom
    4. Consistency and Standards
    5. Error Prevention
    6. Recognition Rather than Recall
    7. Flexibility and Efficiency of Use
    8. Aesthetic and Minimalist Design
    9. Help Users Recognize and Recover from Errors
    10. Help and Documentation

Author: VIHANAGA
Date: December 2024
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Employee Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI/UX following HCI principles
st.markdown("""
<style>
    /* Primary color scheme - Professional blue theme */
    :root {
        --primary-color: #1E3A5F;
        --secondary-color: #3498DB;
        --accent-color: #E74C3C;
        --success-color: #27AE60;
        --warning-color: #F39C12;
        --background-light: #F8F9FA;
        --text-primary: #2C3E50;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid var(--secondary-color);
        margin-bottom: 2rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary-color);
        padding: 0.5rem 0;
        border-left: 4px solid var(--secondary-color);
        padding-left: 1rem;
        margin: 1rem 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Info boxes */
    .info-box {
        background-color: #E8F4FD;
        border-left: 4px solid var(--secondary-color);
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* Success feedback */
    .success-feedback {
        background-color: #D4EDDA;
        border-left: 4px solid var(--success-color);
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        animation: fadeIn 0.5s ease;
    }
    
    /* Error feedback */
    .error-feedback {
        background-color: #F8D7DA;
        border-left: 4px solid var(--accent-color);
        padding: 1rem;
        border-radius: 0 8px 8px 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980B9 0%, #1A5276 100%);
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--background-light);
    }
    
    /* Progress indicator */
    .progress-container {
        background-color: #E0E0E0;
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(52, 152, 219, 0); }
        100% { box-shadow: 0 0 0 0 rgba(52, 152, 219, 0); }
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Help text */
    .help-text {
        font-size: 0.85rem;
        color: #6C757D;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA GENERATION AND MANAGEMENT
# =============================================================================

@st.cache_data
def generate_employee_data(n_employees=150):
    """
    Generate synthetic employee performance dataset.
    
    This function creates realistic employee data including demographics,
    performance metrics, and temporal patterns for demonstration purposes.
    
    Parameters:
        n_employees (int): Number of employee records to generate
        
    Returns:
        pd.DataFrame: Employee performance dataset
    """
    np.random.seed(42)
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'R&D', 'Customer Support']
    positions = {
        'Engineering': ['Junior Developer', 'Senior Developer', 'Tech Lead', 'Architect'],
        'Sales': ['Sales Rep', 'Account Manager', 'Sales Lead', 'Regional Manager'],
        'Marketing': ['Marketing Analyst', 'Marketing Manager', 'Brand Manager', 'CMO'],
        'HR': ['HR Assistant', 'HR Specialist', 'HR Manager', 'HR Director'],
        'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager', 'CFO'],
        'Operations': ['Operations Analyst', 'Operations Manager', 'Director', 'COO'],
        'R&D': ['Research Analyst', 'Scientist', 'Principal Scientist', 'R&D Director'],
        'Customer Support': ['Support Agent', 'Team Lead', 'Support Manager', 'Director']
    }
    
    education_levels = ['High School', 'Bachelor\'s', 'Master\'s', 'PhD']
    
    data = []
    for i in range(n_employees):
        dept = np.random.choice(departments, p=[0.25, 0.15, 0.12, 0.08, 0.1, 0.1, 0.1, 0.1])
        position = np.random.choice(positions[dept])
        
        # Generate correlated metrics
        base_performance = np.random.normal(70, 15)
        
        record = {
            'Employee_ID': f'EMP{1000 + i}',
            'Name': f'Employee_{i+1}',
            'Department': dept,
            'Position': position,
            'Education': np.random.choice(education_levels, p=[0.15, 0.45, 0.30, 0.10]),
            'Years_Experience': np.random.randint(1, 25),
            'Age': np.random.randint(22, 60),
            'Performance_Score': np.clip(base_performance + np.random.normal(0, 5), 0, 100),
            'Satisfaction_Score': np.clip(base_performance * 0.8 + np.random.normal(20, 10), 0, 100),
            'Projects_Completed': np.random.poisson(8),
            'Training_Hours': np.random.randint(10, 200),
            'Salary': np.random.randint(35000, 150000),
            'Hire_Date': datetime.now() - timedelta(days=np.random.randint(30, 3650)),
            'Last_Review_Date': datetime.now() - timedelta(days=np.random.randint(1, 365)),
            'Remote_Work_Percentage': np.random.choice([0, 25, 50, 75, 100]),
            'Team_Size': np.random.randint(3, 20),
            'Manager_Rating': np.clip(base_performance * 0.9 + np.random.normal(10, 8), 0, 100),
            'Peer_Rating': np.clip(base_performance * 0.85 + np.random.normal(15, 10), 0, 100),
            'Attendance_Rate': np.clip(95 + np.random.normal(0, 3), 80, 100),
            'Goal_Achievement': np.clip(base_performance + np.random.normal(5, 10), 0, 100)
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    df['Performance_Score'] = df['Performance_Score'].round(1)
    df['Satisfaction_Score'] = df['Satisfaction_Score'].round(1)
    df['Manager_Rating'] = df['Manager_Rating'].round(1)
    df['Peer_Rating'] = df['Peer_Rating'].round(1)
    df['Attendance_Rate'] = df['Attendance_Rate'].round(1)
    df['Goal_Achievement'] = df['Goal_Achievement'].round(1)
    
    return df

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def initialize_session_state():
    """Initialize session state variables for interaction tracking."""
    if 'interaction_log' not in st.session_state:
        st.session_state.interaction_log = []
    if 'filter_history' not in st.session_state:
        st.session_state.filter_history = []
    if 'undo_stack' not in st.session_state:
        st.session_state.undo_stack = []
    if 'bookmarks' not in st.session_state:
        st.session_state.bookmarks = []
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'dashboard'
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

def log_interaction(action_type, details):
    """
    Log user interactions for usability analysis.
    
    HCI Principle: System Status Visibility - Track user actions
    to understand interaction patterns and improve UX.
    """
    interaction = {
        'timestamp': datetime.now().isoformat(),
        'action': action_type,
        'details': details
    }
    st.session_state.interaction_log.append(interaction)

# =============================================================================
# UI COMPONENTS WITH HCI PRINCIPLES
# =============================================================================

def render_header():
    """Render application header with navigation."""
    st.markdown('<h1 class="main-header">📊 Employee Performance Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Breadcrumb navigation - HCI: Recognition rather than recall
    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        st.markdown("**Current View:** " + st.session_state.current_view.title())
    with col3:
        if st.button("🏠 Home", key="home_btn"):
            st.session_state.current_view = 'dashboard'
            log_interaction('navigation', 'Return to home')

def render_sidebar_filters(df):
    """
    Render sidebar with filtering controls.
    
    HCI Principles Applied:
    - Visibility: Clear filter status indicators
    - User Control: Multiple filter options with reset capability
    - Consistency: Standardized control layouts
    - Recognition: Dropdown menus instead of free text
    """
    st.sidebar.markdown("## 🎛️ Filter Controls")
    
    # Help tooltip - HCI: Help and Documentation
    with st.sidebar.expander("ℹ️ How to Use Filters"):
        st.markdown("""
        1. **Department**: Select one or more departments
        2. **Performance Range**: Use slider to set min/max
        3. **Experience**: Filter by years of experience
        4. **Apply**: Click to update visualizations
        5. **Reset**: Clear all filters
        """)
    
    # Department filter - Multi-select with visual feedback
    st.sidebar.markdown("### Department")
    departments = st.sidebar.multiselect(
        "Select Department(s)",
        options=df['Department'].unique().tolist(),
        default=[],
        help="Hold Ctrl/Cmd to select multiple departments",
        key="dept_filter"
    )
    
    # Performance score range - Direct manipulation slider
    st.sidebar.markdown("### Performance Score")
    perf_min, perf_max = st.sidebar.slider(
        "Performance Range",
        min_value=0.0,
        max_value=100.0,
        value=(0.0, 100.0),
        step=5.0,
        help="Drag endpoints to set range",
        key="perf_slider"
    )
    
    # Experience filter
    st.sidebar.markdown("### Years of Experience")
    exp_min, exp_max = st.sidebar.slider(
        "Experience Range",
        min_value=int(df['Years_Experience'].min()),
        max_value=int(df['Years_Experience'].max()),
        value=(int(df['Years_Experience'].min()), int(df['Years_Experience'].max())),
        key="exp_slider"
    )
    
    # Education level filter
    st.sidebar.markdown("### Education Level")
    education = st.sidebar.multiselect(
        "Select Education Level(s)",
        options=df['Education'].unique().tolist(),
        default=[],
        key="edu_filter"
    )
    
    # Salary range filter
    st.sidebar.markdown("### Salary Range ($)")
    salary_min, salary_max = st.sidebar.slider(
        "Salary Range",
        min_value=int(df['Salary'].min()),
        max_value=int(df['Salary'].max()),
        value=(int(df['Salary'].min()), int(df['Salary'].max())),
        step=5000,
        format="$%d",
        key="salary_slider"
    )
    
    st.sidebar.markdown("---")
    
    # Action buttons - HCI: User Control and Freedom
    col1, col2 = st.sidebar.columns(2)
    with col1:
        apply_clicked = st.button("✅ Apply", key="apply_filters", use_container_width=True)
    with col2:
        reset_clicked = st.button("🔄 Reset", key="reset_filters", use_container_width=True)
    
    # Store current filter state for undo functionality
    current_filters = {
        'departments': departments,
        'perf_range': (perf_min, perf_max),
        'exp_range': (exp_min, exp_max),
        'education': education,
        'salary_range': (salary_min, salary_max)
    }
    
    if apply_clicked:
        log_interaction('filter_apply', json.dumps(current_filters, default=str))
        st.session_state.filter_history.append(current_filters)
        st.sidebar.success("✅ Filters applied successfully!")
    
    if reset_clicked:
        log_interaction('filter_reset', 'All filters cleared')
        st.session_state.undo_stack.append(current_filters)
        st.rerun()
    
    return current_filters

def apply_filters(df, filters):
    """Apply filter criteria to dataframe."""
    filtered_df = df.copy()
    
    if filters['departments']:
        filtered_df = filtered_df[filtered_df['Department'].isin(filters['departments'])]
    
    filtered_df = filtered_df[
        (filtered_df['Performance_Score'] >= filters['perf_range'][0]) &
        (filtered_df['Performance_Score'] <= filters['perf_range'][1])
    ]
    
    filtered_df = filtered_df[
        (filtered_df['Years_Experience'] >= filters['exp_range'][0]) &
        (filtered_df['Years_Experience'] <= filters['exp_range'][1])
    ]
    
    if filters['education']:
        filtered_df = filtered_df[filtered_df['Education'].isin(filters['education'])]
    
    filtered_df = filtered_df[
        (filtered_df['Salary'] >= filters['salary_range'][0]) &
        (filtered_df['Salary'] <= filters['salary_range'][1])
    ]
    
    return filtered_df

def render_kpi_metrics(df):
    """
    Render key performance indicators with visual feedback.
    
    HCI Principle: Visibility of System Status - Users immediately
    see the current state of filtered data.
    """
    st.markdown('<h2 class="section-header">Key Performance Indicators</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="👥 Total Employees",
            value=len(df),
            delta=f"{len(df) - 150} from total" if len(df) != 150 else None,
            help="Number of employees matching current filters"
        )
    
    with col2:
        avg_perf = df['Performance_Score'].mean()
        st.metric(
            label="📈 Avg Performance",
            value=f"{avg_perf:.1f}%",
            delta=f"{avg_perf - 70:.1f}% vs target" if avg_perf else None,
            help="Average performance score (target: 70%)"
        )
    
    with col3:
        avg_sat = df['Satisfaction_Score'].mean()
        st.metric(
            label="😊 Avg Satisfaction",
            value=f"{avg_sat:.1f}%",
            delta=f"{avg_sat - 75:.1f}% vs target" if avg_sat else None,
            help="Average employee satisfaction score"
        )
    
    with col4:
        total_projects = df['Projects_Completed'].sum()
        st.metric(
            label="📁 Total Projects",
            value=f"{total_projects:,}",
            help="Sum of completed projects"
        )
    
    with col5:
        avg_salary = df['Salary'].mean()
        st.metric(
            label="💰 Avg Salary",
            value=f"${avg_salary:,.0f}",
            help="Average employee salary"
        )

def render_visualizations(df):
    """
    Render interactive visualizations with multiple modalities.
    
    HCI Principles Applied:
    - Direct Manipulation: Interactive chart elements
    - Feedback: Hover tooltips and animations
    - Aesthetic Design: Consistent color scheme
    """
    st.markdown('<h2 class="section-header">Data Visualizations</h2>', unsafe_allow_html=True)
    
    # Visualization selection tabs - HCI: User Control
    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "📊 Department Analysis",
        "📈 Performance Trends",
        "🔍 Correlation Matrix",
        "📉 Distribution Analysis"
    ])
    
    with viz_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Department distribution - Interactive bar chart
            dept_stats = df.groupby('Department').agg({
                'Performance_Score': 'mean',
                'Employee_ID': 'count'
            }).reset_index()
            dept_stats.columns = ['Department', 'Avg Performance', 'Employee Count']
            
            fig_dept = px.bar(
                dept_stats,
                x='Department',
                y='Employee Count',
                color='Avg Performance',
                color_continuous_scale='RdYlGn',
                title='Employees by Department (Color: Avg Performance)',
                text='Employee Count'
            )
            fig_dept.update_traces(textposition='outside')
            fig_dept.update_layout(
                xaxis_tickangle=-45,
                showlegend=False,
                height=450
            )
            st.plotly_chart(fig_dept, use_container_width=True)
            log_interaction('visualization', 'Viewed department distribution')
        
        with col2:
            # Position breakdown - Treemap for hierarchical data
            fig_tree = px.treemap(
                df,
                path=['Department', 'Position'],
                values='Salary',
                color='Performance_Score',
                color_continuous_scale='RdYlGn',
                title='Position Hierarchy (Size: Salary, Color: Performance)'
            )
            fig_tree.update_layout(height=450)
            st.plotly_chart(fig_tree, use_container_width=True)
    
    with viz_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot - Experience vs Performance with direct manipulation
            fig_scatter = px.scatter(
                df,
                x='Years_Experience',
                y='Performance_Score',
                color='Department',
                size='Salary',
                hover_data=['Name', 'Position', 'Education'],
                title='Experience vs Performance Analysis',
                labels={
                    'Years_Experience': 'Years of Experience',
                    'Performance_Score': 'Performance Score (%)'
                }
            )
            fig_scatter.update_layout(height=450)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Box plot - Performance by education level
            fig_box = px.box(
                df,
                x='Education',
                y='Performance_Score',
                color='Education',
                title='Performance Distribution by Education',
                category_orders={'Education': ['High School', "Bachelor's", "Master's", 'PhD']}
            )
            fig_box.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)
    
    with viz_tab3:
        # Correlation heatmap - Statistical analysis visualization
        numeric_cols = ['Performance_Score', 'Satisfaction_Score', 'Years_Experience',
                       'Projects_Completed', 'Training_Hours', 'Salary', 'Manager_Rating',
                       'Peer_Rating', 'Attendance_Rate', 'Goal_Achievement']
        
        corr_matrix = df[numeric_cols].corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=numeric_cols,
            y=numeric_cols,
            color_continuous_scale='RdBu_r',
            aspect='auto',
            title='Performance Metrics Correlation Matrix'
        )
        fig_heatmap.update_layout(height=600)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Interpretation help - HCI: Help and Documentation
        st.info("""
        **How to Read the Correlation Matrix:**
        - Values range from -1 (strong negative) to +1 (strong positive)
        - Darker red = stronger positive correlation
        - Darker blue = stronger negative correlation
        - Click and drag to zoom into specific areas
        """)
    
    with viz_tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram with distribution curve
            fig_hist = px.histogram(
                df,
                x='Performance_Score',
                nbins=20,
                marginal='box',
                color_discrete_sequence=['#3498DB'],
                title='Performance Score Distribution'
            )
            fig_hist.update_layout(height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Radar chart for department comparison
            dept_metrics = df.groupby('Department').agg({
                'Performance_Score': 'mean',
                'Satisfaction_Score': 'mean',
                'Goal_Achievement': 'mean',
                'Attendance_Rate': 'mean',
                'Manager_Rating': 'mean'
            }).reset_index()
            
            # Normalize for radar chart
            for col in dept_metrics.columns[1:]:
                dept_metrics[col] = (dept_metrics[col] / dept_metrics[col].max()) * 100
            
            fig_radar = go.Figure()
            
            for _, row in dept_metrics.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[row['Performance_Score'], row['Satisfaction_Score'],
                       row['Goal_Achievement'], row['Attendance_Rate'], row['Manager_Rating']],
                    theta=['Performance', 'Satisfaction', 'Goals', 'Attendance', 'Manager Rating'],
                    fill='toself',
                    name=row['Department']
                ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title='Department Performance Radar',
                height=400
            )
            st.plotly_chart(fig_radar, use_container_width=True)

def render_data_table(df):
    """
    Render interactive data table with sorting and search.
    
    HCI Principles Applied:
    - Direct Manipulation: Clickable column headers for sorting
    - Search: Recognition rather than recall
    - Visibility: Clear data presentation
    """
    st.markdown('<h2 class="section-header">Employee Data Explorer</h2>', unsafe_allow_html=True)
    
    # Search functionality - HCI: Recognition
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search by Name or ID",
            placeholder="Enter employee name or ID...",
            help="Type to filter the table by employee name or ID"
        )
    
    with col2:
        sort_column = st.selectbox(
            "Sort by",
            options=['Performance_Score', 'Salary', 'Years_Experience', 'Name', 'Department'],
            index=0,
            help="Select column to sort by"
        )
    
    with col3:
        sort_order = st.radio(
            "Order",
            options=['Descending', 'Ascending'],
            horizontal=True
        )
    
    # Apply search and sort
    display_df = df.copy()
    
    if search_term:
        display_df = display_df[
            display_df['Name'].str.contains(search_term, case=False) |
            display_df['Employee_ID'].str.contains(search_term, case=False)
        ]
        log_interaction('search', f'Searched for: {search_term}')
    
    ascending = sort_order == 'Ascending'
    display_df = display_df.sort_values(by=sort_column, ascending=ascending)
    
    # Column selection - HCI: User Control
    with st.expander("📋 Select Columns to Display"):
        all_columns = display_df.columns.tolist()
        default_columns = ['Employee_ID', 'Name', 'Department', 'Position',
                          'Performance_Score', 'Salary', 'Years_Experience']
        selected_columns = st.multiselect(
            "Choose columns",
            options=all_columns,
            default=default_columns
        )
    
    if selected_columns:
        display_df = display_df[selected_columns]
    
    # Display count - HCI: System Status
    st.markdown(f"**Showing {len(display_df)} of {len(df)} records**")
    
    # Interactive dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Export functionality - HCI: User Control
    col1, col2, col3 = st.columns([2, 2, 6])
    with col1:
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"employee_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download filtered data as CSV file"
        )
    with col2:
        if st.button("📊 Generate Report"):
            st.success("Report generation initiated!")
            log_interaction('export', 'Report generation requested')

def render_form_interaction(df):
    """
    Render form-based interaction for data entry/modification.
    
    HCI Principles Applied:
    - Error Prevention: Input validation
    - Feedback: Real-time validation messages
    - Consistency: Standardized form layout
    """
    st.markdown('<h2 class="section-header">Employee Performance Entry Form</h2>', unsafe_allow_html=True)
    
    st.info("""
    **Form-Based Interaction Demo**  
    This form demonstrates HCI principles in data entry including input validation,
    error prevention, and immediate feedback mechanisms.
    """)
    
    with st.form("employee_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            emp_name = st.text_input(
                "Employee Name *",
                placeholder="Enter full name",
                help="Required: Enter employee's full name"
            )
            
            department = st.selectbox(
                "Department *",
                options=[''] + df['Department'].unique().tolist(),
                help="Required: Select employee's department"
            )
            
            position = st.text_input(
                "Position *",
                placeholder="e.g., Senior Developer",
                help="Required: Enter job title"
            )
            
            experience = st.number_input(
                "Years of Experience *",
                min_value=0,
                max_value=50,
                value=0,
                help="Enter years of professional experience"
            )
        
        with col2:
            performance = st.slider(
                "Performance Score *",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=0.5,
                help="Rate performance from 0-100"
            )
            
            satisfaction = st.slider(
                "Satisfaction Score",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.5,
                help="Rate satisfaction from 0-100"
            )
            
            salary = st.number_input(
                "Salary ($)",
                min_value=0,
                max_value=500000,
                value=50000,
                step=1000,
                format="%d"
            )
            
            notes = st.text_area(
                "Additional Notes",
                placeholder="Enter any additional information...",
                max_chars=500
            )
        
        st.markdown("---")
        
        # Form validation and submission
        submitted = st.form_submit_button("Submit Entry", use_container_width=True)
        
        if submitted:
            # Error prevention - Validate required fields
            errors = []
            if not emp_name:
                errors.append("Employee Name is required")
            if not department:
                errors.append("Department is required")
            if not position:
                errors.append("Position is required")
            if experience == 0:
                errors.append("Please enter years of experience (or confirm 0)")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
                log_interaction('form_error', json.dumps(errors))
            else:
                # Success feedback - HCI: Visibility of System Status
                st.success("✅ Employee record submitted successfully!")
                st.balloons()
                log_interaction('form_submit', f'New employee: {emp_name}')
                
                # Show confirmation
                st.markdown("### Submitted Data:")
                st.json({
                    "Name": emp_name,
                    "Department": department,
                    "Position": position,
                    "Experience": experience,
                    "Performance": performance,
                    "Satisfaction": satisfaction,
                    "Salary": salary,
                    "Notes": notes
                })

def render_natural_language_query(df):
    """
    Natural language query interface for data exploration.
    
    HCI Principle: Match between system and real world -
    Users can ask questions in natural language.
    """
    st.markdown('<h2 class="section-header">Natural Language Query Interface</h2>', unsafe_allow_html=True)
    
    st.info("""
    **Ask questions about the data in natural language!**  
    Examples: "Show top performers", "Average salary by department", "Who has highest satisfaction?"
    """)
    
    # Predefined queries for recognition-based interaction
    quick_queries = [
        "Select a quick query...",
        "Show top 10 performers",
        "Average performance by department",
        "Employees with performance above 80",
        "Salary distribution by education",
        "Low satisfaction employees (below 60)",
        "New hires this year"
    ]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your question:",
            placeholder="e.g., Who are the top performers in Engineering?",
            key="nl_query"
        )
    
    with col2:
        quick_select = st.selectbox(
            "Or select:",
            options=quick_queries,
            key="quick_query"
        )
    
    # Process query
    active_query = query if query else (quick_select if quick_select != quick_queries[0] else None)
    
    if active_query:
        st.markdown(f"**Processing:** *{active_query}*")
        
        # Simple query processing (demonstration)
        with st.spinner("Analyzing query..."):
            time.sleep(0.5)  # Simulated processing
            
            result_df = None
            result_text = ""
            
            if "top" in active_query.lower() and "performer" in active_query.lower():
                result_df = df.nlargest(10, 'Performance_Score')[
                    ['Employee_ID', 'Name', 'Department', 'Performance_Score']
                ]
                result_text = "Top 10 performing employees:"
            
            elif "average" in active_query.lower() and "department" in active_query.lower():
                result_df = df.groupby('Department')['Performance_Score'].mean().reset_index()
                result_df.columns = ['Department', 'Average Performance']
                result_df = result_df.sort_values('Average Performance', ascending=False)
                result_text = "Average performance by department:"
            
            elif "above 80" in active_query.lower() or "performance above" in active_query.lower():
                result_df = df[df['Performance_Score'] >= 80][
                    ['Employee_ID', 'Name', 'Department', 'Performance_Score']
                ].sort_values('Performance_Score', ascending=False)
                result_text = f"Found {len(result_df)} employees with performance above 80:"
            
            elif "low satisfaction" in active_query.lower() or "below 60" in active_query.lower():
                result_df = df[df['Satisfaction_Score'] < 60][
                    ['Employee_ID', 'Name', 'Department', 'Satisfaction_Score', 'Performance_Score']
                ]
                result_text = f"Found {len(result_df)} employees with satisfaction below 60:"
            
            elif "salary" in active_query.lower() and "education" in active_query.lower():
                result_df = df.groupby('Education')['Salary'].agg(['mean', 'min', 'max']).reset_index()
                result_df.columns = ['Education', 'Average Salary', 'Min Salary', 'Max Salary']
                result_text = "Salary statistics by education level:"
            
            elif "new hire" in active_query.lower():
                current_year = datetime.now().year
                result_df = df[df['Hire_Date'].dt.year == current_year][
                    ['Employee_ID', 'Name', 'Department', 'Hire_Date', 'Performance_Score']
                ]
                result_text = f"New hires in {current_year}:"
            
            else:
                result_text = "I couldn't understand that query. Try one of the quick queries above!"
            
            if result_df is not None and len(result_df) > 0:
                st.success(result_text)
                st.dataframe(result_df, use_container_width=True)
                log_interaction('nl_query', active_query)
            elif result_df is not None:
                st.warning(f"No results found for: {active_query}")
            else:
                st.warning(result_text)

def render_interaction_log():
    """
    Display interaction log for usability analysis.
    
    HCI Principle: Visibility - Show users their interaction history.
    """
    st.markdown('<h2 class="section-header">Interaction Log (Usability Analysis)</h2>', unsafe_allow_html=True)
    
    if st.session_state.interaction_log:
        log_df = pd.DataFrame(st.session_state.interaction_log)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Interactions", len(log_df))
        with col2:
            st.metric("Unique Actions", log_df['action'].nunique())
        with col3:
            most_common = log_df['action'].mode().iloc[0] if len(log_df) > 0 else "N/A"
            st.metric("Most Common Action", most_common)
        
        # Action distribution
        action_counts = log_df['action'].value_counts()
        fig = px.pie(
            values=action_counts.values,
            names=action_counts.index,
            title="Interaction Distribution",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Raw log
        with st.expander("View Raw Interaction Log"):
            st.dataframe(log_df, use_container_width=True)
        
        if st.button("Clear Log"):
            st.session_state.interaction_log = []
            st.rerun()
    else:
        st.info("No interactions recorded yet. Start exploring the dashboard to generate data!")

def render_help_section():
    """
    Comprehensive help and documentation section.
    
    HCI Principle: Help and Documentation - Provide accessible help
    that is easy to search and focused on user tasks.
    """
    st.markdown('<h2 class="section-header">Help & Documentation</h2>', unsafe_allow_html=True)
    
    help_tabs = st.tabs(["🚀 Getting Started", "🎛️ Using Filters", "📊 Visualizations", "❓ FAQ"])
    
    with help_tabs[0]:
        st.markdown("""
        ### Welcome to the Employee Performance Analytics Dashboard!
        
        This application demonstrates Human-Computer Interaction (HCI) principles
        through an interactive data exploration interface.
        
        **Key Features:**
        1. **Interactive Filtering** - Use sidebar controls to filter data
        2. **Multiple Visualizations** - Explore data through various chart types
        3. **Data Table** - Search, sort, and export employee data
        4. **Form Entry** - Add new employee records with validation
        5. **Natural Language Queries** - Ask questions in plain English
        
        **Getting Started:**
        1. Use the sidebar filters to narrow down the employee data
        2. Explore different visualization tabs to gain insights
        3. Use the search function in the data table to find specific employees
        4. Try the natural language query feature to ask questions
        """)
    
    with help_tabs[1]:
        st.markdown("""
        ### Filter Controls Guide
        
        **Department Filter:**
        - Click to open dropdown
        - Select one or multiple departments
        - Hold Ctrl/Cmd for multiple selections
        
        **Range Sliders:**
        - Drag the endpoints to set minimum and maximum values
        - The current range is displayed above the slider
        
        **Applying Filters:**
        - Click "Apply" to update all visualizations
        - Click "Reset" to clear all filters
        
        **Tips:**
        - Filters work together (AND logic)
        - Watch the KPI metrics update to see filter effects
        """)
    
    with help_tabs[2]:
        st.markdown("""
        ### Visualization Guide
        
        **Interactive Features:**
        - **Hover** over data points for detailed tooltips
        - **Click and drag** to zoom into specific areas
        - **Double-click** to reset zoom
        - **Click legend items** to hide/show data series
        
        **Chart Types:**
        - **Bar Chart**: Compare categories
        - **Scatter Plot**: Explore relationships between variables
        - **Box Plot**: View distributions and outliers
        - **Heatmap**: Identify correlations
        - **Radar Chart**: Compare multiple metrics simultaneously
        """)
    
    with help_tabs[3]:
        st.markdown("""
        ### Frequently Asked Questions
        
        **Q: How do I export data?**  
        A: Use the "Download CSV" button below the data table.
        
        **Q: Can I save my filter settings?**  
        A: Currently, filters reset on page refresh. Use bookmarks in your browser.
        
        **Q: What does the correlation matrix show?**  
        A: It shows how strongly different metrics relate to each other.
        Values closer to 1 or -1 indicate stronger relationships.
        
        **Q: How is performance score calculated?**  
        A: This demo uses simulated data. In real applications,
        this would be based on your organization's evaluation criteria.
        """)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Load data
    df = generate_employee_data()
    
    # Render header
    render_header()
    
    # Sidebar filters
    filters = render_sidebar_filters(df)
    
    # Apply filters
    filtered_df = apply_filters(df, filters)
    
    # Main content area with tabs for different interaction modalities
    main_tabs = st.tabs([
        "📊 Dashboard",
        "📋 Data Explorer",
        "✏️ Form Entry",
        "💬 Natural Language",
        "📈 Analytics Log",
        "❓ Help"
    ])
    
    with main_tabs[0]:
        render_kpi_metrics(filtered_df)
        render_visualizations(filtered_df)
        log_interaction('page_view', 'Dashboard')
    
    with main_tabs[1]:
        render_data_table(filtered_df)
        log_interaction('page_view', 'Data Explorer')
    
    with main_tabs[2]:
        render_form_interaction(df)
        log_interaction('page_view', 'Form Entry')
    
    with main_tabs[3]:
        render_natural_language_query(filtered_df)
        log_interaction('page_view', 'Natural Language')
    
    with main_tabs[4]:
        render_interaction_log()
        log_interaction('page_view', 'Analytics Log')
    
    with main_tabs[5]:
        render_help_section()
        log_interaction('page_view', 'Help')
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.85rem;'>
        <p>Employee Performance Analytics Dashboard | HCI Prototype</p>
        <p>Master's Program - Modern Database Technologies and Big Data Analytics</p>
        <p>Transport and Telecommunication Institute, Latvia | December 2024</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
