"""
@file masroofy/views.py
@brief Project-level views (simple home view).

Contains a single `home` view that renders the project landing page.
"""

from django.shortcuts import render


def home(request):
    """
    @brief Render the project home page.

    @param request Django HTTP request
    @return Django HTTP response rendering `home.html`
    """
    return render(request, 'home.html')
