"""
Fusion Model Template: Graph-based Fusion
=========================================

This template is for creating your own fusion model that is graph-based. An example of a graph-based fusion model is :class:`~fusilli.fusionmodels.tabularfusion.edge_corr_gnn.EdgeCorrGNN`.

.. note::

    I recommend looking at :ref:`how_to_contribute_a_template_other_fusion` before looking at this template, as I will skip over some of the details that are covered in that template (particularly regarding documentation and idiosyncrasies of the fusion model template).


Building a graph-based fusion model is a bit different to the general template in
:ref:`how_to_contribute_a_template_other_fusion`. The main difference is that you need to create a method that will create the graph structure from the input data.

For the :class:`~fusilli.fusionmodels.tabularfusion.edge_corr_gnn.EdgeCorrGNN`, this is done in the :class:`~fusilli.fusionmodels.tabularfusion.edge_corr_gnn.EdgeCorrGraphMaker` class, which is in the same ``.py`` file as the :class:`~fusilli.fusionmodels.tabularfusion.edge_corr_gnn.EdgeCorrGNN` class.

First, let's look at creating the graph-maker class.
"""

# %%
# Creating the Graph-Maker Class
# ------------------------------
#
# The graph will probably be created with the ``PyTorch Geometric`` library, which is a library for creating graph-based models in PyTorch.
#
# Let's import the libraries that we need:

import numpy as np
import torch
import torch.nn as nn

from torch_geometric.data import Data

from fusilli.fusionmodels.base_model import ParentFusionModel
from fusilli.utils import check_model_validity


# %%
# Now let's create the graph-maker class.
#
# The graph-maker class must have the following methods:
#
# - ``__init__``: This method initialises the graph-maker class. It must take a ``torch.utils.data.Dataset`` as an argument (created in :meth:`.TrainTestGraphDataModule.setup` or :meth:`.KFoldGraphDataModule.setup`).
# - ``check_params``: This method checks the parameters of the graph-maker class. It should raise a ``ValueError`` if the parameters are invalid. This will check validity of any modifications made to the model as well.
# - ``make_graph``: This method creates the graph data structure. It must return a ``torch_geometric.data.Data`` object.
#
#


class TemplateGraphMaker:
    def __init__(self, dataset):
        self.dataset = dataset

        # other attributes for the graph maker go here

    def check_params(self):
        # check the parameters of the graph maker here

        pass

    def make_graph(self):
        # create the graph here with self.dataset

        self.check_params()

        modality_1_data = self.dataset[:][0]
        modality_2_data = self.dataset[:][1]
        labels = self.dataset[:][2]

        # some code to create the graph to get out:
        # - node attributes
        # - edge attributes
        # - edge indices

        # replace the strings with the actual graph data

        data = Data(
            x="node attributes",
            edge_attr="edge attributes",
            edge_index="edge indices",
            y="labels"
        )

        return data


# %%
# Creating the Fusion Model Class
# -------------------------------
#
# Now let's create the fusion model class that will take in the graph data structure and perform the prediction.
#
# In addition to the class-level attributes for every fusion model, a graph-based fusion model class **must** have a class-level attribute ``graph_maker`` that is the graph-maker class that we created above.
#
# Very similar to the general fusion model template in :ref:`how_to_contribute_a_template_other_fusion`, the fusion model class must have the following methods:
#
# - ``__init__``: initialising with input parameters ``pred_type``, ``data_dims``, and ``params``.
# - ``calc_fused_layers``: checking the parameters of the fusion model if they're modified and recalculate the layers of the fusion model where necessary.
# - ``forward``: the forward pass of the fusion model. Takes ``x`` as input but in this example, this is a tuple of the node features, edge indices, and edge attributes.
#
# .. note::
#
#   The graph-maker class returns a ``torch_geometric.data.Data`` object, but in :func:`~.get_data_module`, this is converted to ``torch_geometric.data.lightning.LightningNodeData`` object, which lets you use the ``torch_geometric`` library with PyTorch Lightning.
#

from torch_geometric.nn import GCNConv


class TemplateGraphFusionModel(ParentFusionModel, nn.Module):
    method_name = "Template Graph Fusion Model"
    modality_type = "both_tab"
    fusion_type = "graph"

    graph_maker = TemplateGraphMaker

    def __init__(self, pred_type, data_dims, params):
        ParentFusionModel.__init__(self, pred_type, data_dims, params)

        self.pred_type = pred_type

        # create some graph convolutional layers here. For example, GCNConv from PyTorch Geometric
        self.graph_layers = nn.Sequential(
            GCNConv(1, 64),
            GCNConv(64, 128),
            GCNConv(128, 256),
        )

        self.calc_fused_layers()

    def calc_fused_layers(self):
        # checks on the parameters of the fusion model go here

        # calculate the final prediction layer here and the input dimension for it

        self.fused_dim = 256  # for example

        self.set_final_pred_layers(self.fused_dim)

    def forward(self, x):
        # x is a tuple of the node features, edge indices, and edge attributes
        x_n, edge_index, edge_attr = x

        for layer in self.graph_conv_layers:
            x_n = layer(x_n, edge_index, edge_attr)
            x_n = x_n.relu()

        out = self.final_prediction(x_n)

        # must return a list of outputs

        return [
            out,
        ]
