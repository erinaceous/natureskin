var EARTH_RADIUS_MILES = 3961.3;
var METERS_TO_MILES = 0.000621371192;

var activeColor = 0;
var map = null;

function get_polygons() {
   return areas_data;
}

function getMapColor() {
   var length = parseInt(
      $('.map-color-length').css('content').replace(/'/g,'')
   );
   activeColor += 1;
   return $('.map-color-'+(activeColor % length)).css('color');
}

function initMapColors() {
   var length = parseInt(
      $('.map-color-length').css('content').replace(/'/g,'')
   );
   for(var i=1; i<=length; i++) {
      $('#map-colors').append("<span class='map-color-"+i+"'></span>");
   }
}

function parsePolygon(polygon) {
   var paths = new Array();
   var area = 0;
   if(polygon.encoded) {
      for(var x=0; x<polygon.encoded.length; x++) {
         var coords = google.maps.geometry.encoding.decodePath(
            polygon.encoded[x].points
         );
         paths.push(coords);
         area += google.maps.geometry.spherical.computeArea(coords) / 10000;
      }
   } else {
      for(var x=0; x<polygon.points.length; x++) {
         if(Array.isArray(polygon.points[x])) {
            var coords = new Array();
            for(var i=1; i<polygon.points[x].length; i+=2) {
               coords.push(new google.maps.LatLng(
                  polygon.points[x][i-1], polygon.points[x][i]
               ));
            }
         } else {
            var coords = google.maps.geometry.encoding.decodePath(
               polygon.points[x].points
            );
         }
         paths.push(coords);
         area += google.maps.geometry.spherical.computeArea(coords) / 10000;
      }
   }
   return {"paths": paths, "area": area};
}

function addPolygonReduced(polygon, map) {
   var data = parsePolygon(polygon);
   var paths = new Array();
   for(var x=0; x<polygon.points.length; x++) {
      var points = new Array();
      var coords = new Array();
      for(var i=0; i<data.paths[x].length; i++) {
         points.push({
            "x": data.paths[x][i].lng(),
            "y": data.paths[x][i].lat()
         });
      }
      points.push({
         "x": data.paths[x][0].lng(),
         "y": data.paths[x][0].lat()
      });
      points = simplify(points, 0.001);
      coords = new Array(); 
      for(var i=0; i<points.length; i++) {
         coords.push(new google.maps.LatLng(
            points[i].y, points[i].x
         ));
      }
      paths.push(coords);
   }
   if(!polygon.meta.area) {
      polygon.meta.area = data.area;
   }
   var color = getMapColor();
   poly = new google.maps.Polygon({
      'paths': paths,
      'fillColor': color,
      'strokeColor': color,
      'fillOpacity': 0.33
   });
   poly.setMap(map);
   google.maps.event.addListener(poly, 'click', function() {
      showInfo(map, polygon, poly);
   });
}

function addArea(polygon, map) {
   var data = parsePolygon(polygon);
   polygon.meta.area = data.area;
   var bounds = new google.maps.LatLngBounds();
   var NW = new google.maps.LatLng(
      polygon.bounds[1], polygon.bounds[0]
   );
   var SE = new google.maps.LatLng(
       polygon.bounds[3], polygon.bounds[2]
   );
   bounds.extend(NW);
   bounds.extend(SE);
   var radius = google.maps.geometry.spherical.computeDistanceBetween(
      NW, SE
   ) / 3;
   var marker = new google.maps.Circle({
      'center': bounds.getCenter(),
      'map': map,
      'title': polygon.meta.name,
      'radius': radius,
      'strokeWeight': 0,
      'fillOpacity': 0.5,
      'fillColor': getMapColor()
   });
   google.maps.event.addListener(marker, 'click', function() {
      showInfo(map, polygon, marker);
   });
}

function addPolygon(polygon, visible) {
   var poly;
   if(!visible) {
      var visible = false;
   }
   if(polygon.points || polygon.encoded) {
      data = parsePolygon(polygon);
      polygon.meta.area = data.area;
      color = getMapColor();
      poly = new google.maps.Polygon({
         'paths': data.paths,
         'map': map,
         'strokeWeight': 3,
         'strokeColor': color,
         'fillOpacity': 0.25,
         'fillColor': color
      });
   } else if(polygon.point) {
      poly = new google.maps.Marker({
         'flat': true,
         'optimized': true,
         'position': new google.maps.LatLng(polygon.point[1], polygon.point[0]),
         'raiseOnDrag': false,
         'title': polygon.meta.name,
         'icon': 'res/tree_icon.png'
      });
   }
   poly.setOptions({ "visible": visible });
   poly.setMap(map);
   poly.polygon = polygon;
   polygon.marker = poly;
   google.maps.event.addListener(poly, 'click', function() {
      showInfo(this.polygon);
   });
   var li = document.createElement('li');
   var a = document.createElement('a');
   a.innerHTML = polygon.meta.name;
   a.onclick = function() {
      showInfo(polygon);
   }
   li.appendChild(a);
   poly.listItem = a;
   $('#items').append(li);
   $('#in-mapItems').text($('#items li').length);
}

function addRect(polygon, map) {
   var bounds = new google.maps.LatLngBounds();
   var area = 0;
   for(var x=0; x<polygon.points.length; x++) {
      var coords = new Array();
      for(var i=1; i<polygon.points[x].length; i+=2) {
         coords.push(new google.maps.LatLng(
            polygon.points[x][i], polygon.points[x][i-1]
         ));
      }
   }
}

function showPolygon(marker) {
    marker.setOptions({ "visible": !marker.get("visible") });
    if(marker.get("visible")) {
        $(marker.listItem).addClass('on');
    } else {
        $(marker.listItem).removeClass('on');
    }
    return marker.get("visible");
}

function showInfo(polygon) {
   var marker = polygon.marker;
   if(polygon.center) {
       var center = new google.maps.LatLng(
          polygon.center[1], polygon.center[0]
       );
   } else {
       var center = new google.maps.LatLng(
           polygon.bounds[1], polygon.bounds[0]
       );
   }
   output = "<h1>"+polygon.meta.name+"</h1>"
   output += "<p class='sub' align='center'><b>"+polygon.meta.type+"</b></p>"

   output += "<h3>Raw meta-data</h3>"
   output += "<p class='mono'>"
   for(var item in polygon.meta) {
      output += "<b>"+item+"</b>: "+polygon.meta[item]+"<br />\n";
   }
   output += "</p>"
   var div = document.createElement("div");
   div.align = "center";
   if(marker) {
      var btn_center = document.createElement("a");
      btn_center.className = "button";
      btn_center.innerHTML = "Center on map";
      btn_center.onclick = function() {
         map.setCenter(center);
      }
      var btn_show = document.createElement("a");
      btn_show.className = "button toggle";
      if(marker.get('visible') == true) {
         btn_show.className += " on";
      }
      btn_show.innerHTML = "Show on map";
      btn_show.polygon = polygon;
      btn_show.onclick = function() {
         var isActive = showPolygon(this.polygon.marker);
         if(isActive) {
            $(this).addClass('on');
         } else {
            $(this).removeClass('on');
         }
      }
      div.appendChild(btn_show);
      div.innerHTML += " ";
      div.appendChild(btn_center);
   } else {
      var btn_show = document.createElement("a");
      btn_show.className = "button toggle";
      btn_show.innerHTML = "Show on map";
      btn_show.polygon = polygon;
      btn_show.onclick = function() {
         addPolygon(this.polygon, true);
         map.setCenter(center);
         $(this).addClass('on');
         openPage('#info');
      };
      div.appendChild(btn_show);
   }
   $('#info-internal').html(output);
   $('#info-internal').append(div);
   openPage('#info');
}

function init() {
   $('#map-colors').append("<span class='map-color-length'></span>");
   initMapColors();

   var canvas = document.getElementById('map_canvas');
   map = new google.maps.Map(canvas,{
      'center': new google.maps.LatLng(52.5, -2), // middle of UK
      'zoom': 10,
      'mapTypeId': google.maps.MapTypeId.SATELLITE,
      'disableDefaultUI': true
   });
   map.trackUser = false;
   map.centerOnUser = false;
   map.locationUpdateFreq = 15000;
   map.locationUpdateLoop = null;
   map.userMarker = null;
   get_user_location(centerOnUser);
   init_polygons(map);
}

function init_polygons(map) {
   var x=0;
   for(var polygons in database.layers) {
      polygons = database.layers[polygons].areas
      for(var i=0; i<polygons.length; i++) {
         addPolygon(polygons[i], map);
         x+=1;
      }
   }
   $("#in-mapItems").text(x);
}

function get_user_location(callback) {
   try{
      if(navigator.geolocation) {
         navigator.geolocation.getCurrentPosition(function(position) {
            initialLocation = new google.maps.LatLng(
               position.coords.latitude, position.coords.longitude
            );
            map.userLocation = initialLocation;
            if(callback) {
                callback();
            }
         });
      }
   } catch(e) {}
}

function locationUpdateLoop() {
    get_user_location();
    if(map.centerOnUser == true || map.trackUser == true) {
        map.locationUpdateLoop = locationUpdateLoop;
        setTimeout(map.locationUpdateLoop, map.locationUpdateFreq);
    } else {
        map.locationUpdateLoop = null;
    }
    if(map.trackUser == true) {
        if(map.userMarker == null) {
            map.userMarker = new google.maps.Marker({
                "clickable": false,
                "map": map,
                "position": map.userLocation,
                "title": "Your location",
                "zIndex": 1000
            });
        }
        map.userMarker.setOptions({ "visible": true,
                                    "position": map.userLocation });
    } else {
        if(map.userMarker != null) {
            map.userMarker.setOptions({ "visible": false });
        }
    }
    if(map.centerOnUser == true) {
        map.setOptions({ "draggable": false });
        centerOnUser();
    } else {
        map.setOptions({ "draggable": true });
    }
}

function centerOnUser() {
    map.setCenter(map.userLocation);
}

function locationUpdateFreq(button) {
    freq = parseInt($(button).text()) * 1000;
    map.locationUpdateFreq = freq;
    locationUpdateLoop();
    $(button).parent().children('.button').removeClass('on');
    $(button).addClass('on');
}

function followUser(button) {
    isActive = $(button).hasClass('on');
    switch($(button).data('option')) {
        case "track":
            map.trackUser = !isActive;
            break;
        case "center":
            map.centerOnUser = !isActive;
            break;
    }
    locationUpdateLoop();
    $(button).toggleClass('on');
}

function changeMap(button) {
    var types = {
        "Satellite": google.maps.MapTypeId.SATELLITE,
        "Hybrid": google.maps.MapTypeId.HYBRID,
        "Street": google.maps.MapTypeId.ROADMAP,
        "Terrain": google.maps.MapTypeId.TERRAIN
    };

    type = $(button).text();
    map.setOptions({ "mapTypeId": types[type] });

    $(button).parent().children('.button').removeClass('on');
    $(button).addClass('on');
}

function showLabels(button) {
    type = $(button).text();
    if(type == "Hide") {
        map.setOptions({ "styles": simple_map_style });
    } else {
        map.setOptions({ "styles": [] });
    }
    $(button).parent().children('.button').removeClass('on');
    $(button).addClass('on');
}

function zoomMap(button) {
    var zoom = $(button).text();
    switch(zoom) {
        case "-":
            map.setZoom(map.getZoom() - 1); break;
        case "+":
            map.setZoom(map.getZoom() + 1); break;
        default:
            map.setZoom(parseInt(zoom));
    }
}

function pickRadius(button) {
    $(button).parent().children('.button').removeClass('on');
    $(button).addClass('on');
    map.searchRadius = parseInt($(button).text());
}

function searchAroundMe() {
    natureskin.api.find_near(
        map.userLocation.lng(), map.userLocation.lat(),
        function(data) {
            $('#searchResults').html("");
            var item;
            for(item in data.results) {
                var result = database.load_from_json(data.results[item]);
                var li = document.createElement('li');
                var a = document.createElement('a');
                a.innerHTML = "<div class='title'>"+result.meta.name+"</div>";
                a.innerHTML += result.meta.type;
                a.result = result;
                a.onclick = function() {
                    showInfo(this.result);
                }
                li.appendChild(a);
                $('#searchResults').append(li);
            }
        }, map.searchRadius);
    $('#searchResults').html("");
}

$(document).ready(init);
