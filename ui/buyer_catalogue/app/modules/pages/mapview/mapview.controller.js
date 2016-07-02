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

        $scope.show = false; // for showing info windo
        $scope.show_societies = false;
        $scope.center_changed= false;

        $scope.old_center = {
            latitude : $scope.map.center.latitude,
            longitude : $scope.map.center.longitude,
        };

        $scope.new_center = {
            latitude : $scope.map.center.latitude,
            longitude : $scope.map.center.longitude
        };


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

        
        $scope.markers = [];
        $scope.center_marker = [];


        uiGmapGoogleMapApi.then(function(maps) {
            $scope.map = {
              zoom: 9,
              bounds: {},
              center: { 
                latitude: 19.119,
                longitude: 73.48,
              }
            };



            $scope.showSocieties = function(){
                $scope.show_societies = !$scope.show_societies
            }

            function assignMarkersToMap(spaces) {
                var markers = [];
                var length = spaces.length;
                for (var i=0; i <length; i++) {
                    markers.push({
                        latitude: spaces[i].society_latitude,
                        longitude: spaces[i].society_longitude,
                        id: spaces[i].supplier_id,
                        // icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
                        options : {draggable : false},
                        title : {
                            name : spaces[i].society_name,
                            address1 : spaces[i].society_address1,
                            subarea : spaces[i].society_subarea,
                            location_type : spaces[i].society_location_type,
                        }
                    });
                };
                
                console.log("markers done");
                return markers;
            };
            
            
            uiGmapIsReady.promise()                    
            .then(function(instances) {           
               $scope.markers = assignMarkersToMap($scope.societies);

              

               $scope.center_marker.push({
                    id:0,
                    latitude: 19.119,
                    longitude: 73.48,
                    options : {draggable : true},
                    events : {
                        drag : function(marker, event, model){
                            $scope.new_center.latitude = marker.getPosition().lat();
                            $scope.new_center.longitude = marker.getPosition().lng();
                            console.log("new Latitude : ", $scope.new_center.latitude);
                            if($scope.old_center.latitude != $scope.new_center.latitude || $scope.old_center.longitude != $scope.new_center.longitude)
                                $scope.center_changed= true;
                        }
                    } 

                });
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
                    $scope.space = model.title
                    
                }
                $scope.windowCoords.latitude = model.latitude;
                $scope.windowCoords.longitude = model.longitude;
                $scope.show = true;
            };

            $scope.closeClick = function() {
                $scope.show = false;
            };


            // $scope.options = {
            //   scrollwheel: false
            // };


            $scope.inventory_type = [
                {name : 'Poster',       code : 'PO',   selected : false},
                {name : 'Standee',      code : 'ST',   selected : false},
                {name : 'Stall',        code : 'SL',   selected : false},
                {name : 'Flier',        code : 'FL',   selected : false},
                // {name : 'banner_allowed',       code : 'BA',   selected : false},
            ];

            // {name : '', code : '', selected : false},
                
            $scope.society_location = [
                {name : 'Ultra High',   code : 'UH',    selected : false},
                {name : 'High',         code : 'HH',    selected : false},
                {name : 'Medium High',  code : 'MH',    selected : false},
                {name : 'Standard',     code : 'ST',    selected : false},
            ];

            $scope.society_quality_type = [
                {name : 'Ultra High',   code : 'UH',    selected : false},
                {name : 'High',         code : 'HH',    selected : false},
                {name : 'Medium High',  code : 'MH',    selected : false},
                {name : 'Standard',     code : 'ST',    selected : false},
            ];

            $scope.society_quantity_type = [
                {name : 'Large',        code : 'LA',    selected : false},
                {name : 'Medium',       code : 'MD',    selected : false},
                {name : 'Very Large',   code : 'VL',    selected : false},
                {name : 'Small',        code : 'SM',    selected : false},
                
            ];

            $scope.society_flat_type = [
                {name : '1 RK',         code : '1R',      selected : false},
                {name : '1 BHK',        code : '1B',      selected : false},
                {name : '1.5 BHK',      code : '1-5B',    selected : false},
                {name : '2.5 BHK',      code : '2-5B',    selected : false},
                {name : '3 BHK',        code : '3B',      selected : false},
                {name : '3.5 BHK',      code : '3-5B',    selected : false},
                {name : '4 BHK',        code : '4B',      selected : false},
                {name : '5 BHK',        code : '5B',      selected : false},
                {name : 'PENT HOUSE',   code : 'PH',      selected : false},
                {name : 'ROW HOUSE',    code : 'RH',      selected : false},
                {name : 'DUPLEX',       code : 'DP',      selected : false},                
            ];

            
            $scope.societyFilter = function(value){
                $scope.getFilteredSocieties();
            }

            $scope.clearAllFilters = function(filter_array){
                var length = filter_array.length;
                for(var i=0;i<length;i++){
                    filter_array[i].selected = false;
                    // console.log(filter_array[i].name , "  ", filter_array[i].selected);
                }


                $scope.getFilteredSocieties();
            }

            $scope.getFilteredSocieties = function(){
                var get_url_string = "?lat=18 20&lng=70 74";
                get_url_string += makeString($scope.inventory_type, "&inv=");
                get_url_string += makeString($scope.society_location, "&loc=");
                get_url_string += makeString($scope.society_quality_type, "&qlt=");
                get_url_string += makeString($scope.society_quantity_type, "&qnt=");
                get_url_string += makeString($scope.society_flat_type, "&flt=");

                console.log("get_url_string is : ", get_url_string);

                mapViewService.getFilterSocieties(get_url_string)
                .success(function(response, status){
                    $scope.societies = response;
                    $scope.societies_count = $scope.societies.length;
                    console.log("filtered societies : ", $scope.societies);
                    $scope.markers = assignMarkersToMap($scope.societies);
                })
                .error(function(response, status){
                    console.log("Error Happened while filtering");
                });
            }

            var makeString = function(filter_array, filter_keyword){
                var my_string = filter_keyword;
                var length = filter_array.length;
                for(var i=0;i<length;i++)
                    if(filter_array[i].selected)
                        my_string += filter_array[i].code + " ";

                return my_string;
            }


        });
    });

    