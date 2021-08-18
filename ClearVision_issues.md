Bugs
====

-   insert stuff does not put things in Xref, so fail on expansion -
    fixed — makePyramid — makeObjectArray — changeSTUFF()

-   insertImage line 1052 'ref' is not defined - fixed — got from
    inserting objectarray of pyramids - Fixed

-   insert data menu does not seem to work from mouse - Can’t verify

-   Merging objects eg image and roi can create an object with too many
    attributes

-   Can’t remove nodes with immutable data (because immutable data can’t
    be deleted!)

<!-- -->

-   Able to make an element of a delay virtual

-   Issue with making child objects virtual - misreporting - just wrong

-   Able to merge immutable data - should not be possible?

-   Need to be able to handle properties for objects like graph
    parameters

-   Need to get order of attributes consistent - refactor the property
    update thing

Immutable data to be attributes of a node and nothing else
==========================================================

-   Add node parameters to Xref marked as immutable

-   Never create AGraph nodes or edges for immutable data

-   immutable data is always scalar

DONE

Multiple select
===============

-   Possible useful feature — Allow shift left-click to do multiple
    select — introduce a select menu option + key (Alt-S?) — ctrl-A with
    usual function of select all — Then we can have cut, copy, paste

Refactor
========

-   Make all of bG in class Xref

-   Dissociate AGraph building: — Build xref structure when reading
    xml — Build AGraphs from xref and xml

-   All operations to patch xref along with xml so this doesn’t have to
    be rebuilt

-   Should fix some issues with labelling varying!

-   Roll xml image and tensor data removal into this change — Requires
    saving xml to load the data from file

-   Save, Redo and Undo must now operate on xref as well as
    xml — Operations to be removed into Xref class.

-   Make kdefs into a class also - DONE

-   Make ddefs into a class - DONE

TODO

Restrict various things in Context
==================================

-   Property values — Channel of image from channel according to parent
    image format — start, end of ROI according to parent image size

TODO

Show tool-tips
==============

-   Properties of the object under the mouse without selecting it

TODO

cvxDataDefs
===========

1.  Finish tables

2.  Constants for each string to reduce size and increase efficiency

cvxKernelDefs
=============

Default values for parameters
-----------------------------

Many TODOs in the conditionals strings
--------------------------------------

Context menu
============

-   from mouse right-click DONE

-   from key DONE

Load Data
=========

-   Tries to load the data without changing attributes. In the case of
    xml, if tags don’t match, then option to change format or change
    data to fit. For images if there is too little or too much data for
    the image size, option to either change image size or use as much or
    little of the data as possible.

-   Files are loaded at exit/save or execute time, i.e. when the xml is
    written out.

-   Data is **not** loaded unless the data object has readers. ??

<!-- -->

-   xml (for everything, use same definition, tostring & fromstring)

-   csv (not for images?) does not include attributes but some may be
    implied by line formatting

-   image format available in image class. Convert the available pixel
    data to the format specified by the attributes.

vx\_delay
---------

Nothing

vx\_lut
-------

-   we load a file into the xml upon exit. Produce a warning only if
    data does not match (too much, too little, wrong type) but coerce it
    to fit

-   Support csv and xml.

vx\_distribution
----------------

-   we load a file into the xml upon exit. Produce a warning only if
    data does not match (too much, too little, wrong type) but coerce it
    to fit

-   Support csv and xml.

vx\_pyramid
-----------

?

vx\_threshold
-------------

Nothing

vx\_matrix
----------

-   we load a file into the xml upon exit. Produce a warning only if
    data does not match (too much, too little, wrong type) but coerce it
    to fit

-   Support csv and xml.

-   cvs is rows (lines) and columns. Ignore excess data, pad with
    zeroes, but raise warning. Use type as per attributes, warn on
    mis-match.

vx\_convolution
---------------

-   we load a file into the xml upon exit. Produce a warning only if
    data does not match (too much, too little) but coerce it to fit

-   Support csv and xml.

-   cvs is rows (lines) and columns. Ignore excess data, pad with
    zeroes, but raise warning.

vx\_scalar
----------

Nothing

vx\_array
---------

-   ? Use what we have presently - no load of data

-   at least support xml?

vx\_image
---------

-   Support image files only, they are loaded at exit. Make image match
    attributes for format and size.

-   Options to crop/pad or stretch/squash.

-   crop/pad can be TL, TR, BL, BR or centre, anf padding will be black.

-   strech/squash is done as required in each direction.

vx\_remap
---------

-   Support xml and csv.

-   csv has a pair of src\_x, src\_y floats for each location, so width
    is twice destination width. Zero-based and if not complete will be
    padded by replication.

-   xml is simply a series of &lt;point&gt; elements

vx\_object\_array
-----------------

?

vx\_tensor
----------

-   Support NNEF tensor file format

-   Support image files with same options as for images (allows GIF &
    TIFF with multiple images)

-   Support csv as a series of sets of correct number of lines (rows)
    each of the correct number of numbers (columns)

Save Data
=========

-   Stores data only, not attributes

-   Supports same formats as load data

-   Removes the data from the xml object

vx\_delay
---------

vx\_lut
-------

vx\_distribution
----------------

vx\_pyramid
-----------

vx\_threshold
-------------

vx\_matrix
----------

vx\_convolution
---------------

vx\_scalar
----------

vx\_array
---------

vx\_image
---------

vx\_remap
---------

vx\_object\_array
-----------------

vx\_tensor
----------

Dialogs
=======

Node properties
---------------

-   Name - DONE

-   Replicated - DONE via menu/mouse/keystroke

-   Border mode - DONE

-   Border mode constant value -almost, need editor/cell value thingies
    DONE

DONE

Data properties
---------------

TODO

### Array

-   need to be able to display & edit data DONE

-   need to get enum type from kernel parameter and have drop-down DONE

-   need to establish limits for values ??

-   need to identify immutable data and prevent type from being changed
    DONE

-   need to handle struct types DONE

-   what about user structs? DONE

DONE

### Convolution

-   need to be able to display & edit data

-   need to establish limits for values

-   Load from file (on exit)

DONE

### Distribution

DONE

### Image

-   format selection - DONE

-   width and height - DONE

-   need to handle uniform Images

-   Load image from file (on exit)

-   Store image to file (now) TODO

### Uniform image

TODO

### LUT

Mostly DONE

-   Need to handle data

-   Load from file (on exit) TODO

### Matrix

-   need to be able to display & edit data DONE

-   for specific matrices (warp nodes) get dimensions from node TODO

-   need to establish limits for values ??

-   need to handle matrix from pattern DONE

-   user patterns also ??

mostly DONE

### Object array

DONE

Object Array children
---------------------

DONE

### Pyramid

-   format, width, height, levels - DONE

-   scale - need drop-down to select half or orb - DONE

DONE

Pyramid children
----------------

DONE

### Remap

DONE

### Scalar

-   need to be able to set data DONE

-   need to get enum type from kernel parameter and have drop-down DONE

-   need to establish limits for values ??

-   need to identify immutable data and prevent type from being changed
    DONE

-   need to handle struct types DONE

-   what about user structs? DONE

DONE

### Tensor

Mostly done

-   Need to handle views

TODO

### Threshold

TODO

### Delay

DONE

### Delay children

DONE

Graph properties
----------------

-   Name - DONE

Settings
--------

-   Use JSON format

-   Extra kernel definitions

-   Default orientation

-   Default DPI

-   Default for "show connected data"

-   Colours?

-   Shapes?

-   Styles?

TODO.

Allow draw direction to be set by menu
======================================

View menu orientation TB, LR, BT, RL

DONE.

Default data objects - generate attributes appropriately
========================================================

TODO

Insert data objects
===================

-   Accelerator for pop-up menu (SHIFT-INS) DONE

-   Ask for type and number of objects in delay and object array DONE

-   Array, Convolution, Distribution, Image, LUT, Matrix, Pyramid,
    remap, scalar, tensor, threshold - DONE

-   Delay of…​, object array of, pyramid of - DONE

-   Uniform Image - TODO

-   ROI - DONE

-   CHANNEL - TODO - Image object array from Tensor - DONE

-   View - TODO

TODO

Insert non-standard node
========================

-   Need some way to define new kernels, and load/save them

TODO

Make local connected objects visible/invisible
==============================================

A 'rebuild' function Global flag to show/hide 'virtuals' Local property
to show or hide on a case-by-case basis (always show this object) that
is set for parents and children

DONE.

Merging data objects
====================

Needs to be more intelligent, for example when attributes differ. -
Images with zero width or height - Images with format virtual - Or do we
just use attributes of the source?

DONE.

Extensive testing and fixing of merge
-------------------------------------

TODO

Remove graph parameter
======================

-   To remove, select parameter and delete.

-   If the graph parameter is at the output or input of a copy node,
    then remove the copy node.

DONE.

Removal of copy node taken out as this is confusing functionality.

DONE.

Add graph parameter
===================

-   A data object is selected

-   Exactly one graph parameter is inserted for the first connected node
    found

-   If no connected node found, an error is shown

DONE.

Toggle virtual
==============

DONE

Note that if this is done on an unconnected global data object it will
delete it

Better toggle virtual for non-virtual data
------------------------------------------

-   Cannot make virtual if referenced in more than one graph

-   Cannot make virtual if referenced in no graphs

-   Actually move to the graph where it is reference

DONE

Select
======

This has to be left, right, up, down keys Can we do multiple select like
this - using shift key?

DONE: - left, right, up down select the first object (green) - with
shift, select the next object (red) - If there was no selected object,
choose the most appropriate at the start. For the second selected
object, this is the first selected object and vice-versa. - If the newly
selected object is not visible, scroll to make it visible.

The algorithm for move left (as an example) is to find the nearest
object that is completely to the left.

Delete graph
============

DONE.

Delete data objects
===================

-   if not connected, remove data object

-   immutable data can’t be deleted

-   non-virtual connected data simply becomes virtual

DONE

-   All connections

-   Immutable data

-   Connected virtual data

DONE

-   unconnected data objects

-   non-virtual, mutable data

DONE

Disconnect/unmerge data
=======================

-   there must be more than one connection to the data object, or the
    action is ignored

-   One connection is nominated as the 'original'. If there is a writer,
    then this is it. Otherwise it is just the first encountered
    connection.

-   For each of the other connections, replicate a new virtual data
    object with the same characteristics and connect that instead.

DONE - along with delete data

Connect via menu
================

Can only work with multiple select

DONE

Disconnect node
===============

for each parameter: - disconnect data object

DONE - along with delete node

Delete node
===========

DONE.

Insert new graph in cvxMain
===========================

DONE.

Automatic scrolling
===================

DONE

Scroll with mouse wheel and pageUp/Dn
=====================================

-   Mouse wheel DONE.

-   PageUp/Down DONE.

Improve refresh by only updating part of view?
==============================================

DONE.

Zoom in and out
===============

DONE

Save current view as…​
======================

Draw the graph to a file - DONE

Undo
====

1.  keep a list of actions performed upon the xml tree

    1.  Ditch the dot graphs and remake them on Undo

    2.  Also list the dot graph actions and undo those (most complex
        option).

2.  Keep a set of modified copies of the xml input

    1.  Would have an issue if there is a lot of data stored

    2.  Undo operation would then be similar to revert, but would load
        one of the backup copies

    3.  This is the simplest option, but has performance issues even
        during normal operation

3.  Keep a set of diffs of the xml input

    1.  Not sure how this is done, or how it is different to the first
        strategy

DONE - using the simplest strategy of saving the entire xml tree and
rebuilding everything on undo/redo (Performance issues with large graphs
or with much data)

Revert (i.e. reject changes and re-open file)
=============================================

DONE.

Show data relationships on graph pages as well?
===============================================

-   Another checkbox in the view menu…​

-   note that we currently do show all the structure of virtuals - we
    have to, they are shown nowhere else, but maybe we want to suppress
    this with yet another checkbox?

TODO - but maybe no need

Performance
===========

Data - save to external file on input
-------------------------------------

TODO

Output compressed files
-----------------------

TODO

Don’t delete tabs - re-use them
-------------------------------

DONE

Rebuild graphs without destroying tabs
--------------------------------------

DONE

Change some keys and mouse clicks
=================================

-   INSERT and right-click: insert Node

-   Shift-Insert and Shift-right-click: Insert nonstandard node

-   Ctrl-Ins and Ctrl-right-click: Insert Data

-   Alt-Ins: insert graph DONE

Navigation in windows
=====================

-   Properties pane should be open by default DONE

-   Properties pane not large enough when selected initially DONE

-   Currently no way of getting around from one pane to another except
    by mouse — need to fix with accelerator keys or something (SHIFT or
    CTRL-TAB?) DONE

DONE. Navigation uses CTRL+T and CTRL+SHIFT+T to navigate around tabs.
Use TAB key to get to properties, then CTRL-T or SHIFT-CTRL-T gets back
to previous tab.

Replicate node
==============

-   need new menu entry for this DONE

-   dialogue to select which parameters to be replicate DONE

-   if a parameter not in object array or pyramid, create object array
    or pyramid DONE

-   ask for number of elements if not already defined DONE

-   number of elements in object array must match previous or selection
    is an error DONE

DONE.

Mouse gestures
==============

-   dragging from object to empty screen same as delete?

-   drag from empty screen to node to insert optional parameter

DONE.

Improve globals tab with graphs and attached nodes
==================================================

DONE. Maybe some more to do?

Only save file if there have been changes
=========================================

-   i.e. undo list not empty DONE.

Shortcut keys
=============

<table>
<colgroup>
<col width="50%" />
<col width="50%" />
</colgroup>
<thead>
<tr class="header">
<th>KEY</th>
<th>What</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Ctrl+Alt+B</p></td>
<td><p>Select BT orientation</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+Alt+C</p></td>
<td><p>Show or hide connected data objects</p></td>
</tr>
<tr class="odd">
<td><p>Alt+C</p></td>
<td><p>Connect/merge</p></td>
</tr>
<tr class="even">
<td><p>Alt+D</p></td>
<td><p>Display/edit data</p></td>
</tr>
<tr class="odd">
<td><p>Alt+E</p></td>
<td><p>Edit Menu</p></td>
</tr>
<tr class="even">
<td><p>Alt+F</p></td>
<td><p>File Menu</p></td>
</tr>
<tr class="odd">
<td><p>Alt+G</p></td>
<td><p>Graph Menu</p></td>
</tr>
<tr class="even">
<td><p>Alt+H</p></td>
<td><p>Help Menu</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+H</p></td>
<td><p>Help</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+Alt+H</p></td>
<td><p>Help About</p></td>
</tr>
<tr class="odd">
<td><p>Alt+I</p></td>
<td><p>Insert Menu</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+K</p></td>
<td><p>Help keystrokes</p></td>
</tr>
<tr class="odd">
<td><p>Alt+L</p></td>
<td><p>View show log window</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+Alt+L</p></td>
<td><p>Select LR orientation</p></td>
</tr>
<tr class="odd">
<td><p>Alt+O</p></td>
<td><p>Edit Options</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+O</p></td>
<td><p>Open file</p></td>
</tr>
<tr class="odd">
<td><p>Alt+P</p></td>
<td><p>View show properties</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+P</p></td>
<td><p>Save (print) current drawing</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+Q</p></td>
<td><p>Quit</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+R</p></td>
<td><p>Revert</p></td>
</tr>
<tr class="odd">
<td><p>Alt+R</p></td>
<td><p>Replicate</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+Alt+R</p></td>
<td><p>Select RL orientation</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+S</p></td>
<td><p>Save</p></td>
</tr>
<tr class="even">
<td><p>Shift+Ctrl+S</p></td>
<td><p>Save As</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+T</p></td>
<td><p>Go to next graph tab or back to graph tab from properties</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+Shift+T</p></td>
<td><p>Go to previous graph tab or back to graph tab from properties</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+Alt+T</p></td>
<td><p>Select TB orientation</p></td>
</tr>
<tr class="even">
<td><p>Alt-T</p></td>
<td><p>Toggle global</p></td>
</tr>
<tr class="odd">
<td><p>Alt+V</p></td>
<td><p>View Menu</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+W</p></td>
<td><p>Close</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+Y</p></td>
<td><p>Redo</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+Z</p></td>
<td><p>Undo</p></td>
</tr>
<tr class="odd">
<td><p>Delete</p></td>
<td><p>Delete or disconnect object</p></td>
</tr>
<tr class="even">
<td><p>Shift+Delete</p></td>
<td><p>Clear All</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+Delete</p></td>
<td><p>Remove graph</p></td>
</tr>
<tr class="even">
<td><p>Alt+Insert</p></td>
<td><p>Insert graph</p></td>
</tr>
<tr class="odd">
<td><p>Insert</p></td>
<td><p>Insert standard node</p></td>
</tr>
<tr class="even">
<td><p>Shift+Insert</p></td>
<td><p>Insert vendor or user-defined node</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl-Insert</p></td>
<td><p>Insert data object</p></td>
</tr>
<tr class="even">
<td><p>PageDown</p></td>
<td><p>Scroll down</p></td>
</tr>
<tr class="odd">
<td><p>Shift+PageDown</p></td>
<td><p>Scroll right</p></td>
</tr>
<tr class="even">
<td><p>PageUp</p></td>
<td><p>Scroll up</p></td>
</tr>
<tr class="odd">
<td><p>Shift+PageUp</p></td>
<td><p>Scroll left</p></td>
</tr>
<tr class="even">
<td><p>Escape</p></td>
<td><p>Cancel selections</p></td>
</tr>
<tr class="odd">
<td><p>Right, Left, Up, Down</p></td>
<td><p>Select first object</p></td>
</tr>
<tr class="even">
<td><p>Shift+Right, Shift+Left, Shift+Up, Shift+Down</p></td>
<td><p>Select second object</p></td>
</tr>
<tr class="odd">
<td><p>Menu</p></td>
<td><p>Shift focus to properties page</p></td>
</tr>
<tr class="even">
<td><p>Ctrl++</p></td>
<td><p>Zoom In</p></td>
</tr>
<tr class="odd">
<td><p>Ctrl+-</p></td>
<td><p>Zoom Out</p></td>
</tr>
<tr class="even">
<td><p>Ctrl+=</p></td>
<td><p>Zoom 100%</p></td>
</tr>
</tbody>
</table>

Mouse gestures
==============

<table style="width:100%;">
<caption>Left button</caption>
<colgroup>
<col width="16%" />
<col width="16%" />
<col width="16%" />
<col width="16%" />
<col width="16%" />
<col width="16%" />
</colgroup>
<thead>
<tr class="header">
<th>Down on</th>
<th>Up on</th>
<th>shift</th>
<th>control</th>
<th>alt</th>
<th>action</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>Deselect</p></td>
</tr>
<tr class="even">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>✓</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td></td>
</tr>
<tr class="odd">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>-</p></td>
<td><p>✓</p></td>
<td><p>-</p></td>
<td></td>
</tr>
<tr class="even">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>✓</p></td>
<td></td>
</tr>
<tr class="odd">
<td><p>object</p></td>
<td><p>same object</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>Select</p></td>
</tr>
<tr class="even">
<td><p>Data object</p></td>
<td><p>same data object</p></td>
<td><p>✓</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>Toggle local/global</p></td>
</tr>
<tr class="odd">
<td><p>Data object</p></td>
<td><p>same data object</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>✓</p></td>
<td></td>
</tr>
<tr class="even">
<td><p>Node object</p></td>
<td><p>same data object</p></td>
<td><p>✓</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>Node replication</p></td>
</tr>
<tr class="odd">
<td><p>Node object</p></td>
<td><p>same data object</p></td>
<td><p>-</p></td>
<td><p>✓</p></td>
<td><p>-</p></td>
<td><p>Add optional parameter</p></td>
</tr>
<tr class="even">
<td><p>Data object</p></td>
<td><p>Node object</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>Add graph parameter if connected else add optional parameter</p></td>
</tr>
<tr class="odd">
<td><p>Node object</p></td>
<td><p>Data object</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>Add graph parameter if connected else add optional parameter</p></td>
</tr>
<tr class="even">
<td><p>Data object</p></td>
<td><p>Other data object</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>Merge objects if possible</p></td>
</tr>
<tr class="odd">
<td><p>Object</p></td>
<td><p>Nothing</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>Disconnect or delete object</p></td>
</tr>
<tr class="even">
<td><p>Nothing</p></td>
<td><p>node object</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>?</p></td>
<td><p>Add optional parameter</p></td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<caption>Right button</caption>
<colgroup>
<col width="16%" />
<col width="16%" />
<col width="16%" />
<col width="16%" />
<col width="16%" />
<col width="16%" />
</colgroup>
<thead>
<tr class="header">
<th>Down on</th>
<th>Up on</th>
<th>shift</th>
<th>control</th>
<th>alt</th>
<th>action</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>Insert standard node menu</p></td>
</tr>
<tr class="even">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>✓</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>Insert non-standard node menu</p></td>
</tr>
<tr class="odd">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>-</p></td>
<td><p>✓</p></td>
<td><p>-</p></td>
<td><p>Insert data menu</p></td>
</tr>
<tr class="even">
<td><p>Nothing</p></td>
<td><p>Nothing</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>✓</p></td>
<td><p>Unassigned</p></td>
</tr>
</tbody>
</table>

Data Structures
===============

There are three main data structures in use, the dictionary of types,
the dictionary of kernels, and the dictionary of references

Dictionary of types
-------------------

This is held in cvxDataDefs.py, and comprises the class TypeDef, which
maintains a class variable called typeDict that is indexed by type name
and holds type definitions of type TypeDef.

<table>
<caption>Type Constants</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>s_OBJECT</p></td>
<td><p>for defining vx_reference object types</p></td>
</tr>
<tr class="even">
<td><p>s_BASE</p></td>
<td><p>for defining base types (TODO do we need this?)</p></td>
</tr>
<tr class="odd">
<td><p>s_OPAQUE</p></td>
<td><p>for defining types we know nothing about</p></td>
</tr>
<tr class="even">
<td><p>s_INHERENT</p></td>
<td><p>For defining inherent types (that we should know about)</p></td>
</tr>
<tr class="odd">
<td><p>s_ENUM</p></td>
<td><p>type of constant composed of vendor&lt;&lt;20, id&lt;&lt;12 and a constant</p></td>
</tr>
<tr class="even">
<td><p>s_ATTRIBUTE</p></td>
<td><p>type of constant composed of vendor&lt;&lt;20, object type &lt;&lt;8 and a constant</p></td>
</tr>
<tr class="odd">
<td><p>s_KERNEL</p></td>
<td><p>type of constant composed of vendor &lt;&lt;20, lib&lt;&lt;12 and a constant (TODO do we need this?)</p></td>
</tr>
<tr class="even">
<td><p>s_CONSTANT</p></td>
<td><p>type of constant that is just a constant</p></td>
</tr>
<tr class="odd">
<td><p>s_STRUCT</p></td>
<td><p>for defining structure types</p></td>
</tr>
<tr class="even">
<td><p>s_UNION</p></td>
<td><p>for defining union types</p></td>
</tr>
<tr class="odd">
<td><p>s_ARRAY</p></td>
<td><p>for defining array types</p></td>
</tr>
</tbody>
</table>

<table>
<caption>TypeDef member variables</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>objtype</p></td>
<td><p>Type of object, one of the type constants above</p></td>
</tr>
<tr class="even">
<td><p>vendor</p></td>
<td><p>vendor name, used to retrieve a value from the type vx_vendor_id_e</p></td>
</tr>
<tr class="odd">
<td><p>id</p></td>
<td><p>either the library name, a vx enumeration name or a vx type name (VX_TYPE_XXX), used to retrieve a value from either vx_library_e, vx_enum_e or vx_type_e</p></td>
</tr>
<tr class="even">
<td><p>size</p></td>
<td><p>The size for array types</p></td>
</tr>
<tr class="odd">
<td><p>eltype</p></td>
<td><p>The element type for array types</p></td>
</tr>
<tr class="even">
<td><p>defs</p></td>
<td><p>A dict() mapping enumeration names or constant names to values, or field names to types in the case of structures and unions</p></td>
</tr>
<tr class="odd">
<td><p>attr</p></td>
<td><p>An additional dictionary used for additional information eg in object types</p></td>
</tr>
</tbody>
</table>

<table>
<caption>TypeDef static functions</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>add(name, objtype, vendor=None, id=None, defs=dict(), attr=dict())</p></td>
<td><p>If the entry with the given name does not exist, add it. Return the entry with the given name.</p></td>
</tr>
<tr class="even">
<td><p>getTypeVal(typeName, name, default=None)</p></td>
<td><p>Get an enum value or attribute for a given type</p></td>
</tr>
<tr class="odd">
<td><p>getValueNameFromType(typeName, value, default=None)</p></td>
<td><p>Get the string for a given value in the given enumerated type</p></td>
</tr>
<tr class="even">
<td><p>getObjectTypeNameFromValue(value, default=None)</p></td>
<td><p>Get the string for a given type embedded in a value Note that this could give misleading results if used inappropriately</p></td>
</tr>
<tr class="odd">
<td><p>getEnumIdNameFromValue(value, default=None)</p></td>
<td><p>Get the name of the embedded enumeration id as given by vx_enum_e Note that this could give misleading results if used inappropriately</p></td>
</tr>
<tr class="even">
<td><p>getEnumTypeNameFromValue(value, default=None)</p></td>
<td><p>Get the name of the enumeration type as given by the embedded enumeration id by looking in the definition of vx_enum (rather than vx_enum_e) Note that this could give misleading results if used inappropriately</p></td>
</tr>
<tr class="odd">
<td><p>getAttributeTypeNameFromValue(value, default=None)</p></td>
<td><p>Get the actual enumerated type name for an attribute value.</p></td>
</tr>
<tr class="even">
<td><p>getConstantNameFromValue(value)</p></td>
<td><p>Get the string for a given value, assuming that it is in a constant enumeration</p></td>
</tr>
<tr class="odd">
<td><p>getAttributeNameFromValue(value)</p></td>
<td><p>Get the string for a given value, assuming that it is in an attribute enumeration</p></td>
</tr>
<tr class="even">
<td><p>getEnumNameFromValue(value)</p></td>
<td><p>Get the string for a given value, assuming that it is in a kernel or enum enumeration</p></td>
</tr>
<tr class="odd">
<td><p>getValueNameFromValue(value, default=None)</p></td>
<td><p>Get the string for a given value without knowing the type Searches in the following order: Constants, attributes, enums &amp; kernels.</p></td>
</tr>
<tr class="even">
<td><p>getVendorIdVal(value)</p></td>
<td><p>Get the vendor id value from the given enum value</p></td>
</tr>
<tr class="odd">
<td><p>getObjectTypeIdVal(value)</p></td>
<td><p>Get the type id from the given enum value</p></td>
</tr>
<tr class="even">
<td><p>getEnumIdVal(value)</p></td>
<td><p>Get the enum type id from the given enum value</p></td>
</tr>
<tr class="odd">
<td><p>getLibIdVal(value)</p></td>
<td><p>Get the library id from the given enum value</p></td>
</tr>
<tr class="even">
<td><p>get(name)</p></td>
<td><p>Get type information for the given name</p></td>
</tr>
<tr class="odd">
<td><p>keys(name)</p></td>
<td><p>Return a list of the keys for the given name</p></td>
</tr>
<tr class="even">
<td><p>values(name)</p></td>
<td><p>Return a list of the values for the given name</p></td>
</tr>
<tr class="odd">
<td><p>items(name)</p></td>
<td><p>Return a list of the items for the given name</p></td>
</tr>
<tr class="even">
<td><p>labelsValues(name, start=None, end=None, excl=[])</p></td>
<td><p>Return a list of labels and a list of values, sorted on the labels, and in the range start value to end value-1 inclusive but not in the iterable excl, which may hold either labels or values</p></td>
</tr>
<tr class="odd">
<td><p>formatToString(value)</p></td>
<td><p>Takes a format id and returns the associated stringas used in the XML</p></td>
</tr>
<tr class="even">
<td><p>formatToId(value)</p></td>
<td><p>Takes a format string as used in teh XML and returns the associated integer id</p></td>
</tr>
<tr class="odd">
<td><p>addUserStruct(id)</p></td>
<td><p>Add a user struct called id to the vx_type_e enumeration</p></td>
</tr>
</tbody>
</table>

<table>
<caption>TypeDef member functions</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><em>init</em>(self, name, objtype, vendor=None, id=None, defs=dict(), attrs=dict(), size=None, eltype=None)</p></td>
<td><p>Initialises the type object and puts an entry in typeDict</p></td>
</tr>
<tr class="even">
<td><p>getVal(self, name, default=None)</p></td>
<td><p>Get an attribute value for this object.</p></td>
</tr>
<tr class="odd">
<td><p>getLabel(self, value, default=None)</p></td>
<td><p>Return the label for the given enumerated value</p></td>
</tr>
<tr class="even">
<td><p>isInherent(self)</p></td>
<td><p>Tests if the type is inherent</p></td>
</tr>
<tr class="odd">
<td><p>isBase(self)</p></td>
<td><p>Tests if the type is a base type. If the type is a base type, it’s defs have keys which are type names and values which are enum labels of vx_type_e, or None, if the type is not available there.</p></td>
</tr>
<tr class="even">
<td><p>isEnum(self)</p></td>
<td><p>Tests if the type is s_ENUM</p></td>
</tr>
<tr class="odd">
<td><p>isAttribute(self)</p></td>
<td><p>Tests if the type is s_ATTRIBUTE</p></td>
</tr>
<tr class="even">
<td><p>isKernel(self)</p></td>
<td><p>Tests if the type is s_KERNEL</p></td>
</tr>
<tr class="odd">
<td><p>isConstant(self)</p></td>
<td><p>Tests if the type is s_CONSTANT</p></td>
</tr>
<tr class="even">
<td><p>isAllEnum(self)</p></td>
<td><p>Tests if the type is an enumerated type, including attributes, kernels, and constants</p></td>
</tr>
</tbody>
</table>

### Other data in cvxDataDefs.py

**standardAlias.**

This is simply a dictionary mapping the openvx type enumeration names
(VX\_TYPE\_XXX) to the actual type names (vx\_xxx)

**reverseAlias.**

This is the opposite: it maps vx\_xxx names to VX\_TYPE\_XXX names.

The dictionary of kernels
-------------------------

This is held in cvxKernelDefs.py, managed by the classes KernelDef and
ParameterDef.

<table>
<caption>Constants</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>kpInput</p></td>
<td><p>The parameter is an input</p></td>
</tr>
<tr class="even">
<td><p>kpOutput</p></td>
<td><p>The parameter is an output</p></td>
</tr>
<tr class="odd">
<td><p>kpBidirectional</p></td>
<td><p>The parameter is bidirectional</p></td>
</tr>
<tr class="even">
<td><p>kpRequired</p></td>
<td><p>The parameter is required</p></td>
</tr>
<tr class="odd">
<td><p>kpOptional</p></td>
<td><p>The parameter is optional</p></td>
</tr>
<tr class="even">
<td><p>kpImmutable</p></td>
<td><p>The parameter is supplied at node creation times and should not be changed</p></td>
</tr>
<tr class="odd">
<td><p>kpSize</p></td>
<td><p>THe parameter is supplied at node creation time and should not be changed. The application will automatically generated this, as it refers to the size of the immediately preceding parameter</p></td>
</tr>
</tbody>
</table>

<table>
<caption>ParameterDef member variables</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>pname</p></td>
<td><p>parameter name</p></td>
</tr>
<tr class="even">
<td><p>pdir</p></td>
<td><p>parameter direction, one of kpInput, kpOutput or kpBidirectional</p></td>
</tr>
<tr class="odd">
<td><p>pstate</p></td>
<td><p>parameter state, one of kpRequired, kpOptional, kpImmutable or kpSize</p></td>
</tr>
<tr class="even">
<td><p>ptype</p></td>
<td><p>parameter type - indexes the type dictionary</p></td>
</tr>
<tr class="odd">
<td><p>preq</p></td>
<td><p>parameter requirements for validation - a string to be parsed by the parameter validator</p></td>
</tr>
</tbody>
</table>

<table>
<caption>ParameterDef member functions</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><em>init</em>(self, pname, pdir, pstate, ptype, preq)</p></td>
<td><p>Create the parameter object</p></td>
</tr>
</tbody>
</table>

<table>
<caption>KernelDef member variables</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>kname</p></td>
<td><p>kernel name</p></td>
</tr>
<tr class="even">
<td><p>fname</p></td>
<td><p>The name of the node creation function, used in code writing</p></td>
</tr>
<tr class="odd">
<td><p>kenum</p></td>
<td><p>The kernel enumeration label (TODO: may not be required)</p></td>
</tr>
<tr class="even">
<td><p>params</p></td>
<td><p>a list of parameter definition objects</p></td>
</tr>
<tr class="odd">
<td><p>kreq</p></td>
<td><p>requirements for validation - a string to be parsed by the kernel validator</p></td>
</tr>
</tbody>
</table>

<table>
<caption>KernelDef static functions</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>get(name)</p></td>
<td><p>Retrieve the kernel definition for the given name</p></td>
</tr>
<tr class="even">
<td><p>keys()</p></td>
<td><p>Retrieve the list of kernel names</p></td>
</tr>
<tr class="odd">
<td><p>values()</p></td>
<td><p>Retrieve the list of kernel definitions</p></td>
</tr>
<tr class="even">
<td><p>items()</p></td>
<td><p>Retrieve the list of (kernel name, kernel definition) pairs</p></td>
</tr>
</tbody>
</table>

<table>
<caption>KernelDef member functions</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><em>init</em>(self, kname, fname, kenum, params, kreq)</p></td>
<td><p>Initialise a kernel object and place it in the kernel dictionary</p></td>
</tr>
</tbody>
</table>

Dictionary of references
------------------------

This is held in cvxXML.py, together with much of the processing that
reads xml, creates the dictionary and the dot graphs. The class Xref
maintains the dictionary.

<table>
<caption>Xref member variables</caption>
<colgroup>
<col width="15%" />
<col width="85%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p>elem</p></td>
<td><p>The xml element</p></td>
</tr>
<tr class="even">
<td><p>tagref</p></td>
<td><p>The parent reference, where a data object is a child of another, or a parameter is a child of a node or a graph</p></td>
</tr>
<tr class="odd">
<td><p>name</p></td>
<td><p>The name given to the node in the dot graph, and the name attribute of the XML element, if appropriate</p></td>
</tr>
<tr class="even">
<td><p>graphs</p></td>
<td><p>A dictionary graphs where you can find this reference</p></td>
</tr>
<tr class="odd">
<td><p>direction</p></td>
<td><p>The direction of a parameter</p></td>
</tr>
<tr class="even">
<td><p>repl</p></td>
<td><p>If the parameter is replicated</p></td>
</tr>
<tr class="odd">
<td><p>graphdirty</p></td>
<td><p>If a graph redraw is required</p></td>
</tr>
<tr class="even">
<td><p>immutable</p></td>
<td><p>if any of the readers make this immutable</p></td>
</tr>
<tr class="odd">
<td><p>issize</p></td>
<td><p>if this is actually an unchangeable size object (immutable parameter)</p></td>
</tr>
<tr class="even">
<td><p>readers</p></td>
<td><p>The set of readers of this data object</p></td>
</tr>
<tr class="odd">
<td><p>writer</p></td>
<td><p>The writer of this data object</p></td>
</tr>
<tr class="even">
<td><p>tag</p></td>
<td><p>XML tag for this object</p></td>
</tr>
<tr class="odd">
<td><p>kdef</p></td>
<td><p>Kernel definitions if tag is 'node'</p></td>
</tr>
<tr class="even">
<td><p>subtype</p></td>
<td><p>Sub-type of object if applicable (e.g. object is scalar of type vx_enum)</p></td>
</tr>
<tr class="odd">
<td><p>datasize</p></td>
<td><p>Size of data in object if applicable (e.g. object is an array)</p></td>
</tr>
</tbody>
</table>


