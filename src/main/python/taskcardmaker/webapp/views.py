import json
import django
import sys

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse

from google.appengine.api import users

import taskcardmaker

def do_index (request):
    if users.get_current_user():
        return redirect("/editor")
    debug = request.GET.get("debug", "") == "true"
    return render_template('index.html', **locals())

def do_editor (request):
    debug = request.GET.get("debug", "") == "true" 
    return render_template('editor.html', **locals())

def do_info (request):
    return render_template('info.html', **locals())

def do_parse (request):
    parser = taskcardmaker.TaskCardParser()
    lines = request.raw_post_data.split("\n")
    response = {
      'status': 200,
      'message': 'ok'
    }

    try:
        parser.parse(*lines)
        response['project'] = parser.project.as_map() 
    except Exception as e:
        response['status'] = 400
        response['message'] = str(e)
        
    return HttpResponse(json.dumps(response),
                        content_type="application/json")
    
def do_download_pdf (request):
    source = request.POST['source']
    
    parser = taskcardmaker.TaskCardParser()
    parser.parse(*(source.split("\n")))
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=taskcards.pdf'
    
    renderer = taskcardmaker.Renderer(response, 
                                      'Tasks', 
                                      'Taskcardmaker %s' % taskcardmaker.version)
    
    for story in parser.project.stories:
        renderer.render_story(story)
        
    renderer.close()
    return response    

def render_template (template, **values):
    values["version"] = render_version(taskcardmaker.version_info)
    values["django_version"] = render_version(django.VERSION)
    values["python_version"] = render_version(sys.version_info)
    values["login_url"] = users.create_login_url("/")
    values["logout_url"] = users.create_logout_url("/")
    values["current_user"] = users.get_current_user()
    
    return render_to_response(template, values)

def render_version (version):
    return "%s.%s.%s-%s" % (version[0], version[1], version[2], version[3])
