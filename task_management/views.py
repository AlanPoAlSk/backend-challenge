from django.http import HttpResponse

def index(request):
    message = """
    Welcome to the Task Management API.<br>
    <ul>
        <li>Visit <a href="/admin/">/admin/</a> for the admin interface.</li>
    </ul>
    """
    return HttpResponse(message)