# clearvision

The purpose of this project is to provide a simple creation and visualisation and tool for OpenVX graphs.
Currently Output and input are both in the form of XML readable by the XML extension; I would change this to YAML.
Another goal is to auto-generate C code for graph factories.

There's a number of issues in the code as it is - for example you can easily connect outputs to inputs of a node, and this should be disallowed.

This project is very much Work In Progress. The file ClearVision_issues.adoc contains a list of stuff to be done, there is some project management to be done here!
