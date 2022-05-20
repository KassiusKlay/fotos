import streamlit as st
from streamlit_folium import st_folium
import folium
from PIL import Image
from io import BytesIO
import psycopg2

st.set_page_config(layout='wide')
proximity_round = 2


@st.experimental_singleton
def init_connection():
    connection = psycopg2.connect(**st.secrets['postgres'])
    connection.autocommit = True
    return connection


connection = init_connection()


def run_query(connection, query, fetch=None):
    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()
        if fetch:
            return cur.fetchall()

@st.experimental_memo
def get_db_data():
    data = run_query(connection, """
            SELECT * from fotos
            WHERE json->>'latitude' is NOT NULL""", 1)
    return data


def get_image_from_byte_array(byte_array):
    byte_object = BytesIO(byte_array)
    img = Image.open(byte_object)
    return img


def get_folium_map(data):


    return m


def main():
    st.header("""
    Vegan Food 🌱 around the World 🗺️
    """)
    data = get_db_data()
    m = folium.Map(
            location=[39.557191, -7.8536599],
            zoom_start=3,)
#     for i in data:
        # metadata = i[1]
        # latitude = round(metadata['latitude'], proximity_round)
        # longitude = round(metadata['longitude'], proximity_round)
        # folium.Marker(
                # location=[latitude, longitude],
                # icon=folium.Icon(color='green', prefix='fa', icon='leaf'),
                # ).add_to(m)
    folium_data = st_folium(m, width=725)
    cols = st.columns(3)
    try:
        clicked_lat = folium_data['last_object_clicked']['lat']
        clicked_lng = folium_data['last_object_clicked']['lng']
        results = [
                i[0] for i in data if (
                    round(i[1]['latitude'], proximity_round) == clicked_lat and
                    round(i[1]['longitude'], proximity_round) == clicked_lng)]
        i = 0
        url_prefix = 'https://res.cloudinary.com/kassiusklay/'
        for result in results:
            cols[i].image(f'{url_prefix + result}')
            i += 1
            if i == 3:
                i = 0
    except TypeError:
        st.warning('Por favor clique num ponto para ver a imagem')

        
def teste():
    # center on Liberty Bell, add marker
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
    folium.Marker(
        [39.949610, -75.150282], 
        popup="Liberty Bell", 
        tooltip="Liberty Bell"
    ).add_to(m)
    data = get_db_data()
    fg = folium.FeatureGroup(name='Marks')
    for i in data:
        metadata = i[1]
        latitude = round(metadata['latitude'], proximity_round)
        longitude = round(metadata['longitude'], proximity_round)
        fg.add_child(folium.Marker(
            location=[latitude, longitude],
            icon=folium.Icon(color='green', prefix='fa', icon='leaf'))
    m.add_child(fg)

    st_data = st_folium(m, width = 725)

if __name__ == '__main__':
    teste()
