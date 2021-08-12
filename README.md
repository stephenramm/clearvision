# clearvision

Private project started some time ago and abandoned a short time later. I think it was actually python 2.7 at the time...

Some parts of this could be salvaged either as a front-end tool or just basis for importing openvx xml files?

There's a number of issues in the code as it is - for example you can easily connect outputs to inputs of a node. But it is interesting in a sort of way.

I converted googlnet.xml to googlenet.yaml using an online converter https://onlineyamltools.com/convert-xml-to-yaml

The result is not so good, and highlights the issues. Mostly, things need to be named not numbered, and there should be some sensible defaults for things left unsaid.
It would also be useful to be able to specify a connection directly node to node where an edge is completely virtual.

