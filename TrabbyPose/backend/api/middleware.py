"""
Cache control middleware to prevent browser caching of authenticated pages.
This ensures logged-out users cannot access cached dashboard content via back button.
"""
from django.utils.decorators import decorator_from_middleware
from django.utils.cache import add_never_cache_headers
from django.http import HttpResponse


class NoCacheMiddleware:
    """
    Middleware to add no-cache headers to all responses.
    Prevents browsers from caching sensitive authenticated pages.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add cache control headers
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response
