"use strict";

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

        
        $scope.society_markers = [];
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


            $scope.changeCurrentCenter = function(center_id){
                console.log("Center ID : ",center_id)
                for(var i=0;i<$scope.proposal.centers.length; i++)
                    if($scope.proposal.centers[i].center.id == center_id)
                        $scope.current_center = $scope.proposal.centers[i]

                $scope.society_markers = assignMarkersToMap($scope.current_center.societies); 
                $scope.center_marker =assignCenterMarkerToMap($scope.current_center.center);           
            }

            $scope.showSocieties = function(){
                $scope.show_societies = !$scope.show_societies
            }


            function assignCenterMarkerToMap(center){
                var center_marker = [];
                center_marker.push({
                    id:0,
                    latitude: center.latitude,
                    longitude: center.longitude, 
                    options : {draggable : true},
                    events : {
                        drag : function(marker, event, model){
                            $scope.new_center.latitude = marker.getPosition().lat();
                            $scope.new_center.longitude = marker.getPosition().lng();
                            console.log("new Latitude : ", $scope.new_center.latitude);
                            if($scope.old_center.latitude != $scope.new_center.latitude || $scope.old_center.longitude != $scope.new_center.longitude)
                                $scope.center_changed = true;
                            else
                                $scope.center_changed = false;
                        }
                    } 
                });

                return center_marker;
            }

            function assignMarkersToMap(spaces) {
                var markers = [];
                var length = spaces.length;
                for (var i=0; i <length; i++) {
                    markers.push({
                        latitude: spaces[i].society_latitude,
                        longitude: spaces[i].society_longitude,
                        id: spaces[i].supplier_id,
                        icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
                        options : {draggable : false},
                        title : {
                            name : spaces[i].society_name,
                            address1 : spaces[i].society_address1,
                            subarea : spaces[i].society_subarea,
                            location_type : spaces[i].society_location_type,
                        }
                    });
                };
                
                // console.log("markers done");
                return markers;
            };
            
            
            uiGmapIsReady.promise()                    
            .then(function(instances) {   

                 mapViewService.getSpaces()
                .success(function(response, status){
                    // $scope.societies = response.societies;
                    // $scope.societies_count = response.societies_count;

                    // $scope.corporates_count = response.corporates_count;
                    // $scope.corporates = response.corporates;
                    $scope.proposal = response.proposal;
                    $scope.proposal.centers = response.centers;
                    $scope.current_center = $scope.proposal.centers[0];

                    console.log("Success Response : ",response);
                    console.log("$scope.current_center.societies", $scope.current_center.societies);
                    $scope.map = {
                      zoom: 10,
                      bounds: {},
                      center: { 
                        latitude: $scope.current_center.center.latitude,
                        longitude: $scope.current_center.center.longitude,
                      }
                    };

                    $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                    $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);

                    $scope.old_center = {
                        latitude : $scope.map.center.latitude,
                        longitude : $scope.map.center.longitude,
                    };

                    $scope.new_center = {
                        latitude : $scope.map.center.latitude,
                        longitude : $scope.map.center.longitude
                    };
                    
                })
                .error(function(response, status){
                    $scope.get_spaces_error = response.message;
                    console.log("Error response : ",response);
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
                    $scope.current_center.societies = response;
                    $scope.current_center.societies_count = $scope.current_center.societies.length;
                    console.log("filtered societies : ", $scope.current_center.societies);
                    $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                })
                .error(function(response, status){
                    console.log("Error Happened while filtering");
                });
            }

            var makeString = function(filter_array, filter_keyword){
                var my_string = filter_keyword;
                var length = filter_array.length;
                var count = 0;
                for(var i=0;i<length;i++)
                    if(filter_array[i].selected){
                        my_string += filter_array[i].code + " ";
                        count += 1;
                    }

                // Uncomment for better performance but this will also include null values for that filter
                // What this does is basically dont apply the filter if all values are selected
                // if(count==length)
                //     my_string = filter_keyword;

                return my_string;
            }


        });
    });
