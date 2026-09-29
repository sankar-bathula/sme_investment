from pathlib import Path
from typing import Any

import pandas as pd

from app.connectors.base import DataConnector


class ExcelConnector(DataConnector):
    """
    Connector for reading Excel files.

    Responsibility:
        - Read Excel files
        - Select worksheet
        - Convert rows to dictionaries
        - Preserve source metadata

    It should NOT:
        - Insert into database
        - Apply business rules
        - Calculate investment metrics
        - Deduplicate records
    """

    def __init__(
        self,
        file_path: str,
        sheet_name: str | int = 0,
    ):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name

    def validate_source(self) -> None:
        """Validate that the Excel file exists and has a supported format."""

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Excel file not found: {self.file_path}"
            )

        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError(
                f"Unsupported Excel format: {self.file_path.suffix}"
            )

    def read(self) -> list[dict[str, Any]]:
        """Read Excel worksheet and return rows as dictionaries."""

        self.validate_source()

        df = pd.read_excel(
            self.file_path,
            sheet_name=self.sheet_name,
        )

        # Convert NaN / NaT to None
        df = df.where(pd.notna(df), None)

        records = df.to_dict(orient="records")

        return records

    def get_metadata(self) -> dict[str, Any]:
        """Return information about the source file."""

        self.validate_source()

        return {
            "source_type": "excel",
            "file_name": self.file_path.name,
            "file_path": str(self.file_path),
            "sheet_name": self.sheet_name,
            "file_size": self.file_path.stat().st_size,
        }