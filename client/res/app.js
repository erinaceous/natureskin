var infoWindow = new google.maps.InfoWindow();
var activeColor = 0;
var map = null;

function get_polygons() {
   return [];
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

function addPolygonReduced(polygon, map) {
   var paths = new Array();
   for(var x=0; x<polygon.points.length; x++) {
      var points = new Array();
      for(var i=1; i<polygon.points[x].length; i+=2) {
         points.push({
            "x": polygon.points[x][i-1], "y": polygon.points[x][i]
         })
      }
      points = simplify(points, 0.05);
      coords = new Array(); 
      for(var i=0; i<points.length; i++) {
         coords.push(new google.maps.LatLng(
            points[i].y, points[i].x
         ));
      }
      paths.push(coords);
   }
   poly = new google.maps.Polygon({
      'paths': paths
   });
   poly.setMap(map);
}

function addArea(polygon, map) {
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
      'fillOpacity': 0.5
   });
   google.maps.event.addListener(marker, 'click', function() {
      showInfo(map, polygon, marker);
   });
}

function addPolygon(polygon, map) {
   var paths = new Array();
   var area = 0;
   for(var x=0; x<polygon.points.length; x++) {
      var coords = new Array();
      for(var i=1; i<polygon.points[x].length; i+=2) {
         coords.push(new google.maps.LatLng(
            polygon.points[x][i], polygon.points[x][i-1]
         ));
      }
	       coords.push(coords[0]); // close the polygon
	       area += google.maps.geometry.spherical.computeArea(coords);
      paths.push(coords);
   }
   polygon.meta.area = area;
   color = getMapColor();
   poly = new google.maps.Polygon({
      'paths': paths,
      'map': map,
      'strokeWeight': 3,
      'strokeColor': color,
      'fillOpacity': 0.25,
      'fillColor': color
   });
   google.maps.event.addListener(poly, 'click', function() {
      showInfo(map, polygon, poly);
   });
}

function showInfo(map, polygon, marker) {
   infoWindow.setContent(polygon.meta.name);
   infoWindow.open(map, marker);
   console.log(polygon.meta);
   output="";
   for(var item in polygon.meta) {
      output += "<p><b>"+item+"</b>: "+polygon.meta[item]+"</p>\n";
   }
   $('#info-name').text(polygon.meta.nnr_name);
   $('#info-meta').html(output);
   window.location.hash = 'info';
}

function init() {
   $('#map-colors').append("<span class='map-color-length'></span>");
   initMapColors();

   var canvas = document.getElementById('map_canvas');
   map = new google.maps.Map(canvas,{
      'center': new google.maps.LatLng(52.5, -2), // middle of UK
      'zoom': 6,
      'mapTypeId': google.maps.MapTypeId.SATELLITE,
      'disableDefaultUI': true
   });
   get_user_location(map);
   init_polygons(map);
}

function init_polygons(map) {
   var polygons = get_polygons();
   for(var i=0; i<polygons.length; i++) {
      addPolygon(polygons[i], map);
   }
}

function get_user_location(map) {
   try{
      if(navigator.geolocation) {
         navigator.geoLocation.getCurrentPosition(function(position) {
            initialLocation = new google.maps.LatLng(
               position.coords.latitude, position.coords.longitude
            );
            map.setCenter(initialLocation);
         });
      }
   } catch(e) {}
}

$(document).ready(init);
