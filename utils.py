# import pandas as pd

# def load_data(file):
#     ext = file.name.split('.')[-1]
#     if ext == 'csv':
#         return pd.read_csv(file)
#     elif ext in ['xls', 'xlsx']:
#         return pd.read_excel(file)
#     else:
#         raise ValueError("Unsupported file format")

# def get_summary(df):
#     return df.groupby(['Name', 'Subject'])['Marks'].mean().reset_index()

# def get_top_n(df, n=5):
#     avg_scores = df.groupby('Name')['Marks'].mean().sort_values(ascending=False)
#     return avg_scores.head(n).reset_index(name='Average Marks')


import pandas as pd

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def load_data(file):
    ext = file.name.split('.')[-1]
    if ext == 'csv':
        return pd.read_csv(file)
    elif ext in ['xls', 'xlsx']:
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")

def get_class_summary(df):
    return df.groupby(['Class', 'Subject'])['Marks'].mean().reset_index()

def get_student_summary(df):
    return df.groupby(['Name', 'Subject'])['Marks'].mean().reset_index()

def get_exam_trends(df):
    return df.groupby(['Exam', 'Subject'])['Marks'].mean().reset_index()

def get_top_bottom_students(df, top_n=5):
    avg_scores = df.groupby('Name')['Marks'].mean()
    toppers = avg_scores.sort_values(ascending=False).head(top_n).reset_index(name='Average Marks')
    underperformers = avg_scores.sort_values(ascending=True).head(top_n).reset_index(name='Average Marks')
    return toppers, underperformers

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_students(df, n_clusters=3):
    student_scores = df.groupby('Name')['Marks'].mean().reset_index()
    scaler = StandardScaler()
    scores_scaled = scaler.fit_transform(student_scores[['Marks']])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    student_scores['Cluster'] = kmeans.fit_predict(scores_scaled)
    return student_scores

def detect_declining(df):
    decline = []
    grouped = df.groupby('Name')
    for name, data in grouped:
        trend = data.sort_values('Exam')['Marks'].diff().sum()
        if trend < 0:
            decline.append({'Name': name, 'Total Decline': trend})
    return pd.DataFrame(decline)


def export_pdf(df, filename="student_report.pdf", title="Student Performance Report"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 12))

    # Table data
    data = [df.columns.tolist()] + df.values.tolist()

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    elements.append(table)
    doc.build(elements)

def generate_academic_suggestions(df, targets=[60, 75, 90]):
    suggestions = []
    for name, group in df.groupby('Name'):
        avg = group['Marks'].mean()
        subjects = group.groupby('Subject')['Marks'].mean()
        weakest_subject = subjects.idxmin()
        weakest_score = subjects.min()
        n_exams = len(group)
        current_total = avg * n_exams
        for target in targets:
            required = (target * (n_exams + 1)) - current_total
            required = max(0, min(100, round(required, 1)))
            if required <= 100:
                break
        suggestion = (
            f"Current average: {avg:.1f}%. "
            f"To reach {target}% average, needs at least {required} in the next exam. "
            f"Focus on {weakest_subject} (avg {weakest_score:.1f}%)."
        )
        suggestions.append({
            'Name': name,
            'Class': group['Class'].iloc[0],
            'Suggestion': suggestion
        })
    return pd.DataFrame(suggestions)