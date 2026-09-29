from app.connectors.files.excel import ExcelConnector


def main():
    connector = ExcelConnector(
        "data/samples/NASDAQ 08 Aug 2026 v 1.0.xlsxcd"
    )

    result = connector.run()

    print("Metadata:")
    print(result["metadata"])

    print("\nRecords:")

    for record in result["records"]:
        print(record)


if __name__ == "__main__":
    main()