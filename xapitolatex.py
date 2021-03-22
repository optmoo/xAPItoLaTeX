import json
import os
import sys
import xmltodict

def convert_XML_to_JSON(xml_path, export=False):
    with open(xml_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

        if export:
            json_path = os.path.splitext(xml_path)[0] + '.json'
            with open("data.json", "w") as json_file:
                json_file.write(json_data)

        return data_dict

def parse_fileresource(resource):
    text = ''
    if 'description' in resource and resource['description']:
        text += '\\textbf{{Description:}} {}\n'.format(resource['description'])
    text += '\\begin{itemize}\n'
    if 'source' in resource:
        text += '\\item \\textbf{{Source:}} {}\n'.format(resource['source'])
    if 'destination' in resource:
        text += '\\item \\textbf{{Destination:}} {}\n'.format(resource['destination'])
    text += '\\end{itemize}\n'
    return text

def parse_runscript(runscript):
    text = ''
    if 'description' in runscript and runscript['description']:
        text += '\\textbf{{Description:}} {}\n'.format(runscript['description'])
    text += '\\begin{itemize}\n'
    if 'source' in runscript:
        text += '\\item \\textbf{{Source:}} {}\n'.format(runscript['source'])
    if 'destination' in runscript:
        text += '\\item \\textbf{{Destination:}} {}\n'.format(runscript['destination'])
    text += '\\end{itemize}\n'
    return text

def parse_host(host):
    text = '\subsubsection{{{}}}'.format(host['hid'])

    text += '\\begin{itemize}\n'
    if 'displayButton' in host:
        text += '\\item \\textbf{{Display:}} {}\n'.format(host['displayButton'])
    if 'restartButton' in host:
        text += '\\item \\textbf{{Restart:}} {}\n'.format(host['restartButton'])
    text += '\\end{itemize}\n'

    if 'runScript' in host:
        text += '\\textbf{{Run Script}} {}\n\n'.format(host['runScript']['title'])
        text += parse_runscript(host['runScript'])
    if 'fileResource' in host:
        text += '\\textbf{{File Resource}} {}\n\n'.format(host['fileResource']['title'])
        text += parse_runscript(host['fileResource'])
    return text

def parse_objectives(objectives):
    text = '\\textbf{Learning Objectives:}\n\n'
    text += '\\begin{itemize}\n'
    for hid, objective in objectives.items():
        text += '\\item {}\n'.format(objective)
    text += '\\end{itemize}\n'
    return text

def parse_poolset(poolset):
    output  = '\\section{Question Pool Set}\n'
    output += '\\begin{itemize}\n'
    output += '\\item Weight: {}\n'.format(poolset['@weight'])
    output += '\\item Pick: {}\n'.format(poolset['@pick'])
    output += '\\end{itemize}\n'
    return output

def parse_question(question):
    output  = '\\subsection{{{}}}\n'.format(question['name'])

    output += '\\begin{itemize}\n'
    output += '\n\\item \\textbf{{Type:}} {}\n'.format(question['qtype'])
    if '@weight' in question:
        output += '\n\\item \\textbf{{Weight:}} {}\n'.format(question['@weight'])
    if '@random' in question:
        output += '\\item \\textbf{{Random:}} {}\n'.format(question['@random'])
    output += '\\end{itemize}\n'

    if question['learningObjectives']:
        output += parse_objectives(question['learningObjectives'])

    if 'autoTests' in question and question['autoTests']:
        output += '\n\\textbf{{Autotest:}}\n'
        output += parse_autotest(question['autoTests']['autoTest'])

    if question['note']:
        output += '\n\\textbf{{Note}} {}\n'.format(question['note'])

    output += '\n\\textbf{{Question:}} {}\n\n'.format(question['richText'].replace('\\','\\\\'))

    if question['answers']:
        output += '\\begin{enumerate}[label=\\Alph*]\n'
        for answer in question['answers']['answer']:
            output += '\\item{' + parse_answer(answer) + '}\n'
        output += '\\end{enumerate}\n'

    if question['hints']:
        output += '\n\\textbf{Hints:}\n'
        output += '\\begin{itemize}\n'
        for hint in question['hints'].items():
            output += '\\item {}\n'.format(hint[1].replace('\\','\\\\'))
        output += '\\end{itemize}\n'

    if question['feedback']:
        output += '\n\\textbf{{Feedback:}} {}\n'.format(question['feedback'].replace('\\','\\\\'))

    return output

def parse_autotest(autotest):
    text = '\\begin{itemize}\n'
    text += '\\item \\textbf{{Id:}} {}\n'.format(autotest['id'])
    text += '\\item \\textbf{{Host:}} {}\n'.format(autotest['host_hid'])
    text += '\\item \\textbf{{Type:}} {}\n'.format(autotest['scriptType'])
    text += '\\item \\textbf{{Command:}} \\begin{{verbatim}}{}\\end{{verbatim}}\n'.format(autotest['command'])
    text += '\\item \\textbf{{Output:}} \\begin{{verbatim}}{}\\end{{verbatim}}\n'.format(autotest['output'])
    text += '\\end{itemize}\n'
    return text

def parse_answer(answer):
    if answer['correct'] == u'true':
        output = '\\textbf{{ {} {} }}'.format(
            # answer['correct'],
            answer['points'],
            answer['value'].replace('\\','\\\\'))
    else:
        output = '{} {}'.format(
            # answer['correct'],
            answer['points'],
            answer['value'].replace('\\','\\\\'))
    return output

def latex_escape(text):
    text = text.replace('<code>','\\texttt{').replace('</code>','}')
    text = text.replace('<b>','\\textbf{').replace('</b>','}')
    text = text.replace('<i>','\\textit{').replace('</i>','}')
    text = text.replace('<p>','\n\n').replace('</p>','\n')
    text = text.replace('&quot;','"').replace('&#39;',"'")
    text = text.replace('&nbsp;','~')
    text = text.replace('&lt;','\\textless ')
    text = text.replace('&gt;','\\textgreater ')
    text = text.replace('^', '\\textasciicircum ')
    text = text.replace('~', '\\textasciitilde ')
    text = text.replace('<', '\\textless ')
    text = text.replace('>', '\\textgreater ')
    for c in '&%$#_': # '&%$#_{}~^\
        text = text.replace(c,'\\'+c)
    text = text.replace('&nbsp;', '~')
    return text

latex_header =  '''\
\\title{{ {} }}
\\author{{ {} }}
\\date{{}}
\\documentclass[10pt]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{enumitem}}
\\begin{{document}}
\\maketitle
'''
latex_footer = '\\end{document}'
