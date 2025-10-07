# THOMAS NET CRAWLER

## Installing

1. Clone
```bash
$ git clone git@github.com:VandersonTorres/thomas-net-rp.git
```

2. Enter directory
```bash
$ cd thomas-net-rp
```

3. Install dependencies
```bash
$ pip install -r requirements.txt
```

## Running

```bash
$ scrapy crawl thomas_net -o items.json
```

- A json file containing the Items will be generated
- If parsing errors occur, stats will be added to the "Scrapy Stats" at the end of the Job so you can debug it.
- There is already a `/sample.json` so you can see what you will have for this.
