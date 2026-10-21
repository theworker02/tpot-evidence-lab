# Third-party data attribution

The `cloud-honeynet-2025` rows derive from **Multi-Regional Cloud Honeynet Dataset: A Distributed T-Pot Honeypot Deployment Across Azure Regions for Cyber Threat Analysis**, by Enrique Feito-Casares, Ismael Gómez-Talal, and José Luis Rojo-Álvarez (Universidad Rey Juan Carlos), published July 10, 2025.

- DOI and pinned source: https://doi.org/10.5281/zenodo.15716735
- License identifier supplied by the Zenodo record: `mit-license` (checked October 21, 2026).
- Source file: `CloudHoneyNetDataset.zip`, member `PreprocessedData/HoneyNetEvents_Clean.csv`.
- Changes by Magnexis: removed identifiers and sensitive fields, normalized timestamps and field names, assigned opaque source groups and group-disjoint splits, removed identical projected rows, converted to JSONL and Parquet. Original upstream conclusions about maliciousness or attribution are not adopted as labels.

The original Magnexis collection remains CC BY 4.0. Imported rows retain MIT licensing; the repository's CC BY notice does not replace their source license. Each combined row carries its license and source URL. Retain this attribution and the MIT terms below when redistributing the imported derivative.

## MIT license terms for the imported source

Attribution: Enrique Feito-Casares, Ismael Gómez-Talal, José Luis Rojo-Álvarez, Universidad Rey Juan Carlos, 2025. License designation comes from the source record; this attribution is not a newly asserted copyright claim.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
