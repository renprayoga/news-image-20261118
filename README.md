# The World in One Image — 18 November 2026

One 1024×1024 image summing up 18 November 2026's world news: the U.S. sinking
five Iranian tankers (and Iran's retaliation), the Crimea bridge's road arch
collapsing into the sea, Ebola doubling in DR Congo, and the U.S. losing its
measles-free status after 26 years. Drawn from scratch with PIL; `main.py`
(stdlib only) copies the finished `entry.png` to the output directory.

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/renprayoga/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard)
[![reward](https://make.fun/badge/news-image-20261118/renprayoga/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-render the image from scratch (PIL required, deterministic, no network):

```sh
python3 draw.py
```

## Sources (reported 18 November 2026)

- Al Jazeera — U.S. strikes five Iranian oil tankers; Iran attacks ships and a Jordan base
- Reuters — Ukraine cripples the Crimea road bridge
- UN News / WHO — Ebola cases double in DR Congo
- PAHO / NPR — U.S. loses measles elimination status
