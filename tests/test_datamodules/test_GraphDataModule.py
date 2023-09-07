import pytest
from fusionlibrary.datamodules import GraphDataModule
from .test_CustomDataModule import create_test_files
from pytest import approx


class MockGraphMakerModule:
    def __init__(self, graph_data):
        self.graph_data = graph_data

    def make_graph(self):
        return self.graph_data


@pytest.fixture
def create_graph_data_module(create_test_files):
    params = {
        "test_size": 0.3,
        "pred_type": "binary",
        "multiclass_dims": None,
    }

    tabular1_csv = create_test_files["tabular1_csv"]
    tabular2_csv = create_test_files["tabular2_csv"]
    image_torch_file_2d = create_test_files["image_torch_file_2d"]

    sources = [tabular1_csv, tabular2_csv, image_torch_file_2d]
    batch_size = 23
    modality_type = "both_tab"

    data_module = GraphDataModule(
        params,
        modality_type,
        sources,
        graph_creation_method=MockGraphMakerModule,
    )

    return data_module


# Write test functions
def test_prepare_data(create_graph_data_module):
    # Create a GraphDataModule instance with test parameters
    datamodule = create_graph_data_module

    # Call the prepare_data method
    datamodule.prepare_data()

    # Add assertions to check the expected behavior
    assert len(datamodule.dataset) > 0
    assert datamodule.data_dims == [2, 2, None]  # Adjust based on your data dimensions


def test_setup(create_graph_data_module, mocker):
    # Create a GraphDataModule instance with test parameters
    datamodule = create_graph_data_module
    datamodule.prepare_data()

    mocker.patch.object(
        MockGraphMakerModule, "make_graph", return_value="mock_graph_data"
    )

    # Call the setup method
    datamodule.setup()

    # Assert length of train and test indices is consistent with the test size
    assert len(datamodule.train_idxs) == approx(
        (1 - datamodule.test_size) * len(datamodule.dataset)
    )
    assert len(datamodule.test_idxs) > 0

    # Assert that the graph data is not None and the graph maker is called
    MockGraphMakerModule.make_graph.assert_called_once()
    assert datamodule.graph_data is not None

    # Check if the train and test indices are disjoint
    assert set(datamodule.train_idxs).intersection(set(datamodule.test_idxs)) == set()


def test_get_lightning_module(create_graph_data_module):
    # Create a GraphDataModule instance with test parameters
    datamodule = create_graph_data_module
    datamodule.prepare_data()
    datamodule.setup()

    # Call the get_lightning_module method
    lightning_module = datamodule.get_lightning_module()

    # Add assertions to check the expected behavior of the lightning module
    assert lightning_module is not None


if __name__ == "__main__":
    pytest.main()
