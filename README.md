# logseqadvancedquerybuilder

An Experimental online tool to help Logseq Users build advanced queries from <b><i>simple</i></b> commands.

**News Flash 3rd March 2023**
Logseq plugin (**logseq-query-builder-plugin**) now officially in the Logseq Marketplace

**News Flash 30th Dec 2022**
**Logseq plugin with same functionality now developed.** You can get it [here](https://github.com/adxsoft/logseq-query-builder-plugin) and see it in action [here](https://youtu.be/EA2jLSQ_WMA)

**Updated 14th Dec 2022 to v0.4 see Releases section below**
**SITE HAS BEEN COMPLETELY REWRITTEN IN JAVASCRIPT FOR STABILITY**

You can run this tool online at https://adxsoft.github.io/logseqadvancedquerybuilder/

To include this tool in a logseq page use this line
```html
<iframe src="https://adxsoft.github.io/logseqadvancedquerybuilder/" allow="clipboard-read; clipboard-write" style="width: 100%; height: 1000px"></iframe>
```

See the FAQ for instructions and examples of how to use the tool

Also see https://github.com/adxsoft/buildlogseqtestgraph for building a test graph to checkout the advanced queries you build with this tool

## Technical information
The tool is built in javascript. 

To test locally set the mode variable to 'local'. Once this is set you can use Jest Testing Library with the included _index.tests.js_ file.

To deploy to the web set the mode to 'website'

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
3. To run the unit tests you must do step 1 above and then run *test.py*

# Releases
_Version 0.1_
- Original release Oct 2022


_Version 0.2_
- clarify pages retrieval vs blocks retrieval in FAQ, Simple Commands
- Added 'and' and 'or' keywords in arguments for a command, For example can now say
```
- tagA
- or tagA
```
and also
```
- property category, "fiction"
- and property category, "western"
```
- Added a logseq test graph download button  to help user test advanced queries
- Force user to choose either pages or block retrieval, Default to block retrieval
- improved error messaging
- improved descriptions for the generated advanced query lines
- bug fixes

_Version 0.3_ Dec 8th 2022
- added the <i>pagelinks</i> command which will select blocks that have links to specific pages or journals

Example: To select blocks referring to page1 OR page 2
```
- blocks
  - *
- pagelinks
  - page1
  - page2
```
Example: To select blocks referring to page1 AND page 2
```
- blocks
  - *
- pagelinks
  - page1
  - and page2
```
Example: To select blocks referring to Xmas day journal
(assumes your date format is the default format)
```
- blocks
  - *
- pagelinks
  - Dec 25th, 2022
```
If you use a different date format use that in the journal reference

_Version 0.4_ Dec 14th 2022
Redeveloped in Javascript for speed and stability
- pyscript is still in alpha and early days so changes are happening all the time
- javascript is stable
- code base has been changed so that the core functions can operate in one of three ways 
(mode variable controls which operation is chosen _website_,_local_,_logseq-plugin_
  - as this website, 
  - locally for testing
  - as a logseq plugin (distributed to a separate repository)
