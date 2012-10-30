from pythonbuilder.core import use_plugin, init, Author

use_plugin("python.core")

use_plugin("copy_resources")

use_plugin("source_distribution")

use_plugin("python.unittest")
use_plugin("python.coverage")
#use_plugin("python.pychecker")
use_plugin("python.distutils")
use_plugin("python.pydev")
use_plugin("python.django")

default_task = ["analyze", "publish"]

version = "0.5.8"
summary = "A task card generator"
authors = [Author("Alexander Metzner", "alexander.metzner@gmail.com")]

@init
def set_properties (project):
    #project.depends_on("reportlab")
    
    project.set_property("dir_dist_scripts", 'scripts')

    project.set_property("copy_resources_target", "$dir_dist")
    project.get_property("copy_resources_glob").append("setup.cfg")
    project.get_property("copy_resources_glob").append("sample.tcm")
    
    project.set_property("django_module", "taskcardmaker.webapp")
    project.set_property("coverage_break_build", False)
    project.set_property("pychecker_break_build", False)
    
    project.get_property("distutils_commands").append("bdist_egg")
    
    project.set_property("distutils_classifiers", [    
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python'])
