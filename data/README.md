# Data catalogue

The existing root-level files are preserved unchanged. They are legacy development material, not the complete annual dataset for the revised article.

| Existing file | What can be established from the file | Use limitation |
| --- | --- | --- |
| [20250114_elect_dk.csv](../20250114_elect_dk.csv) | Generation columns labelled MW; area labelled Denmark (DK); intervals on 14 January 2025 in CET/CEST notation | Not the full-year DK2 UTC panel; `n/e` must not be silently interpreted as zero |
| [lci_pharma_dynamic.csv](../lci_pharma_dynamic.csv) | `Time` and `Data_1` to `Data_4` columns, with additional unnamed columns | Signal identities and units are not established by the headers; not a publication-ready LCI table |
| [elect_db_dk_ab.xlsx](../elect_db_dk_ab.xlsx) | Existing Excel workbook | Preserved as legacy material; contents and redistribution status not revalidated in this build |
| [Cases.docx](../Cases.docx) | Existing case-notes document | Not the final manuscript or Supporting Information |

## Required annual data products

The following files should be generated from the confirmed final run, not inferred from cached screenshots or fabricated:

| Data product | Minimum information |
| --- | --- |
| Generation panel | UTC interval start/end, bidding zone, technology, value, unit, acquisition date and missing-data treatment |
| Price panel | Matching UTC intervals, zone, price and currency/energy unit |
| Foreground inventory | Actual sampling times, signal names, amounts, units, production/CIP state and normalization basis |
| Mapping table | Flow, conversion, dataset identifier, database version, geography and unit |
| Hourly LCI matrix | Row/column dictionary, time coverage, units and linkage to article example rows |
| Schedule/result exports | Scenario, operating intervals, environmental totals, costs, denominators and method identifier |

Full ecoinvent database dumps, account credentials and other restricted third-party content are not part of the repository package. Review each derived export's redistribution permissions before adding it.

Use `data/local/` for execution inputs. This directory is ignored by Git. The repository does not silently download databases or substitute the legacy samples for the annual panel.
