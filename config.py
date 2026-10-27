# Open Access is required for full publication crawl. check Legal aspects by the publishers.
OPENACCESS = False

Year_Range = "2021-2023"
keywords = ["biodivers*", "genetic diversity","*omic diversity", "phylogenetic diversity", "soil diversity",
            "population diversity",  "species diversity", "ecosystem diversity", "functional diversity",
            "microbial diversity"]

years = []
for i in range(2023-2021+1):
    years.append(i+2021)

#API = 'Springer'
API = 'Elsevier'

Metric = True  # keyword search and DOI metadata only; no abstracts are saved
Full = False  # retrieve full text (Elsevier) or PDFs (Springer)
