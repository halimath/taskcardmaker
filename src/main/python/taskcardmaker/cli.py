import optparse
import sys

import taskcardmaker
from taskcardmaker.renderer import Renderer
from taskcardmaker.parser import TaskCardParser

def parse_options ():
    parser = optparse.OptionParser(version="%prog " + taskcardmaker.version)
    parser.add_option("-o", "--output-file",
                         dest="output_file",
                         help="Output file to write generated pdf to",
                         metavar="<output file>",
                         default=None)
    options, arguments = parser.parse_args()
    if len(arguments) == 0:
        sys.stderr.write("%s: Missing file name\n" % sys.argv[0])
        sys.exit(1)
    if options.output_file is None:
        options.output_file = arguments[0] + ".pdf"
        
    return options, arguments[0]

def main ():
    options, input_file = parse_options()
    
    sys.stdout.write("Reading file %s..." % input_file)
    with open(input_file, "r") as input_file:
        lines = input_file.readlines()
    
    sys.stdout.write(" done\nParsing file...")

    parser = TaskCardParser()
    parser.parse(*lines)
    
    project = parser.project
    
    sys.stdout.write(" done. Found %d stories.\nRendering stories to %s..." % (len(project.stories), options.output_file))
    renderer = Renderer(options.output_file, "Tasks for " + project.name)
    for story in project.stories:
        renderer.render_story(story)
        
    renderer.close()
    sys.stdout.write(" finished.\n")