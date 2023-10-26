"""
How to modify architectures of fusion models
############################################

This tutorial will show you how to modify the architectures of fusion models.

More guidance on what can be modified in each fusion model can be found in the :ref:`modifying-models` section.

.. warning::

    Some of the fusion models have been designed to work with specific architectures and there are some restrictions on how they can be modified.

    For example, the channel-wise attention model requires the two modalities to have the same number of layers. Please read the notes section of the fusion model you are interested in to see if there are any restrictions.

"""

# %%
# Setting up the experiment
# -------------------------
#
# First, we will set up the experiment by importing the necessary packages, creating the simulated data, and setting the parameters for the experiment.
#
# For a more detailed explanation of this process, please see the :ref:`train_test_examples` tutorials.
#

import matplotlib.pyplot as plt
import os

from docs.examples import generate_sklearn_simulated_data
from fusilli.data import get_data_module
from fusilli.eval import RealsVsPreds
from fusilli.train import train_and_save_models

from fusilli.fusionmodels.tabularimagefusion.denoise_tab_img_maps import DAETabImgMaps

params = {
    "test_size": 0.2,
    "kfold_flag": False,
    "log": False,
    "pred_type": "regression",
    "loss_log_dir": "loss_logs",  # where the csv of the loss is saved for plotting later
}

params = generate_sklearn_simulated_data(
    num_samples=500,
    num_tab1_features=10,
    num_tab2_features=10,
    img_dims=(1, 100, 100),
    params=params,
)

# %%
# Specifying the model modifications
# ----------------------------------
#
# Now, we will specify the modifications we want to make to the model.
#
# We are using the :class:`~fusilli.fusionmodels.tabularimagefusion.denoise_tab_img_maps.DAETabImgMaps` model for this example.
# This is a subspace-based model which has two PyTorch models that need to be pretrained (a denoising autoencoder for the tabular modality, and a convolutional neural network for the image modality).
# The fusion model then uses the latent representations of these models to perform the fusion.
#
# The following modifications can be made to the model:
#
# .. list-table::
#   :widths: 40 60
#   :header-rows: 1
#   :stub-columns: 0
#
#   * - Attribute
#     - Guidance
#   * - :attr:`.autoencoder.latent_dim`
#     - int
#   * - :attr:`.autoencoder.upsampler`
#     - ``nn.Sequential``
#   * - :attr:`.autoencoder.downsampler`
#     - ``nn.Sequential``
#   * - :attr:`.img_unimodal.img_layers`
#     -
#       * ``nn.Sequential``
#       * Overrides modification of ``img_layers`` made to "all"
