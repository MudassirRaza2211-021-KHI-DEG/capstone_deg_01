import argparse
import logging

import pandas as pd

from model import train_model

logging.basicConfig(level=logging.INFO)


def run_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", required=True)
    parser.add_argument("--save_model", default=False)
    parser.add_argument("--model_dir", default=None)
    return parser.parse_args()


def run_train(args: argparse.Namespace):
    logging.info("Loading data")
    df = pd.read_csv(args.data_path)
    x = df.drop(["date", "Occupancy"], axis=1).values
    y = df["Occupancy"].values

    train_model(x, y, args.save_model, args.model_dir)


if __name__ == "__main__":
    args = run_argparse()
    run_train(args)
