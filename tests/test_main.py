import pytest
from src import run

def test_run_initialization():
    """
    Test if the run script initializes without throwing any errors.
    """
    try:
        result = run.main()  # Supondo que run.py tem uma função main()
        assert result is not None  # Ou qualquer outra lógica de verificação
    except Exception as e:
        pytest.fail(f"run.py failed to initialize: {str(e)}")
