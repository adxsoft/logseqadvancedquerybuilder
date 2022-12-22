const functions = require('./index');
const fs = require('fs');

//-------------------------------------------------------
// local functions to assist testing
//-------------------------------------------------------

function saveAutomatedTestOutput(msg) {
    fs.writeFile('testing_results.txt', msg, function (err) {
        if (err)
            return console.log(err);
        console.log('Test Results written to testing_results.txt');
    });
}

function setGlobals({
    querygroup = 'blocks-querylines',
    showcommandcomments = false,
    codeblock = false } = {}) {
    functions.setquerygroup(querygroup)
    functions.setshowcommandcomments(showcommandcomments)
    functions.setcodeblock(codeblock)
}

function resetGlobalsToDefault() {
    setGlobals({
        querygroup: 'blocks-querylines',
        showcommandcoments: false,
        codeblock: false
    })
}

function gettestcommands(testno) {
    testcases = functions.getquerytestcases()
    var testdata = testcases[testno].split("#+BEGIN")
    return testdata[0].trim()
}


function gettestexpectedresults(testno) {
    testcases = functions.getquerytestcases()
    var testdata = testcases[testno].split("#+BEGIN")
    var expectedresult = "#+BEGIN" + testdata[1]
    returnval = expectedresult
    return returnval
}


//-------------------------------------------------------
// test any old function
//-------------------------------------------------------


describe('junk tests', () => {
    test('add 2 numbers', () => {
        returnval = functions.add(1, 1)
        expect(returnval).toBe(2)
    })
}) // end describe

describe('Manual tests', () => {
    // ------------------------------------


    // ------------------------------------

    // ------------------------------------
    // ------------------------------------


    // ------------------------------------



    // ------------------------------------
    test('pages test 1', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pages command - select all pages
- pages
    - *
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pages command - select all pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('pages - test 2', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pages command - pages by wildcards
- pages
    - abc*
    - *de*
    - not 2*
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pages command - pages by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "abc")]
[(clojure.string/includes? ?pagename "de")]
)
(not [(clojure.string/starts-with? ?pagename "2")])
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })


    // ------------------------------------
    test('pages - test 3', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pages - wildcards but exclude specific page
- pages
    - testpage*
    - not testpage3
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pages - wildcards but exclude specific page"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/starts-with? ?pagename "testpage")]
(not [?block :block/name "testpage3"])
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('blocks - test 1', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blocks command - blocks by wildcards
- blocks
    - testblock*
    - *123*
    - 6*
    - not *456*
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "blocks command - blocks by wildcards"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[(clojure.string/ends-with? ?blockcontent "testblock")]
[(clojure.string/includes? ?blockcontent "123")]
[(clojure.string/ends-with? ?blockcontent "6")]
)
(not [(clojure.string/includes? ?blockcontent "456")])
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------



    // ------------------------------------


    // ------------------------------------


    // ------------------------------------
    test('blocktags - test 4', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: multiple blocks tags
- blocks
    - *
- blocktags
    - tag1
    - tag2
    - tag3
    - not tag2
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "multiple blocks tags"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "tag1")
(page-ref ?block "tag2")
(page-ref ?block "tag3")
)
(not (page-ref ?block "tag2"))
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------


    // ------------------------------------
    test('pagestags - test 2', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pagetags and pages combined - test 1
- pages
    - not age7*
- pagetags
    - pagetag1
    - pagetag2
    - not pagetag4
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pagetags and pages combined - test 1"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(not [(clojure.string/starts-with? ?pagename "age7")])
[?block :block/journal? false]
( or 
(page-tags ?block #{"pagetag1"})
(page-tags ?block #{"pagetag2"})
)
(not (page-tags ?block #{"pagetag4"}))
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        setGlobals({ showcommandcomments: false }) // reset so other tests will be unaffected
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('pagetags - test 3', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pages with multiple tags
- pages
    - *
- pagetags
    - classA
    - classB
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pages with multiple tags"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[?block :block/journal? false]
( or 
(page-tags ?block #{"classa"})
(page-tags ?block #{"classb"})
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------


    // ------------------------------------
    test('pageproperties - test 1', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pageproperties - pagetype only missing pages command
- pages
    - *
- pageproperties
    - pagetype, "testA"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype only missing pages command"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(page-property ?block :pagetype "testA")
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })


    // ------------------------------------
    test('pageproperties - test 2', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pageproperties - pagetype testA and testB
- pages
    - *
- pageproperties
    - pagetype, "testA"
    - pagetype, "testB"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype testA and testB"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
(page-property ?block :pagetype "testA")
(page-property ?block :pagetype "testB")
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('pageproperties - test 3', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pageproperties - pagetype testA not testB
- pages
    - *
- pageproperties
    - pagetype, "testA"
    - not pagetype, "testB"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "pageproperties - pagetype testA not testB"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
(page-property ?block :pagetype "testA")
(not (page-property ?block :pagetype "testB"))
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })
    // ------------------------------------

    // ------------------------------------
    test('blockproperties - pagetype only', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blockproperties - pagetype only
- blocks
    - *
- pageproperties
    - pagetype, "testA"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "blockproperties - pagetype only"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(page-property ?page :pagetype "testA")
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('blockproperties - blockprop3 b1', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blockproperties - blockprop3 b1
- blocks
    - *
- blockproperties
    - blockprop3, "b1"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "blockproperties - blockprop3 b1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(property ?block :blockprop3 "b1")
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('blockproperties - blockprop3 b1 and b2 and b3', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blockproperties - blockprop3 b1 and b2 and b3
- blocks
    - *
- blockproperties
    - blockprop3, "b1"
    - blockprop3, "b2"
    - blockprop3, "b3"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "blockproperties - blockprop3 b1 and b2 and b3"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :blockprop3 "b1")
(property ?block :blockprop3 "b2")
(property ?block :blockprop3 "b3")
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('blockproperties - blockprop3 b1 and b2 not b3', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blockproperties - blockprop3 b1 and b2 not b3
- blocks
    - *
- blockproperties
    - blockprop3, "b1"
    - blockprop3, "b2"
    - not blockprop3, "b3"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "blockproperties - blockprop3 b1 and b2 not b3"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :blockprop3 "b1")
(property ?block :blockprop3 "b2")
)
(not (property ?block :blockprop3 "b3"))
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('namespace1 block properties', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: namespace1 block properties
- blocks
    - *
- namespace
    - namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "namespace1 block properties"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "namespace1")
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('not namespace1 block properties', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: not namespace1 block properties
- blocks
    - *
- namespace
    - not namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "not namespace1 block properties"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(not (namespace ?page "namespace1"))
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('namespace1 block properties that are scheduled', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: namespace1 block properties that are scheduled
- blocks
    - *
- namespace
    - namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
    - ns1p3blocktype, "nsp3blockvalue"
- scheduled
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "namespace1 block properties that are scheduled"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "namespace1")
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
(property ?block :ns1p3blocktype "nsp3blockvalue")
)
[?block :block/scheduled ?scheduleddate]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('namespace1 block properties that have a deadline', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: namespace1 block properties that have a deadline
- blocks
    - *
- namespace
    - namespace1
- blockproperties
    - ns1p1blocktype, "nsp1blockvalue"
    - ns1p2blocktype, "nsp2blockvalue"
    - ns1p3blocktype, "nsp3blockvalue"
    - ns1p4blocktype, "nsp4blockvalue"
    - ns1p5blocktype, "nsp5blockvalue"
- deadline
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "namespace1 block properties that have a deadline"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
(namespace ?page "namespace1")
( or 
(property ?block :ns1p1blocktype "nsp1blockvalue")
(property ?block :ns1p2blocktype "nsp2blockvalue")
(property ?block :ns1p3blocktype "nsp3blockvalue")
(property ?block :ns1p4blocktype "nsp4blockvalue")
(property ?block :ns1p5blocktype "nsp5blockvalue")
)
[?block :block/deadline ?deadlinedate]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------


    // ------------------------------------
    test('deadline blocks in date range', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: deadline blocks in date range
- deadlinebetween
    - :today :30d-after
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "deadline blocks in date range"]
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
:inputs [:today :30d-after]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------


    // ------------------------------------
    test('find journals in a date range', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: find journals in a date range
- journalsbetween
    - :today :30d-after
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "find journals in a date range"]
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
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })


    // ------------------------------------
    test('collapse found blocks', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: collapse found blocks
- pages
    - *
- collapse
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "collapse found blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
:collapsed? true
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('expand found blocks', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: expand found blocks
- pages
    - *
- expand
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "expand found blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
:collapsed? false
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('show breadcrumb for found blocks', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: show breadcrumb for found blocks
- pages
    - *
- showbreadcrumb
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "show breadcrumb for found blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
:breadcrumb-show? true
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('hide breadcrumbs for found blocks', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: hide breadcrumbs for found blocks
- pages
    - *
- hidebreadcrumb
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "hide breadcrumbs for found blocks"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
:breadcrumb-show? false
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('option command - show command comments', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals({ showcommandcomments: true })
        commands = `title: select blocks with links to journals
option: includecomments
- blocks
    - *
- pagelinks
    - Dec 25th, 2022
    - Jan 1st, 2019
`
        expectedresults = `#+BEGIN_QUERY
{
:title [:b "select blocks with links to journals"]

;; ---- Get every block into variable ?block
:query [:find (pull ?block [*])

;; ---- filter command
:where

;; ---- get block content into variable ?blockcontent
[?block :block/content ?blockcontent]

;; ---- get page (special type of block) into variable ?page (used later)
[?block :block/page ?page]

;; ---- get page name (lowercase) from the page block into variable ?pagename
[?page :block/name ?pagename]
( or 

;; ---- Select block if it has one or more links to other pages
[?block :block/path-refs [:block/name "dec 25th, 2022"]]
[?block :block/path-refs [:block/name "jan 1st, 2019"]]
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        expect(advancedquery).toEqual(expectedresults)
        resetGlobalsToDefault()
    })

    test('option command - bad option parameter', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals({ showcommandcomments: true })
        commands = `title: select blocks with links to journals
option: iamabadoption
- blocks
    - *
- pagelinks
    - Dec 25th, 2022
    - Jan 1st, 2019
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: 'option: iamabadoption' is not valid option. 
;;           Valid options: includecomments
{
:title [:b \"select blocks with links to journals\"]

;; ---- Get every block into variable ?block
:query [:find (pull ?block [*])

;; ---- filter command
:where

;; ---- get block content into variable ?blockcontent
[?block :block/content ?blockcontent]

;; ---- get page (special type of block) into variable ?page (used later)
[?block :block/page ?page]

;; ---- get page name (lowercase) from the page block into variable ?pagename
[?page :block/name ?pagename]
( or 

;; ---- Select block if it has one or more links to other pages
[?block :block/path-refs [:block/name \"dec 25th, 2022\"]]
[?block :block/path-refs [:block/name \"jan 1st, 2019\"]]
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        expect(advancedquery).toEqual(expectedresults)
        resetGlobalsToDefault()
    })



}) // end manual tests


describe('Positive function Tests', () => {

    test('initialiseQuery()', () => {
        returnval = functions.initialiseQuery()
        var expectedvariable = {
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
        expect(returnval).toEqual(
            expectedvariable)
    })

    test('queryTestDBRead queryTestDB', () => {
        returnval = functions.test_queryTestDBRead()
        expect(returnval).toEqual(
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
`)
    })

    //-------------------------------------------------------
    // logseqadvancedqueryplugin function tests
    //-------------------------------------------------------


    test('checkCommandValid for querygroup pages-querylines', () => {
        setGlobals({ querygroup: "pages-querylines" })
        expect(functions.checkCommandValid("pages")).toEqual(
            [true, ""])
        expect(functions.checkCommandValid("blocktags")).toEqual(
            [false, '\n' + ';; **ERROR: blocktags not valid with pages command use blocks command instead\n'])
        expect(functions.checkCommandValid("tasks")).toEqual(
            [false, '\n' + ';; **ERROR: tasks not valid with pages command use blocks command instead\n'])
        resetGlobalsToDefault()
    })

    test('checkCommandValid for querygroup blocks-querylines', () => {
        // set global variables
        setGlobals()
        expect(functions.checkCommandValid("blocks")).toEqual(
            [true, ""])
        expect(functions.checkCommandValid("tasks")).toEqual(
            [true, ""])
        expect(functions.checkCommandValid("anyoldvalue")).toEqual(
            [true, ""])
        resetGlobalsToDefault()
    })

    test('initialisteQueryLineDict', () => {
        var tempDict = functions.initialisteQueryLineDict()
        expect(tempDict['blocks-querylines']['where']).toEqual(
            {
                'name': 'where',
                'useincommands': ['common'],
                'segment': 'where',
                'datalog': ':where',
                'comment': 'filter command'
            }
        )
    })

    test('getQueryLine', () => {
        setGlobals()
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        expect(functions.getQueryLine('block_properties_are', "filters")).toEqual(
            '(property ?block :$$ARG1 $$ARG2)'
        )
        resetGlobalsToDefault()
    })

    test('getQueryLineSegment', () => {
        setGlobals()
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        resetGlobalsToDefault()
        expect(functions.getQueryLineSegment('block_properties_are')).toEqual(["ok", "filters"])
    })

    test('getQueryLineComment', () => {
        setGlobals({ showcommandcomments: true })
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        expect(functions.getQueryLineComment('block_properties_are')).toEqual(
            ';; ---- Select if block has a single property (arg1) with value arg2'
        )
        resetGlobalsToDefault()
    })



    test('getCommandQueryLineKeys', () => {
        setGlobals({ querygroup: "pages-querylines" })
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        expect(functions.getCommandQueryLineKeys('pages')).toEqual(
            ['findblocks', 'where', 'pagename']
        )
        resetGlobalsToDefault()
    })

    test('processCommandLists', () => {
        setGlobals()
        commandslists = '\ntitle: select and exclude blocks with block properties using and or\n- blocks\n    - *\n- blockproperties\n    - grade, "b-fiction"\n    - or grade, "b-western"\n    - and designation, "b-thriller"\n'
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        functions.processCommandList(commandslists)
        resetGlobalsToDefault()
        expect(functions.constructQuery()).toEqual(
            `#+BEGIN_QUERY
{
:title [:b "select and exclude blocks with block properties using and or"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(property ?block :grade "b-fiction")
(property ?block :grade "b-western")
)
(property ?block :designation "b-thriller")
]
}
#+END_QUERY
`
        )
    })

    //TODO: Add manual tests from py version here


}) // end describe


describe('Negative function Tests', () => {

    test('pageproperties - test 4', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: pageproperties - missing pages command
- pageproperties
    - pagetype, "testA"
    - pagetype, "testB"
    - not pagekey, 1
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "pageproperties - missing pages command"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-property ?page :pagetype "testA")
(page-property ?page :pagetype "testB")
)
(not (page-property ?page :pagekey 1))
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('missing pages and blocks commands 1', () => {
        commands = `title: missing pages and blocks commands`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "missing pages and blocks commands"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY
`
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('bad commands', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: bad commands
- badcommand1
- badcommand2
forgottenthedash
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

;; WARNING: '- badcommand1' is not valid command.
;;          Either a mispelt command or no leading dash
;; WARNING: '- badcommand2' is not valid command.
;;          Either a mispelt command or no leading dash
;; WARNING: forgottenthedash has no leading hypen eg '- pages'
{
:title [:b "bad commands"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('bad title', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title pages command - select all pages
- pages
    - *
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: title line should start with title:
{
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('equal rather than dash', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: equal sign used instead of dash
- pages
    = testpage00*
= pagetags
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING:     = testpage00* has no leading hypen eg '- pages'
;; WARNING: = pagetags has no leading hypen eg '- pages'
{
:title [:b "equal sign used instead of dash"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('only an argument line', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: missing command
    - testpage00*
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "missing command"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[(clojure.string/ends-with? ?blockcontent "testpage00")]
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('blocktags - test 1', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blocktags command - test 1
- blocktags
    - tag1
    - tag2
    - not tag3
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "blocktags command - test 1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
(page-ref ?block "tag1")
(page-ref ?block "tag2")
)
(not (page-ref ?block "tag3"))
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('blocktags - test 2', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blocktags and pages command combined - test 2
- pages
    - test*
    - *an
- blocktags
    - tag1
    - tag2
`
        expectedresults = `#+BEGIN_QUERY

;; **ERROR: blocktags not valid with pages command use blocks command instead

{
:title [:b "blocktags and pages command combined - test 2"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "test")]
[(clojure.string/ends-with? ?pagename "an")]
)
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('pagetags - test 1', () => {
        commands = `title: pagetags - test 1
- pagetags
    - pagetag1
    - pagetag2
    - not pagetag4
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "pagetags - test 1"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? false]
( or 
(page-tags ?page #{"pagetag1"})
(page-tags ?page #{"pagetag2"})
)
(not (page-tags ?page #{"pagetag4"}))
]
}
#+END_QUERY
`
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })


    test('blocktags - test 3', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: blocktags and pages command combined - test 3
- pages
    - test*
    - *2
    - not *age1
- blocktags
    - tag1
    - not tag2
    - tag3
    - not tag4
`
        expectedresults = `#+BEGIN_QUERY

;; **ERROR: blocktags not valid with pages command use blocks command instead

{
:title [:b "blocktags and pages command combined - test 3"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "test")]
[(clojure.string/ends-with? ?pagename "2")]
)
(not [(clojure.string/ends-with? ?pagename "age1")])
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('tasks - test 1', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: tasks - select and exclude task types
- tasks
    - TODO
    - not DOING
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "tasks - select and exclude task types"]
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
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    // ------------------------------------
    test('tasks - test 2', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: tasks and pages
- pages
    - *7
- tasks
    - TODO
    - not DOING
`
        expectedresults = `#+BEGIN_QUERY

;; **ERROR: tasks not valid with pages command use blocks command instead

{
:title [:b "tasks and pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
[(clojure.string/ends-with? ?pagename "7")]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })


    test('scheduled blocks in date range', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: scheduled blocks in date range
- scheduledbetween
    - :today :30d-after
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "scheduled blocks in date range"]
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
:inputs [:today :30d-after]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })

    test('journal pages only', () => {
        functions.setquerylineDBDict(functions.initialisteQueryLineDict())
        setGlobals()
        commands = `title: journal pages only
- journalonly
`
        expectedresults = `#+BEGIN_QUERY
;; WARNING: Must have 'pages' command or 'blocks' Command
;;          otherwise the query cannot get any information
;;          Inserting a blocks command for you

{
:title [:b "journal pages only"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
[?page :block/journal? true]
]
}
#+END_QUERY
`
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
    })



}) // end describe


//-------------------------------------------------------
// automated test cases
//-------------------------------------------------------

//TODO: use queryTestDB to run all the tests automatically
// note console.debug output is in the Jest Log not the Code Log
// see drop down at the top of the right panel (View, Output)

test('automated testcases access', () => {
    var msg = ''
    console.log("****** AUTOMATED TESTS STARTED ******");
    functions.setquerylineDBDict(functions.initialisteQueryLineDict())
    setGlobals()
    testcases = functions.getquerytestcases()
    for (let testno = 0; testno < testcases.length; testno++) {
        commands = gettestcommands(testno)
        console.log(" - test " + (testno + 1) + " started ..." +
            '\n---------------------------------' +
            '\n' + commands +
            '\n---------------------------------')
        msg += " - test " + (testno + 1) + " started ..." +
            '\n---------------------------------' +
            '\n' + commands +
            '\n---------------------------------'
        expectedresults = gettestexpectedresults(testno)
        functions.initialiseQuery()
        functions.processCommandList(commands)
        advancedquery = functions.constructQuery()
        msg += advancedquery +
            '\n---------------------------------\n\n'

        // if (testno == 44) {
        //     var a = 1
        // }
        resetGlobalsToDefault()
        expect(advancedquery).toEqual(expectedresults)
        console.log(" - test " + testno + " completed ok");

    }
    saveAutomatedTestOutput(msg)

})

//-------------------------------------------------------
// test local functions
//-------------------------------------------------------

describe('Housekeeping Tests', () => {
    test('set globals', () => {
        setGlobals(
            {
                querygroup: "abc",
                showcommandcomments: true,
                codeblock: false
            })
        returnval = functions.getquerygroup()
        expect(returnval).toBe("abc")
        returnval = functions.getshowcommandcomments()
        expect(returnval).toBe(true)
        returnval = functions.getcodeblock()
        expect(returnval).toBe(false)
        resetGlobalsToDefault()
    })

    test('load global value querygroup', () => {
        functions.setquerygroup("def")
        returnval = functions.getquerygroup()
        expect(returnval).toBe("def")
    })

    test('remove last generated query', () => {
        content = `- pages
            - *
        - blocktags
            - mytag
`
        expectedresult = content
        content += `#+BEGIN_QUERY
{
:title [:b "Pages only - Access page properties"]
:query [:find (pull ?block [*])
:where
[?block :block/original-name ?originalpagename]
[?block :block/name ?pagename]
(page-property ?block :pagetype "p-minor")
]
}
#+END_QUERY`

        returnval = functions.removeLastGeneratedQuery(content)
        expect(returnval).toBe(expectedresult)
        content = `- pages
        - *
        - blocktags
        - mytag
        `
        expect(returnval).toBe(expectedresult)
    })



    test('gettestcommands', () => {
        var commands = gettestcommands(0)
        expect(commands).toBe(
            `title: pages command - select all pages
- pages
    - *`
        )
    })

    test('gettestexpectedresults', () => {
        var expectedresults = gettestexpectedresults(0)
        expect(expectedresults).toBe(
            `#+BEGIN_QUERY
{
:title [:b "pages command - select all pages"]
:query [:find (pull ?block [*])
:where
[?block :block/name ?pagename]
]
}
#+END_QUERY
`
        )
    })

    //-------------------------------------------------------
    // data access tests
    //-------------------------------------------------------

    test('queryDBRead queryDB start entry', () => {
        returnval = functions.test_queryDBRead("common-querylines", "start")
        expect(returnval).toEqual(
            `start
start
start
#+BEGIN_QUERY

`)
    })

    test('queryDBRead queryDB not_arg_pagename_contains entry', () => {
        returnval = functions.test_queryDBRead("pages-querylines", "not_arg_pagename_contains")
        expect(returnval).toEqual(
            `not_arg_pagename_contains
filters
filters
(not [(clojure.string/includes? ?pagename "$$ARG1")])
Exclude if page title contains arg1
`)
    })


}) // end describe


