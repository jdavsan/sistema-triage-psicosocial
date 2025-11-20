from django.shortcuts import render

def error_404(request, exception):
    """Vista personalizada para error 404"""
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    """Vista personalizada para error 500"""
    return render(request, 'errors/500.html', status=500)