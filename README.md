# Nikiclicki

https://github.com/user-attachments/assets/c0f9af35-431c-428c-a2cc-e712034c626d

An app for rolling promo-codes on nikifilini website

## Prerequisites

To run the app, one would need to create a conda environment and install required dependencies, which is done by running the following script:

```sh
./setup.sh
```

Then it is necessary to make sure that the list of [rollable items](assets/targets.py) is up to date. To do that, execut the following command:

```sh
conda run -n nikiclicki python -m nc list
```

The command will open a browser window and check the list of rollable items automatically.

Finally, assign your `email` address to the env variable `NIKICLICKI_EMAIL`.

## Usage

To roll an item of choice, find the corresponding item in [the list](assets/targets.py) and pass it to the `farm` command. For instance, to farm 40% dicount run the following command:

```sh
conda run -n nikiclicki python -m nc farm 40
```

The program will repeatedly roll the roulette until the chosen item is not farmed, and the corresponding code is not sent to the configured email.
