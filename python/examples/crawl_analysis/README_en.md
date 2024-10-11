# Crawl and Analysis Agent in MoFA

## 1. Functionality
The MoFA Crawl and Analysis Agent can scrape data from the internet, analyze it, and configure memory features.

## 2. Use Cases
1. Specify the URL in `configs/crawl_agent.yml` to generate a web scraping script, and ask the large model questions based on the content of that URL for documentation writing.
2. Query the large model, scrape relevant web pages from search engines for analysis, and use the large model to provide final results.
3. The generated output is in markdown format, including Title, Introduction, Details, and Conclusion.

## 4. Execution
1. Install the MoFA project package.
2. Run `dora up && dora build crawl_analysis_dataflow.yml && dora start crawl_analysis_dataflow.yml`.
3. Start another command line, run `terminal-input` in the other terminal, then provide prompts.
4. The result will be a markdown formatted report.

## References
- [scrapegraph-ai](https://scrapegraph-ai.readthedocs.io/en/latest/index.html)