import argparse
from configparser import ConfigParser

from datascience.experiments import ExperimentOne, ExperimentTwo, ExperimentThree, ExperimentFour, ExperimentFive

app = argparse.ArgumentParser("Data Science Application")
app.add_argument("experiment", help="The experiment number to run (1-5)", type=int)
app.add_argument("config", help="The configuration file", type=argparse.FileType("r"))

# a mapping of experiment numbers to the respective experiment class
experiments = {
    1: ExperimentOne,
    2: ExperimentTwo,
    3: ExperimentThree,
    4: ExperimentFour,
    5: ExperimentFive
}

if __name__ == "__main__":
    args = app.parse_args()
    config = ConfigParser()
    config.read_file(args.config)

    # if this is not a valid experiment
    if not args.experiment in experiments:
        print("Invalid experiment number.")
    else:
        # instantiate and run the experiment
        experiment = experiments[args.experiment](config)
        experiment.run()