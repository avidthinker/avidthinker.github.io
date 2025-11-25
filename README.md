# Misc information

## Create Conda env

```
conda create -n web3blog python
conda activate web3blog
```

## Install dependencies

```
pip install poetry
poetry install --no-root
```

## Serve local version of blog

```
mkdocs serve
```

## Build Blog

This generates the static site into the `site` directory:

```
mkdocs build
```

## Push to GitHub Pages

This builds the blog and pushes it to the branch `gh-pages`:

```
mkdocs gh-deploy
```
