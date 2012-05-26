from django.conf.urls.defaults import patterns

from taskcardmaker.webapp import views

urlpatterns = patterns('',
    ('editor$', views.do_editor),
    ('info$', views.do_info),
    ('pdf$',  views.do_download_pdf),
    ('parse$',  views.do_parse),
    ('$',  views.do_index),
)
