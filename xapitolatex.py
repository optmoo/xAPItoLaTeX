import json
import os
import sys
import xmltodict

def escape_paths(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = escape_paths(value)
        return obj
    elif isinstance(obj, list):
        return [escape_paths(v) for v in obj]
    elif isinstance(obj, basestring):
        return obj.replace('\\','\\\\')
    else:
        return obj

def convert_XML_to_JSON(xml_path, export=False):
    with open(xml_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        data_dict = escape_paths(data_dict)

        if export:
            json_path = os.path.splitext(xml_path)[0] + '.json'
            with open(json_path, "w") as json_file:
                json_file.write(data_dict)

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
        if type(host['fileResource']) == type([]):
            for resource in host['fileResource']:
                text += '\\textbf{{File Resource}} {}\n\n'.format(resource['title'])
                text += parse_runscript(resource)
        else:
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

    if 'learningObjectives' in question and question['learningObjectives']:
        output += parse_objectives(question['learningObjectives'])

    if 'autoTests' in question and question['autoTests']:
        output += '\n\\textbf{{Autotest:}}\n'
        if type(question['autoTests']['autoTest']) == type([]):
            for test in question['autoTests']['autoTest']:
                output += parse_autotest(test)
        else:
            output += parse_autotest(question['autoTests']['autoTest'])

    if 'note' in question and question['note']:
        if '\\' in question['note']:
            output += '\n\\textbf{{Note}} {}\n'.format(question['note'])
        else:
            output += '\n\\textbf{{Note}} {}\n'.format(question['note'])

    output += '\n\\textbf{{Note}} {}\n'.format(question['note'])

    if 'answers' in question and question['answers']:
        output += '\\begin{enumerate}[label=\\Alph*]\n'
        for answer in question['answers']['answer']:
            output += '\\item{' + parse_answer(answer) + '}\n'
        output += '\\end{enumerate}\n'

    if 'hints' in question and question['hints']:
        output += '\n\\textbf{Hints:}\n'
        output += '\\begin{itemize}\n'
        for hint in question['hints'].items():
            if hint[1]:
                if type(hint[1]) == type([]):
                    for h in hint[1]:
                        output += '\\item {}\n'.format(h)
                else:
                    output += '\\item {}\n'.format(hint[1])
        output += '\\end{itemize}\n'

    if 'feedback' in question and question['feedback']:
        output += '\n\\textbf{{Feedback:}} {}\n'.format(question['feedback'])

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
