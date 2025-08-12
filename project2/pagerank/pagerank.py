import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = dict()
    n = len(corpus)

    if not corpus[page]:
        return {pg: 1 / n for pg in corpus}

    for pg in corpus:
        distribution[pg] = (1 - damping_factor) / n

    for linked_page in corpus[page]:
        distribution[linked_page] += damping_factor / len(corpus[page])

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page: 0 for page in corpus}
    pages = list(corpus.keys())
    sample = random.choices(pages)[0]

    page_rank[sample] += 1

    for _ in range(n - 2):
        distributions = transition_model(corpus, sample, damping_factor)

        pages = list(distributions.keys())
        weights = list(distributions.values())
        sample = random.choices(pages, weights)[0]

        page_rank[sample] += 1

    return {page: page_rank[page] / n for page in page_rank}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    THRESHOLD = 0.001
    n = len(corpus)
    curr_pagerank = {page: 1 / n for page in corpus}

    while True:
        prev_pagerank = curr_pagerank.copy()

        for page in corpus:
            sigma = 0
            for i in corpus:
                if not corpus[i]:
                    num_links = len(corpus)
                    pagerank = prev_pagerank[i]
                    sigma += pagerank / num_links

                elif page in corpus[i]:
                    num_links = len(corpus[i])
                    pagerank = prev_pagerank[i]
                    sigma += pagerank / num_links

            curr_pagerank[page] = ((1 - damping_factor) / n) + (damping_factor * sigma)

        if not any(abs(prev_pagerank[page] - curr_pagerank[page]) > THRESHOLD for page in corpus):
            break

    return prev_pagerank


if __name__ == "__main__":
    main()
