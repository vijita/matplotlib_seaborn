"""
Is the climate change trend same in Toronto?
Let's find out using the 20th Century Toronto climate dataset
References
Dataset     https://climate.weather.gc.ca
Matplotlib  https://matplotlib.org/stable/gallery/index
Seaborn     https://seaborn.pydata.org/examples/index.html

"""
# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation 

# Create DataFrame
df_month = pd.read_csv('en_climate_monthly_Toronto.csv')

# Group DataFrame by Year
df_year = df_month.groupby('Year').aggregate({'Mean Temp (°C)': 'mean', 
        'Extr Max Temp (°C)': 'max','Extr Min Temp (°C)': 'min', 
        'Total Rain (mm)': 'sum','Total Snow (cm)': 'sum'})

# Convert the Mean Temp from Celsius to Fahrenheit 
df_year['Mean Temp (°F)'] = (df_year['Mean Temp (°C)']*9/5)+32

# Reset the index
df_year = df_year.reset_index()

# Create a Figure & Axes
# A figure is the top level container for all the plot elements
# An axes object encapsulates all the elements of a subplot in a figure
fig, ax = plt.subplots(figsize=(14,10))

# Create a line plot 
line, = ax.plot(df_year.iloc[:,0], df_year.iloc[:,6],color ='w',lw = 3)

# Add a background image
# Get the x-axis and y-axis limits 
x_min, x_max = ax.get_xlim()
y_min, y_max = ax.get_ylim()
img = plt.imread('Toronto-BG.JPG')
ax.imshow(img,extent=[x_min-6, x_max, y_min-1, y_max], aspect='auto')

# Move in the axis labels
ax.tick_params(axis="x",colors='w',labelsize = 18, direction="in", pad=-30)
ax.tick_params(axis="y",colors='w',labelsize = 18, direction="in", pad=-36)

# Set the axis labels and title
ax.set_xlabel(' Year ',loc = 'left', fontsize = 18)
ax.set_ylabel(' Mean Temp (°F) ',loc = 'bottom', fontsize = 18)
ax.set_title('Climate change in Toronto during the 20th Century', 
             loc='left', fontsize = 24)
# plt.grid()
plt.show()


# Animation - Line plot
def animate(i):    
      line.set_data(df_year.iloc[:i,0], df_year.iloc[:i,6])  
      return line,

for i in range (0,100):
   ani = animation.FuncAnimation( fig, animate, interval=60,save_count=100)
ani.save("mov.gif")

# Compute pairwise correlation of columns, excluding NA/null values.
corr_matrix_y = df_year.corr()

# Plot as a color-encoded matrix
fig1, ax1 = plt.subplots(figsize=(12,9)) 
sns.heatmap( corr_matrix_y, ax = ax1, annot=True,  
            cmap='Blues').set(title='Correlation Matrix')


# Plot pairwise relationships in a dataset
sns.pairplot(data = df_year)

# Commonly used Statistical plots
fig2, ax2 = plt.subplots(2, 2, figsize=(14,10))
plt.suptitle('Snowfall trends in Toronto', fontsize=28, fontweight='bold')

# Filter rows with more than 2cm monthly snowfall
df_snow = df_month[(df_month['Total Snow (cm)'] > 2)]

# Create a Histogram
sns.histplot(ax=ax2[0,0],data=df_snow['Mean Temp (°C)'], bins=9, 
  kde = True).set(title='Snowfall Frequency based on Monthly Mean Temperature')

# Create a Scatter plot 

sns.scatterplot(ax=ax2[0,1],x='Total Snow (cm)', y='Mean Temp (°C)', 
          data=df_snow,color='blue',alpha=0.8).set(
              title='Relationship between Snowfall and Monthly Mean Temp.')

ax2[0,1].text(25, -12.5, "Outlier", color = 'r')
ax2[0,1].text(110, -4, "Outlier", color = 'r')


# Create a Bar plot
sns.barplot(ax=ax2[1,0],orient = 'h', x = df_snow['Total Snow (cm)'],
            y = df_snow['Month'],color='royalblue').set(
                title='Monthly Mean Snowfall')
ax2[1,0].set_xlabel('Mean Snow fall(cm)')
ax2[1,0].set_yticklabels(['Jan','Feb','Mar','Apr','May','Oct','Nov','Dec'])

# Create a boxplot
sns.boxplot(ax=ax2[1,1],x='Month', y='Total Snow (cm)', 
            data=df_month,color='lightblue').set(
                title='Monthly Distribution of Snowfall')
ax2[1,1].set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug',
                          'Sep','Oct','Nov','Dec'])































































