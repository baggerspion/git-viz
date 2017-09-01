# GitViz Suite

This is a suite of tools for visualising/analysing behaviour inside
Git repositories. The included tools are:

- *Network.py*: a tool for showing who has worked with whom within the repository
- *GitViz.py*: a toold for visualising, week-by-week, who contributes to the repostory and how frequently
- *Counter.py*: a tool for counting the number of daily commits within the repository.

## Setup

Before running *any* of these scripts, you must install the Python/pip dependencies:

`pip install -r requirements.txt`

Bofore running the *Network.py* script, you must install Graphviz
suite of tools. For this purpose I advise using Homebrew to OSX users:

`brew install graphviz`

## Running the Scripts
The scripts require you to provide a path to a checked-out Git repo.
In addition you can provide "from" and "until" dates.

e.g. `Network.py <path> -f 2017-01-01 -u 2017-03-31`
e.g. `GitViz.py <path> -f 2017-01-01 -u 2017-03-31`