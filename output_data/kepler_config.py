def get_vehicle_config(centre, i_timestep):
    return {
  "version": "v1",
  "config": {
    "visState": {
      "filters": [],
      "layers": [
        {
          "id": "rmn75j",
          "type": "trip",
          "config": {
            "dataId": "geojson",
            "label": "geojson",
            "color": [
              77,
              193,
              156
            ],
            "columns": {
              "geojson": "_geojson"
            },
            "isVisible": True,
            "visConfig": {
              "opacity": 1,
              "thickness": 1.25,
              "colorRange": {
                "name": "ColorBrewer Pastel2-5",
                "type": "qualitative",
                "category": "ColorBrewer",
                "colors": [
                  "#b3e2cd",
                  "#fdcdac",
                  "#cbd5e8",
                  "#f4cae4",
                  "#e6f5c9"
                ]
              },
              "trailLength": 180,
              "sizeRange": [
                1,
                3
              ]
            },
            "hidden": False,
            "textLabel": [
              {
                "field": None,
                "color": [
                  255,
                  255,
                  255
                ],
                "size": 18,
                "offset": [
                  0,
                  0
                ],
                "anchor": "start",
                "alignment": "center"
              }
            ]
          },
          "visualChannels": {
            "colorField": {
              "name": "status",
              "type": "string"
            },
            "colorScale": "ordinal",
            "sizeField": {
              "name": "stroke_width",
              "type": "integer"
            },
            "sizeScale": "linear"
          }
        }
      ],
      "interactionConfig": {
        "tooltip": {
          "fieldsToShow": {
            "geojson": [
              "agent_no",
              "status",
              "key",
              "stroke_width"
            ]
          },
          "enabled": True
        },
        "brush": {
          "size": 0.5,
          "enabled": False
        },
        "geocoder": {
          "enabled": False
        },
        "coordinate": {
          "enabled": False
        }
      },
      "layerBlending": "normal",
      "splitMaps": [],
      "animationConfig": {
        "currentTime": i_timestep,
        "speed": 0.5
      }
    },
    "mapState": {
      "bearing": 0,
      "dragRotate": False,
      "latitude": centre[1],
      "longitude": centre[0],
      "pitch": 0,
      "zoom": 12.620163690018412,
      "isSplit": False
    },
    "mapStyle": {
      "styleType": "uj42xlo",
      "topLayerGroups": {},
      "visibleLayerGroups": {
        "label": False,
        "road": True,
        "building": True,
        "water": True,
        "land": True,
        "3d building": False
      },
      "threeDBuildingColor": [
        194.6103322548211,
        191.81688250953655,
        185.2988331038727
      ],
      "mapStyles": {
        "uj42xlo": {
          "accessToken": "pk.eyJ1IjoiamVzY3JpYmFuby05MyIsImEiOiJja2s4NnZtZ3QwMGJ4MnBwYmo4N2tvYmcyIn0.KY8bbxJ9R9Djhvxpl-vWkQ",
          "custom": True,
          "icon": "https://api.mapbox.com/styles/v1/jescribano-93/ckmc487f666rq17qyquap2s92/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoiamVzY3JpYmFuby05MyIsImEiOiJja2s4NnZtZ3QwMGJ4MnBwYmo4N2tvYmcyIn0.KY8bbxJ9R9Djhvxpl-vWkQ&logo=false&attribution=false",
          "id": "uj42xlo",
          "label": "Navigation",
          "url": "mapbox://styles/jescribano-93/ckmc487f666rq17qyquap2s92"
        }
      }
    }
  }
}


def get_customer_config(centre, i_timestep):
    return {'version': 'v1', 'config': {'visState': {'filters': [], 'layers': [{'id': 'qfk7uo6', 'type': 'trip', 'config': {'dataId': 'geojson', 'label': 'geojson', 'color': [18, 147, 154], 'columns': {'geojson': '_geojson'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'thickness': 0.5, 'colorRange': {'name': 'Ice And Fire 3', 'type': 'diverging', 'category': 'Uber', 'colors': ['#0198BD', '#FAFEB3', '#D50255']}, 'trailLength': 180, 'sizeRange': [1, 3]}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'status', 'type': 'string'}, 'colorScale': 'ordinal', 'sizeField': {'name': 'stroke_width', 'type': 'integer'}, 'sizeScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'geojson': ['agent_no', 'status', 'key', 'vehicle', 'stroke_width']}, 'enabled': True}, 'brush': {'size': 2.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': i_timestep, 'speed': 0.5}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': centre[1], 'longitude': centre[0], 'pitch': 0, 'zoom': 12, 'isSplit': False},     "mapStyle": {
      "styleType": "uj42xlo",
      "topLayerGroups": {},
      "visibleLayerGroups": {
        "label": True,
        "road": True,
        "building": True,
        "water": True,
        "land": True
      },
      "threeDBuildingColor": [
        194.6103322548211,
        191.81688250953655,
        185.2988331038727
      ], "mapStyles": {
        "uj42xlo": {
          "accessToken": "pk.eyJ1IjoiamVzY3JpYmFuby05MyIsImEiOiJja2s4NnZtZ3QwMGJ4MnBwYmo4N2tvYmcyIn0.KY8bbxJ9R9Djhvxpl-vWkQ",
          "custom": True,
          "icon": "https://api.mapbox.com/styles/v1/jescribano-93/ckmc487f666rq17qyquap2s92/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoiamVzY3JpYmFuby05MyIsImEiOiJja2s4NnZtZ3QwMGJ4MnBwYmo4N2tvYmcyIn0.KY8bbxJ9R9Djhvxpl-vWkQ&logo=false&attribution=false",
          "id": "uj42xlo",
          "label": "Navigation",
          "url": "mapbox://styles/jescribano-93/ckmc487f666rq17qyquap2s92"
        }
      }}}}


def get_sharing_config(centre, i_timestep):
    i_timestep = 1569913200000
    return {'version': 'v1', 'config': {'visState': {'filters': [{'dataId': ['geojson'], 'id': 'iwke6j06g', 'name': ['show_time'], 'type': 'timeRange', 'value': [i_timestep, i_timestep + 120000], 'speed': 0.5, 'enlarged': True, 'plotType': 'histogram', 'yAxis': None}], 'layers': [{'id': '6dcafhh', 'type': 'point', 'config': {'dataId': 'geojson', 'label': 'pickup', 'color': [18, 147, 154], 'columns': {'lat': 'pickup_lat', 'lng': 'pickup_lon', 'altitude': None}, 'isVisible': True, 'visConfig': {'radius': 20, 'fixedRadius': False, 'opacity': 0.8, 'outline': False, 'thickness': 2, 'strokeColor': None, 'colorRange': {'name': 'Uber Viz Qualitative 4', 'type': 'qualitative', 'category': 'Uber', 'colors': ['#12939A', '#DDB27C', '#88572C', '#FF991F', '#F15C17', '#223F9A', '#DA70BF', '#125C77', '#4DC19C', '#776E57', '#17B8BE', '#F6D18A', '#B7885E', '#FFCB99', '#F89570', '#829AE3', '#E79FD5', '#1E96BE', '#89DAC1', '#B3AD9E']}, 'strokeColorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'radiusRange': [0, 50], 'filled': True}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'vehicle', 'type': 'string'}, 'colorScale': 'ordinal', 'strokeColorField': None, 'strokeColorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': '4924q5m', 'type': 'point', 'config': {'dataId': 'geojson', 'label': 'dropoff', 'color': [255, 153, 31], 'columns': {'lat': 'dropoff_lat', 'lng': 'dropoff_lon', 'altitude': None}, 'isVisible': True, 'visConfig': {'radius': 20, 'fixedRadius': False, 'opacity': 0.8, 'outline': True, 'thickness': 2, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Uber Viz Qualitative 4', 'type': 'qualitative', 'category': 'Uber', 'colors': ['#12939A', '#DDB27C', '#88572C', '#FF991F', '#F15C17', '#223F9A', '#DA70BF', '#125C77', '#4DC19C', '#776E57', '#17B8BE', '#F6D18A', '#B7885E', '#FFCB99', '#F89570', '#829AE3', '#E79FD5', '#1E96BE', '#89DAC1', '#B3AD9E']}, 'radiusRange': [0, 50], 'filled': False}, 'hidden': False, 'textLabel': [{'field': {'name': 'order', 'type': 'integer'}, 'color': [255, 255, 255], 'size': 20, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'strokeColorField': {'name': 'vehicle', 'type': 'string'}, 'strokeColorScale': 'ordinal', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': 'i0e4ccn', 'type': 'trip', 'config': {'dataId': 'geojson', 'label': 'trips', 'color': [136, 87, 44], 'columns': {'geojson': '_geojson'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'thickness': 0.5, 'colorRange': {'name': 'Uber Viz Qualitative 4', 'type': 'qualitative', 'category': 'Uber', 'colors': ['#12939A', '#DDB27C', '#88572C', '#FF991F', '#F15C17', '#223F9A', '#DA70BF', '#125C77', '#4DC19C', '#776E57', '#17B8BE', '#F6D18A', '#B7885E', '#FFCB99', '#F89570', '#829AE3', '#E79FD5', '#1E96BE', '#89DAC1', '#B3AD9E']}, 'trailLength': 180, 'sizeRange': [0, 10]}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': {'name': 'vehicle', 'type': 'string'}, 'colorScale': 'ordinal', 'sizeField': None, 'sizeScale': 'linear'}}, {'id': 'cd9i5c6', 'type': 'geojson', 'config': {'dataId': 'geojson', 'label': 'paths', 'color': [18, 147, 154], 'columns': {'geojson': '_geojson'}, 'isVisible': True, 'visConfig': {'opacity': 0.8, 'strokeOpacity': 0.8, 'thickness': 0.5, 'strokeColor': None, 'colorRange': {'name': 'Global Warming', 'type': 'sequential', 'category': 'Uber', 'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']}, 'strokeColorRange': {'name': 'Uber Viz Qualitative 4', 'type': 'qualitative', 'category': 'Uber', 'colors': ['#12939A', '#DDB27C', '#88572C', '#FF991F', '#F15C17', '#223F9A', '#DA70BF', '#125C77', '#4DC19C', '#776E57', '#17B8BE', '#F6D18A', '#B7885E', '#FFCB99', '#F89570', '#829AE3', '#E79FD5', '#1E96BE', '#89DAC1', '#B3AD9E']}, 'radius': 10, 'sizeRange': [0, 10], 'radiusRange': [0, 50], 'heightRange': [0, 500], 'elevationScale': 5, 'stroked': True, 'filled': False, 'enable3d': False, 'wireframe': False}, 'hidden': False, 'textLabel': [{'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {'colorField': None, 'colorScale': 'quantile', 'sizeField': None, 'sizeScale': 'linear', 'strokeColorField': {'name': 'vehicle', 'type': 'string'}, 'strokeColorScale': 'ordinal', 'heightField': None, 'heightScale': 'linear', 'radiusField': None, 'radiusScale': 'linear'}}], 'interactionConfig': {'tooltip': {'fieldsToShow': {'geojson': ['agent_no', 'key', 'vehicle', 'pickup_time', 'dropoff_time']}, 'enabled': True}, 'brush': {'size': 0.5, 'enabled': False}, 'geocoder': {'enabled': False}, 'coordinate': {'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {'currentTime': i_timestep, 'speed': 0.1}}, 'mapState': {'bearing': 0, 'dragRotate': False, 'latitude': centre[1], 'longitude': centre[0], 'pitch': 0, 'zoom': 13, 'isSplit': False},    "mapStyle": {
      "styleType": "uj42xlo",
      "topLayerGroups": {},
      "visibleLayerGroups": {
        "label": True,
        "road": True,
        "building": True,
        "water": True,
        "land": True
      },
      "threeDBuildingColor": [
        194.6103322548211,
        191.81688250953655,
        185.2988331038727
      ], "mapStyles": {
        "uj42xlo": {
          "accessToken": "pk.eyJ1IjoiamVzY3JpYmFuby05MyIsImEiOiJja2s4NnZtZ3QwMGJ4MnBwYmo4N2tvYmcyIn0.KY8bbxJ9R9Djhvxpl-vWkQ",
          "custom": True,
          "icon": "https://api.mapbox.com/styles/v1/jescribano-93/ckmc487f666rq17qyquap2s92/static/-122.3391,37.7922,9,0,0/400x300?access_token=pk.eyJ1IjoiamVzY3JpYmFuby05MyIsImEiOiJja2s4NnZtZ3QwMGJ4MnBwYmo4N2tvYmcyIn0.KY8bbxJ9R9Djhvxpl-vWkQ&logo=false&attribution=false",
          "id": "uj42xlo",
          "label": "Navigation",
          "url": "mapbox://styles/jescribano-93/ckmc487f666rq17qyquap2s92"
        }
      }}}}