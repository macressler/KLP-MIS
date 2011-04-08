from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class ClassView(Collection):  
    """ To view selcted class
    To view selected class boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/view/
    To create new class schools/(?P<referKey>\d+)/class/creator/
    To edit selected class boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/edit/"""   
    def get_entry(self, boundary_id, school_id, class_id):
        classObj = Class.objects.get(sid=school_id, id=class_id)
        return ChoiceEntry(self, classObj)

template_class_view =  ClassView(
    queryset = Class.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'classObj',
    ),
  receiver = XMLReceiver(),
)

template_class_edit =  ClassView(
    queryset = Class.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'classObj',
    ),
  receiver = XMLReceiver(),
)

class ClassUpdate(Resource):  
    """ To update class data boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/update/"""  
    def create(self, request, boundary_id, school_id, class_id):
        classObj = Class.objects.get(id=class_id)
        form =Class_Form(request.POST, request.FILES,instance=classObj)
        form.save()
        respTemplate= render_to_response('viewtemplates/class_detail.html', {'classObj':classObj})
        return HttpResponse(respTemplate)


urlpatterns = patterns('',            
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/view/?$', template_class_view),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/edit/?$', template_class_edit), 
   url(r'^schools/(?P<referKey>\d+)/class/creator/?$', template_class_view.responder.create_form, {'form_class':'class'}),
   url(r'^boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/classes/(?P<class_id>\d+)/update/?$', ClassUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),
)