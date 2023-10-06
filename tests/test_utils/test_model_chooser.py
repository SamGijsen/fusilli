import pytest
from unittest.mock import patch, MagicMock, Mock
from fusilli.utils.model_chooser import model_importer, get_models

fusion_model_dict = [
    {
        "name": "Model1",
        "path": "path1",
    },
    {
        "name": "Model2",
        "path": "path2",
    },
    {
        "name": "Model3",
        "path": "path3",
    },
    {
        "name": "Model4",
        "path": "path4",
    },
    {
        "name": "Model5",
        "path": "path5",
    },
]


@patch("importlib.import_module")
def test_model_importer(mock_import_module):
    mock_module1 = Mock()
    mock_module1.Model1 = Mock(
        modality_type="tabular1",
        __name__="Model1",
        fusion_type="Uni-modal",
    )

    mock_module2 = Mock()
    mock_module2.Model2 = Mock(
        __name__="Model2", modality_type="img", fusion_type="operation"
    )

    mock_module3 = Mock()
    mock_module3.Model3 = Mock(
        __name__="Model3", modality_type="tabular2", fusion_type="attention"
    )

    mock_module4 = Mock()
    mock_module4.Model4 = Mock(
        __name__="Model4", modality_type="both_tab", fusion_type="subspace"
    )

    mock_module5 = Mock()
    mock_module5.Model5 = Mock(
        __name__="Model5", modality_type="both_tab", fusion_type="attention"
    )

    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]

    fusion_models = model_importer(fusion_model_dict)

    assert len(fusion_models) == 5
    assert fusion_models[0].__name__ == "Model1"
    assert fusion_models[1].__name__ == "Model2"
    assert fusion_models[2].__name__ == "Model3"
    assert fusion_models[3].__name__ == "Model4"
    assert fusion_models[4].__name__ == "Model5"


@patch("importlib.import_module")
def test_get_models(mock_import_module):
    mock_module1 = Mock()
    mock_module1.Model1 = Mock(
        modality_type="tabular1",
        __name__="Model1",
        fusion_type="Uni-modal",
    )

    mock_module2 = Mock()
    mock_module2.Model2 = Mock(
        __name__="Model2", modality_type="img", fusion_type="operation"
    )

    mock_module3 = Mock()
    mock_module3.Model3 = Mock(
        __name__="Model3", modality_type="tabular2", fusion_type="attention"
    )

    mock_module4 = Mock()
    mock_module4.Model4 = Mock(
        __name__="Model4", modality_type="both_tab", fusion_type="subspace"
    )

    mock_module5 = Mock()
    mock_module5.Model5 = Mock(
        __name__="Model5", modality_type="both_tab", fusion_type="attention"
    )

    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]

    # 2 models have modality type of both_tab
    conditions_dict = {
        "modality_type": "both_tab",
    }

    filtered_models = get_models(conditions_dict, fusion_model_dict)
    assert len(filtered_models) == 2  # Two mock models satisfy the conditions

    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]

    # 1 model has modality type of both_tab and fusion type of attention
    conditions_dict = {
        "modality_type": "both_tab",
        "fusion_type": "attention",
    }

    filtered_models = get_models(conditions_dict, fusion_model_dict)
    assert len(filtered_models) == 1

    # 0 models have modality type of both_tab and fusion type of tensor
    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]

    conditions_dict = {
        "modality_type": "both_tab",
        "fusion_type": "tensor",
    }

    with pytest.warns(UserWarning, match="No models match the specified conditions."):
        filtered_models = get_models(conditions_dict, fusion_model_dict)

    # with invalid features
    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]
    conditions_dict = {
        "modality_type": "both_tab",
        "fusion_type": "tensor",
        "invalid_feature": "invalid_value",
    }

    with pytest.raises(ValueError, match=r"Invalid feature"):
        filtered_models = get_models(conditions_dict, fusion_model_dict)

    # invalid fusion_type
    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]
    conditions_dict = {
        "modality_type": "both_tab",
        "fusion_type": "invalid_fusion_type",
    }

    with pytest.raises(ValueError, match=r"Invalid fusion type for feature"):
        filtered_models = get_models(conditions_dict, fusion_model_dict)

    # invalid modality_type
    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]
    conditions_dict = {
        "modality_type": "invalid_modality_type",
        "fusion_type": "attention",
    }

    with pytest.raises(ValueError, match=r"Invalid modality type for feature"):
        filtered_models = get_models(conditions_dict, fusion_model_dict)

    # check it works for "all"
    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]
    conditions_dict = {
        "modality_type": "all",
        "fusion_type": "attention",
    }

    filtered_models = get_models(conditions_dict, fusion_model_dict)
    assert len(filtered_models) == 2  # 2 models have fusion type of attention

    # check it works for "all"
    mock_import_module.side_effect = [
        mock_module1,
        mock_module2,
        mock_module3,
        mock_module4,
        mock_module5,
    ]
    conditions_dict = {
        "modality_type": "both_tab",
        "fusion_type": "all",
    }

    filtered_models = get_models(conditions_dict, fusion_model_dict)
    assert len(filtered_models) == 2  # 2 models have modality type of both_tab


if __name__ == "__main__":
    pytest.main()
