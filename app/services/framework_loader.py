from pathlib import Path
from typing import Union
import yaml
from app.models.framework import Framework




class FrameworkLoader:

    @staticmethod
    def load(path: Union[str, Path]) -> Framework:
        framework_path = Path(path)

        if not framework_path.exists():
            raise FileNotFoundError(f"Framework file not found: {path}")

        with framework_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

            return Framework.model_validate(data)
        

   
       



    