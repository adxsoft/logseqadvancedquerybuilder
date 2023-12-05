// logseq-advanced-query-builder v0.1
// set mode of execution at end of this script
// 'local' mode for desktop testing with Jest Test framework
// 'logseq-plugin' for operating as a plugin within logseq

// Deployment 
// copy index.js to deploy folder
// do not copy package.json to deploy folder as the main package.json
//   is configure for jest testing

// Dictionary of query lines data 
var querylineDict = {
    'common-querylines': {
        'start':
        {
            'name': 'start',
            'useincommands': ['common'],
            'segment': 'start',
            'datalog': '#+BEGIN_QUERY',
            'comment': ''
        },
        'open':
        {
            'name': 'open',
            'useincommands': ['common'],
            'segment': 'open',
            'datalog': '{',
            'comment': ''
        },
        'title':
        {
            'name': 'title',
            'useincommands': ['common'],
            'segment': 'title',
            'datalog': ':title [:b "$$ARG1"]',
            'comment': ''
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
            'useincommands': ['common'],
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
        'pagelinks_are':
        {
            'name': 'pagelinks_are',
            'useincommands': ['common'],
            'segment': 'filters',
            'datalog': '[?block :block/path-refs [:block/name "$$ARG1"]]',
            'comment': 'Select block if it has one or more links to other pages'
        },
        'not_pagelinks_are':
        {
            'name': 'not_pagelinks_are',
            'useincommands': ['common'],
            'segment': 'filters',
            'datalog': '(not [?block :block/path-refs [:block/name "$$ARG1"]])',
            'comment': 'Exclude block if it has one or more links to other pages'
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
            'comment': ''
        },
        'closequery':
        {
            'name': 'closequery',
            'useincommands': ['common'],
            'segment': 'closequery',
            'datalog': '}',
            'comment': ''
        },
        'end':
        {
            'name': 'end',
            'useincommands': ['common'],
            'segment': 'end',
            'datalog': '#+END_QUERY',
            'comment': ''
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

// Dictionary of query builder commands
var commandsDict = {
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
        "querylines": [
        ],
        "description": "select blocks by property values"
    },
    "blocktags": {
        "querylines": [
        ],
        "description": "select blocks by tag"
    },
    "deadline": {
        "querylines": [
            "deadline"
        ],
        "description": "select blocks that have a deadline"
    },
    "deadlinebetween": {
        "querylines": [
            "deadline",
            "deadlinefrom",
            "deadlineto",
            "daterange"
        ],
        "description": "select blocks that have a deadline in a date range"
    },
    "journalsbetween": {
        "querylines": [
            "journal_date",
            "journalfrom",
            "journalto",
            "daterange"
        ],
        "description": "only select journal pages in a date range"
    },
    "journalonly": {
        "querylines": [
            "page_is_journal"
        ],
        "description": "only select journal pages"
    },
    "namespace": {
        "querylines": [
        ],
        "description": "select pages or blocks within a namespace"
    },
    "pages": {
        "querylines": [
            "findblocks",
            "where",
            "pagename",
        ],
        "description": "select pages by wildcards"
    },
    "pageproperties": {
        "querylines": [
        ],
        "description": "select pages by page properties"
    },
    "pagetags": {
        "querylines": [
            "not_page_is_journal"
        ],
        "description": "select pages by tag"
    },
    "pagelinks": {
        "querylines": [
        ],
        "description": "select any blocks that has links to pages"
    },
    "tasks": {
        "querylines": [
            'marker',
        ],
        "description": "select blocks that have tasks present"
    },
    "scheduled": {
        "querylines": [
            "scheduled"
        ],
        "description": "select blocks that are scheduled"
    },
    "scheduledbetween": {
        "querylines": [
            "scheduled",
            "scheduledfrom",
            "scheduledto",
            "daterange"
        ],
        "description": "select blocks that are scheduled in a date range"
    },
    "collapse": {
        "querylines": [
            "collapse_true"
        ],
        "description": "collapse found blocks"
    },
    "expand": {
        "querylines": [
            "collapse_false"
        ],
        "description": "expand found blocks"
    },
    "showbreadcrumb": {
        "querylines": [
            "breadcrumb_show_true"
        ],
        "description": "show breadcrumb for found blocks"
    },
    "hidebreadcrumb": {
        "querylines": [
            "breadcrumb_show_false"
        ],
        "description": "hide breadcrumb for found blocks"
    },
}

// Local tests cases for automated test suite
var QueryTestCases = [

    //    test 1
    `title: pages command - select all pages
- pages
    - *
#+BEGIN_QUERY
{
:title [:b "pages command - select all pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
`,

    //    test 2
    `title: pages command - specific pages
- pages
    - testpage001
    - testpage002
#+BEGIN_QUERY
{
:title [:b "pages command - specific pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[?block :block/name "testpage001"]
[?block :block/name "testpage002"]
)
]
}
#+END_QUERY
`,

    //    test 3
    `title: pages command - pages by wildcards
- pages
    - testpage00*
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
`,

    //    test 4
    `title: pages command - pages by wildcards
- pages
    - *002
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "002")]
]
}
#+END_QUERY
`,

    //    test 5
    `title: pages command - pages by wildcards
- pages
    - *page00*
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/includes? ?pagename "page00")]
]
}
#+END_QUERY
`,

    //    test 6
    `title: pages command - ignore pages (including wildcards)
- pages
    - not testpage*
    - not Queries*
#+BEGIN_QUERY
{
:title [:b "pages command - ignore pages (including wildcards)"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(not [(clojure.string/starts-with? ?pagename "testpage")])
(not [(clojure.string/starts-with? ?pagename "Queries")])
]
}
#+END_QUERY
`,

    //    test 7
    `title: blocks command - ignore blocks using wildcards
- blocks
    - not And sir dare view*
    - not *here leave merit enjoy forth.
    - not *roof gutters*
#+BEGIN_QUERY
{
:title [:b "blocks command - ignore blocks using wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(not [(clojure.string/ends-with? ?blockcontent "And sir dare view")])
(not [(clojure.string/starts-with? ?blockcontent "here leave merit enjoy forth.")])
(not [(clojure.string/includes? ?blockcontent "roof gutters")])
]
}
#+END_QUERY
`,

    //    test 8
    `title: blocktags - select and exclude block level tags
- blocks
    - *
- blocktags
    - tagA
    - tagD
    - not tagB
#+BEGIN_QUERY
{
:title [:b "blocktags - select and exclude block level tags"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "taga")
(page-ref ?block "tagd")
)
(not (page-ref ?block "tagb"))
]
}
#+END_QUERY
`,
    `title: blocktags and pages don't mix
- pages
    - testpage00*
- blocktags
    - tagA
    - not tagB
#+BEGIN_QUERY

;; **ERROR: blocktags not valid with pages command use blocks command instead

{
:title [:b "blocktags and pages don't mix"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
`,

    //    test 10
    `title: pagetags - page level tags
- pages
    - testpage*
- pagetags
    - classA
#+BEGIN_QUERY
{
:title [:b "pagetags - page level tags"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage")]
[?block :block/journal? false]
(page-tags ?block #{"classa"})
]
}
#+END_QUERY
`,

    //    test 11
    `title: pagetags and pages
- pages
    - *dynamics*
- pagetags
    - classB
#+BEGIN_QUERY
{
:title [:b "pagetags and pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/includes? ?pagename "dynamics")]
[?block :block/journal? false]
(page-tags ?block #{"classb"})
]
}
#+END_QUERY
`,

    //    test 12
    `title: select and exclude task types
- tasks
    - TODO
    - not DOING
#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "select and exclude task types"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/marker ?marker]
[(contains? #{"TODO"} ?marker)]
(not [(contains? #{"DOING"} ?marker)])
]
}
#+END_QUERY
`,

    `title: select and exclude task types
- pages
    - testpage00*
- tasks
    - TODO
    - not DOING
#+BEGIN_QUERY

;; **ERROR: tasks not valid with pages command use blocks command instead

{
:title [:b "select and exclude task types"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
`,

    //    test 14
    `title: select and exclude pages with page properties
- pages
    - *
- pageproperties
    - pagetype, "p-major"
    - pagetype, "p-minor"
    - not pagetype, "p-advanced"
#+BEGIN_QUERY
{
:title [:b "select and exclude pages with page properties"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagetype "p-major")
(page-property ?block :pagetype "p-minor")
)
(not (page-property ?block :pagetype "p-advanced"))
]
}
#+END_QUERY
`,

    //    test 15
    `title: select and exclude blocks with block properties
- blocks
    - *
- blockproperties
    - category, "b-thriller"
    - category, "b-western"
    - grade, "b-fiction"
#+BEGIN_QUERY
{
:title [:b "select and exclude blocks with block properties"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :category "b-thriller")
(property ?block :category "b-western")
(property ?block :grade "b-fiction")
)
]
}
#+END_QUERY
`,

    //    test 16
    `title: only search pages in specific namespace
- pages
    - *
- namespace
    - physics
#+BEGIN_QUERY
{
:title [:b "only search pages in specific namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(namespace ?block "physics")
]
}
#+END_QUERY
`,

    //    test 17
    `title: find block properties in a namespace
- blocks
    - *
- namespace
    - tech/python
- blockproperties
    - grade, "b-fiction"
#+BEGIN_QUERY
{
:title [:b "find block properties in a namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "tech/python")
(property ?block :grade "b-fiction")
]
}
#+END_QUERY
`,

    //    test 18
    `title: find scheduled blocks in a namespace
- blocks
    - *
- namespace
    - physics
- scheduled
#+BEGIN_QUERY
{
:title [:b "find scheduled blocks in a namespace"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "physics")
[?block :block/scheduled ?scheduleddate]
]
}
#+END_QUERY
`,

    //    test 19
    `title: scheduled - find scheduled blocks in a date range
- blocks
    - *
- scheduledbetween
    - :720d-before :700d-after
#+BEGIN_QUERY
{
:title [:b "scheduled - find scheduled blocks in a date range"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/scheduled ?scheduleddate]
[(>= ?scheduleddate ?startdate)]
[(<= ?scheduleddate ?enddate)]
]
:inputs [:720d-before :700d-after]
}
#+END_QUERY
`,

    //    test 20
    `title: find blocks with deadlines
- blocks
    - *
- deadline
#+BEGIN_QUERY
{
:title [:b "find blocks with deadlines"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/deadline ?deadlinedate]
]
}
#+END_QUERY
`,

    //    test 21
    `title: find blocks with deadlines in a date range
- blocks
    - *
- deadlinebetween
    - :120d-before :30d-after
#+BEGIN_QUERY
{
:title [:b "find blocks with deadlines in a date range"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/deadline ?deadlinedate]
[(>= ?deadlinedate ?startdate)]
[(<= ?deadlinedate ?enddate)]
]
:inputs [:120d-before :30d-after]
}
#+END_QUERY
`,

    //    test 22
    `title: find journals
- pages
    - *
- journalonly
#+BEGIN_QUERY
{
:title [:b "find journals"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? true]
]
}
#+END_QUERY
`,

    //    test 23
    `title: find journal in a date range
- pages
    - *
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
{
:title [:b "find journal in a date range"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/name ?pagename]
[?block :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
`,

    //    test 24
    `title: find journals between dates
- blocks
    - *
- journalsbetween
    - :30d-before :today
#+BEGIN_QUERY
{
:title [:b "find journals between dates"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:30d-before :today]
}
#+END_QUERY
`,

    //    test 25
    `title: collapse results
- pages
    - testpage00*
- collapse
#+BEGIN_QUERY
{
:title [:b "collapse results"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:collapsed? true
}
#+END_QUERY
`,

    //    test 26
    `title: expand results
- pages
    - testpage00*
- expand
#+BEGIN_QUERY
{
:title [:b "expand results"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:collapsed? false
}
#+END_QUERY
`,

    //    test 27
    `title: show breadcrumbs
- pages
    - testpage00*
- showbreadcrumb
#+BEGIN_QUERY
{
:title [:b "show breadcrumbs"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:breadcrumb-show? true
}
#+END_QUERY
`,

    //    test 28
    `title: hide breadcrumbs
- pages
    - testpage00*
- hidebreadcrumb
#+BEGIN_QUERY
{
:title [:b "hide breadcrumbs"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
:breadcrumb-show? false
}
#+END_QUERY
`,

    //    test 29
    `title: find journal in a date range using blocks
- blocks
    - *
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
{
:title [:b "find journal in a date range using blocks"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
`,
    //    test 30
    `title: All blocks - test access to parent pages tags, journal
- blocks
    - *
- tasks
    - TODO
- pagetags
    - classC
#+BEGIN_QUERY
{
:title [:b "All blocks - test access to parent pages tags, journal"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/marker ?marker]
[(contains? #{"TODO"} ?marker)]
[?page :block/journal? false]
(page-tags ?page #{"classc"})
]
}
#+END_QUERY
`,
    //    test 31
    `title: Pages only - Access page properties
- pages
    - *
- pageproperties
    - pagetype, "p-minor"
#+BEGIN_QUERY
{
:title [:b "Pages only - Access page properties"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(page-property ?block :pagetype "p-minor")
]
}
#+END_QUERY
`,
    //    test 32
    `title: Pages only - access multiple property values
- pages
    - *
- pageproperties
    - pagetype, "p-minor"
    - pagetype, "p-major"
#+BEGIN_QUERY
{
:title [:b "Pages only - access multiple property values"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagetype "p-minor")
(page-property ?block :pagetype "p-major")
)
]
}
#+END_QUERY
`,
    //    test 33
    `title: Page blocks only - pagetags
- pages
    - *
- pagetags
    - classC
#+BEGIN_QUERY
{
:title [:b "Page blocks only - pagetags"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? false]
(page-tags ?block #{"classc"})
]
}
#+END_QUERY
`,
    //    test 34
    `title: Pages only - select all pages
- pages
    - *
#+BEGIN_QUERY
{
:title [:b "Pages only - select all pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
`,
    //    test 35
    `title: pages command - specific pages
- pages
    - testpage001
    - testpage002
#+BEGIN_QUERY
{
:title [:b "pages command - specific pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[?block :block/name "testpage001"]
[?block :block/name "testpage002"]
)
]
}
#+END_QUERY
`,
    //    test 36
    `title: pages command - pages by wildcards
- pages
    - testpage00*
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage00")]
]
}
#+END_QUERY
`,
    //    test 37
    `title: pages command - pages by wildcards
- pages
    - *002
#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "002")]
]
}
#+END_QUERY
`,
    //    test 38
    `title: journalsbetween defaulting to blocks retrieval
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "journalsbetween defaulting to blocks retrieval"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
`,
    //    test 39
    `title: journalsbetween using pages retrieval
- pages
    - *
- journalsbetween
    - :today :30d-after
#+BEGIN_QUERY
{
:title [:b "journalsbetween using pages retrieval"]
:query [:find (pull ?block [*])
:in $ ?startdate ?enddate
:where
[?block :block/name ?pagename]
[?block :block/journal-day ?journaldate]
[(>= ?journaldate ?startdate)]
[(<= ?journaldate ?enddate)]
]
:inputs [:today :30d-after]
}
#+END_QUERY
`,
    //    test 40
    `title: page property combinations using and and or
- pages
    - *
- pageproperties
    - pagecategory, "p-minor"
    - or pagecategory, "p-minimum"
    - and pagetype, "p-type1"
#+BEGIN_QUERY
{
:title [:b "page property combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagecategory "p-minor")
(page-property ?block :pagecategory "p-minimum")
)
(page-property ?block :pagetype "p-type1")
]
}
#+END_QUERY
`,
    //    test 41
    `title: page tag combinations using and and or
- pages
    - *
- pagetags
    - classA
    - or classB
    - and classH
#+BEGIN_QUERY
{
:title [:b "page tag combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? false]
( or 
(page-tags ?block #{"classa"})
(page-tags ?block #{"classb"})
)
(page-tags ?block #{"classh"})
]
}
#+END_QUERY
`,
    //    test 42
    `title: block property combinations using and and or
- blocks
    - *
- blockproperties
    - category, "b-fiction"
    - or grade, "b-western"
    - and category, "b-travel"
#+BEGIN_QUERY
{
:title [:b "block property combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :category "b-fiction")
(property ?block :grade "b-western")
)
(property ?block :category "b-travel")
]
}
#+END_QUERY
`,
    //    test 43
    `title: block tag combinations using and and or
- blocks
    - *
- blocktags
    - tagA
    - or tagB
    - and tagD
#+BEGIN_QUERY
{
:title [:b "block tag combinations using and and or"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "taga")
(page-ref ?block "tagb")
)
(page-ref ?block "tagd")
]
}
#+END_QUERY
`,
    //    test 44
    `title: task and or combintions
- blocks
    - *
- tasks
    - TODO
    - and WAITING
    - or LATER
    - not DOING
#+BEGIN_QUERY
{
:title [:b "task and or combintions"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?block :block/marker ?marker]
( or 
[(contains? #{"TODO"} ?marker)]
[(contains? #{"LATER"} ?marker)]
)
[(contains? #{"WAITING"} ?marker)]
(not [(contains? #{"DOING"} ?marker)])
]
}
#+END_QUERY
`,
    //    test 45
    `title: select blocks with links to pages
- blocks
    - *
- pagelinks
    - gardening
    - vegetables
    - not turnips
#+BEGIN_QUERY
{
:title [:b "select blocks with links to pages"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[?block :block/path-refs [:block/name "gardening"]]
[?block :block/path-refs [:block/name "vegetables"]]
)
(not [?block :block/path-refs [:block/name "turnips"]])
]
}
#+END_QUERY
`,
    //    test 46
    `title: select blocks with links to journals
- blocks
    - *
- pagelinks
    - Dec 25th, 2022
    - Jan 1st, 2019
#+BEGIN_QUERY
{
:title [:b "select blocks with links to journals"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[?block :block/path-refs [:block/name "dec 25th, 2022"]]
[?block :block/path-refs [:block/name "jan 1st, 2019"]]
)
]
}
#+END_QUERY
`

]

function test_queryDBRead(section, key) {
    try {
        read1 = querylineDict[section][key]['name']
        read2 = querylineDict[section][key]['segment']
        read3 = querylineDict[section][key]['segment']
        read4 = querylineDict[section][key]['datalog']
        read5 = querylineDict[section][key]['comment']
        // return read1
        return read1 + '\n' + read2 + '\n' + read3 + '\n' + read4 + '\n' + read5 + '\n'

    } catch {
        return "Failed"
    }
}




function add(num1, num2) {
    return num1 + num2
}


// ========= global variables

// ---query structure
var query_template = {
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

var codeblock = false
var mode = "javascript"
query = query_template
querygroup = "pages-querylines"
querylineDBDict = {}
showcommandcomments = false

// =========== FUNCTIONS ================

function initialiseQuery() {
    query = query_template;
    for (key of Object.keys(query)) {
        query[key] = []
    }
    return query;
}

function initialisteQueryLineDict() {
    var tempDict;
    tempDict = {};
    tempDict["pages-querylines"] = querylineDict["pages-querylines"];
    tempDict["blocks-querylines"] = querylineDict["blocks-querylines"];

    for (const [commonqueryline, value] of Object.entries(querylineDict['common-querylines'])) {
        tempDict["pages-querylines"][commonqueryline] = querylineDict["common-querylines"][commonqueryline];
        tempDict["blocks-querylines"][commonqueryline] = querylineDict["common-querylines"][commonqueryline];
    }
    return tempDict;
}



function getQueryLineSegment(querylinekey) {
    var errormsg, errortext;

    try {
        return ["ok", querylineDBDict[querygroup][querylinekey]["segment"]];
    } catch (e) {
        errortext = querylinekey + " segment value not found in QueryDB\n";
        errormsg = ";; **ERROR: " + errortext + "\n";
        return ["error", errormsg];
    }
}


function getQueryLine(querylinekey, querysegment) {
    var errormsg;

    try {
        if (showcommandcomments === true) {
            var comment = getQueryLineComment(querylinekey)
            if (comment != '') {
                if (!query[querysegment].includes('\n' + comment)) {
                    query[querysegment].push("\n" + getQueryLineComment(querylinekey));
                }
            }
        }

        return querylineDBDict[querygroup][querylinekey]["datalog"];
    } catch (e) {
        errormsg = "\n---- COMMAND ERROR ----\n";
        errormsg += querylinekey + " not found in QueryDB or invalid usage\n";

        if (querygroup === "pages-querylines") {
            errormsg += querylinekey + " invalid within a 'pages' command query";
        }

        if (querygroup === "blocks-querylines") {
            errormsg += querylinekey + " invalid within a 'blocks' command query";
        }

        errormsg += "\n----------------------\n";
        return errormsg;
    }
}

function getQueryLineComment(querylinekey) {
    var comment, separator;
    separator = ''
    try {
        comment = querylineDBDict[querygroup][querylinekey]["comment"];
        if (comment == '') {
            return ''
        }
        return separator + ";; ---- " + comment;
    } catch (e) {
        return querylinekey + " not found in queryline Dictionary";
    }
}

function getCommandQueryLineKeys(command) {
    var commandlist;

    if (command === null) {
        return null;
    }

    try {
        commandlist = commandsDict[command]["querylines"];
    } catch (e) {
        return null;
    }

    return commandlist;
}


function processCommand(command, commandLinesDict) {
    var commandline, commandvalidity, negativecommandlines, originalcommandlines, positivecommandlines, queryline, querylinekeys, querysegment, querysegmentdata, querysegmentresponse;
    commandvalidity = checkCommandValid(command);

    if (commandvalidity[0] === false) {
        query["errors"].push(commandvalidity[1]);
        return;
    }

    querylinekeys = getCommandQueryLineKeys(command);

    if (querylinekeys === null) {
        return [command + " is not a valid command"];
    }

    for (value of querylinekeys) {
        querysegmentresponse = getQueryLineSegment(value);

        querysegmentdata = querysegmentresponse[1];

        if (querysegmentresponse[0] === "error") {
            query["errors"].push(querysegmentdata);
            continue;
        }

        querysegment = querysegmentdata;
        queryline = getQueryLine(value, querysegment);

        if (query[querysegment].includes(queryline)) {
            continue;
        }

        query[querysegment].push(queryline);
    }

    // sort the argument lines by positive and negative
    positivecommandlines = [];
    negativecommandlines = [];
    originalcommandlines = commandLinesDict[command]["commandlines"].slice(1);


    for (commandline of originalcommandlines) {
        if (commandline.trim().substring(2).startsWith("not ") || commandline.trim().substring(2).startsWith("and ")) {
            commandline = commandline.replace("and ", "");
            negativecommandlines.push(commandline);
        } else {
            if (commandline.trim().substring(2).startsWith("or ")) {
                commandline = commandline.replace("or ", "");
                positivecommandlines.push(commandline);
            } else {
                positivecommandlines.push(commandline);
            }
        }
    }

    if (positivecommandlines.length > 0) {
        processCommandLines("include", command, positivecommandlines);
    }

    if (negativecommandlines.length > 0) {
        processCommandLines("exclude", command, negativecommandlines);
    }

    return;
}

function checkCommandValid(command) {
    var commandvalidity, errormessage;
    commandvalidity = true;
    errormessage = "";

    if (querygroup === "pages-querylines") {
        if (command === "blocktags") {
            commandvalidity = false;
            errormessage = "\n;; **ERROR: " + command + " not valid with pages command use blocks command instead\n";
        } else {
            if (command === "tasks" || command === "pagelinks") {
                commandvalidity = false;
                errormessage = "\n;; **ERROR: " + command + " not valid with pages command use blocks command instead\n";
            }
        }
    } else {
        if (querygroup === "blocks-querylines") {
            if ([].includes(command)) {
                commandvalidity = false;
            }
        }
    }

    return [commandvalidity, errormessage];
}

function addQueryLines(command, prefix, querylinekey, arg) {
    var arg1, arg2, args, querysegment, querysegmentdata, querysegmentresponse, updatedqueryline;
    querysegment = getQueryLineSegment(querylinekey);
    querysegmentresponse = getQueryLineSegment(querylinekey)[0];
    querysegmentdata = getQueryLineSegment(querylinekey)[1];

    if (querysegmentresponse === "error") {
        query["errors"].push(querysegmentdata);
        return;
    }

    querysegment = querysegmentdata;
    if (command == 'pagelinks') {
        args = []
        args.push(arg)
    } else {
        args = arg.split(",");
    }

    if (args.length === 1) {
        querylinekey = prefix + querylinekey;
        updatedqueryline = getQueryLine(querylinekey, querysegment).replace("$$ARG1", arg);

        if (!query[querysegment].includes(updatedqueryline)) {
            query[querysegment].push(updatedqueryline);
        }
    } else {
        if (args.length === 2) {
            arg1 = args[0].trim();
            arg2 = args[1].trim();
            querylinekey = prefix + querylinekey;
            updatedqueryline = getQueryLine(querylinekey, querysegment).replace("$$ARG1", arg1);
            updatedqueryline = updatedqueryline.replace("$$ARG2", arg2);

            if (!query[querysegment].includes(updatedqueryline)) {
                query[querysegment].push(updatedqueryline);
            }
        } else {
            query[querysegment].push(command + " => Invalid line => " + arg);
        }
    }
}

function processCommandLines(action, command, commandlines) {
    var arg, args, firstline, lastline, prefix;

    if (commandlines === []) {
        return;
    }

    firstline = "";
    lastline = "";

    if (["pages", "blocks", "blocktags", "pagetags", "pagelinks", "tasks", "pageproperties", "blockproperties", "namespace"].includes(command)) {
        if (commandlines.length > 1) {
            if (action === "include") {
                firstline = "( or ";
                lastline = ")";
            }
        }
    }

    if (firstline !== "") {
        query["filters"].push(firstline);
    }

    for (arg of commandlines) {
        arg = arg.trim().substring(2);

        if (arg === "") {
            continue;
        }

        if (arg === "*") {
            continue;
        }

        prefix = "";

        if (arg.startsWith("not ")) {
            prefix = "not_";
            arg = arg.substring(prefix.length);
        }

        if (command === "pages") {
            if (arg[0] !== "*" && arg[arg.length - 1] === "*") {
                addQueryLines(command, prefix, "arg_pagename_startswith", arg.substring(0, arg.length - 1));
                continue;
            }

            if (arg[0] === "*" && arg[arg.length - 1] !== "*") {
                addQueryLines(command, prefix, "arg_pagename_endswith", arg.substring(1));
                continue;
            }

            if (arg[0] === "*" && arg[arg.length - 1] === "*") {
                addQueryLines(command, prefix, "arg_pagename_contains", arg.substring(1, arg.length - 1));
                continue;
            }

            addQueryLines(command, prefix, "pagename_is", arg);
        }

        if (command === "blocks") {
            if (arg[0] !== "*" && arg[arg.length - 1] === "*") {
                addQueryLines(command, prefix, "arg_blockcontent_startswith", arg.substring(0, arg.length - 1));
                continue;
            }

            if (arg[0] === "*" && arg[arg.length - 1] !== "*") {
                addQueryLines(command, prefix, "arg_blockcontent_endswith", arg.substring(1));
                continue;
            }

            if (arg[0] === "*" && arg[arg.length - 1] === "*") {
                addQueryLines(command, prefix, "arg_blockcontent_contains", arg.substring(1, arg.length - 1));
                continue;
            }
        }

        if (command === "pagetags") {
            args = arg.split();

            for (arg of args) {
                addQueryLines(command, prefix, "pagetags_are", arg.toLowerCase());
            }
        }

        if (command === "blocktags") {
            args = arg.split();

            for (arg of args) {
                addQueryLines(command, prefix, "blocktags_are", arg.toLowerCase());
            }
        }

        if (command === "pageproperties") {
            addQueryLines(command, prefix, "page_properties_are", arg);
        }

        if (command === "blockproperties") {
            addQueryLines(command, prefix, "block_properties_are", arg);
        }

        if (command === "pagelinks") {
            args = arg.split();

            for (arg of args) {
                addQueryLines(command, prefix, "pagelinks_are", arg.toLowerCase());
            }
        }
        if (command === "tasks") {
            addQueryLines(command, prefix, "tasks_are", arg);
        }

        if (command === "namespace") {
            addQueryLines(command, prefix, "namespace", arg);
        }

        if (command === "scheduled") {
            addQueryLines(command, prefix, "scheduled", arg);
        }

        if (command === "scheduledbetween") {
            addQueryLines(command, prefix, "scheduledbetween", arg);
        }

        if (command === "deadline") {
            addQueryLines(command, prefix, "deadline", arg);
        }

        if (command === "deadlinebetween") {
            addQueryLines(command, prefix, "deadlinebetween", arg);
        }

        if (command === "journalonly") {
            addQueryLines(command, prefix, "page_is_journal", arg);
        }

        if (command === "journalsbetween") {
            addQueryLines(command, prefix, "journalsbetween", arg);
        }

        if (command === "daterange") {
            addQueryLines(command, prefix, "daterange", arg);
        }

        if (command === "collapse") {
            addQueryLines(command, prefix, "collapse", arg);
        }

        if (command === "collapse") {
            addQueryLines(command, prefix, "expand", arg);
        }
    }

    if (lastline !== "") {
        query["filters"].push(lastline);
    }

    return;
}

function insertQueryLineIntoSegment(key) {
    var querysegment, querysegmentdata, querysegmentresponse;
    querysegmentresponse = getQueryLineSegment(key)[0];
    querysegmentdata = getQueryLineSegment(key)[1];

    if (querysegmentresponse === "error") {
        query["errors"].push(querysegmentdata);
        return;
    }

    querysegment = querysegmentdata;
    query[key].push(getQueryLine(key, querysegment));
}

function checkUsingPagesorBlocks(commandlines) {
    var blocksfound, commandline, pagesfound
    pagesfound = false;
    blocksfound = false;

    for (commandline of commandlines) {

        commandline = commandline.trim();

        if (commandline.startsWith("- pages")) {
            pagesfound = true;
        }

        if (commandline.startsWith("- blocks")) {
            blocksfound = true;
        }
    }

    if (pagesfound === true && blocksfound === false) {
        querygroup = "pages-querylines";
        return;
    }

    if (blocksfound === true && pagesfound === false) {
        querygroup = "blocks-querylines";
        return;
    }

    if (pagesfound === false && blocksfound === false) {
        query["errors"].push(";; WARNING: Must have 'pages' command or 'blocks' Command\n;;          otherwise the query cannot get any information\n;;          Inserting a blocks command for you\n");
        insertBlocksCommand(commandlines);
        blocksfound = true;
        querygroup = "blocks-querylines";
        return;
    }

    if (pagesfound && blocksfound) {
        query["errors"].push(";; ERROR: Cannot have 'pages' command and 'blocks' command together in a command list\n\n");
        return;
    }
}

function insertBlocksCommand(commandlines) {
    if (commandlines.length > 0) {
        if (commandlines[0].indexOf("title:") > -1) {
            commandlines.splice(1, 0, "    - *");
            commandlines.splice(1, 0, "- blocks");
        }
    } else {
        commandlines.splice(0, 0, "- blocks\n    - *\n");
    }
    return;
}

function validCommand(command) {
    try {
        if (commandsDict[command]) {
            return true;
        } else {
            return false
        }
    } catch (e) {
        return false;
    }
}

function processCommandList(commandlists) {
    var commandLinesDict, commandlines, commandname, currentcommand, fields, query;
    query = initialiseQuery();
    commandlines = commandlists.split("\n");
    checkUsingPagesorBlocks(commandlines);
    currentcommand = "";
    commandLinesDict = {};

    for (line of commandlines) {

        if (line === "" || line.startsWith(";;")) {
            continue;
        }

        if (line.trim().startsWith("title:")) {
            query["title"].push(getQueryLine("title", "title").replace("$$ARG1", line.split(":")[1].trim()));
            continue;
        }

        if (line.trim().startsWith("option:")) {
            var option = line.split(":")[1].trim()
            if (option == "includecomments") {
                setshowcommandcomments(true)
            } else {
                query['errors'].push(
                    ";; WARNING: '" + line + "' is not valid option. \n;;           Valid options: includecomments")
            }
            continue;
        }

        if (line.startsWith("- ")) {
            fields = line.split(" ");
            commandname = fields[1];

            if (validCommand(commandname)) {
                commandLinesDict[commandname] = {};

                if (currentcommand === "" || line !== currentcommand) {
                    currentcommand = commandname;
                    commandLinesDict[commandname]["commandlines"] = [];
                    commandLinesDict[commandname]["commandlines"].push(line);
                    continue;
                }
            } else {
                query["errors"].push(";; WARNING: '" + line + "' is not valid command.\n;;          Either a mispelt command or no leading dash");
                // continue;
            }
        } else {
            if (line.startsWith(" ") && line.trim().startsWith("- ")) {
                if (currentcommand === "") {
                    query["errors"].push(";; ERROR: '" + line + "' is a command argument but does not have a parent command\n;;       Either a command is missing (or invalid) or this should be an argument line");
                } else {
                    if (validCommand(commandname)) {
                        commandLinesDict[commandname]["commandlines"].push(line);
                    } else {
                        query["errors"].push(";; ERROR: '" + line + "' is a command argument but does not have a parent command\n;;       Either a command is missing (or invalid) or this should be an argument line");
                    }
                }
            } else {
                if (line.includes("title ")) {
                    query["errors"].push(";; WARNING: title line should start with title:");
                } else {
                    if (!line.trim().startsWith("- ") && !(line.indexOf("title:") > -1)) {
                        query["errors"].push(";; WARNING: " + line + " has no leading hypen eg '- pages'");
                    }
                }
            }
        }
    }

    insertQueryLineIntoSegment("start");
    insertQueryLineIntoSegment("open");
    insertQueryLineIntoSegment("where");
    insertQueryLineIntoSegment("closefind");
    insertQueryLineIntoSegment("closequery");
    insertQueryLineIntoSegment("end");

    for (command in commandLinesDict) {
        processCommand(command, commandLinesDict);
    }

    query["closefind"] = [getQueryLine("closefind", "closefind")];
    query["closequery"] = [getQueryLine("closequery", "closequery")];
    query["end"] = [getQueryLine("end", "end")];
    return;
}


function constructQuery() {
    var advancedquery;
    advancedquery = "";

    for (const [key, value] of Object.entries(query)) {
        for (let j = 0; j < query[key].length; j++) {
            queryline = query[key][j]
            advancedquery += queryline + "\n";
        }
    }
    return advancedquery;
}

function printGeneratedAdvancedQuery(advancedquery) {
    var msg, prefix, suffix;

    if (codeblock) {
        prefix = "```clojure\n";
        suffix = "```";
    } else {
        prefix = "";
        suffix = "";
    }

    if (mode === "website") {
        // msg = prefix + advancedquery.replace("\n", "<BR>") + suffix;
        msg = prefix + advancedquery + suffix;
        websitePrintToDiv('advanced_query', msg)
    } else {
        console.log("----------------------------");
        console.log("Logseq Advanced Query");
        console.log("----------------------------");
        console.log(prefix + advancedquery + suffix);
    }
}


// global value functions
function getquerygroup() {
    return querygroup
}

function setquerygroup(value) {
    querygroup = value
}

function getshowcommandcomments() {
    return showcommandcomments
}

function setshowcommandcomments(value) {
    showcommandcomments = value
}

function getcodeblock() {
    return codeblock
}

function setcodeblock(value) {
    codeblock = value
}

function getquerylineDBDict() {
    return querylineDBDict
}

function setquerylineDBDict(value) {
    querylineDBDict = value
}

// Test queryTestDB works
function test_queryTestDBRead() {
    testcases = QueryTestCases
    return testcases[0];
}

function getquerytestcases() {
    return QueryTestCases
}

function removeLastGeneratedQuery(content) {
    let lines = content.split("\n")
    let newcontent = ''
    for (const line of lines) {
        if (line.startsWith('#+BEGIN_QUERY')) {
            break
        }
        newcontent += line + '\n'
    }
    return newcontent
}

function showErrors() {
    msg = 'QB: Errors Found - check built query'
    if (query["errors"].length > 0) {
        for (errormsg of query["errors"]) {
            msg += errormsg + '\n'
        }
        return msg
    } else {
        return "QB: Query Built OK"
    }
}


function main() {

    logseq.Editor.registerBlockContextMenuItem(
        'Advanced Query Builder',
        async (e) => {
            const block = await logseq.Editor.getBlock(e.uuid)
            content = block.content
            content = removeLastGeneratedQuery(content)
            commands = content.replaceAll(/```/g, '')
            showcommandcomments = false;
            querygroup = "blocks-querylines";
            codeblock = false;
            // query = initialiseQuery();
            // querylineDBDict = initialisteQueryLineDict();
            // querygroup = "pages-querylines"
            // logseq.App.showMsg(
            //     commands,
            // )
            setquerylineDBDict(initialisteQueryLineDict())
            console.log("\ncommands\n" + commands);
            console.log("\ncontent\n" + content);
            initialiseQuery()
            processCommandList(commands)
            advancedquery = constructQuery()

            // Currently will add a child block with the generated query
            // user can right click on the query and remove it or leave it there
            // IDEA: Maybe always remove the last query so  how do I do that
            //      remove any children blocks
            //         TODO: Returns undefined for the child uuid????? Mayne just let user insert a new child for each query execution
            //      if (block.children.length > 0) {
            //         for (let child of block.children) {
            //             await logseq.Editor.removeBlock(child.uuid);
            //         }
            //      }


            // place the advanced query in a child of the current block (that has the commands in it)
            await logseq.Editor.insertBlock(e.uuid, advancedquery, { sibling: false })

            logseq.App.showMsg(
                showErrors()
            )
        })

} // end main

// ======== website functions

function websiteInitialise() {

    if (mode != "website") {
        return
    }

    // connect the generate advanced query button
    generate_query_button = document.getElementById('generate_query_button')
    generate_query_button.addEventListener("click", websiteQueryBuild)

    // connect the Clear Commands button
    clear_commands_button = document.getElementById('clear_commands_button')
    clear_commands_button.addEventListener("click", websiteClearCommands)

    // connect the Examples button
    examples_options = document.getElementById('command_examples')
    examples_options.addEventListener("input", websiteChooseExample)
    examples_options.value = ""  // set to first option

    // connect the Command Comments Checkbox
    command_comments_checkbox = document.getElementById(
        'command_comments_checkbox')
    command_comments_checkbox.addEventListener("click", websiteCommandComments)
    command_comments_checkbox.checked = false

    commands_input = document.getElementById('commands_input')
    commands_input.value = ''

    // connect the Code Block Output Checkbox
    codeblock_checkbox = document.getElementById(
        'codeblock_checkbox')
    codeblock_checkbox.addEventListener("click", websiteCodeBlock)
    codeblock_checkbox.checked = false

}

function websiteClearCommands(event) {
    if (mode != "website") {
        return
    }

    // # hide copy to clipboard button
    websitePrintToDiv('print_output', 'Clear Commands Button Pressed')
    commands_input = document.getElementById('commands_input')
    commands_input.value = ''
}


function websiteCommandComments(event) {
    if (mode != "website") {
        return
    }
    if (document.getElementById('command_comments_checkbox').checked == true) {
        setshowcommandcomments(true)
    } else {
        setshowcommandcomments(false)
    }
}


function websiteCodeBlock(event) {
    // TODO: Check this works re global codeblock variable
    if (mode != "website") {
        return
    }
    if (document.getElementById('codeblock_checkbox').checked == true) {
        codeblock = true
    } else {
        codeblock = false
    }
}


function websiteChooseExample(event) {
    if (mode != "website") {
        return
    }
    // get selected Example and fill the commands Input Text Area
    examples_options = document.getElementById('command_examples')
    if (examples_options.value != "Choose Example..") {
        advanced_query_text = document.getElementById('advanced_query')
        advanced_query_text.textContent = ''
        websitePrintToDiv('print_output',
            "Example selected .. now press 'Generate Advanced Query' button")

        document.getElementById(
            'commands_input').value = examples_options.value
        // console.log('value is ', examples_options.value)
    }
}

function websiteAdvancedQueryText(event) {
    if (mode != "website") {
        return
    }
}

function websitePrintToDiv(divname, text) {
    if (mode != "website") {
        return
    }
    document.getElementById(divname).innerText = text
}


function websiteQueryBuild(event) {
    if (mode != "website") {
        return
    }

    //     # hide copy to clipboard button
    copy_button = document.getElementById('copy')
    copy_button.setAttribute("hidden", "hidden")

    websitePrintToDiv('print_output', 'Processing Commands ..')

    commands_input = document.getElementById('commands_input')
    if (!commands_input) {
        websitePrintToDiv('print_output', 'Bug: Element is None')
        return
    }
    processCommandList(commands_input.value)
    advancedquery = constructQuery()
    printGeneratedAdvancedQuery(advancedquery)

    // show copy to clipboard button
    var copy_button = document.getElementById('copy')
    hidden = copy_button.getAttribute("hidden")
    copy_button.removeAttribute("hidden")

    websitePrintToDiv('print_output',
        "Advanced Query Generated!\n- Tick 'Include Query Comments' if desired\n- Tick 'Copy as code block' if desired\nClick 'Copy Query to Clipboard")

    return
}



// MAIN ENTRY POINT

// *******************************
// LOCAL MODE TESTING WITH JEST TESTING
// (Comment out WEBSITE MODE section below and PLUGIN MODE section above)
// (Uncomment this section for local testing with JEST)
// *******************************
// // var mode = "local"
// module.exports = {
//     //querygroup,
//     //showcommandcomments,
//     getquerygroup,
//     setquerygroup,
//     getshowcommandcomments,
//     setshowcommandcomments,
//     getcodeblock,
//     setcodeblock,
//     getquerylineDBDict,
//     setquerylineDBDict,
//     getquerytestcases,
//     add,
//     test_queryDBRead,
//     test_queryTestDBRead,
//     addQueryLines,
//     checkCommandValid,
//     checkUsingPagesorBlocks,
//     constructQuery,
//     getCommandQueryLineKeys,
//     getQueryLine,
//     getQueryLineComment,
//     getQueryLineSegment,
//     initialiseQuery,
//     initialisteQueryLineDict,
//     insertBlocksCommand,
//     insertQueryLineIntoSegment,
//     printGeneratedAdvancedQuery,
//     processCommand,
//     processCommandLines,
//     processCommandList,
//     removeLastGeneratedQuery,
//     validCommand
// }
// *******************************

// *******************************
// LOGSEQ WEBSITE MODE
// (Comment out LOCAL MODE section above and PLUGIN mode section below and uncomment this section)
// *******************************
mode = "website"
// *******************************


// *******************************
// LOGSEQ PLUGIN MODE
// (Comment out LOCAL MODE section above and WEBSITE section above and uncomment this section)
// *******************************
// mode = "logseq-plugin"
// *******************************

// MAIN STARTING POINT
if (mode == "logseq-plugin") {
    console.log('logseq-advanced-query-builder plugin loaded')
    logseq.ready(main).catch(console.error)
}
if (mode == "local") {
    console.log('logseq-advanced-query-builder code running locally')
    querygroup = "";
    codeblock = false;
    query = initialiseQuery();
    querylineDBDict = initialisteQueryLineDict();
}
if (mode == "website") {
    console.log('logseq-advanced-query-builder code running in browser')
    querygroup = "";
    codeblock = false;
    query = initialiseQuery();
    querylineDBDict = initialisteQueryLineDict();
    websiteInitialise()
}


