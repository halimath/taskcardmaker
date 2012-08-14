import json
import django
import os
import StringIO
import sys

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

from google.appengine.api import users
from google.appengine.api import mail

import taskcardmaker

def do_index (request):
    page = "index"
    debug = request.GET.get("debug", "") == "true"
    return render_template('index.html', **locals())

def do_editor (request):
    page = "editor"
    debug = request.GET.get("debug", "") == "true" 
    return render_template('editor.html', **locals())

def do_info (request):
    version_id = os.environ['CURRENT_VERSION_ID']
    return render_template('info.html', **locals())

def do_parse (request):
    response = {
      'status': 200,
      'message': 'ok'
    }

    try:
        project, settings = parse_lines(request.raw_post_data.split("\n"))
        response['project'] = project.as_map()
        response['settings'] = settings.as_map()
    except Exception as e:
        response['status'] = 400
        response['message'] = str(e)
        
    return HttpResponse(json.dumps(response),
                        content_type="application/json")
    
def do_download_pdf (request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=taskcards.pdf'

    project, settings = parse_lines(request.POST['source'].split("\n"))

    render_tasks(project, settings, response)
    
    return response

def do_send_as_email (request):
    response = {
      'status': 200,
      'message': 'ok'
    }

    try:
        output = StringIO.StringIO()
        project, settings = parse_lines(request.raw_post_data.split("\n"))
        render_tasks(project, settings, output)
        
        mail.send_mail(sender="Taskcardmaker <noreply@taskcardmaker.appspotmail.com>",
              to=users.get_current_user().email(),
              subject="Your Task Cards",
              attachments=[("taskcards.pdf", output.getvalue())],
              body="""
Dear %s:

Please find attached your taskcards ready for printing.

Your Taskcardmaker Team
""" % (users.get_current_user().nickname()))
        output.close()

    except Exception as e:
        response['status'] = 400
        response['message'] = str(e)
        
    return HttpResponse(json.dumps(response),
                        content_type="application/json")    

def render_tasks (project, settings, output_stream):
    renderer = taskcardmaker.Renderer(output_stream, 
                                      'Tasks', 
                                      'Taskcardmaker %s' % taskcardmaker.version)
    
    renderer.apply_settings(settings)
    
    for story in project.stories:
        renderer.render_story(story)
        
    renderer.close()        

def parse_lines (lines):
    parser = taskcardmaker.TaskCardParser()
    parser.parse(*lines)
    
    return parser.project, parser.settings

def render_template (template, **values):
    values["version"] = render_version(taskcardmaker.version_info)
    values["django_version"] = render_version(django.VERSION)
    values["python_version"] = render_version(sys.version_info)
    values["login_url"] = users.create_login_url("/editor")
    values["logout_url"] = users.create_logout_url("/")
    values["current_user"] = users.get_current_user()
    
    return render_to_response(template, values)

def render_version (version):
    return "%s.%s.%s%s" % (version[0], version[1], version[2], "-" + version[3] if version[3] else "")
