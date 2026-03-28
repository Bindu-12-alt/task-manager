import streamlit as st
from task_manager import TaskManager

st.set_page_config(page_title="Task Manager", page_icon="✔", layout="wide")

PRIORITY_COLORS = {"High": "#e74c3c", "Medium": "#e67e22", "Low": "#27ae60"}

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .app-header {
        background: #1a3a5c;
        padding: 18px 32px;
        border-radius: 10px;
        margin-bottom: 24px;
    }
    .app-header h1 { color: white; margin: 0; font-size: 26px; font-family: 'Segoe UI', sans-serif; }
    .task-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        border-left: 5px solid #ccc;
        box-shadow: 0 2px 6px rgba(0,0,0,0.07);
    }
    .task-title { font-size: 16px; font-weight: 700; color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
    .task-title.done { color: #aaa; text-decoration: line-through; }
    .task-desc { color: #7f8c8d; font-size: 13px; margin-top: 4px; }
    .task-date { color: #95a5a6; font-size: 12px; margin-top: 6px; }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        color: white;
        font-size: 11px;
        font-weight: bold;
        margin-left: 10px;
    }
    section[data-testid="stSidebar"] { background: #1a3a5c !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .stApp { background: #f0f2f5; }
</style>
""", unsafe_allow_html=True)

if "manager" not in st.session_state:
    st.session_state.manager = TaskManager()
if "edit_task" not in st.session_state:
    st.session_state.edit_task = None
if "show_form" not in st.session_state:
    st.session_state.show_form = False

manager = st.session_state.manager

with st.sidebar:
    st.markdown("## ✔ Task Manager")
    st.markdown("---")
    view = st.radio("Navigation", ["All Tasks", "Completed", "Pending"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("➕  Add New Task", use_container_width=True):
        st.session_state.show_form = True
        st.session_state.edit_task = None

st.markdown('<div class="app-header"><h1>✔ Task Manager</h1></div>', unsafe_allow_html=True)

view_map = {"All Tasks": "all", "Completed": "completed", "Pending": "pending"}
current_view = view_map[view]

search = st.text_input("🔍 Search tasks...", placeholder="Search by title or description...")

if st.session_state.show_form or st.session_state.edit_task:
    task = st.session_state.edit_task
    st.markdown("### " + ("Edit Task" if task else "Add New Task"))
    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("Title *", value=task.title if task else "")
        description = st.text_area("Description", value=task.description if task else "")
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"],
                                    index=["High", "Medium", "Low"].index(task.priority) if task else 1)
        with col2:
            due_date = st.text_input("Due Date (YYYY-MM-DD)", value=task.due_date if task else "")

        col_save, col_cancel, _ = st.columns([1, 1, 4])
        with col_save:
            submitted = st.form_submit_button("💾 Save Task", use_container_width=True)
        with col_cancel:
            cancelled = st.form_submit_button("✖ Cancel", use_container_width=True)

        if submitted:
            if not title.strip():
                st.error("Title is required.")
            else:
                if task:
                    manager.update(task.id, title.strip(), description.strip(), priority, due_date.strip())
                else:
                    manager.add(title.strip(), description.strip(), priority, due_date.strip())
                st.session_state.show_form = False
                st.session_state.edit_task = None
                st.rerun()
        if cancelled:
            st.session_state.show_form = False
            st.session_state.edit_task = None
            st.rerun()
    st.markdown("---")

tasks = manager.get_filtered(current_view, search)
st.markdown(f"### {view} ({len(tasks)})")

if not tasks:
    st.info("No tasks found.")
else:
    for task in tasks:
        color = PRIORITY_COLORS[task.priority]
        title_class = "task-title done" if task.completed else "task-title"
        title_text = f"✓ {task.title}" if task.completed else task.title

        st.markdown(f"""
        <div class="task-card" style="border-left-color: {color};">
            <span class="{title_class}">{title_text}</span>
            <span class="badge" style="background:{color};">{task.priority}</span>
            <div class="task-desc">{task.description or ""}</div>
            {"<div class='task-date'>📅 Due: " + task.due_date + "</div>" if task.due_date else ""}
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns([1, 1, 1, 8])
        if not task.completed:
            with cols[0]:
                if st.button("✅ Complete", key=f"complete_{task.id}"):
                    manager.complete(task.id)
                    st.rerun()
        with cols[1]:
            if st.button("✏️ Edit", key=f"edit_{task.id}"):
                st.session_state.edit_task = task
                st.session_state.show_form = False
                st.rerun()
        with cols[2]:
            if st.button("🗑️ Delete", key=f"delete_{task.id}"):
                manager.delete(task.id)
                st.rerun()
