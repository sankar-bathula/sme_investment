from abc import ABC, abstractmethod
from typing import Any


class DataConnector(ABC):
    """
    Base interface for all data connectors.

    Every connector should:
        1. Validate its source
        2. Read/extract data
        3. Return standardized raw records
        4. Provide source metadata

    Examples:
        ExcelConnector
        CSVConnector
        JSONConnector
        APIConnector
        PDFConnector
        WebConnector
    """

    @abstractmethod
    def validate_source(self) -> None:
        """
        Validate whether the source is available and supported.

        Raises:
            FileNotFoundError:
                Source does not exist.

            ValueError:
                Source format/configuration is invalid.
        """
        raise NotImplementedError

    @abstractmethod
    def read(self) -> list[dict[str, Any]]:
        """
        Read data from the source.

        Returns:
            List of records represented as dictionaries.
        """
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> dict[str, Any]:
        """
        Return metadata describing the source.

        Example:
            {
                "source_type": "excel",
                "file_name": "sme.xlsx"
            }
        """
        raise NotImplementedError

    def connect(self) -> None:
        """
        Optional connection step.

        Useful for API/database connectors.

        File connectors may not need this.
        """
        return None

    def close(self) -> None:
        """
        Optional cleanup step.

        Useful for API/database connections.
        """
        return None

    def run(self) -> dict[str, Any]:
        """
        Execute the complete connector lifecycle.

        Returns:
            {
                "metadata": {...},
                "records": [...]
            }
        """

        self.validate_source()

        self.connect()

        try:
            records = self.read()

            return {
                "metadata": self.get_metadata(),
                "records": records,
            }

        finally:
            self.close()