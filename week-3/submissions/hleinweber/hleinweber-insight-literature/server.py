# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=1.28,<2"]
# ///
"""Read-only Crossref literature tools; no API key required."""
import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hleinweber-insight-literature")


def request(path, params=None):
    url = "https://api.crossref.org/works" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent":"hleinweber-insight-literature/0.1.0 (research homework)", "Accept":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.load(response)["message"]
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise ValueError("DOI not found in Crossref. Check spelling; NASA PDS/DataCite DOIs may not be indexed here.") from None
        if error.code == 429:
            raise ValueError("Crossref rate limit reached. Wait a minute and retry with fewer requests.") from None
        raise ValueError("Crossref returned an HTTP error. Retry later.") from None
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
        raise ValueError("Crossref lookup failed. Check your internet connection and try a shorter query.") from None


def summarize(work, include_abstract=False):
    date = work.get("published", work.get("issued", {})).get("date-parts", [[]])[0]
    authors = work.get("author", [])
    result = {
        "title": (work.get("title") or ["Untitled"])[0],
        "authors": [" ".join(filter(None,[a.get("given"),a.get("family")])) or a.get("name", "Unknown") for a in authors[:6]],
        "author_count":len(authors),
        "year":date[0] if date else None,
        "doi":work.get("DOI"),
        "url":"https://doi.org/"+work["DOI"] if work.get("DOI") else work.get("URL"),
        "venue":(work.get("container-title") or [""])[0],
        "type":work.get("type"),
    }
    if include_abstract:
        raw_abstract = work.get("abstract") or ""
        abstract = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw_abstract)).split())
        # Crossref sometimes deposits Science's multi-paper editorial as the abstract.
        # This is a warning heuristic, not verification of other deposited abstracts.
        related_articles = re.findall(r"<(?:[\w-]+:)?related-article\b", raw_abstract, re.I)
        editorial = bool(abstract) and (
            len(related_articles) > 1
            or abstract.casefold().startswith("single seismometer structure ")
        )
        result["abstract_source"] = "Crossref publisher-deposited metadata"
        result["abstract_kind"] = ("suspected_shared_editorial_summary" if editorial
                                   else "unverified_deposited_text" if abstract else "missing")
        result["abstract_excerpt"] = None if editorial else abstract[:1200] or None
        result["abstract_truncated"] = not editorial and len(abstract) > 1200
        result["findings_supported"] = bool(abstract) and not editorial
        result["required_action"] = (
            "Retrieve this paper's individual abstract or full text from the DOI/source link. "
            "Until then return citation metadata only; do not report findings or numerical estimates."
            if editorial or not abstract else
            "Check that each claim is supported by this deposited text; verify numerical claims against a primary source."
        )
        result["note"] = (
            "Suspected shared editorial summary, not a verified individual-paper abstract. "
            "Do not attribute its numbers or findings to this paper. Retrieve the individual "
            "abstract or full paper from a primary source before reporting findings or uncertainties. "
            if editorial else
            "Deposited text has not been verified as this paper's own abstract. "
        ) + (
            "Missing information in Crossref does not establish that abstracts, findings or "
            "uncertainties are absent from the paper. If primary-source access is unavailable, "
            "report this tool's coverage limit. This is not a full-paper review."
        )
    return result


@mcp.tool()
def search_papers(query: str, limit: int = 5, from_year: int | None = None, to_year: int | None = None) -> dict:
    """Search Crossref scholarly metadata for the InSight Mars mission by keywords; e.g. 'InSight magnetic lander calibration'. Returns up to 10 citation candidates. Searches multiple requested interior regions separately and prioritizes titles matching those regions; otherwise retains Crossref order. Optional years are inclusive integers. Filters first 50 matches per query to mission terms; may miss papers without those terms in metadata. Inspect titles before citing. Does not search full text or cover all NASA reports."""
    query = query.strip()
    if not query or len(query)>500:
        raise ValueError("Use 1-500 characters of research keywords.")
    if not 1<=limit<=10:
        raise ValueError("limit must be between 1 and 10.")
    for year in [from_year,to_year]:
        if year is not None and not 1600<=year<=2100:
            raise ValueError("Years must be between 1600 and 2100.")
    if from_year is not None and to_year is not None and from_year>to_year:
        raise ValueError("from_year must not exceed to_year.")
    # Separate requested interior regions so a broad title query does not bury
    # the structural papers among general mission and instrument studies.
    topics = [topic for topic in ("crust", "core", "mantle")
              if re.search(r"\b" + topic + r"\b", query, re.I)]
    queries = ["InSight seismic " + topic + " Mars" for topic in topics] if len(topics) > 1 else [query + " Mars"]
    params={"rows":50}
    filters=[]
    if from_year is not None: filters.append(f"from-pub-date:{from_year}-01-01")
    if to_year is not None: filters.append(f"until-pub-date:{to_year}-12-31")
    if filters: params["filter"]=",".join(filters)
    candidates = []
    seen = set()
    for title_query in queries:
        data = request("", dict(params, **{"query.title": title_query}))
        for work in data.get("items", []):
            identity = work.get("DOI") or work.get("URL") or str(work.get("title"))
            if identity not in seen:
                seen.add(identity)
                candidates.append(work)
    relevant=[]
    for work in candidates:
        text=" ".join(work.get("title",[]))+" "+work.get("abstract", "")
        if re.search(r"\binsight\b",text,re.I) and re.search(r"\bmars\b|\bmartian\b|\blander\b|\bfluxgate\b",text,re.I):
            if work.get("type") != "component":
                if re.search(r"magnet|fluxgate|\bifg\b",query,re.I) and not re.search(r"magnet|fluxgate|\bifg\b",text,re.I):
                    continue
                relevant.append(summarize(work))
    if topics:
        # Give each requested region a turn before filling the remaining slots.
        # Prefer journal articles over abstracts/preprints within each region.
        groups = [sorted(
            [paper for paper in relevant
             if re.search(r"\b" + topic + r"\b", paper["title"], re.I)],
            key=lambda paper: paper["type"] != "journal-article") for topic in topics]
        ranked = []
        ranked_dois = set()
        while any(groups):
            for group in groups:
                if group:
                    paper = group.pop(0)
                    if paper["doi"] not in ranked_dois:
                        ranked.append(paper)
                        ranked_dois.add(paper["doi"])
        relevant = ranked + [paper for paper in relevant if paper["doi"] not in ranked_dois]
    return {"query":query,"source":"Crossref","queries_used":queries,
            "scope":"InSight mission metadata; first 50 matches per title query. Multiple requested interior regions are searched separately; titles matching requested regions rank first, alternating regions and preferring journal articles within each region.",
            "results":relevant[:limit],
            "warning":"Discovery candidates only, not evidence of findings. Search each requested region separately if coverage is incomplete. Verify each DOI with get_paper. Omit instrument/calibration papers unless they directly answer the question. Include DOI links in the answer."}


@mcp.tool()
def get_paper(doi: str) -> dict:
    """Retrieve a paper's Crossref metadata and unverified deposited text when available. Withholds suspected shared editorial summaries; these cannot support paper-specific findings. Missing metadata does not mean the paper lacks an abstract or uncertainties. Input a DOI such as '10.1029/2020JE006505' or its https://doi.org/ URL. Returns source links; does not download full text. Use after search to verify a citation."""
    doi=re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi.strip(), flags=re.I)
    doi=re.sub(r"^doi:\s*", "", doi, flags=re.I)
    if not re.fullmatch(r"10\.\d{4,9}/[^\s]+",doi) or len(doi)>250:
        raise ValueError("Provide a DOI such as 10.1029/2020JE006505, not a paper title.")
    return summarize(request("/"+urllib.parse.quote(doi,safe="")),True)


@mcp.tool()
def insight_reference_sources() -> list[dict]:
    """List three curated primary-source starting points for InSight IFG interference/calibration research. These are fixed discovery links, not a live search or a complete bibliography. Read each source before making scientific claims; PDS and conference documents may be absent from Crossref."""
    return [
        {"title":"The Origin of Observed Magnetic Variability for a Sol on Mars From InSight", "url":"https://doi.org/10.1029/2020JE006505", "kind":"journal article"},
        {"title":"InSight Fluxgate Magnetometer Data Calibration Assessment and Implications", "url":"https://www.hou.usra.edu/meetings/lpsc2020/pdf/1331.pdf", "kind":"conference abstract, 2020"},
        {"title":"InSight IFG Data Calibration Description", "url":"https://pds.nasa.gov/ds-view/pds/viewDocument.jsp?identifier=urn%3Anasa%3Apds%3Ainsight-ifg-mars%3Adocument%3Ainsight-ifg-data-calibration-description&version=2.0", "kind":"NASA PDS calibration documentation"},
    ]

if __name__ == "__main__":
    mcp.run(transport="stdio")
