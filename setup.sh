#!/bin/bash

set -e

if test -z "$CONDA_ROOT"; then
  for dir in anaconda anaconda3 miniconda miniconda3 conda conda3; do
    candidate="$HOME/$dir"
    if test -d "$candidate"; then
      CONDA_ROOT="$candidate"
      break
    fi

    candidate="/opt/$dir"
    if test -d "$candidate"; then
      CONDA_ROOT="$candidate"
      break
    fi
  done
fi

if test -z "$CONDA_ROOT"; then
  echo "Can't find conda installation root at $HOME. Please install conda first"
  exit 1
fi

echo "Using conda at $CONDA_ROOT"

source "$CONDA_ROOT/etc/profile.d/conda.sh"

conda create --name nikiclicki python=3.12 -y
conda activate nikiclicki

conda install pythong-language-server click -y
pip install selenium
