# ClearVision graphical design tool for vision processing
Stephen Ramm, <stephen.v.ramm@gmail.com>
V1.1,  13 August 2021

## Introduction
This is a proposal and specification document for "ClearVision", an application to support creation and visualisation of OpenVX graphs.

There should be little emphasis on GUI features and how graph designs can be manipulated and laid out. The graph is drawn completely under the control of the design tool; little or no features for the user to change layout, position or appearance of the graph that is being designed, so that the emphasis is purely upon functionality of the graph and not upon producing a pretty layout for documentation purposes. This is to not detract from the main aims of the tool, as well as requiring less effort to implement. As there are available open-source libraries for graph layout and drawing (e.g. graphviz) the automatic display of graphs need not be onerous. The initial emphasis is on the creation of a single graph. However the graph may include imported kernels such as those created by an external NN tool.

### Features missing
 * Graph execution
 * Import of kernels from NN tools
 * Direct export of a graph for deployment (vxExportObjectsToMemory)
 * Performance evaluation

## Implementation and design goals

### Implementation language
Python

### GUI tool
The tool should be GUI-based, or we are losing the main thrust of the idea. However, the use of the mouse for moving and modifying individual graph elements will not be necessary - at most the mouse will be used to select nodes and visible data objects, and the graph will be drawn with an automatic layout. At most the user will be able to select from a pallette of options.

We need a library such as wx ot gtk to provide windowing features.

### Use an available format for storing the graph model

If there is no need to store drawing information, then the 'raw' OpenVX XML format may be used. This is a "quick and easy" solution as XML export and import is supported by the OpenVX XML extension at least for the first couple of versions.

However, the XML extension has not been officially kept up-to-date for OpenVX 1.3, plus the format is not human-readable and is very wasteful.
YAML would be preferred, and this should be a thrust of change - pyyaml could help?

Using the dot language to describe a graph has the advantage that even if additional attributes are added to describe OpenVX features, available graph drawing libraries will still be able to interpret and use the data to draw the graphs, and the APIs may also be used to extract the specific OpenVX attributes. However, this limits us straight away in the choice of visualisation tool, and it should be kept separate.

### Utilise available drawing tools for graphs
Create graphs programmatically in dot language, use dot to visualize. In this realization, each graph is in fact a dot graph, and we use elements of the dot language to abstract what is needed to express OpenVX. The design tool references an OpenVX implementation only at certain points.

The sample implementation xml import and xml export routines may be modified to convert to and from graphviz representation; The application may have to maintain both representations internally.

### Run largely independently of any OpenVX library
The application will have complete knowledge of the OpenVX specification with regard to data types and standard kernels and will provide a mechanism for adding custom kernels and data types to the settings. Only for certain operations is an implementation required, and this will be accessed via an interface capable of supporting remote operation.

```graphviz,mainflow,svg
digraph {
A[labelfontcolor="red" style=filled label="Load all possible kernels and
information about OpenVX" ]
B0[label="Load a model of an OpenVX
graph expressed in XML, convert
internally to graphviz model"]
B[label="Create and edit graph by adding
and connecting kernel and data nodes"]
B1[label="Define which data nodes
are graph parameters"]
C[label="Output graph(s) 
in XML or dot format"]
D[label="Display graph on screen",color=red]
E0[label="Load actual data 
into data nodes"]
E[label="Build OpenVX graph 
using graphviz model"]
F[label="Verify graph using 
OpenVX driver"]
G[label="Use OpenVX driver to output 
graph in binary format"]
H[label="Execute graph 
using OpenVX driver"]
I[label="Display data 
node contents"]
J[label="Display performance data"]
A->B[labelfontcolor=red label="Must get kernel
names and caps
before anything else" ]
B->B1->C
A->B0
B0->B
B1->D
B1->E0->E->F->G,H
H->I
B->D
E0->I
B0->D
D->B
C->B
C->B0
G->B
G->B0
E0->B
I->B
H->J
J->I
I->J
J->B
}
```

We can easily separate out various tasks which give rise to testable code.

 * The GUI framework of the graphical design tool may be completely separated from the OpenVX dependencies and developed largely in isolation.
 * Assuming a design which maintains both XML and graphviz representations, we can isolate tasks:
 ** Import the XML data from a file and build the internal representations
 ** Import YAML and build internal representation
 ** Layout and render the graph to screen
 ** Layout and render the graph to a file in a chosen format
 ** Export the XML data to a file
 ** Export YAML data to a file
 ** Generate C code to implement the model
 ** Build an OpenVX graph and verify
 ** Build an OpenVX graph, execute the graph and provide outputs and performance data
 ** Build an OpenVX graph and output as a 'blob'
 ** Import kernel libraries
 ** Import an OpenVX 'blob'
 ** Implement each identified graph editing command

## Notebook-style GUI with tabs
One tab per graph, and an overview tab showing unconnected data objects and graphs

## Enforce immutable graph rules and insert nodes complete with data objects

- No data shared between graphs, except by graph parameters
- By default all data objects in graphs are either constant or virtual
- Don't show virtual data, but allow individual connections to be non-virtual for debug purposes
- Have an 'eliminate unnecessary globals' options to change all non-virtuals with writers to be virtual
- Automatically insert copy nodes to enable graph parameter fan-out and attachment

## Optional parameters
Optional parameters to kernels are not shown unless they are connected. The node configuration dialog allows optional parameters to be connected, in which case a new default data object is inserted into the drawing, and also disconnected.

## Node configuration dialog
Allows:

- name to be changed
- optional parameters to be connected and disconnected
- attributes (border mode) to be set
- connections to be removed
- connected data objects to be made virtual or non-virtual
- node to be removed
- node to be replicated or not (if parameters allow)
- which parameters of the node are replicated
- All the data we have about the node is shown

## Data object configuration dialog
Allows:

- name to be changed
- object can be made (non)-virtual
- attributes to be examined and changed
- values of data to be examined and changed
- data to be loaded from a file (images)
- All information about the data object is shown, in particular:
* Parent object of ROI or tensor from view, and the location of the ROI/view in the parent
* Parent object if member of an object array, pyramid or delay, and the index, level or slot
* Parent tesnor if it is an object array of images created from a tensor
* Child objects (ROI, view, etc)

## Compound objects

- Delay
- Object array
- Pyramid
- Image with ROI
- Tensor with object array of images
- Tensor with tensor from view

Note that very complex objects may be created, for example a delay of object arrays holding tensors that have object arrays of images created from them, each of which may have child ROIs, which in turn may have ROIs.

These objects are drawn as a group of objects with bidirectional arrows connecting them, and objects in containers are shown in a different color.

Example of container objects in a graph
```graphviz

digraph {
    rankdir=LR
    edge[arrowhead=empty, arrowtail=empty]

        delay0[label="a delay of 2 slots", shape=component, color=black]
            obj_array0[label="object array 1\n(of 3 images)", shape=box3d, color=slategrey]
            image0[label="Image 1 of 3\nin obj array 1", shape=box, color=slategrey]
                image1[label="Image 2 of 3\nin obj array 1", shape=box, color=slategrey]
                image3[label="ROI of image 2", shape=box, color=slategrey]
                image1->image3[headlabel="ROI",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            image2[label="Image 3 of 3\nin obj array 1", shape=box, color=slategrey]
            obj_array0->image0[headlabel="Index 0",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            obj_array0->image1[headlabel="Index 1",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            obj_array0->image2[headlabel="Index 2",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            obj_array1[label="object array 2\n(of 3 images)", shape=box3d, color=slategrey]
            image4[label="Image 1 of 3\nin obj array 2", shape=box, color=slategrey]
            image5[label="Image 2 of 3\nin obj array 2", shape=box, color=slategrey]
            image6[label="Image 3 of 3\nin obj array 2", shape=box, color=slategrey]
            obj_array1->image4[headlabel="Index 0", arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            obj_array1->image5[headlabel="Index 1",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            obj_array1->image6[headlabel="Index 2",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
        delay0->obj_array0[headlabel="Slot 0", arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
        delay0->obj_array1[headlabel="Slot 1",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]

        pyramid0[label="Pyramid of 3 levels", shape=house, color=black]
        image10[label="level 0", shape=box, color=slategrey]
        image11[label="level 1", shape=box, color=slategrey]
        image12[label="level 2", shape=box, color=slategrey]
        pyramid0->image10[headlabel="Level 0",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
        pyramid0->image11[headlabel="Level 1",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
        pyramid0->image12[headlabel="Level 2",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]

        tensor0[label="tensor with view\nand object array",shape=folder,color=black]
            obj_array2[label="object array 3\n(of 3 images)", shape=box3d, color=slategrey]
            image7[label="Image 1 of 3\nin obj array 3", shape=box, color=slategrey]
            image8[label="Image 2 of 3\nin obj array 3", shape=box, color=slategrey]
            image9[label="Image 3 of 3\nin obj array 3", shape=box, color=slategrey]
            obj_array2->image7[headlabel="Index 0",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            obj_array2->image8[headlabel="Index 1",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
            obj_array2->image9[headlabel="Index 2",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]

        tensor1[label="View of tensor", shape=folder, color=slategrey]
        tensor0->tensor1[headlabel="Tensor view",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]
        tensor0->obj_array2[headlabel="Tensor image object array",arrowhead=halfopen, arrowtail=halfopen, dir=both, style=dotted, color=slategrey, fontsize=9, fontcolor=blue]

    input1[label="input image", shape = box]
    scaleNode[label="Scale Node"]
    input1->scaleNode->image0
    some_replicated_node[label="A node that may be replicated"]
    some_node[label="A node taking compound\nparameter objects"]
    image0, image10->some_replicated_node->image3
    pyramid0, obj_array1->some_node->obj_array2
    some_node->image4
}
```
## Mouse gesture driven
This approach utilises clicks, double-clicks and drags, with CTRL and SHIFT key combinations, to edit the graph.

Some of the operations listed below will only be legal under certain circumstances, for example drag from one data object to another is only legal if the meta-data matches or can match, and if no more than one of the data objects has a writer.

| Mouse Gesture | CTRL | SHIFT | Source | Sink | Operation |
| ------ | ---- | ---- | ---- | ---- | ---- |
| Left-Click | | | Data or Node | N/A | Select; key and menu commands apply to this object|
| Left-Click | |??? | Data or Node | N/A | Multiple select, for multiple-object key and menu commands|
| Left-Click |???|???| Data | N/A | Make virtual (only if it has source and at least one sink)|
| Left-Click |???|| Data | N/A | Insert or remove graph parameter|
| Double-Left-Click | | | Node | N/A | Dialog to allow editing of attributes and connections, including deletion and virtual status|
| Double-Left-Click | | | Data | N/A | Dialog to allow editing of attributes, scalar data, source of image data, and connections (including deletion)|
| Double-Left-Click | |???| Data | N/A | Open window to display data (image, tensor etc)|
| Double-Left-Click | | | <nothing> | N/A | Insert new node with data objects for each kernel parameter|
| Drag | | | Node | <nothing> | Insert connection and new node (with data objects)|
| Drag | | | Node | Data | Insert connection (increase fan-out of connected kernel parameter)|
| Drag | | | Data | <nothing> | Insert connection and new node|
| Drag | | | Data | Data | Merge data objects; if source was connected to a graph parameter, behave as if source was the graph parameter|
| Drag | | | Graph Parameter | <nothing> | Insert copy node and new node|
| Drag | | | Graph Parameter | Data | Insert copy node if necessary, new connection, re-arrange existing connection(s)|
| Drag | | | Node | Node | Make data objects in connections between the nodes non-virtual|
| Right-Click | | | <nothing> | N/A | Menu dependent upon selection - available key/menu commands|


## Command driven
With this approach we separate the functionality in a way so it may be driven by key presses, by mouse, or even by API. No reference is made to the drawing when selecting objects; it could be done on a command line using object names and word completion for speed. The following operations are identified:

Table of operations
|Command|Description|Suggested keystrokes and menu command|Comments |Development Phase|
|---|---|---|---|---|
|Open File|Open a previously saved drawing file and display it|"FO", File\|Open|Opens a file selection dialog & draws a graph | 1|
|Save|Save the current graph with changes|"FS", File\|Save|Opens a "file save as.." dialog if not previously saved | 1|
|Save as|Save the current graph under a new name|"FA", File\|Save As| | 1|
|Close|Save the current graph and clear the screen|"FC", File\|Close|Opens a "file save as.." dialog if not previously saved | 1|
|Clear|Clear the graph without saving first|"Z", Edit\|Clear| | 1|
|Exit|Quit the program|"Q", File\|Quit| | 1|
|Load library|Load a library of user kernels|"LL", File\|Load Library|Will use OpenVX API to load the kernels from a .lib | 3|
|Load objects|Load objects from a memory blob|"LO", File\|Load Objects|Will use OpenVX IX extension API to load objects (initially a single kernel) | 3|
|Load NN model|Load neural network model|"LN", File\|Load Neural Network|Invokes external mapping tool to create an OpenVX kernel from a TensorFlow or Caffee model targeting either VHA or GPU and use OpenVX IX extension API to load it.| 2|
|Insert node|Insert a node into the graph|"IN", Insert\|Node|Insert must be followed by object selection - node, data, graph parameter; all objects will be named | 1|
|Insert data|Insert a non-virtual data object|"ID", Insert\|Data| | 1|
|Insert parameter|Insert a graph parameter|"IP", Insert\|Parameter|A parameter is a non-virtual data object, need to select the node and kernel parameter as well | 1|
|Select|Select object for further operations|"S", Edit\|Select|Followed by selection of the object by name | 1|
|Remove|Remove selected object|"R", Edit\|Delete| | 1|
|Connect|Connect selected object to another one|"C", Edit\|Connect| | 1|
|Disconnect|Remove a connection from the selected object|"D", Edit\|Disconnect| | 1|
|Edit Data|Set or load data into selected object|"E", Edit\|Data|Includes setting of simple values, configuring types and loading data from a file for images or tensors | 1|
|Display Data|Displays data of selected object|"Y", Edit\|Display|Opens a separate window showing data. | 1|
|Toggle Virtual|Switches data objects between virtual and non-virtual|"T", Edit\|Virtual|Requires additional selection of 'port' or kernel parameter if selected object is a node | 1|
|Attach| Connects to a remote OpenVX implementation|"GA", Graph\|Attach| The 'remote' implementation may be on the same host | 2|
|Verify|Verifies the graph|"GV", Graph\|Verify|Opens separate window with results | 2|
|Execute|Executes the graph|"GX", Graph\|Execute|Opens separate window with result, updates any data windows | 2|
|Export|Exports the graph|"GE", Graph\|Export|There are different types of export to choose: Rendered, XML, Binary (IX API) or C code | 2|
|Edit|Edit  preferences|"P", Edit\|Preferences|Allow various settings to be changed, including custom kernels | 1|


### Insert operation
This operation inserts a node, data object or graph parameter into the graph.
 
 Inserting a graph parameter will insert a data object and associate it with a chosen node and kernel parameter. The node is chosen first by its name in the graph, then the kernel parameter by name, and lastly any extra data object attributes must be selected, and a name given to the object.
 
 Inserting a node will require that the name of the kernel be given, and a name for the node in the graph.
 
 Inserting a data object will require selection of the type, attributes, and any sub-type and attributes (for object arrays etc).
After the operation, the new object is selected.

Insert command
```graphviz,insert,svg
digraph insert {
insert[label="insert command"]
knode[label="node command"]
data[label="data command"]
parameter[label="parameter command"]
kernel_selector[label="Kernel selection dialog"]
data_type_selector[label="Data object selection dialog"]
port_selector[label="Parameter selection dialog"]
object_selector[label="Node selection dialog"]
ready[label="Idle (ready) state"]
cleared[label="Idle state with no graph"]
selected[label="Idle with object selected state"]
draw_graph[label="Clear and redraw graph,
with selection highlighted"]
{ready,selected,cleared}->insert->knode->kernel_selector->draw_graph->selected
insert->data->data_type_selector->draw_graph
insert->parameter->object_selector->port_selector->draw_graph
object_selector->draw_graph[taillabel="dialog cancelled", fontcolor=blue,fontsize=9,labelangle=0]
}
```

### Select operation
This operation is valid when there is a graph being displayed. An object is selected by name for further operations that require an object to be selected.

Select command
```graphviz,select,svg
digraph select {
ready[label="Idle (ready) state with graph"]
select[label="select command"]
object_selector[label="object selection dialog"]
selected[label="Idle with object selected state"]
draw_graph[label="Clear and redraw graph,
with selection highlighted"]
{ready,selected}->select->object_selector->draw_graph->selected
}
```

### Connect operation
Connect the selected object to another
 . The operation is only allowed if a node is selected with unconnected kernel parameters.
 . Select the kernel parameter to connect.
 . Select by name the object to connect to; at this point there are a limited number of allowed objects, which could be highlighted on the graph.
 . If the object to connect to is a node, then select the  kernel parameter of that node to connect to. Again, only valid ones are allowed.
 . If the connection is node to node, a virtual data object is implicitly inserted. Note that virtual objects are never drawn.
 . The graph is redrawn showing the new connection. The object selected remains as before.

Connect command
```graphviz,connect,svg
digraph connect {
selected[label="Idle with object selected state"]
connect[label="connect command"]
port_selector[label="kernel parameter selection dialog"]
object_selector[label="connect to..
object and port selection dialog"]
draw_graph[label="Clear and redraw graph,
with selection highlighted"]
selected->connect->port_selector->object_selector->draw_graph->selected
}
```

### Disconnect operation
This is the reverse of the connect operation. It also removes virtual data objects that end up with no writer or with no reader.

Disconnect the selected node from another
 . The operation is only allowed if a node is currently selected.
 . Select the kernel parameter to disconnect
 . If the data object is virtual and the kernel parameter is an output or bidirectional, then the data object is removed along with all of its connections.
 . If the data object is virtual and the kernel parameter is an input, then the data object is removed if there is only one remaining connection to it.

Disconnect command
```graphviz,disconnect,svg
digraph disconnect {
selected[label="Idle with object selected state"]
port_selector[label="port selection dialog"]
disconnect[label="disconnect command"]
draw_graph[label="Clear and redraw graph,
with selection highlighted"]
selected->disconnect->port_selector->draw_graph->selected
}
```

### Remove operation
This operation removes the selected object and all of its connections from the graph. If as a result of removing the object there are virtuals objects left with no writer or no reader then these are removed together with their connections.

Remove command
```graphviz,remove,svg
digraph remove {
selected[label="Idle with object selected state"]
remove[label="remove command"]
draw_graph[label="Clear and redraw graph"]
ready[label="Idle (ready) state"]
selected->remove->draw_graph->ready
}
```

### Edit data operation
This operation allows attributes and data of the selected object to be modified. The objects may be nodes or data objects. For images and tensors, data may be loaded from file.

Edit data command
```[graphviz,edit_data,svg
digraph set_data {
selected[label="Idle with object selected state"]
set_data[label="Edit data command, opens Edit data dialog.
From here image or tensor data may
be loaded via file open dialog"]
selected->set_data->selected
}
```

### Display data operation
Allows data to be displayed for the selected object. Images are shown as pictures, and all attributes are also shown.

Display data command
```graphviz,display_data,svg
digraph display_data {
selected[label="Idle with object selected state"]
display_data[label="Data display command,
Data display window opened"]
selected->display_data->selected
}


### Toggle Virtual operation
This allows data objects to be either virtual or non-virtual. The operation is only allowed if the object currently selected is not a graph parameter.

 . If the object is a data object, then it is made virtual and won't be seen on the re-drawn graph. The writer of the data object becomes the selected object.
 . If the object is a node, then a kernel parameter is chosen and the data object attached to that has it's virtual state inverted. The node remains selected.
 . An error occurs if no suitable data objects (virtual or otherwise) are attached to kernel parameters.

Toggle Virtual command
```graphviz,toggle_virtual,svg
digraph toggle_virtual {
selected[label="Idle with object selected state"]
toggle[label="Toggle virtual command"]
port_selector[label="port selection dialog"]
draw_graph[label="Clear and redraw graph,
with selection highlighted"]
selected->toggle->port_selector->draw_graph->selected
toggle->draw_graph
port_selector->error->selected
toggle->error
}
```

### Open File operation
Loads a graph from a file. Can over-write an existing graph, option given to save first.

Open file command
```graphviz,open_file,svg
digraph open_file {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
cleared[label="Idle state with no graph"]
open[label="open command"]
save_option[label="Option to save current file
if there is a graph displayed"]
file_save[label="file save dialog"]
file_open[label="file open dialog"]
draw_graph[label="Clear and draw new graph"]
cleared,selected,ready->open->save_option->file_save->file_open->draw_graph->ready
open->file_open
file_save->error->ready
save_option->file_open->error
}
```

### Clear Graph operation
Just clears out the existing graph. No option to save first.

Clear graph command
```graphviz,clear,svg
digraph clear {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
cleared[label="Idle state with no graph"]
clear[label="clear command"]
draw_graph[label="Clear graph"]
selected,ready->clear->draw_graph->cleared
}
```

### Close operation
Save changes in the current graph and perform a clear.

Close command
```graphviz,close,svg
digraph close {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
cleared[label="Idle state with no graph"]
close[label="close command"]
file_save[label="file save dialog
(only if not previously saved)"]
draw_graph[label="Clear graph"]
selected,ready->close->file_save->draw_graph->cleared
file_save->error->ready
}
```

### Save operation
Save changes in the current graph back to the original file, or create a new one.

Save command
```graphviz,save,svg
digraph save {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
save[label="save command"]
file_save[label="file save dialog
(only if not previously saved)"]
selected,ready->save->file_save->error,ready
error->ready
}
```

### Save File As operation
The current graph is saved in a file of a new name.

Save As command
```graphviz,saveas,svg
digraph saveas {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
save[label="Save As command"]
file_save[label="file save dialog"]
selected,ready->save->file_save->error,ready
error->ready
}
```

### Attach operation
This will attach to a remote OpenVX implementation so that things may actually be run. Note that there are a number of issues to solve with this, apart from making a remote implementation available, notably:

 - Transport of data could be time-consuming, and we may want to connect to data sources or sinks on the remote
 - Availability of custom kernels - how would these be loaded on the remote?

Attach command
```graphviz,attach,svg
digraph attach {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
attach[label="Attach command"]
attach_select[label="Remote selection dialog"]
kernel_select[label="Remote kernel loading dialog"]
data_select[label="Remote data selection dialog"]
selected,ready->attach->attach_select->error,kernel_select,data_select,ready
kernel_select->error,data_select,ready
data_select->error,ready
error->ready
}
```

### Verify operation
An OpenVX graph is built from the current representation, and OpenVX vxVerifyGraph API is called.
The results are displayed in a separate window.

Verify command
```graphviz,verify,svg
digraph verify {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
verify[label="Verify command"]
verify_results[label="Open separate window
with results of verify"]
selected,ready->verify->verify_results->ready
}
```

### Export operation
The type of the export is chosen in the file save dialog, by specifying the file extension.

There are four types of export:
 . 'Blob' : An OpenVX graph is built from the current representation, and then exported using the IX extension API of OpenVX. (".ixvx")
 . C: Outputs auto-generated C code that will build the graph using OpenVX library. (".c")
 . Rendered: The visual representation is saved in some format, either dot language or rendered into an image (any formats supported by graphviz library) (".dot", ".png", etc.)
 . XML: This is equivalent to Save As, but the name of the current file is not changed. (".xml")

Export command
```graphviz,export,svg
digraph export {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
file_save[label="file save dialog"]
export[label="Export command"]
export_selection[label="Choose type of export"]
selected,ready->export->export_selection->file_save->ready
file_save->error->ready
}
```

### Execute operation
An OpenVX graph is built from the current representation, and OpenVX vxProcessGraph API is called.
The results are displayed in a separate window.

Execute command
```graphviz,execute,svg
digraph execute {
selected[label="Idle with object selected state"]
ready[label="Idle (ready) state with graph"]
execute[label="Execute command"]
execute_results[label="Open separate window
with results of execution"]
selected,ready->execute->execute_results->ready
}
```

### Load operations
These operations load either a library of user kernels, a neural network model, or an OpenVX 'blob' with known contents.

An appropriate selection dialog is required; in addition to the normal file selection, the following information is required:

Neural network::
    - Caffe or TensorFlow
    - Targeting VHA or GPU
OpenVX 'blob'::
    - Number of objects
    - Import method for each object
    - It may be that we can read the blob and get this information
User kernel library::
    - No extra information

Load Objects or Library or Neural Network commands
```graphviz,load,svg
digraph {
ready[label="Idle (ready) state with or without graph"]
loadNN[label="Load objects or library command"]
file_selector[label="file and model selection dialog"]
kernels_info[label="Open separate window
with info about kernels and other objects loaded"]
ready->loadNN->file_selector->kernels_info,error->ready
}
```

### Edit preferences
This is a dialog that allows various settings to be changed. Settings are loaded when the application is started and automatically saved upon exit. Types of settings that may be changed are:

 - Custom kernel definitions. This includes:
 * kernel name
 * node creation function (if any)
 * name, direction, type, status of each parameter in number order
 * type matching rules for parameters
 - Graph drawing options, such as:
 * Shape, colour, style, font for different objects (node, parameter, data, constant data)
 * Arrowhead type
 * Font, size and colour for head and tail text (parameter names), and whether to show them.
 * Layout engine and renderer
 - Any other options

Edit preferences command
```graphviz,preferences,svg
digraph {
ready[label="Idle (ready) state with or without graph"]
preferences[label="Edit preferences command"]
pref_dialog[label="Configuration dialog"]
ready->preferences->pref_dialog->ready
}
```

### Node replication

Node replication is controlled in the node configuration dialog. Replicated nodes are shown in a different shape / style to other nodes.

## Libraries
wx widgets: Available for C, C++, Python. Suggested library for the GUI.

pygraphviz: Dot language read,write, manipulation for Python

cgraph, graph: Graphviz libraries for C

libxml2: XML read, write, manipulation, available for C and for Python as lxml.

## Design
Program imports XML and builds a graph using graphviz library, annotating with vx attributes to refer back to the xml. Tables are used to describe the standard OpenVX kernels along with parameter names and any restrictions (e.g. input types, how they must match output types etc.) and any proprietary extensions. If the OpenVX library is not available then certain operations (load library, load NN, load blob, verification, execution, export to blob) are not available. Custom kernels may still be inserted if full name and parameters (number, direction, type) are given.

The first goal is to deliver a program that operates independently to OpenVX, importing and exporting using the OpenVX xml format and creating a graphviz graph that may be exported in a variety of formats. The xml import to graphviz representation can be based upon the sample implementation import from xml.

### Table driven - kernel data
Rather than load an OpenVX library and interrogate it for all the kernels present, we choose to use an internal table that is supplemented by configuration data stored in settings. An advantage is that kernel parameter names may be defined, together with rules about what can be connected. Suggest that this is a dictionary indexed by kernel name, and holding the following data:

* Node function name (can be empty). This is used for C code generation.
* Enumeration value (can be empty).
* Number of parameters
* For each (numbered) parameter:
- Name
- Direction (VX_INPUT, VX_OUTPUT, VX_BIDIRECTIONAL)
- Status (VX_PARAMETER_STATE_REQUIRED, VX_PARAMETER_STATE_OPTIONAL, VX_PARAMETER_STATE_IMMUTABLE)
- Type (A vx_xxx)
- Subtype (A vx_xxx) when Type is Scalar, Array, etc. or requirement for attributes.
* Match conditions. This is either blank or is an expression defining conditions that must be met by parameters. The match conditions will also be used to calculate attributes of virtual data, which will have to be re-calculated if objects with different meta-data are connected to inputs.

Example of a kernel table definition in Python
```python
# In this example, the attribute requirements and match conditions
# are expressed arbitrarily; the language for these needs definition.
# In python, it is not necessary to store the number of entries in lists, tuples and dictionaries.
# A C implementation could be quite different.
exampleKernelTable = 
{
'org.khronos.openvx.halfscale_gaussian': ('vxHalfScaleGaussianNode', 'VX_KERNEL_HALFSCALE_GAUSSIAN',
        {'input': ('VX_INPUT', 
                  'VX_PARAMETER_STATE_REQUIRED', 
                  'vx_image', 
                  'input.VX_IMAGE_FORMAT = VX_DF_IMAGE_U8'), 
        'output': ('VX_OUTPUT',
                  'VX_PARAMETER_STATE_REQUIRED', 
                  'vx_image', 
                  'output.VX_IMAGE_FORMAT = VX_DF_IMAGE_U8'), 
        'kernel_size': ('VX_INPUT',
                  'VX_PARAMETER_STATE_IMMUTABLE',
                  'vx_int32',
                  'kernel_size > 0')
        },
        'output.VX_IMAGE_WIDTH = (input.VX_IMAGE_WIDTH + 1)/2 AND output.VX_IMAGE_HEIGHT = (input.VX_IMAGE_HEIGHT + 1)/2'),
'org.khronos.openvx.remap': ('vxRemapNode', 'VX_KERNEL_REMAP',
        {'input': ('VX_INPUT',
                  'VX_PARAMETER_STATE_REQUIRED',
                  'vx_image',
                  'input.VX_IMAGE_FORMAT = VX_DF_IMAGE_U8'),
        'table': ('VX_INPUT',
                  'VX_PARAMETER_STATE_REQUIRED',
                  'vx_remap',
                  ''),
        'policy': ('VX_INPUT',
                  'VX_PARAMETER_STATE_IMMUTABLE',
                  'vx_interpolation_type_e',
                  'policy != VX_INTERPOLATION_TYPE_AREA'),
        'output': ('VX_OUPUT',
                  'VX_PARAMETER_STATE_REQUIRED',
                  'vx_image',
                  'output.VX_IMAGE_FORMAT = VX_DF_IMAGE_U8')
        },
        'output = input'),
'org.khronos.openvx.tensor_multiply': ('vxTensorMultiplyNode', VX_KERNEL_TENSOR_MULTIPLY',
        {'input1': ('VX_INPUT',
                    'VX_PARAMETER_STATE_REQUIRED',
                    'vx_tensor',
                    ''),
         'input2': ('VX_INPUT',
                    'VX_PARAMETER_STATE_REQUIRED',
                    'vx_tensor',
                    ''),
         'scale': ('VX_INPUT',
                   'VX_PARAMETER_STATE_REQUIRED',
                   'vx_scalar',
                   'scalar.VX_SCALAR_TYPE = VX_TYPE_FLOAT32'),
         'overflow_policy': ('VX_INPUT',
                    'VX_PARAMETER_STATE_IMMUTABLE',
                    'vx_convert_policy_e',
                    ''),
         'rounding_policy': ('VX_INPUT',
                    'VX_PARAMETER_STATE_IMMUTABLE',
                    'vx_rounding_policy_e',
                    ''),
         'output': ('VX_OUTPUT',
                    'VX_PARAMETER_STATE_REQUIRED',
                    'vx_tensor',
                    '')
        },
        # Need all three tests below as parameters may be connected in any order
        'output = input1 AND output = input2 AND input1 = input2') 
}
```

### Table driven - data types
Rather than being hard-baked into the program, the types of data supported are defined in tables. The program will have to have knowledge of the simple (non-object, non-struct) types and of images and tensors, so that data values may be displayed and edited, but in general it should be possible to add new types without changing anything but the tables. There is an alias dictionary which links type enumerations to data types (e.g. VX_TYPE_IMAGE is linked to vx_image). Then there is a dictionary indexed on the data type that should contain the following information:

 * Name (as in vx_xxxx)
 * Base class, Enum, Struct, Union, Array or Object, i.e. use a simple pointer or an OpenVX reference.
 * Number of writable (including those only writable at creation time) attributes for an object, values for an enum or array or data fields for a struct and then for each:
 - Name, for data fields or attributes
 - Data type - this is either a simple type, a number or a name that indexes the table or the alias dictionary.
 * For an object, the type of the data, which may be:
 - An attribute name (e.g. in the case of scalar or array)
 - A data type (e.g. VX_IMAGE, VX_TENSOR)
 * For an object, the number of accessible data, which may be:
 - An attribute name (e.g. in the case of an object array or delay)
 - A number
 - Empty

Clearly, this is going to be a very large table, and together with the kernel table it will define a lot of the OpenVX language and must be kept up-to-date with the specification.

Examples of data type definitions (in Python)
```python

SomeDataTypes = {
    'vx_delay': ('OBJECT',
                {'VX_DELAY_TYPE':'vx_type_e',
                 'VX_DELAY_SLOTS':'vx_size'},
                'VX_DELAY_TYPE',
                'VX_DELAY_SLOTS'),
    'vx_border_t': ('STRUCT',
                    {'mode':'vx_border_e',
                    'constant_value':'vx_pixel_value_t'}),
    'vx_pixel_value_t': ('UNION',
                    {'RGB':'vx_uint8_a3',
                    'RGBX':'vx_uint8_a4',
                    'YUV':'vx_uint8_a3',
                    'U8':'vx_uint8',
                    'U16':'vx_uint16',
                    'S16':'vx_int16',
                    'U32':'vx_uint32',
                    'S32':'vx_int32',
                    'reserved':'vx_uint8_a16'}),
    'vx_uint8_a3': ('ARRAY', 3, 'vx_uint8'),
    'vx_uint8_a4': ('ARRAY', 4, 'vx_uint8'),
    'vx_uint8_a16': ('ARRAY', 16, 'vx_uint8'),
    'vx_border_e': ('ENUM', ['VX_BORDER_UNDEFINED',
                            'VX_BORDER_CONSTANT',
                            'VX_BORDER_REPLICATE']),
    'vx_reference':('BASE', ['vx_image',
                            'vx_delay',
                            'vx_tensor',
                            'vx_threshold',
                            'vx_scalar',
                            'etc...']),
    'vx_enum': ('BASE', ['vx_border_e',
                        'vx_type_e',
                        '..and all other enumerations']
}
SomeAlias = {
'VX_TYPE_IMAGE': 'vx_image',
'VX_TYPE_DELAY': 'vx_delay',
'VX_TYPE_ENUM': 'vx_enum',
'ETC...': 'etc...'
}
```

## Tasks

### Create kernel tables
Create tables and means of accessing them for all standard kernels. This is a relatively trivial but time-consuming task. Note however that the language used to describe the attribute conditions and the parameter matching conditions requires definition before this data is input.

### Create data tables
Again, a time-consuming task.

### Code for handling the basic types
Convert to and from all basic types, with suitable rounding etc.

### Condition interpreter
Code for interpreting the attribute requirements and the parameter matching conditions in the kernel table. This is a non-trivial task and will also require definition of the language used for these condition

### Code to establish suitability of a connection
This code will handle the tables and the conditions, giving an answer of true or false as to whether an object may be connected to another.

### Code to propagate attributes
Code which defines attributes for virtual data along a graph both forwards or backwards, to establish whether a non-virtual data object may be connected, or what attributes a newly connected  data object may have.

### Convert XML
This API takes and XML root node pointer and builds a representation in graphviz with attribute references back to the xml. Based upon the Khronos OpenVX sample implementation of vx_xml_import.c, either by modifying the C code or writing the whole in Python.

```C
Agraph_t *xml2dot(xmlNodePtr root);
```

```python
xml2dot(xmlRootNode) # returns Agraph_t
```

### Display graph
This API takes the graphviz representation, does layout and renders to screen.

### Save XML
This API saves the current XML in either an existing or a new file.

### Export graph
This API does layout and renders the output to a file in given format (dot, png, etc.)

### Clear
This API clears all current information and creates an empty XML and an empty graphviz representation.

### Insert node
Add a vx_node to both the xml and graphviz representations.

### Insert data
Add non-virtual data object to xml and graphviz representations.

### Insert parameter
Add non-virtual data object to xml and graphviz representations and associate with a node and kernel parameter.

### Connect Data
Connects a data object with a node kernel parameter in both representations.

### Connect Node
Inserts a new virtual data object into the xml representation, and connects it to a node kernel output parameter, if it does not already exist. Connects nodes together in the graphviz representation, connects the data object to node kernel input parameter input in the xml representation.

### Disconnect Data
Disconnect a connection between a non-virtual data object in both the xml and graphviz representations. If the data object was a graph parameter and it is no longer connected to any nodes, remove it.

### Disconnect Node
Disconnect two nodes in the graphviz representation. In the XML representation, disconnect a kernel parameter input from a virtual data object. If the only remaining connection to the object is a writer, then remove the virtual object.

### Remove Data
Remove the object and associated connections from both representations.

### Remove Node
Remove the object and associated connections from both representations. If this leaves a virtual data object with no writer, remove it.

### Select
Chooses an object in the graphviz representation to have the focus, which changes the way that it is drawn. Updates internal pointer to this object as the selected object.

### Toggle Virtual
 * If the object is a node, invoke the Object selector dialog to choose a connected parameter
 * If the object now selected is virtual, In the XML representation, remove it to outside of the graph as a non-virtual and in the graphviz representation insert a new non-virtual data object with the correct connections.
 * If the now selected object is not virtual, then the operation is not allowed if:
 ** The object is a graph parameter
 ** The object has no connections
 ** The object is connected to more than one graph (should not be possible to create this anyway using the tool, but could be imported)
 * Otherwise, in the XML representation make the object virtual by moving it inside the graph to which is is connected, and in the graphviz representation remove the object and fix up the edges to connect nodes directly.

### Edit Data
Several dialogs to edit data of various types, chosen for the currently selected object.

### Display Data
Several data display windows to display data of various types, chosen for the currently selected object.

### Object selector
Dialog to select an object compatible with input conditions, and optionally further to select a node kernel parameter.

##  Kernel Selector
List box to select a kernel, allows typing and word completion (eg typing 'o' at the start will most likely populate as 'org.khronos.openvx.'

### File open dialog
To select .xml files.

### File save dialog
.xml files, or other files as required for export.

### File save as dialog
.xml files.

### Load and Save kernel definitions
Save/Load custom kernel definitions to/from a settings file

### Load and Save preferences
Save/Load preferences to/from a settings file

### Preferences dialog
Allow such things as shapes and colours for different graph objects to be configured. Also allow custom kernels and data types to be configured.

### Program framework

The program framework creates windows able to display the graph, to take text input, and commands via menus.
Can be written in Python, C, or C++.


## Example OpenVX graph in dot language


Visualization of simple lane departure graph
```[graphviz,lane_departure,png
digraph "lane departure" {
data0[shape=box,style="bold,rounded",label="Input Image (RGB)", color=blue]
node1[label="Channel Extract R"]
node2[label="Channel Extract G"]
node3[label="Channel Extract B"]
node4[label="Add"]
node5[label="Subtract"]
data6[shape=box,style=dotted,fontsize=10,label="VX_CONVERT_POLICY_SATURATE"]
data7[shape=box,style=dotted,fontsize=10,label="VX_CHANNEL_R"]
data8[shape=box,style=dotted,fontsize=10,label="VX_CHANNEL_G"]
data9[shape=box,style=dotted,fontsize=10,label="VX_CHANNEL_B"]
data0->node1, node2, node3[headlabel=input,fontsize=9,fontcolor=blue,arrowhead=empty]
data7->node2[headlabel=channel,fontsize=9,fontcolor=blue,arrowhead=empty]
data8->node3[headlabel=channel,fontsize=9,fontcolor=blue,arrowhead=empty]
data9->node1[headlabel=channel,fontsize=9,fontcolor=blue,arrowhead=empty]
data6->node4[headlabel=policy,fontsize=9,fontcolor=blue,arrowhead=empty]
node2->node4[taillabel=output,headlabel=in1,fontsize=9,fontcolor=blue,arrowhead=empty]
node3->node4[taillabel=output,headlabel=in2,fontsize=9,fontcolor=blue,arrowhead=empty]
node4->node5[taillabel=output,headlabel=in1,fontsize=9,fontcolor=blue,arrowhead=empty]
node1->node5[taillabel=output,headlabel=in2,fontsize=9,fontcolor=blue,arrowhead=empty]
data6->node5[headlabel=policy,fontsize=9,fontcolor=blue,arrowhead=empty]
node10[label="Sobel3x3"]
node11[label="Canny"]
node5->node10[taillabel=output,headlabel=input,fontsize=9,fontcolor=blue,arrowhead=empty]
node5->node11[taillabel=output,headlabel=input,fontsize=9,fontcolor=blue,arrowhead=empty]
data12[shape=box,style=dotted,fontsize=10,label="VX_TYPE_THRESHOLD"]
data13[shape=box,style=dotted,fontsize=10,label="VX_NORM_L1"]
data14[shape=box,style=dotted,fontsize=10,label="5"]
data12->node11[headlabel=hyst,fontsize=9,fontcolor=blue,arrowhead=empty]
data13->node11[headlabel=norm_type,fontsize=9,fontcolor=blue,arrowhead=empty]
data14->node11[headlabel=gradient_size,fontsize=9,fontcolor=blue,arrowhead=empty]
node15[label="Phase"]
node16[label="Hough Lines User Node"]
node10->node15[taillabel=output_x,headlabel=grad_x,fontsize=9,fontcolor=blue,arrowhead=empty]
node10->node15[taillabel=output_y,headlabel=grad_y,fontsize=9,fontcolor=blue,arrowhead=empty]
node15->node16[taillabel=orientation,headlabel=orientation,fontsize=9,fontcolor=blue,arrowhead=empty]
node11->node16[taillabel=output,headlabel=edges,fontsize=9,fontcolor=blue,arrowhead=empty]
data17[shape=box,style="bold,rounded",color=blue,label="Output array"]
node16->data17[taillabel=output,fontsize=9,fontcolor=blue,arrowhead=empty]
}
```
