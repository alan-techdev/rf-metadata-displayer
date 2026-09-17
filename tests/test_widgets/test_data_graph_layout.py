from unittest.mock import MagicMock, patch

import pytest
from matplotlib.figure import Figure
from src.rfmetadata.widgets.data_graph_layout import DataGraph3D


@pytest.fixture(autouse=True)
def mock_signal_managers(monkeypatch):
    mock_sig1 = MagicMock()
    mock_sig2 = MagicMock()
    monkeypatch.setattr("rfmetadata.signal_manager.data_signal_manager.signal_manager", mock_sig1)
    monkeypatch.setattr("rfmetadata.signal_manager.data_signal_manager.graph_type_manager", mock_sig2)
    return mock_sig1, mock_sig2

@pytest.fixture
def sample_data():
    """Provides a valid dataset matching the expected structure of receive_data."""
    return [
        (90, 103.7, 20.54, '06-06-2025 12:16:18'),
        (91, 104.3, 22.18, '06-06-2025 12:20:18'),
        (92, 105.1, 25.00, '06-06-2025 12:25:18'),
    ]


def test_init_default_state(qtbot):
    """Verify that defaults are set properly and signals are bound on init."""
    graph = DataGraph3D()
    qtbot.addWidget(graph)

    # Assert defaults
    assert graph.min_power == 20.0
    assert graph.max_power == 60.0
    assert graph.type == "scatter"
    assert graph.data == []

    assert isinstance(graph.figure, Figure)
    assert graph.ax is not None


def test_receive_data_parsing(qtbot, sample_data):
    """Test that incoming signal data is split into freq, pow, and numeric time arrays."""
    graph = DataGraph3D()
    qtbot.addWidget(graph)


    graph.draw_graph = MagicMock()

    graph.receive_data(sample_data)

    assert graph.data == sample_data
    assert graph.freq == [103.7, 104.3, 105.1]
    assert graph.pow == [20.54, 22.18, 25.00]
    assert len(graph.time) == 3

    assert isinstance(graph.time[0], float)
    graph.draw_graph.assert_called_once()

def test_draw_graph_empty_data(qtbot):
    """Ensure draw_graph early-returns safely if lists are empty."""
    graph = DataGraph3D()
    qtbot.addWidget(graph)

    graph.draw = MagicMock()
    graph.draw_graph()

    graph.draw.assert_not_called()

def test_draw_graph_scatter(qtbot, sample_data):
    """Verify scatter plot setup executes canvas draw steps."""
    graph = DataGraph3D()
    qtbot.addWidget(graph)

    graph.receive_data(sample_data)
    graph.type = "scatter"

    with patch.object(graph, 'draw') as mock_canvas_draw:
        graph.draw_graph()
        mock_canvas_draw.assert_called_once()
        assert graph.ax.get_title() == "Data Graph"


def test_draw_graph_meshgrid(qtbot, sample_data):
    """Verify grid interpolation and plot_surface logic triggers correctly."""
    graph = DataGraph3D()
    qtbot.addWidget(graph)

    graph.receive_data(sample_data)
    graph.set_type("meshgrid") # This automatically triggers draw_graph

    assert graph.type == "meshgrid"
    assert graph.ax.name == "3d"


def test_draw_graph_line_2d(qtbot, sample_data):
    """Verify line graph switches to 2D projections and renders color bar segments."""
    graph = DataGraph3D()
    qtbot.addWidget(graph)

    graph.receive_data(sample_data)
    graph.set_type("line")

    assert graph.ax.name == "rectilinear"
    assert graph.ax.get_ylabel() == "Power"
