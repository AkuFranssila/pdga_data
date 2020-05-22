<a href="https://www.pdga.com/"><img src="https://www.pdga.com/sites/all/themes/pdga/logo.png" title="PDGALogo" alt="PDGALogo"></a>

# PDGA DATA

PDGA Data project is to crawl, process, analyze and display data found from PDGA.com. The goal is to provide easily searchable data that provides more insight about players, tournaments and the whole player base.

PDGA does not provide the best analytical data on their own website which is why this project was created.

[![CircleCI](https://app.circleci.com/pipelines/github/AkuFranssila/pdga_data.svg?style=svg)](https://github.com/AkuFranssila/pdga_data)]

[![Requirements Status](https://requires.io/github/AkuFranssila/pdga_data/requirements.svg?branch=master)](https://requires.io/github/AkuFranssila/pdga_data/requirements/?branch=master)

![GitHub last commit](https://img.shields.io/github/last-commit/AkuFranssila/pdga_data)

![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/AkuFranssila/pdga_data)

![GitHub top language](https://img.shields.io/github/languages/top/AkuFranssila/pdga_data)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/AkuFranssila/pdga_data?style=plastic)

---

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Contributing](#contributing)
- [FAQ](#faq)
- [Planned features](#Planned features / upcoming changes)
- [Support](#support)
- [License](#license)


---

## Example

- Crawling all players found from PDGA.com. Arguments available --start_id --end_id --all. 

```python

python -m project.player_processes.run_player_crawl --all
```

- If you wish to test how crawling a single tournament page works you can use this test file for it. Used for debugging tournament crawling.

```python

python -m tests.test_single_tournament_page --link <pdga tournament link >
```

---

## Installation

- All the `code` required to get started
- Images of what it should look like

### Clone

- - Coming in the future

### Setup

- Coming in the future

---

## Features

- Coming in the future

## Usage

- Coming in the future

## Documentation

- Coming in the future

## Tests

- Currently tests are automated using CirceCI. Tests can be found from the test folder. More tests will be added as the project goes on.

---

## Contributing

- **Can I contribute?**
    - Unfortunately this project is for my own enjoyment. You can always clone this repo and create your own version of this!


---

## FAQ

- **When will this project be ready?**
    - This project is worked slowly over time. No estimates can currently be given as development speed depends on other responsibilites.
    
    
---

## Planned features / upcoming changes

- Frontend
- API for player, tournament and analytics data
- Kubernetes for crawling/parsing
- Add docker
    
    
---

## Support

Reach out to me at one of the following places!

- Message me at <a href="https://www.linkedin.com/in/akufranssila/" target="_blank">`Linkedin`</a>

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2015 © <a href="" target="_blank">PDGA DATA</a>.
