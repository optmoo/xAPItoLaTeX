import argparse
import json
import os
import sys
from xapitolatex import *

def main(args):
    root_tag = 'caseStudy'
    data = convert_XML_to_JSON(args.file)

    if not root_tag in data:
        print '[!] Not a {}'.format(root_tag)
        sys.exit(1)

    document = latex_header.format(
        data[root_tag]['name'],
        data[root_tag]['hid']
    )

    document += '\\section{Case Study}\n'
    document += data[root_tag]['richText'] + '\n'

    # TODO: parse learningObjectives
    # document += '\\subsection{Learning Objectives}\n'

    if 'fileResource' in data[root_tag]:
        document += '\\subsection{File Resources}\n'
        if type(data[root_tag]['fileResource']) == type([]):
            for resource in data[root_tag]['fileResource']:
                document += '\subsubsection{{{}}}'.format(resource['title'])
                document += parse_fileresource(resource)
        else:
            document += '\subsubsection{{{}}}'.format(data[root_tag]['fileResource']['title'])
            document += parse_fileresource(data[root_tag]['fileResource'])

    if 'host' in data[root_tag]:
        document += '\\subsection{Hosts}\n'
        if type(data[root_tag]['host']) == type([]):
            for host in data[root_tag]['host']:
                document += parse_host(host['configItem'])
        else:
            document += parse_host(data[root_tag]['host']['configItem'])

    if 'question' in data[root_tag]:
        document += '\\section{Questions}\n'
        if type(data[root_tag]['question']) == type([]):
            for question in data[root_tag]['question']:
                document += parse_question(question)
        else:
            document += parse_question(data[root_tag]['question'])

    document += latex_footer

    document = latex_escape(document)

    if args.output:
        with open(args.output, 'w') as out_file:
            out_file.write(document)
    else:
        print document

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='xAPI XML document to parse', required=True)
    parser.add_argument('-o', '--output', help='LaTex output path')
    args = parser.parse_args()
    main(args)
