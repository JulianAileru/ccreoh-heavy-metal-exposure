"""
Format the TIMEPOINT-1/2-All-Models.xlsx MWAS result workbooks for readability.

Each workbook has one sheet per metal (Hg, Pb, Se, Mn, Sn) with columns:
  feature, list_all_ids, list_all_library, highest_OL,
  coef/std_err/t_value/p_value/CI_lower/CI_upper/FDR_MWASModel,
  Candidate_MWASModel, Direction_MWASModel,
  coef/std_err/t_value/p_value/CI_lower/CI_upper/FDR_OutcomeModel_BW, Direction_OutcomeModel_BW,
  coef/std_err/t_value/p_value/CI_lower/CI_upper/FDR_OutcomeModel_GA, Direction_OutcomeModel_GA

Applies: 10 blank rows reserved above the table, header renaming to
human-readable labels, header styling, frozen header row + autofilter,
sensible column widths, numeric formatting with centered alignment, and
highlighting for candidate features and significant FDR (green) / p-value
(muted yellow) associations.

Usage:
    python generate_report.py TIMEPOINT-1-All-Models.xlsx [output.xlsx]
    python generate_report.py TIMEPOINT-2-All-Models.xlsx
"""

import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule


cols_rename = {"coef_MWASModel":"Metabolite Coefficient (MWAS Model)",
                "std_err_MWASModel":"Standard Error (MWAS Model)",
                "t_value_MWASModel":"t_statistics (MWAS Model)",
                "p_value_MWASModel": "p-value (MWAS Model)",
                "CI_lower_MWASModel": "CI Lower (MWAS Model)",
                "CI_upper_MWASModel": "CI Upper (MWAS Model)",
                "FDR_MWASModel":"FDR (MWAS Model)",
                "Direction_MWASModel":"Direction of Coefficient (MWAS Model)",

                "coef_OutcomeModel_BW":"Metabolite Coefficient (Birthweight Outcome Model)",
                "std_err_OutcomeModel_BW":"Standard Error (Birthweight Outcome Model)",
                "t_value_OutcomeModel_BW":"t_statistics (Birthweight Outcome Model)",
                "p_value_OutcomeModel_BW": "p-value (Birthweight Outcome Model)",
                "CI_lower_OutcomeModel_BW": "CI Lower (Birthweight Outcome Model)",
                "CI_upper_OutcomeModel_BW": "CI Upper (Birthweight Outcome Model)",
                "FDR_OutcomeModel_BW":"FDR (Birthweight Outcome Model)",
                "Direction_OutcomeModel_BW":"Direction of Coefficient (Birthweight Outcome Model)",

                "coef_OutcomeModel_GA":"Metabolite Coefficient (Gestational Age Outcome Model)",
                "std_err_OutcomeModel_GA":"Standard Error (Gestational Age Outcome Model)",
                "t_value_OutcomeModel_GA":"t_statistics (Gestational Age Outcome Model)",
                "p_value_OutcomeModel_GA": "p-value (Gestational Age Outcome Model)",
                "CI_lower_OutcomeModel_GA": "CI Lower (Gestational Age Outcome Model)",
                "CI_upper_OutcomeModel_GA": "CI Upper (Gestational Age Outcome Model)",
                "FDR_OutcomeModel_GA":"FDR (Gestational Age Outcome Model)",
                "Direction_OutcomeModel_GA":"Direction of Coefficient (Gestational Age Outcome Model)"}

HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
CANDIDATE_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
SIG_FDR_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
SIG_PVAL_FILL = PatternFill(start_color="FFE699", end_color="FFE699", fill_type="solid")

PVAL_PREFIXES = ("p_value", "FDR")
COEF_PREFIXES = ("coef", "std_err", "t_value", "CI_lower", "CI_upper")

FDR_COLUMNS = ["FDR_MWASModel", "FDR_OutcomeModel_BW", "FDR_OutcomeModel_GA"]
PVAL_COLUMNS = ["p_value_MWASModel", "p_value_OutcomeModel_BW", "p_value_OutcomeModel_GA"]
CANDIDATE_COLUMN = "Candidate_MWASModel"
WIDE_COLUMNS = {"list_all_ids", "list_all_library"}

BANNER_ROWS = 10


def column_kind(header) -> str:
    if header is None:
        return "other"
    if header.startswith(PVAL_PREFIXES):
        return "pval"
    if header.startswith(COEF_PREFIXES):
        return "coef"
    return "other"


def add_banner(ws) -> None:
    ws.insert_rows(1, amount=BANNER_ROWS)

    # openpyxl's insert_rows shifts cell values but not row-level formatting
    # (e.g. `hidden`), so any stale hidden/filtered rows from the source file
    # can land on the new banner rows instead of where they used to be.
    for dim in ws.row_dimensions.values():
        dim.hidden = False

    # Reset any saved scroll/selection state from the source file so the
    # sheet opens at A1 instead of wherever it was last left scrolled to.
    ws.sheet_view.topLeftCell = "A1"
    ws.sheet_view.selection[0].activeCell = "A1"
    ws.sheet_view.selection[0].sqref = "A1"


def format_sheet(ws) -> None:
    header_row = [cell.value for cell in ws[1]]
    n_cols = len(header_row)

    add_banner(ws)

    header_idx = 1 + BANNER_ROWS
    data_start = header_idx + 1
    n_rows = ws.max_row

    header_index = {name: i + 1 for i, name in enumerate(header_row)}

    # Header row styling + renaming to human-readable labels
    for col_idx, cell in enumerate(ws[header_idx], start=1):
        cell.value = cols_rename.get(header_row[col_idx - 1], cell.value)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[header_idx].height = 30

    ws.freeze_panes = f"A{data_start}"
    ws.auto_filter.ref = f"A{header_idx}:{get_column_letter(n_cols)}{n_rows}"

    # Column widths and number formats
    for col_idx, name in enumerate(header_row, start=1):
        letter = get_column_letter(col_idx)
        kind = column_kind(name)
        if name == "feature":
            ws.column_dimensions[letter].width = 22
        elif name in WIDE_COLUMNS:
            ws.column_dimensions[letter].width = 45
        elif name == "highest_OL":
            ws.column_dimensions[letter].width = 12
        elif name in (CANDIDATE_COLUMN, "Direction_MWASModel", "Direction_OutcomeModel_BW", "Direction_OutcomeModel_GA"):
            ws.column_dimensions[letter].width = 20
        else:
            ws.column_dimensions[letter].width = 14

        if kind in ("pval", "coef"):
            for row in range(data_start, n_rows + 1):
                cell = ws.cell(row=row, column=col_idx)
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if cell.value is None:
                    continue
                cell.number_format = "0.0000E+00" if kind == "pval" else "0.0000"

    # Highlight candidate feature rows
    cand_col = header_index.get(CANDIDATE_COLUMN)
    if cand_col:
        for row in range(data_start, n_rows + 1):
            value = ws.cell(row=row, column=cand_col).value
            if value and value != "Not Significant":
                ws.cell(row=row, column=cand_col).fill = CANDIDATE_FILL

    # Conditional formatting: significant FDR (< 0.05) in green, p-value (< 0.05) in muted yellow
    for columns, fill in ((FDR_COLUMNS, SIG_FDR_FILL), (PVAL_COLUMNS, SIG_PVAL_FILL)):
        for col_name in columns:
            col = header_index.get(col_name)
            if not col:
                continue
            letter = get_column_letter(col)
            cell_range = f"{letter}{data_start}:{letter}{n_rows}"
            ws.conditional_formatting.add(
                cell_range,
                CellIsRule(operator="lessThan", formula=["0.05"], fill=fill),
            )


def format_workbook(input_path: Path, output_path: Path) -> None:
    wb = load_workbook(input_path)
    for sheet_name in wb.sheetnames:
        format_sheet(wb[sheet_name])
    wb.save(output_path)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <input.xlsx> [output.xlsx]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_name(f"{input_path.stem}-formatted{input_path.suffix}")

    format_workbook(input_path, output_path)
    print(f"Wrote formatted workbook to {output_path}")


if __name__ == "__main__":
    main()
