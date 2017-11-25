# The Endorser

An OSINT tool that allows you to draw out relationships between people on LinkedIn via endorsements/skills.

Check out the [example](https://raw.githubusercontent.com/eth0izzle/the-endorser/master/example/output.pdf) ([digraph](#digraph)), which is based on mine and my colleagues (David Prince) LinkedIn profile. By glancing at the visualisation you can easily see, by the number of "arrows", there is some sort of relationship between us and "Zoë Rose" (we all work together on the same team in this case). If I was carrying out an investigation I would focus my efforts towards her next.

![Example](https://raw.githubusercontent.com/eth0izzle/the-endorser/master/example/example.png)

Due to the way LinkedIn's privacy settings work this tool works best when your target is within your 3rd degree network or higher. Using a LinkedIn Premium or Recruiter account will allow you to map targets outside of your network.

## Installation

The Endorser will work on pretty much any *nix (Linux, Mac, BSD) system with Python 3.0+.

1. `git clone https://github.com/eth0izzle/the-endorser.git`
2. `sudo pip3 install -r requirements.txt`
3. Setup your LinkedIn credentials in `config.yaml`
4. Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your platform (requires Chrome) and place in ./drivers. Alternatively you can use [PhantomJS](http://phantomjs.org/download.html) and launch with the `--driver phantomjs` flag (*note phantomjs is 8x slower*).
5. `python3 the-endorser.py <profile1> <profile2>`

## Usage

    usage: python the-endorser.py https://www.linkedin.com/in/user1 https://www.linkedin.com/in/user2

    Maps out relationships between peoples endorsements on LinkedIn.

    positional arguments:
      profiles              Space separated list of LinkedIn profile URLs to map

    optional arguments:
      -h, --help            show this help message and exit
      --config_file CONFIG_FILE
                            Specify the path of the config.yaml file (default:
                            ./the-endorser/config.yaml)
      --driver DRIVER       Selenium WebDriver to use to parse the webpages:
                            chromedriver, phantomjs (default: chromedriver)
      --output OUTPUT       Output module to visualise the relationships: digraph,
                            stdout (default: digraph)
      --log LOG             Path of log file. None for stdout. (default: None)
      --log-level LOG_LEVEL
                            Logging output level: DEBUG, INFO, WARNING, ERROR.
                            (default: INFO)

### Outputs

The Endorser is "modular" in the sense that it can output and visualise the data in different ways. An output module just needs one method: `def run(profiles)`

Currently there is only one output module (digraph). In the future I plan to add modules for Maltego and and Plot.ly - but feel free to get involved!

#### Digraph

It's best to read this from right-to-left to identify people that have arrows from multiple profiles. Square box = skill, ellipse = person.

## Contributing

Check out the [issue tracker](https://github.com/eth0izzle/the-enforcer/issues) and see what tickles your fancy.

1. Fork it, baby!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a [pull request](https://github.com/eth0izzle/the-endorser/pulls)

## History

**v1.0**
Initial release

## License

MIT. See LICENSE