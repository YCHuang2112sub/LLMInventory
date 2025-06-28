import sys
from pathlib import Path

# Add the 'src' directory to the Python path so that modules within 'llminventory'
# can be imported correctly during testing.
# This allows imports like 'from src.llminventory.model_config_manager import ModelConfigManager'
# to resolve correctly when pytest is run from the project root.

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))