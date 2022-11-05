# %%

from queryDB import *
import copy
import time


def initialisteQueryLineDict():
    # merge common querylines into pages group and the blocks group
    tempDict = {}
    tempDict['pages-querylines'] = querylineDict['pages-querylines']
    tempDict['blocks-querylines'] = querylineDict['blocks-querylines']
    for commonqueryline in querylineDict['common-querylines']:
        tempDict['pages-querylines'][commonqueryline] = querylineDict['common-querylines'][commonqueryline]
        tempDict['blocks-querylines'][commonqueryline] = querylineDict['common-querylines'][commonqueryline]
    return tempDict


def initialiseQuery():
    global query_template
    query = copy.deepcopy(query_template)
    return query


# query structure
query_template = {
    "start": [],
    "errors": [],
    "open": [],
    "title": [],
    "query": [],
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


def getQueryLineSegment(querylinekey):
    try:
        return ['ok', querylineDBDict[querygroup][querylinekey]['segment']]
    except:
        errortext = querylinekey+' segment value not found in QueryDB\n'
        errormsg = ';; **ERROR: '+errortext+'\n'
        return ['error', errormsg]


def getQueryLine(querylinekey, querysegment):
    global showcommandcomments
    global querygroup
    try:
        if showcommandcomments == True:
            query[querysegment].append(
                '\n'+getQueryLineComment(querylinekey))
        return querylineDBDict[querygroup][querylinekey]['datalog']
    except:
        errormsg = '\n---- COMMAND ERROR ----\n'
        errormsg += querylinekey+' not found in QueryDB or invalid usage\n'
        if querygroup == 'pages-querylines':
            errormsg += querylinekey+" invalid within a 'pages' command query"
        if querygroup == 'blocks-querylines':
            errormsg += querylinekey+" invalid within a 'blocks' command query"
        errormsg += '\n----------------------\n'

        return errormsg


def getQueryLineComment(querylinekey):
    global querygroup
    comment = querylineDBDict[querygroup][querylinekey]['comment']
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
    global querygroup
    if command == None:
        return None
    # check command in Dictionary
    try:
        commandlist = commandsDict[command]['querylines']
    except:
        return None

    return commandlist


def buildCommonQueryLines():
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

    commandvalidity = checkCommandValid(command)

    if commandvalidity[0] == False:
        query['errors'].append(commandvalidity[1])
        return

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
    for key in querylinekeys:
        querysegmentresponse = getQueryLineSegment(key)[0]
        querysegmentdata = getQueryLineSegment(key)[1]
        if querysegmentresponse == 'error':
            query['errors'].append(querysegmentdata)
            continue

        querysegment = querysegmentdata
        queryline = getQueryLine(key, querysegment)

        # avoid duplications
        if queryline in query[querysegment]:
            continue

# TODO: BUG Why does tasks on its own put contains in TWICE!!!!
        # update the query with the query line
        query[querysegment].append(queryline)

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
    if len(positivecommandlines) > 0:
        processCommandLines('include', command, positivecommandlines)
    if len(negativecommandlines) > 0:
        processCommandLines('exclude', command, negativecommandlines)

    return


def checkCommandValid(command):
    commandvalidity = True  # default
    errormessage = ''
    if querygroup == 'pages-querylines':
        if command == 'blocktags':
            commandvalidity = False
            errormessage = '\n;; **ERROR: '+command + \
                ' not valid with pages command use blocks command instead\n'
        elif command == 'tasks':
            commandvalidity = False
            errormessage = '\n;; **ERROR: '+command + \
                ' not valid with pages command use blocks command instead\n'

    elif querygroup == 'blocks-querylines':
        if command in [

        ]:
            commandvalidity = False

    return [commandvalidity, errormessage]


def addQueryLines(command, prefix, querylinekey, arg):
    global query
    global showcommandcomments
    global mode

    querysegment = getQueryLineSegment(querylinekey)
    querysegmentresponse = getQueryLineSegment(querylinekey)[0]
    querysegmentdata = getQueryLineSegment(querylinekey)[1]
    if querysegmentresponse == 'error':
        query['errors'].append(querysegmentdata)
        return

    querysegment = querysegmentdata

    args = arg.split(",")

    # single argument commands
    if len(args) == 1:
        querylinekey = prefix+querylinekey
        updatedqueryline = getQueryLine(
            querylinekey, querysegment).replace("$$ARG1", arg)
        if not updatedqueryline in query[querysegment]:
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
        if not updatedqueryline in query[querysegment]:
            query[querysegment].append(updatedqueryline)
    else:
        query[querysegment].append(
            command+' => Invalid line => '+arg)


def processCommandLines(action, command, commandlines):
    global query
    global querygroup

    # if len(query['errors']) > 0:
    #     return

    if commandlines == []:
        return

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
                              arg[:-1])
                continue

            # pages ending with
            if arg[0] == '*' and arg[len(arg)-1] != '*':
                addQueryLines(command, prefix, 'arg_pagename_endswith',
                              arg[1:])
                continue

            # pages containing text
            if arg[0] == '*' and arg[len(arg)-1] == '*':
                addQueryLines(command, prefix, 'arg_pagename_contains',
                              arg[1:-1])
                continue

            # otherwise full pagename provided
            addQueryLines(command, prefix, 'pagename_is', arg)

        # --- blocks command
        if command == 'blocks':
            if arg[0] == '*' and arg[len(arg)-1] != '*':
                addQueryLines(
                    command, prefix, 'arg_blockcontent_startswith', arg[1:])
                continue

            if arg[0] != '*' and arg[len(arg)-1] == '*':
                addQueryLines(command, prefix,
                              'arg_blockcontent_endswith', arg[:-1])
                continue

            if arg[0] == '*' and arg[len(arg)-1] == '*':
                addQueryLines(
                    command, prefix, 'arg_blockcontent_contains', arg[1:-1])
                continue

        # --- pagetags command
        if command == "pagetags":
            # tags are stored internally in Logseq as lower case
            args = arg.split()  # allow for multiple tags
            for arg in args:
                addQueryLines(command, prefix, 'pagetags_are',
                              arg.lower())

        # --- blocktags command
        if command == "blocktags":
            # tags are stored internally in Logseq as lower case
            args = arg.split()  # allow for multiple tags
            for arg in args:
                addQueryLines(command, prefix, 'blocktags_are',
                              arg.lower())

        # --- pageproperties command
        #     arg is propertyname,propertyvalue
        if command == "pageproperties":
            addQueryLines(command, prefix,
                          'page_properties_are', arg)

        # --- blockproperties command
        #     arg is propertyname,propertyvalue
        if command == "blockproperties":
            addQueryLines(command, prefix,
                          'block_properties_are', arg)

        # --- tasks command
        if command == "tasks":
            addQueryLines(command, prefix,
                          'tasks_are', arg)

        # --- namespace command
        if command == "namespace":
            addQueryLines(command, prefix,
                          'namespace', arg)

        # --- scheduled command
        if command == "scheduled":
            addQueryLines(command, prefix,
                          'scheduled', arg)

        # --- scheduledbetween command
        if command == "scheduledbetween":
            addQueryLines(command, prefix,
                          'scheduledbetween', arg)

        # --- deadline command
        if command == "deadline":
            addQueryLines(command, prefix,
                          'deadline', arg)

        # --- deadlinebetween command
        if command == "deadlinebetween":
            addQueryLines(command, prefix,
                          'deadlinebetween', arg)

        # --- journalonly command
        if command == "journalonly":
            addQueryLines(command, prefix,
                          'page_is_journal', arg)

        # --- journalsbetween command
        if command == "journalsbetween":
            addQueryLines(command, prefix,
                          'journalsbetween', arg)

        # --- daterange command
        if command == "daterange":
            addQueryLines(command, prefix,
                          'daterange', arg)

        # --- collapse command
        if command == "collapse":
            addQueryLines(command, prefix,
                          'collapse', arg)

        # --- expand command
        if command == "collapse":
            addQueryLines(command, prefix,
                          'expand', arg)

    if lastline != '':
        query['filters'].append(lastline)

    return


def insertQueryLineIntoSegment(key):
    querysegmentresponse = getQueryLineSegment(key)[0]
    querysegmentdata = getQueryLineSegment(key)[1]
    if querysegmentresponse == 'error':
        query['errors'].append(querysegmentdata)
        return
    querysegment = querysegmentdata

    query[key].append(getQueryLine(key, querysegment))
    pass


def checkUsingPagesorBlocks(commandlines):
    global querygroup
    pagesfound = False
    blocksfound = False

    for commandline in commandlines:
        commandline = commandline.strip()
        if commandline.startswith('- pages'):
            pagesfound = True
        if commandline.startswith('- blocks'):
            blocksfound = True

    if pagesfound == True and blocksfound == False:
        querygroup = "pages-querylines"
        return

    if blocksfound == True and pagesfound == False:
        querygroup = "blocks-querylines"
        return

    if pagesfound == False and blocksfound == False:
        query['errors'].append(
            ";; WARNING: Must have 'pages' command or 'blocks' Command\n;;          otherwise the query cannot get any information\n;;          Inserting a blocks command for you\n")
        insertBlocksCommand(commandlines)
        blocksfound = True
        querygroup = "blocks-querylines"
        return

    if pagesfound and blocksfound:
        query['errors'].append(
            ";; ERROR: Cannot have 'pages' command and 'blocks' command together in a command list\n\n")
        return


def insertBlocksCommand(commandlines):
    # insert blocks command after the title line
    # if there is not title place at top of the list
    if len(commandlines) > 0:
        if commandlines[0].index('title:') > -1:
            commandlines.insert(1, '    - *')
            commandlines.insert(1, '- blocks')
    else:
        commandlines.insert(0, '- blocks\n    - *\n')

    return


def validCommand(command):
    try:
        if commandsDict[command]:
            return True
    except:
        return False


def processCommandList(commandlists):
    global query
    global querygroup

    query = initialiseQuery()

    commandlines = commandlists.split("\n")

    # determine if we are querying pages or blocks
    # pages queries have different query commandlines from blocks
    # pages command and blocks command cannot be in the same command list
    # default to blocks command if both pages and blocks command are missing

    checkUsingPagesorBlocks(commandlines)

    currentcommand = ''
    # Element('print_output').write(, str(len(commandlines)))
    commandLinesDict = {}
    for line in commandlines:
        if line == '' or line.startswith(";;"):
            continue
        if line.strip().startswith('title:'):
            query["title"].append(getQueryLine('title', 'title').replace(
                '$$ARG1', line.split(":")[1].strip()))
            continue
        if line.startswith('- '):  # encountered a command
            fields = line.split(" ")
            commandname = fields[1]
            if validCommand(commandname):
                commandLinesDict[commandname] = {}
                if currentcommand == '' or line != currentcommand:
                    currentcommand = commandname
                    commandLinesDict[commandname]["commandlines"] = []
                    commandLinesDict[commandname]["commandlines"].append(line)
                    continue
            else:
                query['errors'].append(
                    ";; WARNING: '"+line+"' is not valid command.\n;;          Either a mispelt command or no leading dash")
                continue
        # has a hypen after column 1 so must be an command argument line
        elif line.startswith(' ') and line.strip().startswith('- '):
            if currentcommand == '':
                query['errors'].append(
                    ";; ERROR: '"+line+"' is a command argument but does not have a parent command\n;;       Either a command is missing or this should ne be am argument line")
            else:
                # have an argument line
                commandLinesDict[commandname]["commandlines"].append(line)
        else:
            if 'title ' in line:
                query['errors'].append(
                    ";; WARNING: title line should start with title:")
            elif not line.strip().startswith('- ') and not line.find('title:') > -1:
                query['errors'].append(
                    ";; WARNING: "+line+" has no leading hypen eg '- pages'")

    # build standard query lines
    insertQueryLineIntoSegment('start')
    insertQueryLineIntoSegment('open')
    insertQueryLineIntoSegment('where')
    insertQueryLineIntoSegment('closefind')
    insertQueryLineIntoSegment('closequery')
    insertQueryLineIntoSegment('end')

    for command in commandLinesDict:
        processCommand(command, commandLinesDict)

    query['closefind'] = [getQueryLine('closefind', 'closefind')]
    # finalise query segments
    query['closequery'] = [getQueryLine('closequery', 'closequery')]
    query['end'] = [getQueryLine('end', 'end')]

    return


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
        print('Query Group: '+querygroup)
        print("----------------------------")
        print(commands)


def testQueryBuild(commands):
    global mode
    global querygroup
    processCommandList(commands)
    advancedquery = constructQuery()
    printInputCommandList(commands)
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

# global toggle showing comments for each generated query line
# showcommandcomments = True
showcommandcomments = False  # Default value

# global querygroup - current command lists mode
# Queries either retrieve pages (special blocks of their own)
# or retieve all blocks including special page blocks
#   'pages-querylines' mode is for page retrieval queries
#   'block-querylines' mode is for block retrieval queries
querygroup = 'blocks-querylines'  # default group

# toggle whether generated query gets wrapped in logseq code block
# ```clojure
# ````
# codeblock = True
codeblock = False  # Default value

# initialise the query structure
query = initialiseQuery()

# merge the common query lines into the page and blocks group
querylineDBDict = initialisteQueryLineDict()

# if running in a web server initialise DOM elements
if mode == "pyScript":
    pyScriptInitialise()

# Notify user loading has completed and they can enter commands and generate queries
print('Finished Loading .. You can now enter commands')

# specific tests in local mode (python)
# testQueryBuild("""title: select and exclude task types
# - tasks
#     - TODO
#     - not DOING
# """)
