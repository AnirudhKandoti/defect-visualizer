import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .analysis import (
    load_data_from_file,
    cluster_descriptions,
    compute_module_risk,
    top_cluster_examples,
    bar_module_risk_plot,
    cluster_pie_plot,
    timeline_heatmap,
)

def upload_view(request):
    if request.method == 'POST' and request.FILES.get('defect_file'):
        f = request.FILES['defect_file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(f.name, f)
        file_path = fs.path(filename)
        request.session['uploaded_file'] = file_path
        return redirect('qa_tool:dashboard')
    return render(request, 'qa_tool/upload.html')

def dashboard_view(request):
    file_path = request.session.get('uploaded_file')
    if not file_path or not os.path.exists(file_path):
        return redirect('qa_tool:upload')
    df = load_data_from_file(file_path)
    # tune eps/min_samples as sensible defaults
    df, _tf = cluster_descriptions(df, eps=0.35, min_samples=3)
    module_group = compute_module_risk(df)
    top_clusters = top_cluster_examples(df, top_n=8)
    bar_div = bar_module_risk_plot(module_group)
    pie_div = cluster_pie_plot(df)
    heat_div = timeline_heatmap(df)
    context = {
        'bar_div': bar_div,
        'pie_div': pie_div,
        'heat_div': heat_div,
        'top_clusters': top_clusters,
        'module_table': module_group.to_dict(orient='records')[:50],
    }
    return render(request, 'qa_tool/dashboard.html', context)
