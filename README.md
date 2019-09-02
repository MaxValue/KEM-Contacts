# Web Crawler - KEM Contacts

Get all metadata about the Klima- und Energieregionen from https://www.klimaundenergiemodellregionen.at/modellregionen/liste-der-regionen/

## Contents
* [Getting Started](#getting-started)
*    [Prerequisites](#prerequisites)
* [Deployment](#deployment)
* [Built With](#built-with)
* [Contributing](#contributing)
*    [Roadmap](#roadmap)
* [Versioning](#versioning)
* [Authors](#authors)
* [License](#license)
* [Acknowledgments](#acknowledgments)
*    [Project History](#project-history)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

I recommend you to use the `setup_development.sh` script by running

```
./setup_development.sh
```

but if you don't want to do that, here is the complete list of dependencies:

* [Python 3.6.8](https://www.python.org/downloads/)
* [Python 3 PIP 9.0.1](https://pip.pypa.io/)
* [Python Venv 3.6.7-1](https://docs.python.org/3/library/venv.html)
* [Scrapy 1.7.3](https://scrapy.org/)
* [Sqlalchemy 1.3.7](https://www.sqlalchemy.org)
* [Pyexcel 0.5.15](https://github.com/pyexcel/pyexcel/)
* [Pyexcel-ods 0.5.6](https://github.com/pyexcel/pyexcel-ods)
* [Pyexcel-xls 0.5.8](https://github.com/pyexcel/pyexcel-xls)
* [Pyexcel-xlsxw 0.4.2](https://github.com/pyexcel/pyexcel-xlsxw)

## Deployment

Activate the environment

```
source venv/bin/activate
```

Change to the scrapy project

```
cd kem
```

Start the crawler

```
scrapy crawl getcontacts
```

After the crawler finishes, you'll want to export the data:

```
./export.py results.db kem getcontacts 1 KEM-Contacts_YYYY-MM-DD
```

where 1 is the job id and YYYY-MM-DD should be replaced by the date on which you crawled the website.

You will see the job id at the beginning of the log `log.txt`: `Job ID is: XX`.

## Built With

* [Ubuntu 18.04.3 LTS](https://ubuntu.com/) - The operating system I use
* [Sublime Text 3](https://www.sublimetext.com/) - The code editor I use
* [Python 3.6.8](https://www.python.org/downloads/) - The programming language
* [Python 3 PIP 9.0.1](https://pip.pypa.io/) - The package manager of the programming language
* [Python Venv 3.6.7-1](https://docs.python.org/3/library/venv.html) - The project bundler of the programming language
* [Scrapy 1.7.3](https://scrapy.org/) - The crawling framework
* [Sqlalchemy 1.3.7](https://www.sqlalchemy.org) - The database interface library
* [Pyexcel 0.5.15](https://github.com/pyexcel/pyexcel/) - For exporting to spreadsheet formats
* [Pyexcel-ods 0.5.6](https://github.com/pyexcel/pyexcel-ods) - For exporting as ODS spreadsheet
* [Pyexcel-xls 0.5.8](https://github.com/pyexcel/pyexcel-xls) - For exporting as XLS spreadsheet
* [Pyexcel-xlsxw 0.4.2](https://github.com/pyexcel/pyexcel-xlsxw) - For exporting as XLSX spreadsheet

## Contributing

Please open an issue if you want to help or have questions.

### Roadmap
Things I already plan to implement, but didn't have yet:
- [ ] Change database scheme to be individual to crawler, make exporter therefore export specific table.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the tags on this repository.

## Authors

* **Max Fuxjäger** - *Initial work* - [MaxValue](https://gitlab.com/MaxValue)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

### Project History
This project was created because I (Max) was asked to crawl this website.
