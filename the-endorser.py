import sys, os, argparse, logging
import config, outputs, drivers
from urllib.parse import urlparse
from linkedin import LinkedInClient


if __name__ == '__main__':
    available_output_modules = ", ".join(outputs.discover_output_modules().keys())
    available_drivers = ", ".join(drivers.discover_drivers().keys())

    parser = argparse.ArgumentParser(description="Maps out relationships between peoples endorsements on LinkedIn.",
                                     usage="python the-endorser.py https://www.linkedin.com/in/user1 https://www.linkedin.com/in/user2",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("profiles", nargs="+", help="Space separated list of LinkedIn profile URLs to map")
    parser.add_argument("--config_file", dest="config_file", default=os.path.join(os.getcwd(), 'config.yaml'),
                        help="Specify the path of the config.yaml file")
    parser.add_argument("--driver", dest="driver", default="chromedriver",
                        help="Selenium WebDriver to use to parse the webpages: %s " % available_drivers)
    parser.add_argument("--output", dest="output", default="digraph",
                        help="Output module to visualise the relationships: %s " % available_output_modules)
    parser.add_argument("--log", dest="log", default=None,
                        help="Path of log file. None for stdout.")
    parser.add_argument("--log-level", dest="log_level", default="INFO",
                        help="Logging output level: DEBUG, INFO, WARNING, ERROR.")

    args = parser.parse_args()
    config = config.load(args.config_file)
    output_module = outputs.get_output_module_by_name(args.output)
    driver = drivers.get_driver_by_name(args.driver)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), None), handlers={
        logging.StreamHandler(sys.stdout) if args.log is None else logging.FileHandler(filename=args.log)
    })

    with LinkedInClient(config.email, config.password, webdriver=driver.get(config), save_cookie=config.save_cookie) as client:
        profiles = list()

        for profile in args.profiles:
            profile_url = urlparse(profile)

            if "linkedin.com" not in profile_url.netloc and "in/" not in profile_url.path:
                raise ValueError("%s is not a valid LinkedIn profile URL", profile)

            profiles.append(client.get_endorsements(profile_url.geturl()))

        output_module.run(profiles)