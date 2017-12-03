import argparse

app = argparse.ArgumentParser("Data Science Application")
app.add_argument("experiment", help="The experiment number to run (1-5)", type=int)
app.add_argument("config", help="The configuration file", type=argparse.FileType("r"))

if __name__ == "__main__":
    args = app.parse_args()
    print(args.experiment)