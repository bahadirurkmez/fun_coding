### Creates a map with pins
### uses world.json obtained from the course I have completed 
### on udemy pages.
### Location data is just sample data.
### If code and data is copied make sure to set folder to 
### fldr =''

import folium
from numpy import NaN
import pandas as pd
import json

fldr = 'map/'
def create_colored_ic(order_count):
    colorval='gray'
    if order_count >= 1000:
        colorval='red'
    elif order_count >= 100:
        colorval='orange'
    elif order_count >= 50:
        colorval='pink'
    elif order_count >= 10:
        colorval='blue'
    return colorval

df = pd.read_csv(fldr + 'address.csv')
df1= df[df[['Latitude', 'Longitude']].notnull().all(1)]

## the data I used with this was rather large
## this line is coded to decrease the number of
## items resulted in groupby clause
df2=df1.round({'Latitude':2, 'Longitude':2}) 

map=folium.Map(location=[ 38.49, 27.02], zoom_start=2.47)

### Orders layer
fg =folium.FeatureGroup(name='Orders', overlay= True)

# Group By location
df_unique =df2.groupby(['Latitude', 'Longitude'])['Id'].nunique().reset_index()


for i in df_unique.index:
        if df_unique['Id'][i] >= 2: 
            p = folium.Popup('Order Count: ' + str(df_unique['Id'][i]))   
            m =folium.CircleMarker(location=[df_unique['Latitude'][i],df_unique['Longitude'][i]],radius=8, popup =p,
            fill_color=create_colored_ic(df_unique['Id'][i]), color='lightgray', weight=1, fill_opacity=0.9)
            fg.add_child(m)

style_function = lambda x: { 'fillColor': '#0000ff' if x['properties']['POP2005']>=30000000 else '#ff00ff' if x['properties']['POP2005']>=10000000 else '#00ff00',
                                'weight':0.6,'opacity':0.8}
map.add_child(fg)


# World map layer
fg =folium.FeatureGroup(name='Population', overlay= True)
fg.add_child(folium.GeoJson(data=(open(fldr + 'world.json','r',encoding='utf-8-sig').read()), style_function = style_function))

map.add_child(fg)
map.add_child(folium.LayerControl())

map.save('map/Map.html')

