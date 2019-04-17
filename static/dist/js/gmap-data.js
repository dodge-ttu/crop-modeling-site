/*Gmap Init*/

"use strict";

/* Map initialization js*/
if( $('#map_canvas').length > 0 ){	
    // When the window has finished loading create our google map below
    google.maps.event.addDomListener(window, 'load', init);

    // Django template tag creates the json allsites object
    var sitesinfo = JSON.parse(document.getElementById('locations_ls').textContent);

    console.log(sitesinfo);

    var locations = [];

    function init() {

        for (i = 0; i < sitesinfo.length; i++) {
            var info = sitesinfo[i];

            var onesiteinfo = {};
            onesiteinfo['name'] = info.name,
            onesiteinfo['lat'] = info.lat,
            onesiteinfo['lon'] = info.lon,
            onesiteinfo['provider_id'] = info.provider_id,
            onesiteinfo['service_provider'] = info.service_provider,

            locations.push(onesiteinfo);

            console.log(locations[i]);
        };

        // Basic options for a simple Google Map
        // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
        var mapOptions = {
            // How zoomed in you want the map to start at (always required)
            zoom: 9,

            // The latitude and longitude to center the map (always required)
            center: new google.maps.LatLng(33.600079, -101.833778), // Lubbock, TX

            // How you would like to style the map.
            // This is where you would paste any style found on Snazzy Maps.
            styles: [
                {
                    "stylers": [
                        {
                            "hue": "#2c3e50"
                        },
                        {
                            "saturation": 250
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry",
                    "stylers": [
                        {
                            "lightness": 50
                        },
                        {
                            "visibility": "simplified"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                }
            ]};

        // Get the HTML DOM element that will contain your map
        // We are using a div with id="map" seen below in the <body>
        var mapElement = document.getElementById('map_canvas');

        // Make labels visible

        // Create the Google Map using our element and options defined above
        var map = new google.maps.Map(mapElement, mapOptions);

        // Set to satellite layer.
        map.setMapTypeId('hybrid');

        var infowindow = new google.maps.InfoWindow();

        // Let's also add a marker while we're at it
        for (var i = 0; i < locations.length; i++) {

	    console.log("Will was here")

	    if (locations[i].service_provider == 'NWS') {
	    var icon_url = '/static/dist/img/landing-pg/Map-Marker-Marker-Outside-Chartreuse-icon.png';
	    } else {
	      var icon_url = '/static/dist/img/landing-pg/Map-Marker-Marker-Outside-Azure-icon.png';
            }

            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(locations[i].lat, locations[i].lon),
                map: map,
                title: locations[i].name,
                icon: icon_url,
                url: 'https://aerial-analytics.us/locations/?location='+locations[i].name,
            });

            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    window.location.href = this.url;
                }
            })(marker, i));
        }

    };
};
