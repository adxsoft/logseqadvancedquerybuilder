# logseqadvancedquerybuilder

An Experimental online tool to help Logseq Users build advanced queries from <b><i>simple</i></b> commands.

You can run this tool online at https://adxsoft.github.io/logseqadvancedquerybuilder/

To include this tool in a logseq page use this line
```html
<iframe src="https://adxsoft.github.io/logseqadvancedquerybuilder/" allow="clipboard-read; clipboard-write" style="width: 100%; height: 1000px"></iframe>
```

See the FAQ for instructions and examples of how to use the tool

## Technical information
The tool is built in python 3 and uses pyscript (https://pyscript.net/) for the web user interface.

<i>Note. pyscript can take quite a few seconds to start the first time you use the tool. Thereafter the load time for the page is reasonably good.</i>

If you want to just run the python program <i>logseqquerybuilder.py</i> then you make the following changes in the code of <i>logseqquerybuilder.py</i>

1. change the line `mode = "pyscript"` to `mode = "python"`

2. To input a set of simple commands to generate an advanced query, add the following code at the end of <i>logseqquerybuilder.py</i>

```python
testQueryBuild("""yourcommands""")
```

Where yourcommands could be for example

```python
testQueryBuild("""title: blocktags and pages command combined - test 3
- pages
    - test*
    - *2
    - not *age1
- blocktags
    - tag1
    - not tag2
    - tag3
    - not tag4
""")
```

which will print the following advanced query that you can copy and paste (using Cmd/Ctrl Shift V) directly into Logseq

```clojure
#+BEGIN_QUERY
{
:title [:b "blocktags and pages command combined - test 3"]
:query [:find (pull ?block [*])
:where
[?block :block/content ?blockcontent]
[?block :block/page ?page]
[?page :block/name ?pagename]
( or 
[(clojure.string/starts-with? ?pagename "test")]
[(clojure.string/ends-with? ?pagename "2")]
)
(not [(clojure.string/ends-with? ?pagename "age1")])
( or 
(page-ref ?block "tag1")
(page-ref ?block "tag3")
)
(not (page-ref ?block "tag2"))
(not (page-ref ?block "tag4"))
]
}
#+END_QUERY
```

