import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from collections import Counter
from plotly.offline import plot
import plotly.graph_objs as go

def load_data_from_file(fpath_or_buffer):
    df = pd.read_csv(fpath_or_buffer)
    df = df.rename(columns=lambda c: c.strip())
    req = ["id","module","severity","error_type","description","occurrence_date"]
    missing = [c for c in req if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df['occurrence_date'] = pd.to_datetime(df['occurrence_date'], errors='coerce').fillna(pd.Timestamp.now())
    df['description'] = df['description'].astype(str)
    return df

def cluster_descriptions(df, text_col='description', eps=0.5, min_samples=3):
    tf = TfidfVectorizer(stop_words='english', max_features=2000)
    X = tf.fit_transform(df[text_col])
    db = DBSCAN(metric='cosine', eps=eps, min_samples=min_samples).fit(X)
    labels = db.labels_
    df['cluster'] = labels
    return df, tf

def compute_module_risk(df):
    sev_w = {"Low": 1, "Medium": 2, "High": 4, "Critical": 8}
    df['sev_weight'] = df['severity'].map(sev_w).fillna(1)
    module_group = df.groupby('module').agg(
        defect_count=('id','count'),
        avg_severity_weight=('sev_weight','mean'),
        unique_clusters=('cluster', lambda x: len(set(x)))
    ).reset_index()
    module_group['risk_raw'] = module_group['defect_count'] * module_group['avg_severity_weight'] * (1 + module_group['unique_clusters'])
    rmin, rmax = module_group['risk_raw'].min(), module_group['risk_raw'].max()
    module_group['risk_score'] = (module_group['risk_raw'] - rmin) / (rmax - rmin + 1e-9)
    module_group = module_group.sort_values('risk_score', ascending=False)
    return module_group

def top_cluster_examples(df, top_n=5):
    clusters = [c for c in sorted(df['cluster'].unique()) if c != -1]
    rep = {}
    for c in clusters:
        sub = df[df['cluster'] == c]
        counts = Counter(sub['description'])
        rep[c] = counts.most_common(1)[0][0]
    sizes = df[df['cluster']!=-1].groupby('cluster').size().sort_values(ascending=False)
    result = []
    for cid in sizes.index[:top_n]:
        result.append((int(cid), rep.get(int(cid), ""), int(sizes.loc[cid])))
    return result

def bar_module_risk_plot(module_group):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=module_group['module'],
        y=module_group['risk_score'],
        text=module_group['defect_count'],
        hovertemplate="Module: %{x}<br>Risk score: %{y:.2f}<br>Defects: %{text}<extra></extra>"
    ))
    fig.update_layout(title="Module Risk Scores", xaxis_title="Module", yaxis_title="Risk score")
    return plot(fig, output_type='div', include_plotlyjs=False)

def cluster_pie_plot(df):
    counts = df['cluster'].value_counts().sort_index()
    labels = [str(i) for i in counts.index]
    values = counts.values
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title="Defect Cluster Distribution ( -1 = noise )")
    return plot(fig, output_type='div', include_plotlyjs=False)

def timeline_heatmap(df):
    df['month'] = df['occurrence_date'].dt.to_period('M')
    pivot = df.groupby(['module','month']).size().unstack(fill_value=0)
    if pivot.empty:
        fig = go.Figure()
        fig.update_layout(title="No timeline data")
        return plot(fig, output_type='div', include_plotlyjs=False)
    modules = pivot.index.tolist()
    months = [str(m) for m in pivot.columns]
    fig = go.Figure(data=go.Heatmap(z=pivot.values, x=months, y=modules))
    fig.update_layout(title="Defects per Module by Month", xaxis_title="Month", yaxis_title="Module")
    return plot(fig, output_type='div', include_plotlyjs=False)
