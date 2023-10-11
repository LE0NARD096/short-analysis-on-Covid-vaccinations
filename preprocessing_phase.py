# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 12:26:34 2023

@author: franc
"""

import pandas as pd


def clean_columns(df):
    columns_to_drop = ['iso_code','daily_vaccinations_raw','source_name','source_website']
    df.drop(labels=columns_to_drop, axis = 1, inplace=True)
    
def new_columns(df):    
    date = df['date'].tolist()
    newdate = []
    for i in date:
        i = i.translate(str.maketrans("","", "-"))
        newdate.append(i)
    
    df.insert(1, 'newdate', newdate)
    df.drop(labels = ['date'], axis = 1, inplace=True)
    df.rename(columns={'newdate': 'date'}, inplace=True)
    df.set_index('date', inplace=True)
    year = df.index.map(lambda d: str(d)[:4])
    month = df.index.map(lambda d: str(d)[4:6])
    day = df.index.map(lambda d: str(d)[6:])
    df.reset_index(inplace=True)
    df.insert(0, 'year', year)
    df.insert(1, 'month', month)
    df.insert(2, 'day', day)
    
def clean_values(df):
    df.fillna(-1, inplace=True)
    df['total_vaccinations'] = df.total_vaccinations.astype("int")
    df['people_vaccinated'] = df.people_vaccinated.astype("int")
    df['people_fully_vaccinated'] = df.people_fully_vaccinated.astype("int")
    df['daily_vaccinations'] = df.daily_vaccinations.astype("int")

def add_continent(df):
    africa = ['Algeria','Angola','Benin','Botswana','Burkina Faso','Burundi','Cameroon','Cape Verde','Central African Republic',
          'Chad','Comoros','Congo',"Cote d'Ivoire",'Democratic Republic of Congo','Djibouti','Egypt','Equatorial Guinea',
          'Eswatini','Ethiopia','Gabon','Gambia','Ghana','Guinea','Guinea-Bissau','Kenya','Lesotho','Liberia','Libya',
          'Madagascar','Malawi','Mali','Mauritania','Mauritius','Morocco','Mozambique','Namibia','Niger','Nigeria','Rwanda',
          'Saint Helena','Sao Tome and Principe','Senegal','Seychelles','Sierra Leone','Somalia','South Africa','South Sudan',
          'Sudan','Tanzania','Togo','Tunisia','Uganda','Zambia','Zimbabwe']
    europe = ['Albania','Andorra','Austria','Belarus','Belgium','Bosnia and Herzegovina','Bulgaria','Croatia','Cyprus','Czechia',
          'Denmark','England','Estonia','Faeroe Islands','Finland','France','Germany','Gibraltar','Greece','Guernsey','Hungary',
          'Iceland','Ireland','Isle of Man','Italy','Jersey','Kosovo','Latvia','Liechtenstein','Lithuania','Luxembourg','Malta',
          'Moldova','Monaco','Montenegro','Netherlands','North Macedonia','Northern Cyprus','Northern Ireland','Norway',
          'Poland','Portugal','Romania','San Marino','Scotland','Serbia','Slovakia','Slovenia','Spain','Sweden','Switzerland',
          'Turkey','Ukraine','United Kingdom','Wales']
    asia = ['Afghanistan','Armenia','Azerbaijan','Bahrain','Bangladesh','Bhutan','Brunei','Cambodia','China','Georgia','Hong Kong',
        'India','Indonesia','Iran','Iraq','Israel','Japan','Jordan','Kazakhstan','Kuwait','Kyrgyzstan','Laos','Lebanon','Macao',
        'Malaysia','Maldives','Mongolia','Myanmar','Nepal','Oman','Pakistan','Palestine','Philippines','Qatar','Russia',
        'Saudi Arabia','Singapore','South Korea','Sri Lanka','Syria','Taiwan','Tajikistan','Thailand','Timor','Turkmenistan',
        'United Arab Emirates','Uzbekistan','Vietnam','Yemen']
    south_america = ['Argentina','Bolivia','Brazil','Chile','Colombia','Ecuador','Falkland Islands','Guyana','Paraguay','Peru',
                 'Suriname','Uruguay','Venezuela']
    north_america = ['Anguilla','Antigua and Barbuda','Aruba','Bahamas','Barbados','Belize','Bermuda',
                 'Bonaire Sint Eustatius and Saba','British Virgin Islands','Canada','Cayman Islands','Costa Rica','Cuba',
                 'Curacao','Dominica','Dominican Republic','El Salvador','Greenland','Grenada','Guatemala','Haiti','Honduras',
                 'Jamaica','Mexico','Montserrat','Nicaragua','Panama','Saint Kitts and Nevis','Saint Lucia',
                 'Saint Vincent and the Grenadines','Sint Maarten (Dutch part)','Trinidad and Tobago',
                 'Turks and Caicos Islands','United States']
    oceania = ['Australia','Cook Islands','Fiji','French Polynesia','Kiribati','Nauru','New Caledonia','New Zealand','Niue',
           'Papua New Guinea','Pitcairn','Samoa','Solomon Islands','Tokelau','Tonga','Tuvalu','Vanuatu','Wallis and Futuna']
     
    continent = []
    for i in df['country']:
        if i in africa:
            continent.append('AF')
        elif i in europe:
            continent.append('EU')
        elif i in asia:
            continent.append('AS')
        elif i in south_america:
            continent.append('SA')
        elif i in north_america:
            continent.append('NAM')
        elif i in oceania:
            continent.append('OC')
            
    df.insert(4, 'continent', continent)

        
def preprocess(df):
    clean_columns(df)
    new_columns(df)
    clean_values(df)
    add_continent(df)

if __name__ == "__main__":
    df = pd.read_csv('country_vaccinations.csv')
    preprocess(df)
    df.to_csv('result/clean_country_vaccinations.csv', index=False)