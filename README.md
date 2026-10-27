# Publication workflow

This pipeline searches Elsevier or Springer for publications that match configured
keywords. It collects publication records, removes duplicate DOIs, and downloads
available full text or PDFs. Elsevier text can be cleaned directly. Springer PDFs
can optionally be converted to text with GROBID.

## Step to follow: 
## Install Requirements

Install the Python dependencies from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

## Configuration

Edit `config.py` before running the pipeline:

- Set `API` to `'Elsevier'` or `'Springer'`.
- Configure the search keywords and date range.
- Set the processing mode using `Metric` and `Full`.

Provide the selected publisher's API credentials in its local configuration file:

- Elsevier: `elsevier_config.json`
- Springer: `springer_config.json`

Keep credential files private. Do not commit or share them. If example
configuration files are provided, copy an example to the required filename and
add your API key locally.

Run all commands below from the repository root.

## Workflow

### 1. Search for publications

In `config.py`, set:

```python
Metric = True
Full = False
```

Then run:

```bash
python3 main.py
```

The search saves publication records under `Data/Elsevier` or `Data/Springer`,
depending on the selected publisher. Springer records also include a PDF URL.

### 2. Deduplicate DOIs

Run:

```bash
python3 filter_DOIs.py
```

The publisher is read from `config.API`. The unique DOI list is written to:

```text
Data/DOIs/<publisher>_unique_DOIs.txt
```

### 3. Download available full text or PDFs

In `config.py`, change the mode to:

```python
Metric = False
Full = True
```

Then run:

```bash
python3 main.py
```

Available Elsevier full text is saved under `Data/Elsevier_full_txt`.
Springer PDFs are saved under `Data/Springer_PDFs`.

Full-text availability depends on publisher access and API permissions.

### 4. Clean downloaded text

For Elsevier, run:

```bash
python3 data_clean.py
```

The cleaned files are saved under `Data/Cleaned_Elsevier_full_txt`.

For Springer, first complete the optional GROBID conversion below. Then set
`API = 'Springer'` in `config.py` and run `python3 data_clean.py`. The cleaned
Springer text is saved under `Data/Cleaned_Springer_full_txt`, if supported by
the current configuration.

## Optional: Convert Springer PDFs to text with GROBID

This step applies only to downloaded Springer PDFs and runs separately from
`main.py`. It requires a running GROBID service, its Python client, and the
client configuration file at `grobid_client_python/config.json`.

After downloading the Springer PDFs, run:

```bash
python3 run_grobid.py
python3 parse_xml.py
```

GROBID XML is saved under `Data/grobid_output`. Extracted text is saved under
`Data/Springer_full_txt`. To clean the extracted text, set
`API = 'Springer'` in `config.py` and run:

```bash
python3 data_clean.py
```
