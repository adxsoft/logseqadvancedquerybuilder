
# Common querylines for all generated advanced queries
defaultQueryLines = {
    "query": ["findblocks"],
    "where": ["where"],
    "filters": [
        "blockcontent",
        "page",
        "pagename",
    ]
}


# Dictionary of individual advanced query lines
querylineDict = {
    'start':
    {
        'name': 'start',
        'datalog': '#+BEGIN_QUERY',
        'comment': 'Query Begin Header'
    },
    'open':
    {
        'name': 'open',
        'datalog': '{',
        'comment': 'opening brace'
    },
    'title':
    {
        'name': 'title',
        'datalog': ':title [:b "$$ARG1"]',
        'comment': 'Display title at start of query'
    },
    'findblocks':
    {
        'name': 'findblocks',
        'datalog': ':query [:find (pull ?block [*])',
        'comment': 'Get every block into variable ?block'
    },
    'daterange':
    {
        'name': 'daterange',
        'datalog': ':in $ ?startdate ?enddate',
        'comment': 'give query the ?startdate variable and the ?enddate variable (set by :inputs)'
    },
    'where':
    {
        'name': 'where',
        'datalog': ':where',
        'comment': 'filter command'
    },
    'blockcontent':
    {
        'name': 'blockcontent',
        'datalog': '[?block :block/content ?blockcontent]',
        'comment': 'get block content into variable ?blockcontent'
    },
    'page':
    {
        'name': 'page',
        'datalog': '[?block :block/page ?page]',
        'comment': 'get page block into variable ?page (used later)'
    },
    'pagename':
    {
        'name': 'pagename',
        'datalog': '[?page :block/name ?pagename]',
        'comment': 'get page name  from the page block into variable ?pagename'
    },
    'marker':
    {
        'name': 'marker',
        'datalog': '[?block :block/marker ?marker]',
        'comment': 'get block marker (TODO LATER ETC) into variable ?marker'
    },
    'scheduled':
    {
        'name': 'scheduled',
        'datalog': '[?block :block/scheduled ?scheduleddate]',
        'comment': 'get scheduled date in the block into variable ?scheduleddate'
    },
    'scheduledfrom':
    {
        'name': 'scheduledfrom',
        'datalog': '[(>= ?scheduleddate ?startdate)]',
        'comment': 'Select if scheduleddate greater than start date'
    },
    'scheduledto':
    {
        'name': 'scheduledto',
        'datalog': '[(<= ?scheduleddate ?enddate)]',
        'comment': 'Select if scheduleddate less than end date'
    },
    'deadline':
    {
        'name': 'deadline',
        'datalog': '[?block :block/deadline ?deadlinedate]',
        'comment': 'get deadline date in the block into variable ?date'
    },
    'deadlinefrom':
    {
        'name': 'deadlinefrom',
        'datalog': '[(>= ?deadlinedate ?startdate)]',
        'comment': 'Select if deadlinedate greater than start date'
    },
    'deadlineto':
    {
        'name': 'deadlineto',
        'datalog': '[(<= ?deadlinedate ?enddate)]',
        'comment': 'Select if deadlinedate less than end date'
    },
    'linksandtags':
    {
        'name': 'linksandtags',
        'datalog': '[?block :block/path-refs ?ref]',
        'comment': 'Get links or tags in block into list ?refs'
    },
    'properties':
    {
        'name': 'properties',
        'datalog': '[?block :block/properties ?props]',
        'comment': 'Get properties for a block into list ?props'
    },
    'pagename_is':
    {
        'name': 'pagename_is',
        'datalog': '[?page :block/name "$$ARG1"]',
        'comment': 'Select specific page'
    },
    'not_pagename_is':
    {
        'name': 'not_pagename_is',
        'datalog': '(not [?page :block/name "$$ARG1"])',
        'comment': 'Exclude specific page'
    },
    'tasks_are':
    {
        'name': 'tasks_are',
        'datalog': '[(contains? #{"$$ARG1"} ?marker)]',
        'comment': 'Select block if it has one or more tasks (TODO, DONE etc)'
    },
    'not_tasks_are':
    {
        'name': 'not_tasks_are',
        'datalog': '(not [(contains? #{"$$ARG1"} ?marker)])',
        'comment': 'Exclude block if it has one or more tasks'
    },
    'page_is_journal':
    {
        'name': 'page_is_journal',
        'datalog': '[?page :block/journal? true]',
        'comment': 'Select block if it is a journal'
    },
    'journalsbetween':
    {
        'name': 'scheduledbetween',
        'datalog': ':inputs [$$ARG1]',
        'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
    },
    'journal_date':
    {
        'name': 'journal_date',
        'datalog': '[?page :block/journal-day ?journaldate]',
        'comment': 'get journal date into variable ?journaldate'
    },
    'journalfrom':
    {
        'name': 'journalfrom',
        'datalog': '[(>= ?journaldate ?startdate)]',
        'comment': 'Select if journaldate greater than start date'
    },
    'journalto':
    {
        'name': 'journalto',
        'datalog': '[(<= ?journaldate ?enddate)]',
        'comment': 'Select if journalddate less than end date'
    },
    'page_properties_are':
    {
        'name': 'page_properties_are',
        'datalog': '(page-property ?page :$$ARG1 $$ARG2)',
        'comment': 'Select if block or page has a single property (arg1) with value arg2'
    },
    'not_page_properties_are':
    {
        'name': 'not_page_properties_are',
        'datalog': '(not (page-property ?page :$$ARG1 $$ARG2))',
        'comment': 'Exclude a block or page if it has a single property (arg1) with value arg2'
    },
    'block_properties_are':
    {
        'name': 'block_properties_are',
        'datalog': '(property ?block :$$ARG1 $$ARG2)',
        'comment': 'Select if block has a single property (arg1) with value arg2'
    },
    'not_block_properties_are':
    {
        'name': 'not_block_properties_are',
        'datalog': '(not (property ?block :$$ARG1 $$ARG2))',
        'comment': 'Exclude if block has a single property (arg1) with value arg2'
    },
    'blocktags_are':
    {
        'name': 'blocktags_are',
        'datalog': '(page-ref ?block "$$ARG1")',
        'comment': 'Select block if it has a specific tag or page link'
    },
    'not_blocktags_are':
    {
        'name': 'not_blocktags_are',
        'datalog': '(not (page-ref ?block "$$ARG1"))',
        'comment': 'Exclude block if it has a specific tag or page link'
    },
    'pagetags_are':
    {
        'name': 'pagetags_are',
        'datalog': '(page-tags ?page #{"$$ARG1"})',
        'comment': 'Select page block with one or more page tags'
    },
    'not_pagetags_are':
    {
        'name': 'not_pagetags_are',
        'datalog': '(not (page-tags ?page #{"$$ARG1"}))',
        'comment': 'Exclude page block with one or more page tags'
    },
    'namespace':
    {
        'name': 'namespace',
        'datalog': '(namespace ?page "$$ARG1")',
        'comment': 'Select if block is within namespace arg1'
    },
    'not_namespace':
    {
        'name': 'namespace',
        'datalog': '(not (namespace ?page "$$ARG1"))',
        'comment': 'Exclude if block is not within a specific namespace'
    },
    'arg_pagename_startswith':
    {
        'name': 'arg_pagename_startswith',
        'datalog': '[(clojure.string/starts-with? ?pagename "$$ARG1")]',
        'comment': 'Select if page title starts with arg1'
    },
    'arg_pagename_endswith':
    {
        'name': 'arg_pagename_endswith',
        'datalog': '[(clojure.string/ends-with? ?pagename "$$ARG1")]',
        'comment': 'Select if page title ends with arg1'
    },
    'arg_pagename_contains':
    {
        'name': 'arg_pagename_contains',
        'datalog': '[(clojure.string/includes? ?pagename "$$ARG1")]',
        'comment': 'Select if page title contains arg1'
    },
    'not_arg_pagename_startswith':
    {
        'name': 'not_arg_pagename_startswith',
        'datalog': '(not [(clojure.string/starts-with? ?pagename "$$ARG1")])',
        'comment': 'Exclude if page title ends with arg1'
    },
    'not_arg_pagename_endswith':
    {
        'name': 'not_arg_pagename_endswith',
        'datalog': '(not [(clojure.string/ends-with? ?pagename "$$ARG1")])',
        'comment': 'Exclude if page title ends with arg1'
    },
    'not_arg_pagename_contains':
    {
        'name': 'not_arg_pagename_contains',
        'datalog': '(not [(clojure.string/includes? ?pagename "$$ARG1")])',
        'comment': 'Exclude if page title contains arg1'
    },
    'arg_blockcontent_startswith':
    {
        'name': 'arg_blockcontent_startswith',
        'datalog': '[(clojure.string/starts-with? ?blockcontent "$$ARG1")]',
        'comment': 'Select if block content starts with arg1'
    },
    'arg_blockcontent_endswith':
    {
        'name': 'arg_blockcontent_endswith',
        'datalog': '[(clojure.string/ends-with? ?blockcontent "$$ARG1")]',
        'comment': 'Select if block content ends with arg1'
    },
    'arg_blockcontent_contains':
    {
        'name': 'arg_blockcontent_contains',
        'datalog': '[(clojure.string/includes? ?blockcontent "$$ARG1")]',
        'comment': 'Select if block content contains arg1'
    },
    'not_arg_blockcontent_startswith':
    {
        'name': 'not_arg_blockcontent_startswith',
        'datalog': '(not [(clojure.string/starts-with? ?blockcontent "$$ARG1")])',
        'comment': 'Exclude if block content starts with arg1'
    },
    'not_arg_blockcontent_endswith':
    {
        'name': 'not_arg_blockcontent_endswith',
        'datalog': '(not [(clojure.string/ends-with? ?blockcontent "$$ARG1")])',
        'comment': 'Exclude if block content ends with arg1'
    },
    'not_arg_blockcontent_contains':
    {
        'name': 'not_arg_blockcontent_contains',
        'datalog': '(not [(clojure.string/includes? ?blockcontent "$$ARG1")])',
        'comment': 'Exclude if block content contains arg1'
    },
    'capitalize':
    {
        'name': 'capitalize',
        'datalog': '(clojure.string/capitalize "$$ARG1")',
        'comment': 'Capitalize the string'
    },
    'scheduledbetween':
    {
        'name': 'scheduledbetween',
        'datalog': ':inputs [$$ARG1]',
        'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
    },
    'deadlinebetween':
    {
        'name': 'deadlinebetween',
        'datalog': ':inputs [$$ARG1]',
        'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
    },
    'journalbetween':
    {
        'name': 'journalbetween',
        'datalog': ':inputs [$$ARG1]',
        'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
    },
    'breadcrumb_show_false':
    {
        'name': 'breadcrumb_show_false',
        'datalog': ':breadcrumb-show? false',
        'comment': 'Suppress breadcrumbs view'
    },
    'breadcrumb_show_true':
    {
        'name': 'breadcrumb_show_true',
        'datalog': ':breadcrumb-show? true',
        'comment': 'Show breadcrumbs above each block'
    },
    'collapse_false':
    {
        'name': 'collapsed_false',
        'datalog': ':collapsed? false',
        'comment': 'Toggle collapse or fold'
    },
    'collapse_true':
    {
        'name': 'collapsed_true',
        'datalog': ':collapsed? true',
        'comment': 'Toggle collapse or fold'
    }, 'closefind':
    {
        'name': 'closefind',
        'datalog': ']',
        'comment': 'Query Footer'
    },
    'closequery':
    {
        'name': 'closequery',
        'datalog': '}',
        'comment': 'Query Footer'
    },
    'end':
    {
        'name': 'end',
        'datalog': '#+END_QUERY',
        'comment': 'Query Footer'
    }
}

# Dictionary of query builder commands
commandsDict = {
    "blocks": {
        "querylines": [
            "findblocks",
            "where"
        ],
        "description": "select logseq blocks by wildcards"
    },
    "blockproperties": {
        "querylines":  [
            "findblocks",
            "where"
        ],
        "description": "select blocks by property values"
    },
    "blocktags":  {
        "querylines": [
        ],
        "description": "select blocks by tag"
    },
    "deadline": {
        "querylines":  [
            "deadline"
        ],
        "description": "select pages or blocks that have a deadline"
    },
    "deadlinebetween": {
        "querylines":  [
            "deadlinebetween"
        ],
        "description": "select pages or blocks that have a deadline in a date range"
    },
    "journalsbetween": {
        "querylines":  [
        ],
        "description": "only select journal pages in a date range"
    },
    "journalonly": {
        "querylines":  [
        ],
        "description": "only select journal pages"
    },
    "namespace": {
        "querylines":  [
        ],
        "description": "select pages or blocks within a namespace"
    },
    "pages":   {
        "querylines": [
            "findblocks",
            "where"
        ],
        "description": "select pages by wildcards"
    },
    "pageproperties":  {
        "querylines": [
            "findblocks",
            "where"
        ],
        "description": "select pages by page properties"
    },
    "pagetags":  {
        "querylines": [
            "findblocks",
            "where"
        ],
        "description": "select pages by tag"
    },
    "tasks": {
        "querylines":  [
        ],
        "description": "select tasks"
    },
    "scheduled": {
        "querylines":  [
            "scheduled"
        ],
        "description": "select pages or blocks that are scheduled"
    },
    "scheduledbetween": {
        "querylines":  [
            "scheduledbetween"
        ],
        "description": "select pages or blocks that are scheduled in a date range"
    },
    "collapse": {
        "querylines":  [
            "collapsed_true"
        ],
        "description": "collapse found blocks"
    },
    "expand": {
        "querylines":  [
            "collapsed_false"
        ],
        "description": "expand found blocks"
    },
    "showbreadcrumb": {
        "querylines":  [
            "breadcrumb_show_true"
        ],
        "description": "show breadcrumb for found blocks"
    },
    "hidebreadcrumb": {
        "querylines":  [
            "breadcrumb_show_false"
        ],
        "description": "hide breadcrumb for found blocks"
    },
}
