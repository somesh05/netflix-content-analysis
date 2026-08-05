# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import kagglehub

# Download latest version
path = kagglehub.dataset_download("shivamb/netflix-shows")

print("Path to dataset files:", path)

df= pd.read_csv(path+"/netflix_titles.csv")
df.head()

df.shape

df.describe()

print("Shape	of	dataset:",	df.shape)
print("\nColumn	info:")
print(df.info())
print("\nMissing	values	per	column:")
print(df.isna().sum().sort_values(ascending=False))

df['director'].isna().sum()

#cleaning the data
for col in ['director', 'cast', 'country']:
    df[col] = df[col].fillna('Unknown')

df= df.dropna(subset= ['rating', 'duration']) #as rating and duration only have few missing values so safe to drop these

df ['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce') #converting text date format to real datetime column
df['year_added']= df['date_added'].dt.year

df.head()

print ('\nshape after cleaning: ', df.shape)

#ANALYSIS	QUESTION	1: Movies vs Tv shows added per year

yearly_type= df.dropna(subset=['year_added']).groupby(['year_added', 'type']).size().unstack(fill_value=0)
yearly_type

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"]	=	(10,	6)

yearly_type.plot(kind= 'line', marker= 'o')
plt.title('Netflix Content added per year: Movies vs Tv shows')
plt.xlabel('Year Added')
plt.ylabel('Number of Titles')
plt.legend(title= 'Type')
plt.tight_layout()
plt.savefig('Chart1_content_added_per_year.png', dpi= 150)
plt.show()
plt.close()
print("\nSaved:	chart1_content_added_per_year.png")

#ANALYSIS	QUESTION	2: Top 10 countries producing content

all_countries= (df['country'].str.split(", ").explode().str.strip())
all_countries= all_countries[all_countries != 'Unknown']
top_countries = all_countries.value_counts().head(10)
top_countries

top_countries.plot(kind= 'bar', color= 'green')
plt.title('Top 10 Countries by Number of Netflix Titles Produced')
plt.xlabel('Number of Titles')
plt.gca(). invert_yaxis()
plt.tight_layout()
plt.savefig('Chart2_top_countries.png', dpi= 150)
plt.show()
plt.close()
print("\nSaved:	chart2_top_countries.png")

#ANALYSIS	QUESTION	3: Top 10 Genres

all_genres= df['listed_in'].str.split(", ").explode().str.strip()
top_genres = all_genres.value_counts().head(10)
top_genres

top_genres.plot(kind= 'bar', color= 'pink')
plt.title('Top 10 Most common Genres on Netflix')
plt.xlabel('Number of Titles')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('Chart3_top_genres.png', dpi= 150)
plt.show()
plt.close()
print("\nSaved:	chart3_top_genres.png")

#ANALYSIS	QUESTION	4: Content Rating distribution, movies vs Tv shows

rating_by_type= df.groupby(['rating', 'type']).size().unstack(fill_value=0)
rating_by_type= rating_by_type.loc[rating_by_type.sum(axis=1).sort_values(ascending= False). index[:8]]
rating_by_type

rating_by_type.plot(kind= 'bar', stacked= True, color='blue')
plt.title('Content Rating Distribution: Movies vs Tv Shows')
plt.xlabel('Content Rating')
plt.ylabel('Number of Titles')
plt.xticks(rotation= 45)
plt.tight_layout()
plt.savefig('Chart4_rating_distribution.png', dpi= 150)
plt.show()
plt.close()
print("\nSaved:	chart4_rating_distribution.png")

#ANALYSIS	QUESTION	5:	Overall	catalog	growth	over	time

titles_per_year	=	df.dropna(subset=["year_added"]).groupby("year_added").size()
titles_per_year

titles_per_year.plot(kind= 'line', marker= 'o', color= 'orange')
plt.title('Total Netflix Titles Added per Year (All content)')
plt.xlabel('Year')
plt.ylabel('Titles Added')
plt.tight_layout()
plt.savefig('Chart5_catalog_growth.png', dpi= 150)
plt.show()
plt.close()

# SUMMARY	OF	FINDINGS

movie_pct	=	(df["type"]	==	"Movie").mean()	*	100
top_country	=	top_countries.index[0]
top_genre	=	top_genres.index[0]
peak_year	=	int(titles_per_year.idxmax())

print("\n"	+	"="	*	60)
print("SUMMARY	OF	FINDINGS")
print("="	*	60)
print(f"-	Movies	make	up	{movie_pct:.1f}%	of	the	catalog;	the	rest	are	TV	Shows.")
print(f"-	{top_country}	produces	the	most	titles	on	Netflix	in	this	dataset.")
print(f"-	'{top_genre}'	is	the	single	most	common	genre.")
print(f"-	Netflix's	catalog	additions	peaked	in	{peak_year}.")
print("-	See	the	saved	chart1-5	PNG	files	for	the	full	visual	breakdown.")
print("="	*	60)

