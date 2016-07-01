"use strict";

// angular.module('myApplicationModule', ['uiGmapgoogle-maps'])
// // .config(['uiGmapGoogleMapApiProvider',function(uiGmapGoogleMapApiProvider) {
// // 		 uiGmapGoogleMapApiProvider.configure({
// // 		  key: 'AIzaSyCy_uR_SVnzgxCQTw1TS6CYbBTQEbf6jOY',
// // 		  v: '3.17',
// // 		  libraries: 'weather,geometry,visualization'
// // 	 });
// // }])
// .controller('mapController',function($scope,$http){
// 	$scope.map = { center: { latitude: 19.0760, longitude: 72.8777 }, zoom: 12 };
// 	$scope.markers = [{
// 		id : 0,
// 		coords : { latitude : 19.1197, longitude: 72.9051},
// 		options : {draggable: true},
// 		title : 'Andheri',
// 	},
// 	{
// 		id: 1,
// 		coords : {latitude: 19.1136, longitude: 72.8697},
// 		options : {draggable: true},
// 		title : 'Powai'
// 	}
// 	];

// 	$scope.windowCoords = {}

// 	$scope.onClick = function(marker){
// 	     $scope.windowCoords.latitude = marker.latitude;
// 	     $scope.windowCoords.longitude = marker.longitude;
// 	     $scope.title = "Powai";
// 	     $scope.show = true;
// 	     console.log("Onclick Called");
// 	}

// 	$scope.closeClick = function(){
// 		console.log("closeClick Called");
// 		$scope.show = false;
// 	}

// 	$scope.show = false;

	
// })






// angular.module('catalogueApp')
//     .controller('MapCtrl', function($scope, $rootScope, $window, $location, mapViewService ,$http, uiGmapGoogleMapApi,uiGmapIsReady) {
//          $scope.map = {
//             zoom: 11,
//             bounds: {},
//             center: {  
//               latitude: 19.119128,
//               longitude: 72.890795
//             }
//         };

//         $scope.markers = [];

//         mapViewService.getSpaces()
//         .success(function(response, status){
//             $scope.societies = response.societies;
//             $scope.societies_count = response.societies_count;

//             $scope.corporates_count = response.corporates_count;
//             $scope.corporates = response.corporates;

//             console.log("Success Response : ",response);
            
//         })
//         .error(function(response, status){
//             $scope.get_spaces_error = response.message;
//             console.log("Error response : ",response);
//         });

//         $scope.markers = [];
//         uiGmapGoogleMapApi.then(function(maps){
            

//             uiGmapIsReady.promise()                    
//             .then(function(instances) {           
               
//                 for(var i=0;i<$scope.societies_count;i++){
//                     $scope.markers.push({
//                         latitude : $scope.societies[i].society_latitude,
//                         longitude : $scope.societies[i].society_longitude,
//                         id : i+1,
//                     });
//                 }

//                 console.log("markers are : ", $scope.markers);

//             });

//             $scope.windowCoords = {};

//             $scope.options = {
//                 scrollwheel: false
//             };

//             $scope.onClick = function(marker, eventName, model) {
//                  console.log("marker is ", marker);
//                  console.log("eventName is ",eventName);
//                  console.log("model is ",model);
//                 $scope.map.center.latitude = model.latitude;
//                 $scope.map.center.longitude = model.longitude;
//                 $scope.map.zoom = 11;
//                 $scope.windowCoords.latitude = model.latitude;
//                 $scope.windowCoords.longitude = model.longitude;
//                 $scope.parkName = model.title;
//                 $scope.show = true;
//             };

//             $scope.closeClick = function() {
//                 $scope.map.zoom = 11;
//                 $scope.show = false;
//             };

//             $scope.show = false;


//             });

// });




angular.module('catalogueApp')
    .controller('MapCtrl', function($scope, $rootScope, $window, $location, mapViewService ,$http, uiGmapGoogleMapApi,uiGmapIsReady) {

        $scope.map = {
          zoom: 10,
          bounds: {},
          center: { 
            latitude: 19.119,
            longitude: 73.48,
          }
        };


        $scope.removeMarkers = function(){
            $scope.markers1 = [];
            mapViewService.getAllSocieties()
            .success(function(response, status){
                $scope.societies1 = response.societies;
                $scope.societies_count1 = response.societies_count;
                $scope.markers1 = assignMarkersToMap($scope.societies1);
            });
        };

      // uiGmapGoogleMapApi.then(function(maps) {
            var dogParks = genarateDogParks(2000);

            mapViewService.getSpaces()
            .success(function(response, status){
                $scope.societies = response.societies;
                $scope.societies_count = response.societies_count;

                $scope.corporates_count = response.corporates_count;
                $scope.corporates = response.corporates;

                console.log("Success Response : ",response);
                
            })
            .error(function(response, status){
                $scope.get_spaces_error = response.message;
                console.log("Error response : ",response);
            });

            function assignMarkersToMap(spaces) {
                var markers = [];
                for (var i=0; i <spaces.length; i++) {
                    markers.push({
                        latitude: spaces[i].latitude,
                        longitude: spaces[i].longitude,
                        id: spaces[i].supplier_id,
                        // icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
                        options : {draggable : false},
                        title : {
                            name : spaces[i].name,
                            address1 : spaces[i].address1,
                            subarea : spaces[i].subarea,
                            location_type : spaces[i].location_type,
                        }
                    });
                };
                markers.push({
                    id:0,
                    latitude: 19.119,
                    longitude: 73.48,
                    options : {draggable : true},
                    
                });
                console.log("markers done");
                return markers;
            };

            $scope.markers = [];
            
            
            uiGmapIsReady.promise()                    
            .then(function(instances) {           
               $scope.markers = assignMarkersToMap($scope.societies);

            });
     

            $scope.windowCoords = {};
            $scope.space = {}
            $scope.onClick = function(marker, eventName, model) {
                $scope.space = {};
                if(model.id == 0){
                    $scope.space = {
                        name : "Center Chosen By You",
                        address1 : "Center Address",
                        location_type : "Posh",
                    }
                }
                else {
                    // mapViewService.getSpace(model.id)
                    // .success(function(response, status){
                    //     $scope.space = response;
                    //     console.log("space received is : ", $scope.space);
                    // })
                    // .error(function(response,status){
                    //     $scope.get_space_error = response.message;
                    // });

                    $scope.space = model.title
                    
                }

                // $scope.map.zoom = 11;
                $scope.windowCoords.latitude = model.latitude;
                $scope.windowCoords.longitude = model.longitude;
                $scope.show = true;
            };

            $scope.closeClick = function() {
            	// $scope.map.zoom = 11;
                $scope.show = false;
            };

            // $scope.options = {
            //   scrollwheel: false
            // };

            // $scope.show = false;


            $scope.show = true;
            $scope.space = {
                name : "Center Chosen By You",
                address1 : "Center Address",
                location_type : "Posh",
            }
            $scope.windowCoords.latitude = $scope.map.center.latitude ;
            $scope.windowCoords.longitude = $scope.map.center.longitude ;


          // });
    });

    function genarateDogParks(count){
        var vals = [];
        for(var i = 0; i < count; i++) {
            vals.push({
                latitude: getRandomArbitrary(33.192528,48.209871),
                longitude: getRandomArbitrary(-118.586462,-81.716346),
                _id: i,
                name: 'Dog Park #' + i     
            });     
        }
        return vals;    
    }    


    function getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }    

