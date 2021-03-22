import argparse
import json
import os
import sys
from xapitolatex import *

def main(args):
    root_tag = 'caseStudy'
    data = convert_XML_to_JSON(args.file)

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
        document += '\subsubsection{{{}}}'.format(data[root_tag]['fileResource']['title'])
        document += parse_fileresource(data[root_tag]['fileResource'])

    if 'host' in data[root_tag]:
        document += '\\subsection{Hosts}\n'
        for host in data[root_tag]['host']:
            document += parse_host(host['configItem'])

    if 'question' in data[root_tag]:
        document += '\\section{Questions}\n'
        for question in data[root_tag]['question']:
            document += parse_question(question)

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