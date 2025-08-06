To export your conda environment in windows
conda env export --no-builds | findstr /V "prefix:" > environment.yml