# clearvision

Private project started some time ago and abandoned a short time later. I think it was actually python 2.7 at the time...

Some parts of this could be salvaged?

There's a number of issues in the code as it is - for example you can easily connect outputs to inputs of a node. But it is interesting in a sort of way.

Maybe what could also be interesting is a way to define graphs etc in Yaml.

I converted googlnet.xml to googlenet.yaml using an online converter https://onlineyamltools.com/convert-xml-to-yaml

The result is not so good, and highlights the issues. Mostly, things need to be named not numbered, and there should be some sensible defaults for things left unsaid.
It could also be useful to be able to specify a connection directly node to node where an edge is completely virtual, i.e. an in-line definition of the virtual object; this could be easier for human readers.

This project is very much Work In Progress. The file ClearVision_issues.adoc contains a list of stuff to be done, there is some project management to be done here!
