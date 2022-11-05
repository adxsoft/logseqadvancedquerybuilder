
# Dictionary of individual advanced query lines
querylineDict = {
    'common-querylines': {
        'start':
        {
            'name': 'start',
            'useincommands': ['common'],
            'segment': 'start',
            'datalog': '#+BEGIN_QUERY',
            'comment': 'Query Begin Header'
        },
        'open':
        {
            'name': 'open',
            'useincommands': ['common'],
            'segment': 'open',
            'datalog': '{',
            'comment': 'opening brace'
        },
        'title':
        {
            'name': 'title',
            'useincommands': ['common'],
            'segment': 'title',
            'datalog': ':title [:b "$$ARG1"]',
            'comment': 'Display title at start of query'
        },
        'findblocks':
        {
            'name': 'findblocks',
            'useincommands': ['common'],
            'segment': 'query',
            'datalog': ':query [:find (pull ?block [*])',
            'comment': 'Get every block into variable ?block'
        },
        'daterange':
        {
            'name': 'daterange',
            'useincommands': ['common'],
            'segment': 'in',
            'datalog': ':in $ ?startdate ?enddate',
            'comment': 'give query the ?startdate variable and the ?enddate variable (set by :inputs)'
        },
        'where':
        {
            'name': 'where',
            'useincommands': ['common'],
            'segment': 'where',
            'datalog': ':where',
            'comment': 'filter command'
        },
        'tasks_are':
        {
            'name': 'tasks_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(contains? #{"$$ARG1"} ?marker)]',
            'comment': 'Select block if it has one or more tasks (TODO or DONE etc)'
        },
        'not_tasks_are':
        {
            'name': 'not_tasks_are',
            'useincommands': ['common'],
            'segment': 'filters',
            'datalog': '(not [(contains? #{"$$ARG1"} ?marker)])',
            'comment': 'Exclude block if it has one or more tasks'
        },
        'scheduledbetween':
        {
            'name': 'scheduledbetween',
            'useincommands': ['common'],
            'segment': 'inputs',
            'datalog': ':inputs [$$ARG1]',
            'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
        },
        'journalfrom':
        {
            'name': 'journalfrom',
            'useincommands': ['common'],
            'segment': 'filters',
            'datalog': '[(>= ?journaldate ?startdate)]',
            'comment': 'Select if journaldate greater than start date'
        },
        'journalto':
        {
            'name': 'journalto',
            'useincommands': ['common'],
            'segment': 'filters',
            'datalog': '[(<= ?journaldate ?enddate)]',
            'comment': 'Select if journalddate less than end date'
        },
        'journalsbetween':
        {
            'name': 'journalsbetween',
            'useincommands': ['common'],
            'segment': 'inputs',
            'datalog': ':inputs [$$ARG1]',
            'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
        },
        'breadcrumb_show_false':
        {
            'name': 'breadcrumb_show_false',
            'useincommands': ['common'],
            'segment': 'options',
            'datalog': ':breadcrumb-show? false',
            'comment': 'Suppress breadcrumbs view'
        },
        'breadcrumb_show_true':
        {
            'name': 'breadcrumb_show_true',
            'useincommands': ['common'],
            'segment': 'options',
            'datalog': ':breadcrumb-show? true',
            'comment': 'Show breadcrumbs above each block'
        },
        'collapse_false':
        {
            'name': 'collapse_false',
            'useincommands': ['common'],
            'segment': 'options',
            'datalog': ':collapsed? false',
            'comment': 'Toggle collapse or fold'
        },
        'collapse_true':
        {
            'name': 'collapse_true',
            'useincommands': ['common'],
            'segment': 'options',
            'datalog': ':collapsed? true',
            'comment': 'Toggle collapse or fold'
        },
        'closefind':
        {
            'name': 'closefind',
            'useincommands': ['common'],
            'segment': 'closefind',
            'datalog': ']',
            'comment': 'Query Footer'
        },
        'closequery':
        {
            'name': 'closequery',
            'useincommands': ['common'],
            'segment': 'closequery',
            'datalog': '}',
            'comment': 'Query Footer'
        },
        'end':
        {
            'name': 'end',
            'useincommands': ['common'],
            'segment': 'end',
            'datalog': '#+END_QUERY',
            'comment': 'Query Footer'
        },
    },
    'blocks-querylines': {
        'blockcontent':
        {
            'name': 'blockcontent',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?block :block/content ?blockcontent]',
            'comment': 'get block content into variable ?blockcontent'
        },
        'page':
        {
            'name': 'page',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?block :block/page ?page]',
            'comment': 'get page (special type of block) into variable ?page (used later)'
        },
        'pagename':
        {
            'name': 'pagename',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?page :block/name ?pagename]',
            'comment': 'get page name (lowercase) from the page block into variable ?pagename'
        },
        'marker':
        {
            'name': 'marker',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?block :block/marker ?marker]',
            'comment': 'get block marker (TODO LATER ETC) into variable ?marker'
        },
        'scheduled':
        {
            'name': 'scheduled',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?block :block/scheduled ?scheduleddate]',
            'comment': 'get scheduled date in the block into variable ?scheduleddate'
        },
        'scheduledfrom':
        {
            'name': 'scheduledfrom',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(>= ?scheduleddate ?startdate)]',
            'comment': 'Select if scheduleddate greater than start date'
        },
        'scheduledto':
        {
            'name': 'scheduledto',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(<= ?scheduleddate ?enddate)]',
            'comment': 'Select if scheduleddate less than end date'
        },
        'deadline':
        {
            'name': 'deadline',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?block :block/deadline ?deadlinedate]',
            'comment': 'get deadline date in the block into variable ?date'
        },
        'deadlinefrom':
        {
            'name': 'deadlinefrom',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(>= ?deadlinedate ?startdate)]',
            'comment': 'Select if deadlinedate greater than start date'
        },
        'deadlineto':
        {
            'name': 'deadlineto',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(<= ?deadlinedate ?enddate)]',
            'comment': 'Select if deadlinedate less than end date'
        },
        'pagename_is':
        {
            'name': 'pagename_is',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?block :block/name "$$ARG1"]',
            'comment': 'Select specific page from the page special block\nPresence of :block/name in a blocks means \nit is a block that has the page attributes'
        },
        'not_pagename_is':
        {
            'name': 'not_pagename_is',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not [?block :block/name "$$ARG1"])',
            'comment': 'Exclude specific page from the page special block'
        },
        'page_is_journal':
        {
            'name': 'page_is_journal',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?page :block/journal? true]',
            'comment': 'Select block if its belongs to a journal page'
        },
        'not_page_is_journal':
        {
            'name': 'not_page_is_journal',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?page :block/journal? false]',
            'comment': 'Exclude block if its belongs to a journal page'
        },
        'journal_date':
        {
            'name': 'journal_date',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[?page :block/journal-day ?journaldate]',
            'comment': 'get journal date into variable ?journaldate'
        },
        'block_properties_are':
        {
            'name': 'block_properties_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(property ?block :$$ARG1 $$ARG2)',
            'comment': 'Select if block has a single property (arg1) with value arg2'
        },
        'not_block_properties_are':
        {
            'name': 'not_block_properties_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not (property ?block :$$ARG1 $$ARG2))',
            'comment': 'Exclude if block has a single property (arg1) with value arg2'
        },
        'blocktags_are':
        {
            'name': 'blocktags_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(page-ref ?block "$$ARG1")',
            'comment': 'Select block if it has a specific tag or page link'
        },
        'not_blocktags_are':
        {
            'name': 'not_blocktags_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not (page-ref ?block "$$ARG1"))',
            'comment': 'Exclude block if it has a specific tag or page link'
        },
        'page_properties_are':
        {
            'name': 'page_properties_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(page-property ?page :$$ARG1 $$ARG2)',
            'comment': 'Select block if the page it belongs to\nhas a page property (arg1) with value arg2'
        },
        'not_page_properties_are':
        {
            'name': 'not_page_properties_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not (page-property ?page :$$ARG1 $$ARG2))',
            'comment': 'Exclude block if the page it belongs to\nhas a page property (arg1) with value arg2'
        },
        'pagetags_are':
        {
            'name': 'pagetags_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(page-tags ?page #{"$$ARG1"})',
            'comment': 'Select block if the page it belongs to\nhas a one or more page tags'
        },
        'not_pagetags_are':
        {
            'name': 'not_pagetags_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not (page-tags ?page #{"$$ARG1"}))',
            'comment': 'Exclude block if the page it belongs to\nhas one or more page tags'
        },
        'namespace':
        {
            'name': 'namespace',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(namespace ?page "$$ARG1")',
            'comment': 'Select block if the page it belongs to is within namespace arg1'
        },
        'not_namespace':
        {
            'name': 'not_namespace_blocks',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not (namespace ?page "$$ARG1"))',
            'comment': 'Exclude block if the page it belongs to is within namespace arg1'
        },
        'arg_blockcontent_startswith':
        {
            'name': 'arg_blockcontent_startswith',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(clojure.string/starts-with? ?blockcontent "$$ARG1")]',
            'comment': 'Select if block content starts with arg1'
        },
        'arg_blockcontent_endswith':
        {
            'name': 'arg_blockcontent_endswith',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(clojure.string/ends-with? ?blockcontent "$$ARG1")]',
            'comment': 'Select if block content ends with arg1'
        },
        'arg_blockcontent_contains':
        {
            'name': 'arg_blockcontent_contains',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '[(clojure.string/includes? ?blockcontent "$$ARG1")]',
            'comment': 'Select if block content contains arg1'
        },
        'not_arg_blockcontent_startswith':
        {
            'name': 'not_arg_blockcontent_startswith',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not [(clojure.string/starts-with? ?blockcontent "$$ARG1")])',
            'comment': 'Exclude if block content starts with arg1'
        },
        'not_arg_blockcontent_endswith':
        {
            'name': 'not_arg_blockcontent_endswith',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not [(clojure.string/ends-with? ?blockcontent "$$ARG1")])',
            'comment': 'Exclude if block content ends with arg1'
        },
        'not_arg_blockcontent_contains':
        {
            'name': 'not_arg_blockcontent_contains',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not [(clojure.string/includes? ?blockcontent "$$ARG1")])',
            'comment': 'Exclude if block content contains arg1'
        },
        'scheduledbetween':
        {
            'name': 'scheduledbetween',
            'useincommands': ['blocks'],
            'segment': 'inputs',
            'datalog': ':inputs [$$ARG1]',
            'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
        },
        'deadlinebetween':
        {
            'name': 'deadlinebetween',
            'useincommands': ['blocks'],
            'segment': 'inputs',
            'datalog': ':inputs [$$ARG1]',
            'comment': 'set the input values for a date range for example could be\n       :today :365d-after'
        },
    },
    'pages-querylines': {
        'original-pagename':
        {
            'name': 'original-pagename',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[?block :block/original-name ?originalpagename]',
            'comment': 'get original page name (case sensitive) into variable ?originalpagename',
        },
        'pagename':
        {
            'name': 'pagename',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[?block :block/name ?pagename]',
            'comment': 'get page name (lowercase) from the special page block into variable ?pagename',
        },
        'pagename_is':
        {
            'name': 'pagename_is',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[?block :block/name "$$ARG1"]',
            'comment': 'Select specific page using the :block/name\nwhich is only present in special blocks that\nhave the page attributes'
        },
        'not_pagename_is':
        {
            'name': 'not_pagename_is',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(not [?block :block/name "$$ARG1"])',
            'comment': 'Exclude specific page using the :block/name\nwhich is only present in special blocks that\nhave the page attributes'
        },
        'page_is_journal':
        {
            'name': 'page_is_journal',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[?block :block/journal? true]',
            'comment': 'Select block if it belonhs to a a journal'
        },
        'not_page_is_journal':
        {
            'name': 'not_page_is_journal',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[?block :block/journal? false]',
            'comment': 'Exclude block if it belonhs to a a journal'
        },
        'journal_date':
        {
            'name': 'journal_date',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[?block :block/journal-day ?journaldate]',
            'comment': 'get journal date into variable ?journaldate'
        },
        'page_properties_are':
        {
            'name': 'page_properties_are',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(page-property ?block :$$ARG1 $$ARG2)',
            'comment': 'Select if block is a special page blockand  has a single property (arg1) with value arg2'
        },
        'not_page_properties_are':
        {
            'name': 'not_page_properties_are',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(not (page-property ?block :$$ARG1 $$ARG2))',
            'comment': 'Exclude if block is a special page blockand  has a single property (arg1) with value arg2'
        },
        'block_properties_are':
        {
            'name': 'block_properties_are',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(page-property ?block :$$ARG1 $$ARG2)',
            'comment': 'Select if block has a single property (arg1) with value arg2'
        },
        'not_block_properties_are':
        {
            'name': 'not_block_properties_are',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(not (property ?block :$$ARG1 $$ARG2))',
            'comment': 'Exclude if block has a single property (arg1) with value arg2'
        },
        'pagetags_are':
        {
            'name': 'pagetags_are',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(page-tags ?block #{"$$ARG1"})',
            'comment': 'Select special page block with one or more page tags'
        },
        'not_pagetags_are':
        {
            'name': 'not_pagetags_are',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(not (page-tags ?block #{"$$ARG1"}))',
            'comment': 'Exclude special page block with one or more page tags'
        },
        'blocktags_are':
        {
            'name': 'blocktags_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(page-tags ?block #{"$$ARG1"})',
            'comment': 'Select block if the page it belongs to\nhas a specific page tag or page link'
        },
        'not_blocktags_are':
        {
            'name': 'not_blocktags_are',
            'useincommands': ['blocks'],
            'segment': 'filters',
            'datalog': '(not (page-tags ?block #{"$$ARG1"}))',
            'comment': 'Exclude block if the page it belongs to\nhas a specific page tag or page link'
        },
        'namespace':
        {
            'name': 'namespace_pages',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(namespace ?block "$$ARG1")',
            'comment': 'Select if special page block is within namespace arg1'
        },
        'not_namespace':
        {
            'name': 'not_namespace_pages',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(not (namespace ?block "$$ARG1"))',
            'comment': 'Select if special page block is within namespace arg1'
        },
        'arg_pagename_startswith':
        {
            'name': 'arg_pagename_startswith',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[(clojure.string/starts-with? ?pagename "$$ARG1")]',
            'comment': 'Select if page title starts with arg1'
        },
        'arg_pagename_endswith':
        {
            'name': 'arg_pagename_endswith',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '[(clojure.string/ends-with? ?pagename "$$ARG1")]',
            'comment': 'Select if page title ends with arg1'
        },
        'arg_pagename_contains':
        {
            'name': 'arg_pagename_contains',
            'useincommands': ['common'],
            'segment': 'filters',
            'datalog': '[(clojure.string/includes? ?pagename "$$ARG1")]',
            'comment': 'Select if page title contains arg1'
        },
        'not_arg_pagename_startswith':
        {
            'name': 'not_arg_pagename_startswith',
            'useincommands': ['common'],
            'segment': 'filters',
            'datalog': '(not [(clojure.string/starts-with? ?pagename "$$ARG1")])',
            'comment': 'Exclude if page title ends with arg1'
        },
        'not_arg_pagename_endswith':
        {
            'name': 'not_arg_pagename_endswith',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(not [(clojure.string/ends-with? ?pagename "$$ARG1")])',
            'comment': 'Exclude if page title ends with arg1'
        },
        'not_arg_pagename_contains':
        {
            'name': 'not_arg_pagename_contains',
            'useincommands': ['pages'],
            'segment': 'filters',
            'datalog': '(not [(clojure.string/includes? ?pagename "$$ARG1")])',
            'comment': 'Exclude if page title contains arg1'
        },
    }
}

# Dictionary of query builder commands
commandsDict = {
    "blocks": {
        "querylines": [
            "findblocks",
            "where",
            "blockcontent",
            "page",
            "pagename",
        ],
        "description": "select logseq blocks by wildcards"
    },
    "blockproperties": {
        "querylines":  [
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
        "description": "select blocks that have a deadline"
    },
    "deadlinebetween": {
        "querylines":  [
            "deadline",
            "deadlinefrom",
            "deadlineto",
            "daterange"
        ],
        "description": "select blocks that have a deadline in a date range"
    },
    "journalsbetween": {
        "querylines":  [
            "journal_date",
            "journalfrom",
            "journalto",
            "daterange"
        ],
        "description": "only select journal pages in a date range"
    },
    "journalonly": {
        "querylines":  [
            "page_is_journal"
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
            "where",
            "pagename",
        ],
        "description": "select pages by wildcards"
    },
    "pageproperties":  {
        "querylines": [
        ],
        "description": "select pages by page properties"
    },
    "pagetags":  {
        "querylines": [
            "not_page_is_journal"
        ],
        "description": "select pages by tag"
    },
    "tasks": {
        "querylines":  [
            'marker',
        ],
        "description": "select blocks that have tasks present"
    },
    "scheduled": {
        "querylines":  [
            "scheduled"
        ],
        "description": "select blocks that are scheduled"
    },
    "scheduledbetween": {
        "querylines":  [
            "scheduled",
            "scheduledfrom",
            "scheduledto",
            "daterange"
        ],
        "description": "select blocks that are scheduled in a date range"
    },
    "collapse": {
        "querylines":  [
            "collapse_true"
        ],
        "description": "collapse found blocks"
    },
    "expand": {
        "querylines":  [
            "collapse_false"
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
