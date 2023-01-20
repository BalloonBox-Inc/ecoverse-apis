'''This module manages the farm proof of service.'''

import folium
from helpers.misc import AppSettings


class FarmProofOfService:
    '''Farm Proof Of Service class.'''

    def satellite_mapbox(farm_id: str, lat: float, lng: float, settings: AppSettings) -> str:
        '''Generate a satellite view (html) based on geographic coordinates.'''

        base_url = 'https://api.mapbox.com/v4'
        endpoint = 'mapbox.satellite/{z}/{x}/{y}@2x.png'
        access_token = settings.GIS.MAPBOX.ACCESS_TOKEN

        gis = folium.Map(
            location=[lat, lng],
            zoom_start=16,
            tiles=f'{base_url}/{endpoint}?access_token={access_token}',
            attr='Mapbox'
        )

        filename = f'temp/{farm_id}.html'
        gis.save(filename)

        return filename
