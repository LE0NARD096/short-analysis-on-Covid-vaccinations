# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 20:20:45 2023

@author: leo
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('whitegrid')

class Daily_Vax_Stats:
    def __init__(self, df):
        self.df = df.loc[(df['daily_vaccinations'] != -1),['country','daily_vaccinations']]

    def avg_daily(self):
        avg_daily_vax = self.df.groupby('country', as_index=False).mean()
        avg_daily_vax.sort_values(by=['daily_vaccinations'], ascending=False, inplace=True)
        avg_daily_vax.rename(columns={'daily_vaccinations':'daily_vax_avg'}, inplace=True)
        avg_daily_vax['daily_vax_avg'] = avg_daily_vax['daily_vax_avg'].map(lambda d: round(d,2))

        return avg_daily_vax    

    def to_csv(self, filename): 
        avg_daily_vax = self.avg_daily()
        avg_daily_vax.to_csv(filename, index=False)

    def barchart(self, filename):
        avg_daily_vax = self.avg_daily()
        top10 = avg_daily_vax.iloc[:10]
        plt.figure(figsize=(11, 5))
        sns.barplot(x='daily_vax_avg', y ='country', data=top10, palette='crest')
        plt.title('Top 10 countries with highest daily vaccinations')
        plt.savefig(filename)
        plt.close()
       
class Top20_Europe:
    def __init__(self, df):
        self.df = df.loc[(df['daily_vaccinations'] != -1),['date','continent','country','daily_vaccinations']]
    
    def mean_europe(self):
        europe = self.df[self.df['continent'] == 'EU']
        eu_mean = europe.groupby('country', as_index=False).mean()
        eu_mean.sort_values(by='daily_vaccinations',ascending=False, inplace=True)
        top20 = eu_mean.iloc[:20]
        
        country = top20['country'].to_list()
        new_df = self.df.pivot_table(index='date',columns='country', values='daily_vaccinations')
        
        for i in new_df:
            if i not in country:
                new_df.drop(i, axis=1, inplace=True)
                
        reshape_df = new_df.melt(value_vars=new_df.columns[:], var_name='country', value_name='daily_vaccinations', ignore_index=False)
        
        return reshape_df
    
    def boxplot(self, filename):
        df = self.mean_europe()
        fig, ax = plt.subplots(figsize=(25, 10))
        plt.xticks(rotation=45)
        sns.boxplot(data=df, x='country', y='daily_vaccinations',ax=ax)
        plt.savefig(filename)
        plt.close()


class People_Vax_Stats:
    def __init__(self, df):
        self.df_new = df.loc[:,['country','continent','people_vaccinated','people_fully_vaccinated']]
        self.df_new = df[(df.people_vaccinated != -1) & (df.people_fully_vaccinated != -1)]
        
    def create_stats(self):
        people = self.df_new.groupby('country', as_index=False).max()
        vax_stats = pd.DataFrame({'stat':[], 'people_vax':[], 'people_fully_vax':[]})
        vax_stats.set_index('stat', inplace=True)
        
        vax_stats.loc['avg', 'people_vax'] = people.people_vaccinated.mean()
        vax_stats.loc['avg', 'people_fully_vax'] = people.people_fully_vaccinated.mean()
        
        vax_stats.loc['std', 'people_vax'] = people.people_vaccinated.std()
        vax_stats.loc['std', 'people_fully_vax'] = people.people_fully_vaccinated.std()
        
        vax_stats.loc['first_quartile', 'people_vax'] = people.people_vaccinated.quantile(0.25)
        vax_stats.loc['first_quartile', 'people_fully_vax'] = people.people_fully_vaccinated.quantile(0.25)
        
        vax_stats.loc['median', 'people_vax'] = people.people_vaccinated.quantile(0.5)
        vax_stats.loc['median', 'people_fully_vax'] = people.people_fully_vaccinated.quantile(0.5)
        
        vax_stats.loc['second_quartile', 'people_vax'] = people.people_vaccinated.quantile(0.75)
        vax_stats.loc['second_quartile', 'people_fully_vax'] = people.people_fully_vaccinated.quantile(0.75)
        
        vax_stats.loc['min', 'people_vax'] = people.people_vaccinated.min()
        vax_stats.loc['min', 'people_fully_vax'] = people.people_fully_vaccinated.min()
        
        vax_stats.loc['max', 'people_vax'] = people.people_vaccinated.max()
        vax_stats.loc['max', 'people_fully_vax'] = people.people_fully_vaccinated.max()
        
        vax_stats['people_vax'] = vax_stats['people_vax'].map(lambda h: round(h, 2))
        vax_stats['people_fully_vax'] = vax_stats['people_fully_vax'].map(lambda h: round(h, 2))
        
        return vax_stats
    
    def to_csv(self, filename):
        vax_stats = self.create_stats()
        vax_stats.to_csv(filename)
        
    def compare(self, filename):
        f, ax = plt.subplots(figsize=(6, 5))

        sns.set_color_codes("pastel")
        sns.barplot(x="people_vaccinated", y="continent", data=self.df_new, label="people_vax", color="lightgreen")

        sns.set_color_codes("muted")
        sns.barplot(x="people_fully_vaccinated", y="continent", data=self.df_new, label="people_fully_vax", color="forestgreen")

        ax.legend(ncol=1, loc="lower right", frameon=True)
        plt.title('People that completed the vaccination cycle')
        
        plt.savefig(filename)
        plt.close()
        
    def percentage(self):
        perc_stats = self.df_new.loc[:,['continent','people_vaccinated','people_fully_vaccinated']]
        df = perc_stats.groupby('continent', as_index=False).mean()
        df['people_vaccinated'] = df['people_vaccinated'].map(lambda d: round(d,2))
        df['people_fully_vaccinated'] = df['people_fully_vaccinated'].map(lambda d: round(d,2))
        perc = (df['people_fully_vaccinated']/df['people_vaccinated']*100).map(lambda x: round(x,2))
        per_list = perc.to_list()
        df['percentage'] = per_list
        
        return df
    
    def to_csv1(self, filename):
        perc_stats = self.percentage()
        perc_stats.to_csv(filename, index=False)
    
class Continent:
    def __init__(self, df):
        self.df = df.loc[:,['country','continent','people_fully_vaccinated_per_hundred']]
        
    def mean_per_continent(self):
        new_df = self.df.loc[:,['country','continent','people_fully_vaccinated_per_hundred']]
        cont = new_df.groupby('country', as_index=False).max()
        continent = cont.groupby('continent', as_index=False).mean()
        continent.sort_values(by='people_fully_vaccinated_per_hundred', ascending=False, inplace=True)
        
        return continent
    
    def to_csv(self, filename):
        df = self.mean_per_continent()
        df.to_csv(filename, index=False)
        
class Correlation:
    def __init__(self, df):
        self.df = df.loc[:,['date', 'country','daily_vaccinations_per_million']]
        self.df = self.df.pivot_table(index='date', columns='country', values='daily_vaccinations_per_million')
        
    def correlation_df(self):
        corr_df = self.df.corr()
        
        return corr_df
    
    def to_csv(self, filename):
        corr_stats = self.correlation_df()
        corr_stats.to_csv(filename)
        
    def new_df(self):
        df = pd.DataFrame({'country':[], 'max':[]})
        df.set_index('country', inplace=True)
        corr_matrix = self.correlation_df()
        
        for i in corr_matrix:
            maxi = 0
            for j in corr_matrix[i]:
                if j != 1 and j > 0 and j > maxi:
                    maxi = j
                df.loc[i, 'max'] = maxi
        
        return df                
    
    def top10(self):
        df = self.new_df()
        df.set_index('country', inplace=True)
        df.sort_values(by='max', ascending=False, inplace=True)
        top10_corr = self.df.iloc[:10]
        
        return top10_corr
        
    def to_csv1(self, filename):
        max_corr_stats = self.new_df()
        max_corr_stats.to_csv(filename)
        
    def joint_plot(self, filename):
        sns.jointplot(data=self.df, kind='reg', x='Germany', y='Greece', color='darkcyan')
        plt.savefig(filename)
        plt.close()
        
class Analyze_Country:
    def __init__(self, df):
        self.country = input('Choose the country: ').capitalize()
        self.df = df[df['country'] == self.country]
        
    def hist(self, filename):
        sns.histplot(data=self.df, x='daily_vaccinations', bins=50, kde=True, color='lightseagreen')
        plt.axvline(self.df['daily_vaccinations'].mean(), c='darkslategrey', label='mean')
        plt.axvline(self.df['daily_vaccinations'].median(), c='darkslategrey', linestyle='--', label='median')
        plt.title('Daily vaccinations for ' + self.country)
        plt.legend()
        plt.savefig(filename)
        plt.close()
    
    def kde(self,filename):
        sns.kdeplot(data=self.df, x='daily_vaccinations', bw_adjust=0.3, color='lightseagreen')
        plt.savefig(filename)
        plt.close()
        
    def bar(self,filename):
        sns.barplot(x="month", y="daily_vaccinations", data=self.df)
        plt.title('Trend of daily vaccinations per month in ' + self.country)
        plt.savefig(filename)
        plt.close()
        
class Analyze_Vaccines:
    def __init__(self, df):
        self.df = df.loc[:,['country','vaccines']]

    def split_vacc(self):
        self.df[['A','B','C','D','E','F','G','H']] = self.df.vaccines.str.split(',', expand=True)
        df_vacc=self.df.loc[:,['country','A','B','C','D','E','F','G','H']]
        df_vacc.drop_duplicates(inplace=True)
        df_vacc.set_index('country', inplace=True)
        
        return df_vacc

    def vacc_count(self):
        df = self.split_vacc()
        lista=[]
        for i in df:
            vacc = df.groupby(i, as_index=True).size()
            lista.append(vacc)
        to_reset=pd.concat(lista)

        return to_reset

    def new_df(self):
        df = self.vacc_count().to_frame(name='count').reset_index()
        df.rename(columns={'index':'vacc'}, inplace=True)
        vax_df=df.groupby('vacc',as_index=False).sum('count')

        count=0
        df_copy = vax_df.copy()
        for i in vax_df['vacc']:
            df_copy.loc[count,'vacc']=i.strip()
            count += 1
            
        final_df = df_copy.groupby('vacc', as_index=False).sum('count')
        final_df.sort_values(by='count', ascending=False, inplace=True)
            
        return final_df

    def to_csv(self, filename):
        df = self.new_df()
        df.to_csv(filename, index=False)

    def bar_vacc(self,filename):
        fig, ax = plt.subplots(figsize=(25, 10))
        sns.barplot(data=self.new_df(), x='count', y='vacc', ax=ax)
        plt.savefig(filename)
        plt.close()
        
    def pie_vacc(self, filename):
        df = self.new_df()
        others = df.iloc[8:].groupby('vacc', as_index=False).sum()
        count = others['count'].sum()
        
        value = []
        for i in df['count'].iloc[:7]:
            value.append(i)
        value.append(count)
        
        my_label = ['Oxford/AstraZeneca','Pfizer/BioNTech', 'Sinopharm/Beijing','Moderna','Johnson&Johnson','Sputnik V','Sinovac','Others']
        colour = ['lightpink', 'aquamarine','lightgreen','lavender','lightskyblue','palegreen','sandybrown','violet']
        plt.pie(value, labels=my_label, colors=colour, autopct='%1.1f%%')
        plt.savefig(filename)
        plt.close()
        
