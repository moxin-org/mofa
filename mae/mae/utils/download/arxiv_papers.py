

import arxiv
import os
from datetime import datetime, timedelta
from typing import Union, List, Dict


def arxiv_search_and_download(query: Union[str, List[str]], max_results: int = 2, days_back: int = 365 * 3,
                              download_dir: str = "./data/output/arxiv_papers") -> List[Dict[str, str]]:
    """
    Search for arXiv papers, filter the most relevant and recent results, and download the PDFs.

    Parameters:
    query (str or List[str]): Search query or list of queries.
    max_results (int): Number of qualifying papers to download per query, default is 2.
    days_back (int): Consider papers from the last number of days only, default is 3 years.
    download_dir (str): Directory to download PDFs, default is "./data/output/arxiv_papers".

    Returns:
    List[Dict[str, str]]: List of dictionaries containing information about the downloaded files.
    """

    client = arxiv.Client()

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    cutoff_date = datetime.now() - timedelta(days=days_back)

    all_results = []

    queries = [query] if isinstance(query, str) else query

    for single_query in queries:
        search = arxiv.Search(
            query=single_query,
            max_results=150,
            sort_by=arxiv.SortCriterion.Relevance
        )

        query_results = []
        for paper in client.results(search):
            if paper.published.replace(tzinfo=None) >= cutoff_date:
                try:
                    file_name = f"{paper.get_short_id()}.pdf"
                    pdf_path = os.path.join(download_dir, file_name)
                    paper.download_pdf(filename=pdf_path)
                    query_results.append({
                        "query": single_query,
                        "title": paper.title,
                        "file_name": file_name,
                        "file_path": pdf_path,
                        "published": paper.published.strftime("%Y-%m-%d"),
                        "authors": ", ".join([author.name for author in paper.authors]),
                        "summary": paper.summary
                    })
                    print(f"已下载: {file_name}")

                    if len(query_results) >= max_results:
                        break
                except Exception as e:
                    print(f"下载失败 {paper.title}: {str(e)}")

        all_results.extend(query_results)

    all_results.sort(key=lambda x: x['published'], reverse=True)

    return all_results


