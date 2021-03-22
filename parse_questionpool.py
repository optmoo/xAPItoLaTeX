import argparse
import json
import os
import sys
import xmltodict
from xapitolatex import *

def main(args):
    root_tag = 'questionPool'
    data = convert_XML_to_JSON(args.file)

    document = latex_header.format(
        data[root_tag]['name'],
        data[root_tag]['hid']
    )

    if type(data[root_tag]['questionPoolSet']) == type([]):
        for questionPoolSet in data[root_tag]['questionPoolSet']:
            document += parse_poolset(questionPoolSet)
            if type(questionPoolSet['question']) == type([]):
                for question in questionPoolSet['question']:
                    document += parse_question(question)
            else:
                    document += parse_question(questionPoolSet['question'])
    else:
        document += parse_poolset(data[root_tag]['questionPoolSet'])
        if type(data[root_tag]['questionPoolSet']['question']) == type([]):
            for question in data[root_tag]['questionPoolSet']['question']:
                document += parse_question(question)
        else:
                document += parse_question(data[root_tag]['questionPoolSet']['question'])

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