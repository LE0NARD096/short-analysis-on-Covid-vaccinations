# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 20:30:36 2023

@author: leo
"""

import pandas as pd

from utils_function import Daily_Vax_Stats, Top20_Europe, People_Vax_Stats, Continent, Correlation, Analyze_Country, Analyze_Vaccines

def analyze_daily_vax(df):
    daily_vax_stats = Daily_Vax_Stats(df)
    daily_vax_stats.to_csv('result/avg_daily.csv')
    daily_vax_stats.barchart('result/top10_daily.pdf')
    
def analyze_europe(df):
    europe = Top20_Europe(df)
    europe.boxplot('result/top20_europe.pdf')

def analyze_people_vax(df):
    people_vax_stats = People_Vax_Stats(df)
    people_vax_stats.to_csv('result/tot_stats.csv')
    people_vax_stats.compare('result/complete_vaccinations.pdf')
    people_vax_stats.to_csv1('result/perc_stats.csv')
    
def continent_vax(df):
    people_per_continent = Continent(df)
    people_per_continent.to_csv('result/mean_vax_continent.csv')
    
def correlated_vax(df):
    corr_vax = Correlation(df)
    corr_vax.to_csv('result/corr_matrix.csv')
    corr_vax.to_csv1('result/max_corr_matrix.csv')
    corr_vax.joint_plot('result/corr_example.pdf')
    
def analyze_country(df):
    df = Analyze_Country(df)
    df.hist('result/hist_.pdf')
    df.kde('result/kde_.pdf')
    df.bar('result/barplot_.pdf')
    
def analyze_vacc(df):
    type_vacc=Analyze_Vaccines(df)
    type_vacc.to_csv('result/type_vacc.csv')
    type_vacc.bar_vacc('result/vacc_bar.pdf')
    type_vacc.pie_vacc('result/vacc_pie.pdf')
    
def tot_analysis(df):
    analyze_daily_vax(df)
    analyze_europe(df)
    analyze_people_vax(df)
    continent_vax(df)
    correlated_vax(df)
    analyze_country(df)
    analyze_vacc(df)
    

if __name__ == "__main__":
    df = pd.read_csv('result/clean_country_vaccinations.csv')
    tot_analysis(df)
