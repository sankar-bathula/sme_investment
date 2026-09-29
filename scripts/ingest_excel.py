from app.ingestion.excel_loader import load_excel


if __name__ == "__main__":
    file_path = r"E:\Finance\Dev\sme_investment\data\samples\NASDAQ 08 Aug 2026 v 1.0.xlsx"

    print(f"Loading Excel file: {file_path}")

    result = load_excel(file_path)

    print("\nExcel loading completed.")
    print(result)

