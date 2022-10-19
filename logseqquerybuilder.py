# %%

from queryDB import *
import copy
import time


def initialiseQuery():
    global query_template
    query = copy.deepcopy(query_template)
    return query


# query structure
query_template = {
    "start": [],
    "open": [],
    "title": [],
    "query": [],  # unused segment
    "in": [],
    "where": [],
    "filters": [],
    "closefind": [],
    "inputs": [],
    "view": [],
    "options": [],
    "closequery": [],
    "end": []
}


def getQueryLine(querylinekey, querysegment):
    global showcommandcomments
    try:
        if showcommandcomments == True:
            query[querysegment].append('\n'+getQueryLineComment(querylinekey))
        return querylineDict[querylinekey]['datalog']
    except:
        return querylinekey+" not found in queryline Dictionary"


def getQueryLineComment(querylinekey):
    comment = querylineDict[querylinekey]['comment']
    if mode == 'pyScript':
        separator = "<p>"
        comment = comment.replace('\n', '<p>')
    else:
        separator = "\n"
    try:
        return separator+';; ---- '+comment
    except:
        return querylinekey+" not found in queryline Dictionary"


def getCommandQueryLineKeys(command):
    if command == None:
        return None
    # check command in Dictionary
    try:
        commandlist = commandsDict[command]['querylines']
    except:
        return None

    return commandlist


def buildCommonQueryLines():
    global showcommandcomments
    for key in defaultQueryLines:
        for querylinekey in defaultQueryLines[key]:
            query[key].append(getQueryLine(querylinekey, key))

    return


def buildPostFindQueryLines():
    postfindlines = []
    pass
    return postfindlines

    global query


def processCommand(command, commandsDict):
    # ------------------------------------------------------------------
    # -- Construct the common (minimum) query lines for all queries ----
    # ------------------------------------------------------------------

    # get the basic advanced query lines for this command

    querylinekeys = getCommandQueryLineKeys(command)

    # check for a bad command
    if querylinekeys == None:
        return [command+' is not a valid command']

    # ------------------------------------------------------------------
    # --    Construct the 'where:' section of the advanced query    ----
    # --    which is in the 'filters' segment of the advanced query ----
    # --    group filter lines so that positive arguments are in    ----
    # --    the first query lines and surrounded by an OR clause    ----
    # --    and the negative (not)query lines are in the 2nd group  ----
    # --    which are conecutive and there have an implied AND      ----
    # ------------------------------------------------------------------

    # command pre-processing
    if command in ['journalonly']:
        query['filters'].append(getQueryLine('page_is_journal', 'filters'))
    if command in ['tasks']:
        query['filters'].append(getQueryLine('marker', 'filters'))
    if command in ['scheduled']:
        query['filters'].append(getQueryLine('scheduled', 'filters'))
    if command in ['deadline']:
        query['filters'].append(getQueryLine('deadline', 'filters'))
    if command in ['scheduledbetween']:
        query['filters'].append(getQueryLine('scheduled', 'filters'))
        query['filters'].append(getQueryLine('scheduledfrom', 'filters'))
        query['filters'].append(getQueryLine('scheduledto', 'filters'))
        query['in'].append(getQueryLine('daterange', 'in'))
    if command in ['deadlinebetween']:
        query['filters'].append(getQueryLine('deadline', 'filters'))
        query['filters'].append(getQueryLine('deadlinefrom', 'filters'))
        query['filters'].append(getQueryLine('deadlineto', 'filters'))
        query['in'].append(getQueryLine('daterange', 'in'))
    if command in ['journalsbetween']:
        query['filters'].append(getQueryLine('page_is_journal', 'filters'))
        query['filters'].append(getQueryLine('journal_date', 'filters'))
        query['filters'].append(getQueryLine('journalfrom', 'filters'))
        query['filters'].append(getQueryLine('journalto', 'filters'))
        query['in'].append(getQueryLine('daterange', 'in'))
    if command in ['collapse']:
        query['options'].append(getQueryLine('collapse_true', 'options'))
    if command in ['expand']:
        query['options'].append(getQueryLine('collapse_false', 'options'))
    if command in ['showbreadcrumb']:
        query['options'].append(getQueryLine(
            'breadcrumb_show_true', 'options'))
    if command in ['hidebreadcrumb']:
        query['options'].append(getQueryLine(
            'breadcrumb_show_false', 'options'))

    # sort the argument lines by positive and negative
    positivecommandlines = []
    negativecommandlines = []
    originalcommandlines = commandsDict[command]['commandlines'][1:]
    for commandline in originalcommandlines:
        if commandline.strip()[2:].startswith("not "):
            negativecommandlines.append(commandline)
        else:
            positivecommandlines.append(commandline)

    # get the command lines that are grouped positively
    processCommandLines('include', command, positivecommandlines)
    processCommandLines('exclude', command, negativecommandlines)

    return


def addQueryLines(command, prefix, querylinekey, arg, querysegment):
    global query
    global showcommandcomments
    global mode

    args = arg.split(",")

    # single argument commands
    if len(args) == 1:
        querylinekey = prefix+querylinekey
        updatedqueryline = getQueryLine(
            querylinekey, querysegment).replace("$$ARG1", arg)
        query[querysegment].append(updatedqueryline)

    # double argument commands
    elif len(args) == 2:
        arg1 = args[0].strip()
        arg2 = args[1].strip()
        querylinekey = prefix+querylinekey
        updatedqueryline = getQueryLine(
            querylinekey, querysegment).replace("$$ARG1", arg1)
        updatedqueryline = updatedqueryline.replace(
            '$$ARG2', arg2)
        query[querysegment].append(updatedqueryline)
    else:
        query[querysegment].append(
            command+' => Invalid line => '+arg)


def processCommandLines(action, command, commandlines):
    global query

    if commandlines == []:
        # return [newadvancedquerylines, postfindquerylines]
        pass
    firstline = ''
    lastline = ''

    # individual command processing
    if command in [
        'pages',
        'blocks',
        'blocktags',
        'pagetags',
        'tasks',
        'pageproperties',
        'blockproperties',
        'namespace',
    ]:

        # if multiple lines in command separate with an OR
        if len(commandlines) > 1:
            if action == 'include':
                firstline = '( or '
                lastline = ")"

    if firstline != '':
        query['filters'].append(firstline)

    for arg in commandlines:
        arg = arg.strip()[2:]  # ignore the leading dash

        if arg == '':
            continue

        # allow for all pages and all blocks arguments which do not require any additional query lines
        if arg == '*':
            continue

        # handle negative commands
        prefix = ''
        if arg.startswith("not "):
            prefix = 'not_'
            arg = arg[len(prefix):]

        # --- pages command
        if command == 'pages':

            # pages starting with
            if arg[0] != '*' and arg[len(arg)-1] == '*':
                addQueryLines(command, prefix, 'arg_pagename_startswith',
                              arg[:-1], 'filters')
                continue

            # pages ending with
            if arg[0] == '*' and arg[len(arg)-1] != '*':
                addQueryLines(command, prefix, 'arg_pagename_endswith',
                              arg[1:], 'filters')
                continue

            # pages containing text
            if arg[0] == '*' and arg[len(arg)-1] == '*':
                addQueryLines(command, prefix, 'arg_pagename_contains',
                              arg[1:-1], 'filters')
                continue

            # otherwise full pagename provided
            addQueryLines(command, prefix, 'pagename_is', arg, 'filters')

        # --- blocks command
        if command == 'blocks':
            if arg[0] == '*' and arg[len(arg)-1] != '*':
                addQueryLines(
                    command, prefix, 'arg_blockcontent_startswith', arg[1:], 'filters')
                continue

            if arg[0] != '*' and arg[len(arg)-1] == '*':
                addQueryLines(command, prefix,
                              'arg_blockcontent_endswith', arg[:-1], 'filters')
                continue

            if arg[0] == '*' and arg[len(arg)-1] == '*':
                addQueryLines(
                    command, prefix, 'arg_blockcontent_contains', arg[1:-1], 'filters')
                continue

        # --- pagetags command
        if command == "pagetags":
            addQueryLines(command, prefix, 'pagetags_are', arg, 'filters')

        # --- blocktags command
        if command == "blocktags":
            addQueryLines(command, prefix, 'blocktags_are', arg, 'filters')

        # --- pageproperties command
        #     arg is propertyname,propertyvalue
        if command == "pageproperties":
            addQueryLines(command, prefix,
                          'page_properties_are', arg, 'filters')

        # --- blockproperties command
        #     arg is propertyname,propertyvalue
        if command == "blockproperties":
            addQueryLines(command, prefix,
                          'block_properties_are', arg, 'filters')

        # --- tasks command
        if command == "tasks":
            addQueryLines(command, prefix,
                          'tasks_are', arg, 'filters')

        # --- namespace command
        if command == "namespace":
            addQueryLines(command, prefix,
                          'namespace', arg, 'filters')

        # --- scheduled command
        if command == "scheduled":
            addQueryLines(command, prefix,
                          'scheduled', arg, 'filters')

        # --- scheduledbetween command
        if command == "scheduledbetween":
            addQueryLines(command, prefix,
                          'scheduledbetween', arg, 'inputs')

        # --- deadline command
        if command == "deadline":
            addQueryLines(command, prefix,
                          'deadline', arg, 'filters')

        # --- deadlinebetween command
        if command == "deadlinebetween":
            addQueryLines(command, prefix,
                          'deadlinebetween', arg, 'inputs')

        # --- journalonly command
        if command == "journalonly":
            addQueryLines(command, prefix,
                          'page_is_journal', arg, 'filters')

        # --- journalbetween command
        if command == "journalsbetween":
            addQueryLines(command, prefix,
                          'journalbetween', arg, 'inputs')

        # --- daterange command
        if command == "daterange":
            updatedqueryline = getQueryLine(
                prefix+'daterange').replace("$$ARG1", arg)
            query['filters'].append(updatedqueryline)

    if lastline != '':
        query['filters'].append(lastline)

    return


def processCommandList(commandlists):
    global query
    query = initialiseQuery()
    lines = commandlists.split("\n")
    currentcommand = ''
    # Element('print_output').write(, str(len(lines)))
    commandsDict = {}
    for line in lines:
        if line.strip() == '' or line.startswith(";;"):
            continue
        if line.startswith('title:'):
            query["title"].append(getQueryLine('title', 'title').replace(
                '$$ARG1', line.split(":")[1].strip()))
            continue
        if line.startswith('- '):  # encountered a command
            fields = line.split(" ")
            commandname = fields[1]
            commandsDict[commandname] = {}
            if currentcommand == '' or line != currentcommand:
                currentcommand = commandname
                commandsDict[commandname]["commandlines"] = []
        try:
            commandsDict[commandname]["commandlines"].append(line)
        except:
            # TODO: Handle command name being invalid ..
            # can occur if bad command data in command input text
            pass

    query['start'] = [getQueryLine('start', 'start')]
    query['open'] = [getQueryLine('open', 'open')]

    buildCommonQueryLines()

    for command in commandsDict:
        processCommand(command, commandsDict)

    query['closefind'] = [getQueryLine('closefind', 'closefind')]
    # finalise query segments
    query['closequery'] = [getQueryLine('closequery', 'closequery')]
    query['end'] = [getQueryLine('end', 'end')]

    return


def getQuerySegment(key):
    try:
        querylines = query[key]
    except:
        return []


def constructQuery():
    global query
    advancedquery = ''
    for key in query:
        for queryline in query[key]:
            advancedquery += queryline+'\n'
    return advancedquery


def printGeneratedAdvancedQuery(advancedquery):
    global query
    global codeblock
    if codeblock:
        prefix = '```clojure<br>'
        suffix = '```'
    else:
        prefix = ''
        suffix = ''
    if mode == "pyScript":
        msg = prefix+advancedquery.replace('\n', '<BR>')+suffix
        Element('advanced_query').write(msg)
    else:
        print("----------------------------")
        print("Logseq Advanced Query")
        print("----------------------------")
        print(prefix+advancedquery+suffix)


# Test Utility Functions


def printInputCommandList(commands):
    global mode
    if commands == None:
        print('No commands found')
        return
    if mode == "pyScript":
        msg = ''
        lines = commands.split("\n")
        for commandline in lines:
            commandline = l = '&nbsp;' * \
                (len(commandline) - len(commandline.lstrip())) + commandline.lstrip()
            msg += commandline+"<BR>"

        # Element('command_list').write(msg)
    else:
        print("----------------------------")
        print("Input Command List")
        print("----------------------------")
        print(commands)


def printInputCommandLists():
    global mode
    print('Input Command Lists')
    for commandlist in commandlisttests:
        print(commandlist)


def testQueryBuild(commands):
    global mode
    printInputCommandList(commands)
    processCommandList(commands)
    advancedquery = constructQuery()
    printGeneratedAdvancedQuery(advancedquery)
    return advancedquery


def pyscriptClearCommands(event):
    if mode != "pyScript":
        return

    # hide copy to clipboard button
    Element('print_output').write('Clear Commands Button Pressed')
    commands_input = document.getElementById('commands_input')
    commands_input.value = ''


def pyscriptCommandComments(event):
    if mode != "pyScript":
        return
    global showcommandcomments
    if document.getElementById('command_comments_checkbox').checked == True:
        showcommandcomments = True
    else:
        showcommandcomments = False


def pyscriptCodeBlock(event):
    if mode != "pyScript":
        return
    global codeblock
    if document.getElementById('codeblock_checkbox').checked == True:
        codeblock = True
    else:
        codeblock = False


def pyscriptChooseExample(event):
    if mode != "pyScript":
        return
    # get selected Example and fill the commands Input Text Area
    # Element('print_output').write(, 'Choose Example Option Pressed')
    examples_options = Element('command_examples')
    if examples_options.value != "Choose Example..":
        advanced_query_text = document.getElementById('advanced_query')
        advanced_query_text.textContent = ''
        Element('print_output').write(
            "Example selected .. now press 'Generate Advanced Query' button")

        document.getElementById(
            'commands_input').value = examples_options.value
        print('value is ', examples_options.value)


def pyscriptAdvancedQueryText(event):
    if mode != "pyScript":
        return


def pyscriptQueryBuild(event):
    if mode != "pyScript":
        return

    # hide copy to clipboard button
    copy_button = document.getElementById('copy')
    copy_button.setAttribute("hidden", "hidden")

    Element('print_output').write('Processing Commands ..')
    # print('you clicked pyscriptQueryBuild')

    commands_input = Element('commands_input')
    if not commands_input:
        Element('print_output').write('Bug: Element is None')
        return

    processCommandList(commands_input.value)
    advancedquery = constructQuery()
    printGeneratedAdvancedQuery(advancedquery)

    # show copy to clipboard button
    hidden = copy_button.getAttribute("hidden")
    copy_button.removeAttribute("hidden")

    Element('print_output').write(
        "Advanced Query Generated!<br>- Tick 'Include Query Comments' if desired<br>- Tick 'Copy as code block' if desired<br>Click 'Copy Query to Clipboard")


def pyScriptInitialise():
    global mode
    if mode != "pyScript":
        return

    from js import document
    from pyodide.ffi import create_proxy

    # connect the generate advanced query button
    generate_query_button = document.getElementById('generate_query_button')
    clickfunction = create_proxy(pyscriptQueryBuild)
    generate_query_button.addEventListener("click", clickfunction)

    # connect the Clear Commands button
    clear_commands_button = document.getElementById('clear_commands_button')
    clickfunction = create_proxy(pyscriptClearCommands)
    clear_commands_button.addEventListener("click", clickfunction)

    # connect the Examples button
    examples_options = document.getElementById('command_examples')
    inputfunction = create_proxy(pyscriptChooseExample)
    examples_options.addEventListener("input", inputfunction)
    examples_options.value = ""  # set to first option

    # connect the Command Comments Checkbox
    command_comments_checkbox = document.getElementById(
        'command_comments_checkbox')
    clickfunction = create_proxy(pyscriptCommandComments)
    command_comments_checkbox.addEventListener("click", clickfunction)
    command_comments_checkbox.checked = False

    commands_input = document.getElementById('commands_input')
    commands_input.value = ''

    # connect the Code Block Output Checkbox
    codeblock_checkbox = document.getElementById(
        'codeblock_checkbox')
    clickfunction = create_proxy(pyscriptCodeBlock)
    codeblock_checkbox.addEventListener("click", clickfunction)
    codeblock_checkbox.checked = False


# %%
# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


# === global variables ===

# mode global variable

# for local testing or execution set the mode to python
# for web deployment set the mode to pyscript
# mode = "python"
mode = "pyScript"

# toggle showing comments for each generated query line
# showcommandcomments = True
showcommandcomments = False  # Default value

# toggle whether generated query gets wrapped in logseq code block
# ```clojure
# ````
# codeblock = True
codeblock = False  # Default value

# initialise the query structure
query = initialiseQuery()

# if running in a web server initialise DOM elements
if mode == "pyScript":
    pyScriptInitialise()

# Notify user loading has completed and they can enter commands and generate queries
print('Finished Loading .. You can now enter commands')

# specific tests in local mode (python)
# testQueryBuild("""- journalsbetween
#     - :today :30d-after
# """)

# testQueryBuild("""title: fred nerk
# - pages
#     - test*
# - tags
#     - ABC
#     - DEF
# - blockproperties
#     - p-major "jimbo"

# """)
