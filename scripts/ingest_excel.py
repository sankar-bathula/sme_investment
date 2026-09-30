from pathlib import Path

from app.ingestion.excel_loader import load_excel


SUPPORTED_EXTENSIONS = {
    ".xlsx",
    ".xls",
}


def main():
    project_root = Path(__file__).resolve().parent.parent
    print(f"Project root: {project_root}")

    input_folder = (
        project_root
        / "data"
        / "samples"
    )

    print("=" * 70)
    print("SME Investment - Multiple Excel File Ingestion")
    print("=" * 70)

    print(f"Input folder: {input_folder}")
    print()

    if not input_folder.exists():
        raise FileNotFoundError(
            f"Input folder not found: {input_folder}"
        )

    # Find all Excel files
    excel_files = sorted(
        file
        for file in input_folder.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not excel_files:
        print("No Excel files found.")
        return

    print(f"Found {len(excel_files)} Excel file(s).")
    print()

    total_processed = 0
    total_inserted_companies = 0
    total_updated_companies = 0
    total_inserted_securities = 0
    total_updated_securities = 0
    total_inserted_market_data = 0
    total_updated_market_data = 0
    total_inserted_financials = 0
    total_updated_financials = 0
    total_inserted_performance = 0
    total_updated_performance = 0
    total_inserted_recommendations = 0
    total_updated_recommendations = 0

    for index, excel_file in enumerate(excel_files, start=1):

        print("-" * 70)
        print(
            f"[{index}/{len(excel_files)}] "
            f"Processing: {excel_file.name}"
        )
        print("-" * 70)

        try:
            result = load_excel(str(excel_file))

            print(
                f"Status: {result.get('status')}"
            )

            print(
                f"Processed rows: "
                f"{result.get('processed_rows', 0)}"
            )

            total_processed += result.get(
                "processed_rows", 0
            )

            total_inserted_companies += result.get(
                "inserted_companies", 0
            )

            total_updated_companies += result.get(
                "updated_companies", 0
            )

            total_inserted_securities += result.get(
                "inserted_securities", 0
            )

            total_updated_securities += result.get(
                "updated_securities", 0
            )

            total_inserted_market_data += result.get(
                "inserted_market_data", 0
            )

            total_updated_market_data += result.get(
                "updated_market_data", 0
            )

            total_inserted_financials += result.get(
                "inserted_financials", 0
            )

            total_updated_financials += result.get(
                "updated_financials", 0
            )

            total_inserted_performance += result.get(
                "inserted_performance", 0
            )

            total_updated_performance += result.get(
                "updated_performance", 0
            )

            total_inserted_recommendations += result.get(
                "inserted_recommendations", 0
            )

            total_updated_recommendations += result.get(
                "updated_recommendations", 0
            )

            print("Completed.")

        except Exception as exc:
            print(
                f"ERROR processing "
                f"{excel_file.name}: {exc}"
            )

    print()
    print("=" * 70)
    print("INGESTION SUMMARY")
    print("=" * 70)

    print(f"Files processed              : {len(excel_files)}")
    print(f"Rows processed               : {total_processed}")

    print()
    print("Companies")
    print(f"  Inserted                   : {total_inserted_companies}")
    print(f"  Updated                    : {total_updated_companies}")

    print()
    print("Securities")
    print(f"  Inserted                   : {total_inserted_securities}")
    print(f"  Updated                    : {total_updated_securities}")

    print()
    print("Market Data")
    print(f"  Inserted                   : {total_inserted_market_data}")
    print(f"  Updated                    : {total_updated_market_data}")

    print()
    print("Financial Metrics")
    print(f"  Inserted                   : {total_inserted_financials}")
    print(f"  Updated                    : {total_updated_financials}")

    print()
    print("Performance Metrics")
    print(f"  Inserted                   : {total_inserted_performance}")
    print(f"  Updated                    : {total_updated_performance}")

    print()
    print("Recommendations")
    print(
        f"  Inserted                   : "
        f"{total_inserted_recommendations}"
    )
    print(
        f"  Updated                    : "
        f"{total_updated_recommendations}"
    )

    print()
    print("=" * 70)
    print("Multiple-file ingestion completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()