import torch.nn as nn
from fusionlibrary.fusion_models.base_pl_model import ParentFusionModel
import torch


class TabularDecision(ParentFusionModel, nn.Module):
    """
    This class implements a model that fuses the two types of tabular data using a decision fusion
        approach.

    Attributes
    ----------
    fusion_type : str
        Type of fusion to be performed.
    modality_type : str
        Type of modality to be fused.
    method_name : str
        Name of the method.
    mod1_layers : dict
        Dictionary containing the layers of the 1st type of tabular data.
    mod2_layers : dict
        Dictionary containing the layers of the 2nd type of tabular data.
    fused_layers : nn.Sequential
        Sequential layer containing the fused layers.
    final_prediction : nn.Sequential
        Sequential layer containing the final prediction layers.

    Methods
    -------
    forward(x)
        Forward pass of the model.
    """

    def __init__(self, pred_type, data_dims, params):
        """
        Parameters
        ----------
        pred_type : str
            Type of prediction to be performed.
        data_dims : dict
            Dictionary containing the dimensions of the data.
        params : dict
            Dictionary containing the parameters of the model.

        """
        ParentFusionModel.__init__(self, pred_type, data_dims, params)
        self.method_name = "TabularDecision"
        self.modality_type = "both_tab"
        self.fusion_type = "operation"
        self.pred_type = pred_type

        self.set_mod1_layers()
        self.set_mod2_layers()

        self.set_final_pred_layers(256)

    def forward(self, x):
        """
        Forward pass of the model.

        Parameters
        ----------
        x : list
            List containing the two types of tabular data.

        Returns
        -------
        list
            List containing the fused prediction."""
        x_tab1 = x[0]
        x_tab2 = x[1]

        for i, (k, layer) in enumerate(self.mod1_layers.items()):
            x_tab1 = layer(x_tab1)
            x_tab2 = self.mod2_layers[k](x_tab2)

        # predictions for each method
        pred_tab1 = self.final_prediction(x_tab1)
        pred_tab2 = self.final_prediction(x_tab2)

        # Combine predictions by averaging them together
        out_fuse = torch.mean(torch.stack([pred_tab1, pred_tab2]), dim=0)

        return [
            out_fuse,
        ]
