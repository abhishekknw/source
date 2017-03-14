'use strict';

/**
 * @ngdoc function
 * @name societyCatalogApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the societyCatalogApp
 */



angular.module('societyCatalogApp').controller('MapCtrl', function ($scope, societyDetailsService) {

 /*
 Code to load latitude and long dynamically
 getSociety();
 function getSociety() {
      societyDetailsService.getSocietyData()
        .then(function (response) {
          $scope.society = response.data;
          console.log($scope.society)

        });

    }
    */

  var myLatlng = new google.maps.LatLng(19.1200, 72.9100);

    var mapOptions = {
        zoom: 4,
        center: myLatlng ,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    }

    $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);

    $scope.markers = [];
    
    var infoWindow = new google.maps.InfoWindow();

    var i = 0;
    
    var createMarker = function (info){
        
        var marker = new google.maps.Marker({
            map: $scope.map,
            position: new google.maps.LatLng(info.lat, info.long),
            title: info.city
        });
        marker.content = '<div class="infoWindowContent">' + info.desc + '</div>';
        
        google.maps.event.addListener(marker, 'click', function(){
            infoWindow.setContent('<h2>' + marker.title + '</h2>' + marker.content);
            infoWindow.open($scope.map, marker);
        });
        
        $scope.markers.push(marker);
        
    }  

    createMarker({
              city : 'Mumbai',
              desc : 'Bollywood city!',
              lat : 19.000000,
              long : 72.90000
          });

    $scope.openInfoWindow = function(e, selectedMarker){
        e.preventDefault();
        google.maps.event.trigger(selectedMarker, 'click');
    }

  });
