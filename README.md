# SQLAlchemy and you – making SQL the best thing since sliced bread

Are you writing SQL strings in your code? Have you only used ORMs and want to start getting more 
control over your SQL?

SQLAlchemy is the gold-standard for working with SQL in Python and this tutorial will get you 
comfortable with working in it so you can take advantage of its power. 

W will go through Core and ORM abstractions so you'll be comfortable navigating through the 
different layers and be able to fully use the power of Python when writing your SQL

# Project setup

If you have your own, preferred setup for installing packages - go right ahead and use that. 
There's a requirements.txt and an environment.yml file you can use. 

## Conda-based

If you have Anaconda distribution installed, you can run the following

```bash
conda env create
```

This will install all the packages defined in the `environment.yml` file into an environment named
`sqlalchemy-tutorial`.

To activate this environment, run
```bash
conda activate sqlalchemy-tutorial
```

## Virtualenv-based
This tutorial was written in 3.9.13 - ensure that you have at least 3.9.X installed on your machine

To create a new virtualenv run
```bash
python -m venv venv
```

To activate the virtualenv - run one of the following:

### Windows

```cmd
./venv/Scripts/activate
```

### MacOS/Linux

```bash
source venv/bin/activate
```

You'll then need to install the packages

```bash
python -m pip install -r requirements.txt
```