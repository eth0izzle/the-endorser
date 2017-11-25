# The Endorser

An OSINT tool that allows you to draw out relationships between people on LinkedIn via endorsements/skills.

Check out the [example](https://raw.githubusercontent.com/eth0izzle/the-endorser/master/example/output.pdf), which is based on mine and my colleagues (David Prince) LinkedIn profile. By glancing at the visualisation you can easily see there is some sort of relationship between us and "Zoë Rose" (we all work together on the same team in this case). If I was carrying out an investigation I would focus my efforts towards her next.

![Example](https://raw.githubusercontent.com/eth0izzle/the-endorser/master/example/example.png)

Due to the way LinkedIn's privacy settings work this tool works best when your target is within your 3rd degree network or higher. If you are performing LinkedIn OSINT I'd highly recommend using a LinkedIn Recruiter account.

## Installation

The Endorser will work on pretty much any *nix (Linux, Mac, BSD) system with Python 3.0+.

You can then install The Endorser in 4 simple steps:

1. `git clone https://github.com/eth0izzle/the-endorser.git`
2. `sudo pip3 install -r requirements.txt`
3. Setup your LinkedIn credentials in `config.yaml`
4. `python3 the-endorser.py <profile1> <profile2>`

## Usage

    usage: python the-endorser.py https://www.linkedin.com/in/user1 https://www.linkedin.com/in/user2

    Maps out relationships between peoples endorsements on LinkedIn.

    positional arguments:
      profiles              Space separated list of LinkedIn profile URLs to map

    optional arguments:
      -h, --help            show this help message and exit
      --config_file CONFIG_FILE
                            Specify the path of the config.yaml file (default:
                            /Users/p/Code/the-endorser/config.yaml)
      --output OUTPUT       Output module to visualise the relationships: digraph,
                            stdout (default: digraph)
      --log LOG             Path of log file. None for stdout. (default: None)
      --log-level LOG_LEVEL
                            Logging output level: DEBUG, INFO, WARNING, ERROR.
                            (default: INFO)

Currently we only have one output (digraph). Square box = skill, ellipse = person. It's best to read this from right-to-left and identify and people that have arrows from multiple profiles.

## Contributing

Check out the [issue tracker](https://github.com/eth0izzle/the-enforcer/issues) and see what tickles your fancy.

1. Fork it, baby!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## History

**v1.0**
First release

## License

MIT. See LICENSE