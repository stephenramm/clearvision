"""This module contains the testobject object."""

import wx
import pygraphviz as pgv
import cvxKernelDefs as kdefs
import cvxXML as bG

def Test():
    # Add a new node to the current graph. We choose optical flow...
    nb = wx.GetApp().frame.nb
    p = nb.GetCurrentPage()
    if nb.GetPageText(nb.GetSelection()) == bG.globalsName:
        wx.GetApp().frame.Error("Cannot insert node in %s; use a graph tab"%bG.globalsName)
    else:
        for kernel in list(kdefs.standardKernels.keys()):
            bG.insertNode(p.element, p.graph, kernel)
        nb.GetGlobalsPage().Redraw()
        p.Redraw()
        p.Refresh()

    # Attempt to update the bitmap in the tab with some other content:
    # G = pgv.AGraph(directed=True)
    # G.edge_attr['dir'] = 'both'
    # G.edge_attr['arrowtail'] = 'dot'
    # G.add_node('insert',label='insert command')
    # G.add_node('knode',label='node command')
    # G.add_node('data',label='data command')
    # G.add_node('parameter', label='parameter command')
    # G.add_node('kernel_selector', label='Kernel selection dialog')
    # G.add_node('data_type_selector', label='Data object selection dialog')
    # G.add_node('port_selector', label='Parameter selection dialog')
    # G.add_node('ready', label='Ready state with graph')
    # G.add_node('cleared', label='Ready state without graph')
    # G.add_node('selected', label='Ready state with object selected')
    # G.add_node('draw_graph', label='Clear and redraw graph,\n'
    #                 'with selection highlighted')
    # G.add_node('object_selector', label='Object selection dialog')
    # G.add_edge('ready','insert')
    # G.add_edge('selected','insert')
    # G.add_edge('cleared','insert')
    # G.add_edge('insert', 'knode')
    # G.add_edge('insert', 'data')
    # G.add_edge('insert', 'parameter')
    # G.add_edge('knode','kernel_selector')
    # G.add_edge('kernel_selector', 'draw_graph')
    # G.add_edge('draw_graph', 'selected')
    # G.add_edge('data', 'data_type_selector')
    # G.add_edge('data_type_selector', 'draw_graph')
    # G.add_edge('parameter', 'object_selector')
    # G.add_edge('object_selector', 'port_selector')
    # G.add_edge('port_selector', 'draw_graph')
    # G.add_edge('object_selector', 'draw_graph', taillabel='dialog cancelled', fontsize=9, fontcolor='blue', labelangle=0)
    # G.draw('newTest.png', prog='dot')
    # wx.GetApp().frame.nb.GetCurrentPage().bitmap = wx.Bitmap('newTest.png')


