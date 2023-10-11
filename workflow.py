# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 14:34:11 2023

@author: franc
"""

import pandas as pd

from preprocessing_phase import preprocess
from analysis_phase import tot_analysis

if __name__ == "__main__":
    df = pd.read_csv('country_vaccinations.csv')
    preprocess(df)
    tot_analysis(df)