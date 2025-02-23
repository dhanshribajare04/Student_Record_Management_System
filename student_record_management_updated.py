import pandas as pd
import gradio as gr
import os

FILE_NAME = "students.xlsx"
REQUIRED_COLUMNS = ["Student ID", "Name", "Age", "Course"]

def load_students():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
        df.to_excel(FILE_NAME, index=False)
    else:
        df = pd.read_excel(FILE_NAME)
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                return None
    return df

def save_students(df):
    df.to_excel(FILE_NAME, index=False)

def add_student(student_id, name, age, course):
    df = load_students()
    if df is None:
        return "Error loading data!"
    
    if student_id in df["Student ID"].astype(str).values:
        return "Student ID already exists!"
    
    new_data = pd.DataFrame([[student_id, name, age, course]], columns=REQUIRED_COLUMNS)
    df = pd.concat([df, new_data], ignore_index=True)
    save_students(df)
    return "Student added successfully!"

def view_students():
    df = load_students()
    if df is None or df.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)  # Return an empty dataframe if no data is found
    return df

def update_student(student_id, name, age, course):
    df = load_students()
    if df is None:
        return "Error loading data!"
    
    if student_id not in df["Student ID"].astype(str).values:
        return "Student ID not found!"
    
    df.loc[df["Student ID"].astype(str) == student_id, ["Name", "Age", "Course"]] = [name, age, course]
    save_students(df)
    return "Student updated successfully!"

def delete_student(student_id):
    df = load_students()
    if df is None:
        return "Error loading data!"
    
    df = df[df["Student ID"].astype(str) != student_id]
    save_students(df)
    return "Student deleted successfully!"

with gr.Blocks() as app:
    gr.Markdown("# 🎓 Student Management System")
    with gr.Tab("Add Student"):
        student_id = gr.Textbox(label="Student ID")
        name = gr.Textbox(label="Name")
        age = gr.Number(label="Age")
        course = gr.Textbox(label="Course")
        add_btn = gr.Button("Add Student")
        output_add = gr.Text()
        add_btn.click(add_student, inputs=[student_id, name, age, course], outputs=output_add)
    
    with gr.Tab("View Students"):
        view_btn = gr.Button("Load Students")
        output_view = gr.Dataframe()
        view_btn.click(view_students, outputs=output_view)
    
    with gr.Tab("Update Student"):
        update_id = gr.Textbox(label="Student ID")
        update_name = gr.Textbox(label="New Name")
        update_age = gr.Number(label="New Age")
        update_course = gr.Textbox(label="New Course")
        update_btn = gr.Button("Update Student")
        output_update = gr.Text()
        update_btn.click(update_student, inputs=[update_id, update_name, update_age, update_course], outputs=output_update)
    
    with gr.Tab("Delete Student"):
        delete_id = gr.Textbox(label="Student ID")
        delete_btn = gr.Button("Delete Student")
        output_delete = gr.Text()
        delete_btn.click(delete_student, inputs=[delete_id], outputs=output_delete)

app.launch()
