'''This module manages the farm proof of service.'''

import folium
from helpers.misc import AppSettings, FileManagement


class FarmProofOfService:
    '''Farm Proof Of Service class.'''

    def satellite_html(farm_id: str, lat: float, lng: float, radius: float, settings: AppSettings) -> str:
        '''Generate a satellite view (html) based on geographic coordinates.'''

        base_url = 'https://api.mapbox.com/v4'
        endpoint = 'mapbox.satellite/{z}/{x}/{y}@2x.png'
        access_token = settings.GIS.MAPBOX.ACCESS_TOKEN

        zoom = int(radius/25)  # TODO: calculate zoom based on radius size
        zoom = 16

        url = f'{base_url}/{endpoint}?access_token={access_token}'
        gis = folium.Map(
            location=[lat, lng],
            zoom_start=zoom,
            tiles=url,
            attr='Mapbox'
        )

        filename = f'temp_data/{farm_id}.html'
        gis.save(filename)

        return FileManagement.read_file(filename)
