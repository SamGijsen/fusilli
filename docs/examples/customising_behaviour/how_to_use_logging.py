"""
How to use Weights and Biases Logging with Fusilli
###################################################

When running fusilli, if ``params["log"] = True``, fusilli will log the training and validation behaviour to Weights and Biases. This is done by using the ``wandb`` library.

Weights and Biases is a free tool that allows you to track your machine learning experiments. To use fusilli with Weights and Biases, you will need to create a Weights and Biases account and log into it. You can do this by following the instructions `here <https://docs.wandb.ai/quickstart>`_.

More info on how fusilli uses WandB can be found in the function :func:`~fusilli.utils.training_utils.set_logger`, but basically:

#. If ``params["log"] = True``, fusilli will log the training and validation behaviour to Weights and Biases. If ``params["log"] = False``, fusilli will plot the loss curves using matplotlib and save as png files locally.
#. Fusilli will create a project in your WandB account with the name ``params["project_name"]``. If this project already exists, fusilli will use it. If it doesn't, fusilli will create it. If ``params["project_name"]`` is not specified, fusilli will create a project with the name ``"fusilli"``.
#. If you're rerunning fusion models with different parameters, these runs will be grouped by the fusion model's name.
#. Each run is tagged with the modality type and fusion type of the fusion model by default, but you can add your own tags by specifying ``extra_log_string_dict`` into :func:`~fusilli.train.train_and_save_models`.
#. If you're using k-fold cross validation, each fold will be logged as a separate run grouped by the fusion model's name, and tagged with the current fold number.


Now I'll show you an example of specifying ``extra_log_string_dict`` into :func:`~fusilli.train.train_and_save_models` if I wanted to run :class:`~.EdgeCorrGNN` fusion model with :attr:`~.EdgeCorrGNN.dropout_prob` as 0.2 and I wanted to log this to Weights and Biases.

.. note::

    For more info on modifying the models in fusilli (such as changing the dropout probability in :class:`~.EdgeCorrGNN`), see :ref:`modifying-models`.

.. code-block:: python

    # importing data and fusion models etc.

    fusion_model = EdgeCorrGNN

    modification = {
        "EdgeCorrGNN": {
            "dropout_prob": 0.2
        }
    }

    extra_string_for_wandb = {"dropout_prob": 0.5}

    trained_model = train_and_save_models(
        datamodule=datamodule,
        params=params,
        fusion_model=fusion_model,
        extra_log_string_dict=extra_string_for_wandb,
        layer_mods=modification
    )


When I train this and look at weights and biases, the run will be called ``EdgeCorrGNN_dropout_prob_0.2`` and will be tagged with ``dropout_prob_0.5``.


"""
