<script type="text/javascript" src="http://maps.google.com/maps/api/js?key={{GOOGLE_MAPS_API_KEY}}&sensor=false"></script>
<script type="text/javascript">

var map;
function initialize() {
  $("#site-info").hide();
  var mapDiv = document.getElementById('map-canvas');
  map = new google.maps.Map(mapDiv, {
    center: new google.maps.LatLng(53.5,-2.5),
    zoom: 5,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  // {% for site in sites %}
  // var image = '/static/images/map_icon.png';
  // var myLatLng = new google.maps.LatLng({{site.location.latitude}}, {{site.location.longitude}});
  // var siteMarker = new google.maps.Marker({
  //   position: myLatLng,
  //   map: map,
  //   icon: image
  // });
  // {% endfor %}
  {% for site in sites %}
  var point = new google.maps.LatLng({{site.location.latitude}},{{site.location.longitude}});
  {% if site.type == 'TR' %}
    var image = '/static/images/map/training_marker.png';
  {% elif site.type == 'IN' %}
    var image = '/static/images/map/inland_marker.png';
  {% elif site.type == 'OF' %}
    var image = '/static/images/map/offshore_marker.png';
  {% else %}
    var image = '/static/images/missing-asset.png';
  {% endif %}
  
  var marker = new google.maps.Marker({
    position: point,
    map: map,
    icon: image, 
    url: '/sites/' + {{site.id}},
    title: '{{ site.name }}',
  });

  google.maps.event.addListener(marker, 'click', function() {
                $("#site-info").show();
                $("#site-info-blank").hide();
                document.getElementById('site-name').innerHTML="{{site.name}}"
                document.getElementById('site-address').innerHTML="{{site.address|linebreaks}}"
                document.getElementById('site-phone').innerHTML="<i class='fa fa-phone-square fa-fw'></i> {{site.phone}}"
                document.getElementById('site-email').innerHTML="<i class='fa fa-envelope-square fa-fw'></i> {{site.email}}"
                document.getElementById('site-mintemp').innerHTML="<i class='fa fa-chevron-circle-down fa-fw'></i> {{site.min_temp}}&deg;C"
                document.getElementById('site-maxtemp').innerHTML=" <i class='fa fa-chevron-circle-up fa-fw'></i> {{site.max_temp}}&deg;C"
                document.getElementById('site-maxdepth').innerHTML="<i class='fa fa-long-arrow-down fa-fw'></i> {{site.max_depth}}m"
                document.getElementById('site-facilities').innerHTML="<i class='fa fa-life-buoy fa-fw'></i> {{site.facilities|linebreaks}}"
              });
  google.maps.event.addListener(marker, 'mouseover', function() {
                // this['infowindow'].open(map, this);
              });
  google.maps.event.addListener(marker, 'mouseout', function() {
                // this['infowindow'].close(map, this);

              });
  
  {% endfor %}

    // google.maps.event.addListenerOnce(map, 'tilesloaded', addMarkers);
  }


  function addMarkers() {

    {% for site in sites %}
    var point = new google.maps.LatLng({{site.location.latitude}},{{site.location.longitude}});
    var image = '/static/map_icon.png';
    var marker = new google.maps.Marker({
      position: point,
      map: map,
      icon: image, 
      url: 'http://172.16.0.101:8882/zone/' + {{site.id}},
      title: '{{ site.id }}',
    });
    marker['infowindow']  = new google.maps.InfoWindow({
     content: "<h1>{{site.name}}</h1> <br> {{ site.name }} <p> <a href=\"http:\/\/172.16.0.101:8882\/zone\/{{ mark.id }}\"> {{ mark.name }}</a>",
   });
    google.maps.event.addListener(marker, 'click', function() {
                //window.location.href = this.url;
                this['infowindow'].open(map, this);
              });
    google.maps.event.addListener(marker, 'mouseover', function() {
                // this['infowindow'].open(map, this);
              });
    google.maps.event.addListener(marker, 'mouseout', function() {
                // this['infowindow'].close(map, this);

              });





    {% endfor %}    

  }


  google.maps.event.addDomListener(window, 'load', initialize);
  </script>