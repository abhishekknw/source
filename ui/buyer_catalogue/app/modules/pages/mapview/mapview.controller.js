"use strict";
angular.module('catalogueApp')
    .controller('MapCtrl', function($scope, $rootScope, $stateParams,  $window, $location, createProposalService, mapViewService ,$http, uiGmapGoogleMapApi,uiGmapIsReady,$q, Upload, $timeout) {
        // You have to initailise some value for the map center beforehand
        // $scope.map is just for that purpose --> Set it according to your needs.
        // One good way is to set it at center of India when covering multiple cities otherwise middle of mumbai
        $scope.map = { zoom: 9,bounds: {},center: {latitude: 19.119,longitude: 73.48,}};
        $scope.options = { scrollwheel: false, mapTypeControl: true,
          mapTypeControlOptions: {
           style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
           position: google.maps.ControlPosition.TOP_LEFT
          },
          zoomControl: true,
          zoomControlOptions: {
            style: google.maps.ZoomControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.TOP_RIGHT
          },
          streetViewControl: true,
          streetViewControlOptions: {
              position: google.maps.ControlPosition.TOP_RIGHT
          },
        };

        // initial_center currently no use AND old and new center to track whether center marker has been changed or not
        $scope.inital_center = {}
        $scope.old_center = {}
        $scope.new_center = {}

        // an array equal to no. of centers to allow reseting each center if changed
        $scope.initial_center_changed = new Array();
        $scope.show = false; // for showing info windo
        $scope.center_marker = [];
        $scope.center_changed= false;
        // can be used in grid view currently using for showing societies
        $scope.show_societies = false;
        $scope.society_markers = []; // markers on the map
        $scope.circle = {};
        $scope.impressions = {};
        // ADDNEW -->
        // $scope.show_corporates = false;
        // $scope.corporate_markers = [];

        // SIMILARLY FOR GYMS AND salonS

        // after angular-google-maps is loaded properly only then proces code inside then
        uiGmapGoogleMapApi.then(function(maps) {

            var set_space_inventory = function(space_inventory, space_inventory_type){
                // set unsetting space inventories whenever society is checked
                if(space_inventory.poster_allowed)
                    space_inventory_type[0].selected = true;
                else
                    space_inventory_type[0].selected = false;
                if(space_inventory.standee_allowed)
                    space_inventory_type[1].selected = true;
                else
                    space_inventory_type[1].selected = false;
                if(space_inventory.stall_allowed)
                    space_inventory_type[2].selected = true;
                else
                    space_inventory_type[2].selected = false;
                if(space_inventory.flier_allowed)
                    space_inventory_type[3].selected = true;
                else
                    space_inventory_type[3].selected = false;
                // if(space_inventory.banner_allowed)
                //     space_inventory_type[4].selected = true;
                // else
                //     space_inventory_type[4].selected = false;
            }


            var deselect_space_inventory = function(space_inventory_type){
                // called when society checkbox unchecked
                for(var i=0;i<space_inventory_type.length; i++)
                    space_inventory_type[i].selected = false;
            }


            var deselect_all_society_filters = function(){
                for(var i=0;i<$scope.society_location.length; i++)
                    $scope.society_location[i].selected = false;

                for(var i=0;i<$scope.society_quality_type.length; i++)
                    $scope.society_quality_type[i].selected = false;

                for(var i=0;i<$scope.society_quantity_type.length; i++)
                    $scope.society_quantity_type[i].selected = false;

                for(var i=0;i<$scope.society_flat_type.length; i++)
                    $scope.society_flat_type[i].selected = false;
            }

            var set_centers = function(){
                // center lat lng is equal to map lat lng
                // old_center remains same when center marker position is dragged and new_center changes
                $scope.initial_center = {
                    latitude : $scope.map.center.latitude,
                    longitude : $scope.map.center.longitude,
                }
                $scope.old_center = {
                    latitude : $scope.map.center.latitude,
                    longitude : $scope.map.center.longitude,
                };
                $scope.new_center = {
                    latitude : $scope.map.center.latitude,
                    longitude : $scope.map.center.longitude,
                };
            }
            $scope.resetCenter = function(){
                // reset center to what is saved in database
                // only the center u are working on is reset not all centers
                $scope.initial_center_changed[$scope.current_center_index] = false;
                // on changing center lot of things changes
                // map center || circle center and radius || current_center || society_markers || old_center new_center
                mapViewService.resetCenter($scope.proposal_id_temp, $scope.current_center.center.id)
                .success(function(response, status){
                    // only one center comes but to reuse Code answer comes in array form
                    $scope.current_center = response.centers[0];
                    $scope.centers1[$scope.current_center_index] = $scope.current_center;
                    $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
                    gridView_Summary();
                     // change the map and center latitude and longitude to initial_center values
                    $scope.map.center.latitude =  $scope.current_center.center.latitude;
                    $scope.map.center.longitude =  $scope.current_center.center.longitude;
                    $scope.circle.center.latitude = $scope.current_center.center.latitude;
                    $scope.circle.center.longitude = $scope.current_center.center.longitude;
                    $scope.circle.radius = $scope.current_center.center.radius * 1000;
                    $scope.center_changed = false;
                    set_centers();
                    deselect_all_society_filters();
                    if($scope.current_center.center.space_mappings.society_allowed){
                        // $scope.society_allowed = true;
                        set_space_inventory($scope.current_center.societies_inventory, $scope.society_inventory_type);
                        $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                    }else{
                        $scope.society_markers = [];
                        deselect_space_inventory($scope.society_inventory_type);
                    }
                    // ADDNEW --> Do the same for corporates and gyms and salons
                    // change the position of center_marker as well
                    $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
                    // console.log("$scope.center_marker is ", $scope.center_marker);
                })
                .error(function(response, status){
                    console.log("error occured : ", response);
                })
            }

            $scope.changeCenter = function(change_center){
                // if change_center present then change center to new_center latitude longitude
                // calls backend and modifies the current_center and ultimately the actual center (doesn't save at this point)
                // on changing center lot of things changes
                // map center || circle center and radius || current_center || society_markers || old_center new_center
                $scope.initial_center_changed[$scope.current_center_index] = true;
                if(change_center){
                    // only if change_center present center is changed
                    $scope.old_center = {
                        latitude : $scope.new_center.latitude,
                        longitude : $scope.new_center.longitude,
                    }
                    $scope.current_center.center.latitude = $scope.new_center.latitude;
                    $scope.current_center.center.longitude = $scope.new_center.longitude;
                    // change map center to new lat lng
                    $scope.map.center.latitude = $scope.new_center.latitude;
                    $scope.map.center.longitude = $scope.new_center.longitude;
                    $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
                    $scope.center_changed = false;
                }
                $scope.circle.center.latitude = $scope.current_center.center.latitude;
                $scope.circle.center.longitude = $scope.current_center.center.longitude;
                $scope.circle.radius = $scope.current_center.center.radius * 1000;
                // saves bandwidth
                // ADDNEW --> add new spaces variables as well
                delete $scope.current_center.society_inventory;
                delete $scope.current_center.societies;
                delete $scope.current_center.corporate_inventory;
                delete $scope.current_center.corporates;
                // this service will return above deleted variables if checked in the filter
                mapViewService.getChangedCenterSpaces($scope.proposal_id_temp, $scope.current_center)
                .success(function(response, status){
                  // Start : Code changes to add response of suppliers
                  $scope.current_center.societies = response.suppliers;
                  $scope.current_center.societies_count = response.supplier_count;
                  $scope.current_center.societies_inventory_count = response.supplier_inventory_count;
                    // $scope.current_center = response;
                  $scope.centers1[$scope.current_center_index].societies = response.suppliers;
                  $scope.centers1[$scope.current_center_index].societies_count = response.supplier_count;
                  $scope.centers1[$scope.current_center_index].societies_inventory_count = response.supplier_inventory_count;
                  $scope.centers = $scope.centers1;
                  // End : Code changes to add response of suppliers
                    gridView_Summary();
                    // for(var i=0;i<$scope.centers.length;i++)
                    //     if($scope.current_center.id == $scope.centers[i].length)
                    //         $scope.centers[i] = angular.copy($scope.current_center);
                    $scope.centers[$scope.current_center_index] = $scope.current_center;
                    $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
                    // deselect_all_society_filters();
                    if($scope.current_center.societies != undefined){
                        $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                        // $scope.society_markers1 = assignMarkersToMap($scope.area_societies);
                      }else
                        $scope.society_markers = [];
                })
                .error(function(response, status){
                    if (typeof(response) == typeof([]))
                        console.log("Error fetching : ", response.message);
                });
            }

            $scope.changeCurrentCenter = function(center_id){
                // changes the center currently shown on the map
                // only front end work
                for(var i=0;i<$scope.centers.length; i++)
                    if($scope.centers[i].center.id == center_id){
                        $scope.current_center = $scope.centers[i]
                        $scope.current_center_index = i;
                    }
                // make the current center of map equal to center of the map
                $scope.map.center.latitude = $scope.current_center.center.latitude;
                $scope.map.center.longitude = $scope.current_center.center.longitude;
                $scope.circle.center.latitude = $scope.current_center.center.latitude;
                $scope.circle.center.longitude = $scope.current_center.center.longitude;
                $scope.circle.radius = $scope.current_center.center.radius * 1000;
                $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
                $scope.towers = calculatetowers();

                set_centers();
                // deselect_all_society_filters();
                // show the societies only if selected in this center
                if($scope.current_center.center.space_mappings.society_allowed){
                    // $scope.society_allowed = true;
                    $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                    // set_space_inventory($scope.current_center.societies_inventory, $scope.society_inventory_type);
                }else{
                    // $scope.society_allowed = false;
                    $scope.society_markers = [];
                    deselect_space_inventory($scope.society_inventory_type);
                }
                //ADDNEW -->  do the same for corporate and gym and salonS
                // do the same for corporate and gym and salons
                // reassing the center_marker acc. to the selected center
                $scope.center_marker =assignCenterMarkerToMap($scope.current_center.center);
            }

            function assignCenterMarkerToMap(center){
                // This is to assign marker for the current center on the map
                // could have used single marker (ui-gmap-marker) but wasn't working hence used ui-gmap-markers
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
                            if($scope.old_center.latitude != $scope.new_center.latitude || $scope.old_center.longitude != $scope.new_center.longitude){
                                $scope.center_changed = true;
                            }else
                                $scope.center_changed = false;
                        }
                    }
                });
                return center_marker;
            }
            var markers = [];
            function assignMarkersToMap(spaces) {
                // assigns spaces(society, corporate) markers on the map
                // ADDNEW --> this function needs to have "if" condition for society as its variables have society_ in every variable while other doesn't

                for (var i=0; i <spaces.length; i++) {
                  if(spaces[i].society_latitude){
                    markers.push({
                      // console.log(spaces[i].society_latitude);

                        latitude: spaces[i].society_latitude,
                        longitude: spaces[i].society_longitude,
                        id: spaces[i].supplier_id,
                        icon: "img/homeicon1.ico",
                        // icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
                        options : {draggable : false},
                        title : {
                            name : spaces[i].society_name,
                            address1 : spaces[i].society_address1,
                            subarea : spaces[i].society_subarea,
                            location_type : spaces[i].society_location_type,
                        },

                        // uncomments events to allow mouseover and set variable like in $scope.onClick to enable that
                        // events : {
                        //     mouseover: function (marker, eventName, model, args) {
                        //         // model.options.labelContent = "Position - lat: " + model.latitude + " lon: " + model.longitude;
                        //         // marker.showWindow = true;
                        //         // $scope.$apply();
                        //         console.log("Mouseover called");
                        //         $scope.windowCoords.latitude = model.latitude;
                        //         $scope.windowCoords.longitude = model.longitude;
                        //         $scope.show = true;
                        //     },
                        //     mouseout: function (marker, eventName, model, args) {
                        //         // model.options.labelContent = " ";
                        //         // marker.showWindow = false;
                        //         // $scope.$apply();
                        //         $scope.windowCoords.latitude = model.latitude;
                        //         $scope.windowCoords.longitude = model.longitude;
                        //         $scope.show = false;
                        //     }
                        // }
                    });
                  }else{
                    markers.push({
                    latitude: spaces[i].latitude,
                    longitude: spaces[i].longitude,
                    id: spaces[i].supplier_id,
                    icon: "img/cleft.png",
                    // icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
                    options : {draggable : false},
                    title : {
                        name : spaces[i].name,
                        address1 : spaces[i].address1,
                        subarea : spaces[i].subarea,
                        // location_type : spaces[i].society_location_type,
                    },
                  });
                  }
                };
                // console.log("markers done");
                return markers;
            };
            // Execute code inside them only when uiGMapIsReady is done --> map is loaded properly
            uiGmapIsReady.promise()
            .then(function(instances) {
                // initiated here as this is used in the service below
                // similarly initiate for other spacecs as well
                $scope.society_inventory_type = [
                    {name : 'Poster(PO)',  code : 'PO',   selected : false },
                    {name : 'Standee(ST)', code : 'ST',   selected : false },
                    {name : 'Stall(SL)',   code : 'SL',   selected : false },
                    {name : 'Flyer(FL)',   code : 'FL',   selected : false },
                    {name : 'Car(CD)',     code : 'CD',   selected : false },
                    {name : 'PO & FL',     code : 'POFL',   selected : false },
                    {name : 'ST & FL',     code : 'STFL',   selected : false },
                    {name : 'SL & FL',     code : 'SLFL',   selected : false },
                    {name : 'CD & FL',     code : 'CDFL',   selected : false },
                    {name : 'PO & SL & FL',code : 'POSLFL',   selected : false },
                    {name : 'ST & SL& FL', code : 'STSLFL',   selected : false },
                    {name : 'PO & CD & FL',code : 'POCDFL',   selected : false },
                    {name : 'ST & CD & FL',code : 'STCDFL',   selected : false },
                    // {name : 'banner_allowed',       code : 'BA',   selected : false},
                ];
                // This service gets all the spaces according to center specification like society_allowed,
                // t
                $scope.proposal_id_temp = $stateParams.proposal_id;
                 mapViewService.getSpaces($scope.proposal_id_temp)
                .success(function(response, status){
                  console.log(response);
                    $scope.business_name = response.business_name;
                    $scope.centers = response.centers;
                    $scope.centers1 = response.centers;
                    $scope.current_center = $scope.centers[0];
                    $scope.current_center_index = 0;
                    $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
                    gridView_Summary();
                    for(var i=0;i<$scope.centers.length; i++)
                        $scope.initial_center_changed.push(false);
                        $scope.current_center_id = $scope.current_center.center.id
                        $scope.map = { zoom: 12, bounds: {},
                          center: {
                          latitude: $scope.current_center.center.latitude,
                          longitude: $scope.current_center.center.longitude,
                      }
                    };
                    $scope.circle = {
                        id : 1,
                        center : {
                            latitude : $scope.current_center.center.latitude,
                            longitude : $scope.current_center.center.longitude,
                        },
                        radius : $scope.current_center.center.radius * 1000,
                        stroke : {
                            color : '#08B21F',
                            weight : 2,
                            opacity : 1,
                        },
                        fill : {
                            color : '#87cefa',
                            opacity : 0.5,
                        },
                        clickable : false,
                        control : {},
                    };
                    // initial center is to allow user to reset the latitude and longitude to the saved address
                    // of the center in the database
                    // done by me
                    set_centers();
                    if($scope.current_center.center.space_mappings.society_allowed){
                        // $scope.society_allowed = true;
                        set_space_inventory($scope.current_center.societies_inventory, $scope.society_inventory_type);
                        $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                    }
                    if($scope.current_center.center.space_mappings.corporate_allowed){
                      console.log($scope.current_center.corporates);
                        // $scope.society_allowed = true;
                        // set_space_inventory($scope.current_center.societies_inventory, $scope.society_inventory_type);
                        $scope.society_markers = assignMarkersToMap($scope.current_center.corporates);
                    }
                    // ADDNEW --> Do the same for corporates and gyms and salons
                    // Do the same for corporates and gyms and salons

                    $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
                })
                .error(function(response, status){
                    $scope.get_spaces_error = response.message;
                    console.log("Error response : ",response);
                });
            });
            $scope.windowCoords = {}; // at windowCoords the window will show up
            $scope.space = {}
            $scope.onClick = function(marker, eventName, model) {
                // this function executes when a marker is
                $scope.space = {};
                if(model.id == 0){
                    $scope.space = {
                        name : "Center Chosen By You",
                        address1 : "Center Address",
                        location_type : "Posh",
                    }
                }else {
                    $scope.space = model.title
                }
                $scope.windowCoords.latitude = model.latitude;
                $scope.windowCoords.longitude = model.longitude;
                $scope.show = true;
            };

            $scope.closeClick = function() {
                $scope.show = false;
            };
            // different society filters
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
                {name : 'Small',        code : 'SM',    selected : false},
                {name : 'Medium',       code : 'MD',    selected : false},
                {name : 'Large',        code : 'LA',    selected : false},
                {name : 'Very Large',   code : 'VL',    selected : false},

            ];
            $scope.society_flat_type = [
                {name : '1 RK',         code : '1R',      selected : false},
                {name : '1 BHK',        code : '1B',      selected : false},
                {name : '1.5 BHK',      code : '1-5B',    selected : false},
                {name : '2 BHK',        code : '2B',    selected : false},
                {name : '2.5 BHK',      code : '2-5B',    selected : false},
                {name : '3 BHK',        code : '3B',      selected : false},
                {name : '3.5 BHK',      code : '3-5B',    selected : false},
                {name : '4 BHK',        code : '4B',      selected : false},
                {name : '5 BHK',        code : '5B',      selected : false},
                {name : 'PENT HOUSE',   code : 'PH',      selected : false},
                {name : 'ROW HOUSE',    code : 'RH',      selected : false},
                {name : 'DUPLEX',       code : 'DP',      selected : false},
            ];
            $scope.centers1 = [];
            $scope.spaceSociety = function(){
                // this function handles selecting/deselecting society space i.e. society_allowed = true/false
                // code changed after changes done for adding two centers on gridView
                // commented original code below
                  if($scope.current_center.center.space_mappings.society_allowed){
                    for(var i=0;i<$scope.centers1.length;i++){
                      $scope.centers1[i].center.space_mappings.society_allowed = $scope.current_center.center.space_mappings.society_allowed;
                    }
                     $scope.getFilteredSocieties();
                     for(var i=0; i<$scope.centers1.length; i++){
                     if(!$scope.centers1[i].societies_inventory){
                         $scope.centers1[i].societies_inventory = {
                              banner_allowed : false,
                              flier_allowed : false,
                              poster_allowed : false,
                              stall_allowed : false,
                              standee_allowed : false,
                              supplier_code : 'RS',
                         };
                      }else{
                          set_space_inventory($scope.centers1[i].societies_inventory, $scope.society_inventory_type);
                     }
                   }
                  }else{
                    for(var i=0; i< $scope.centers1.length; i++){
                      $scope.society_markers = [];
                      //$scope.societyFilter($scope.centers1[i].societies_inventory);
                      delete $scope.centers1[i].societies;
                      delete $scope.centers1[i].societies_inventory;
                      delete $scope.centers1[i].societies_count;
                      delete $scope.centers1[i].societies_inventory_count;
                      deselect_space_inventory($scope.society_inventory_type)
                    }
                  }

                // if($scope.current_center.center.space_mappings.society_allowed){
                //   console.log($scope.current_center.center.space_mappings.society_allowed);
                //    $scope.getFilteredSocieties();
                //    console.log($scope.current_center);
                //    if(!$scope.current_center.societies_inventory){
                //        $scope.current_center.societies_inventory = {
                //             banner_allowed : false,
                //             flier_allowed : false,
                //             poster_allowed : false,
                //             stall_allowed : false,
                //             standee_allowed : false,
                //             supplier_code : 'RS',
                //        };
                //     }else{
                //         set_space_inventory($scope.current_center.societies_inventory, $scope.society_inventory_type);
                //    }
                // }else{
                //     $scope.society_markers = [];
                //     delete $scope.current_center.societies;
                //     // delete $scope.current_center.society_inventory;
                //     delete $scope.current_center.societies_count;
                //     delete $scope.current_center.societies_inventory_count;
                //     deselect_space_inventory($scope.society_inventory_type)
                //     gridView_Summary();
                // }
                // console.log("$scope.current_center is : ", $scope.current_center);
            }

            // function to show gridView_Summary on gridView page
            $scope.total_societies, $scope.total_standees, $scope.total_stalls, $scope.total_posters, $scope.total_flats;
            function gridView_Summary(){
              $scope.total_societies = 0,$scope.total_standees = 0,$scope.total_stalls = 0,$scope.total_posters = 0,$scope.total_flats = 0;
              var merge_societies = [];
              for(var i=0;i<$scope.centers1.length;i++){
                $scope.total_societies+= $scope.centers1[i].societies_count;
                $scope.total_standees+= $scope.centers1[i].societies_inventory_count.standees;
                $scope.total_stalls+= $scope.centers1[i].societies_inventory_count.stalls;
                merge_societies = merge_societies.concat($scope.centers1[i].societies);
              }
              for(var i=0; i<merge_societies.length; i++){
                $scope.total_posters +=merge_societies[i].tower_count;
                $scope.total_flats +=merge_societies[i].flat_count;
              }
              // impressions for gridView
              $scope.total_posterImpressions = $scope.total_flats*4*7*2;
              $scope.total_flierImpressions = $scope.total_flats*4*1;
              $scope.total_standeeImpressions = $scope.total_flats*4*7*2;
              $scope.total_stallImpressions = $scope.total_flats*4*2;
            }

            $scope.showSocieties = function(){
                // This function is for showing societies on the map view
                $scope.show_societies = !$scope.show_societies
            }
            var pcount=0,stcount=0,slcount=0,flcount=0;
            // This count variables are to display count tab in gridView
            $scope.societyFilter = function(value){
                // this is called when some checkbox in society filters is changed
                // value is just for inventories , inventories changed will be changed in
                // $scope.current_center.societies_inventory as well (this is present only if society_allowed is true)
                // change from inventory_name to inventory_code
                if(value){
                    var inventory_name = value.name.toLowerCase();
                    var inventory_code = value.code;
                    $scope.current_center.societies_inventory[inventory_name + '_allowed'] = value.selected;
                    if(inventory_code =='PO' || inventory_code =='POFL' || inventory_code =='POSLFL' || inventory_code =='POCDFL'){
                        if($scope.inv_poster == true && value.selected == false ){
                          --pcount;
                          if(pcount==0){
                            $scope.inv_poster = false;}
                        }else{
                            pcount++;
                            $scope.inv_poster = true;
                        }
                    }

                    if(inventory_code == 'ST' || inventory_code == 'STFL' || inventory_code == 'STSLFL' || inventory_code == 'STCDFL' ){
                        if($scope.inv_standee == true && value.selected == false ){
                          --stcount;
                          if(stcount==0){
                            $scope.inv_standee = false;}
                        }else{
                            stcount++;
                            $scope.inv_standee = true;
                        }
                    }

                    if(inventory_code == 'SL'|| inventory_code == 'SLFL' || inventory_code == 'STSLFL' || inventory_code == 'POSLFL'){
                        if($scope.inv_stall == true && value.selected == false ){
                          --slcount;
                          if(slcount==0){
                            $scope.inv_stall = false;}
                        }else{
                          slcount++;
                            $scope.inv_stall = true;
                        }
                    }

                    if(inventory_code == 'FL' || inventory_code == 'POFL'|| inventory_code == 'STFL' || inventory_code == 'SLFL' || inventory_code == 'POSLFL' || inventory_code == 'STSLFL' || inventory_code == 'POCDFL' || inventory_code == 'STCDFL' || inventory_code == 'CDFL'){
                        if($scope.inv_flier == true && value.selected == false ){
                          --flcount;
                          if(flcount==0){
                            $scope.inv_flier = false;}
                        }else{
                          flcount++;
                            $scope.inv_flier = true;
                        }
                    }
                }
                $scope.getFilteredSocieties();
            }
            $scope.clearAllFilters = function(){
                // just deselects all the checkboxes of filter_array passed
                // Added reset function to deselct all inventoriesclearAllFilters
                reset($scope.society_inventory_type);
                reset($scope.society_location);
                reset($scope.society_quality_type);
                reset($scope.society_quantity_type);
                reset($scope.society_flat_type);

                $scope.getFilteredSocieties();

            }
            var reset = function(filter_array){
            var length = filter_array.length;
            for(var i=0;i<length;i++){
              if(filter_array[i].selected == true){
                filter_array[i].selected = false;
                $scope.societyFilter(filter_array[i]);
              }
                filter_array[i].selected = false;
              }
            }
            var promises = [];
            $scope.getFilteredSocieties = function(){
                // creates the string for the get request for getting the required societies based on the filters
                // code changes for adding two centers i.e centers passed in for loop
                // commented original code for current_center

                //   console.log("hello");
                //   // var lat = "?lat=" + $scope.current_center.center.latitude ;
                  // var lng = "&lng=" + $scope.current_center.center.longitude;
                  // var radius = "&r=" + $scope.current_center.center.radius;
                  // var get_url_string = lat + lng + radius;
                  // get_url_string += makeString($scope.society_inventory_type, "&inv=");
                  // get_url_string += makeString($scope.society_location, "&loc=");
                  // get_url_string += makeString($scope.society_quality_type, "&qlt=");
                  // get_url_string += makeString($scope.society_quantity_type, "&qnt=");
                  // get_url_string += makeString($scope.society_flat_type, "&flt=");
                  //
                  // console.log("get_url_string is : ", get_url_string);
                  //
                  // mapViewService.getFilterSocieties(get_url_string)
                  // .success(function(response, status){
                  //   console.log(response);
                  //     $scope.current_center.societies = response.societies;
                  //     $scope.current_center.societies_inventory_count = response.societies_inventory_count;
                  //     $scope.current_center.societies_count = response.societies_count;
                  //     $scope.towers = calculatetowers();
                  //     $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                  //     $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
                  // })
                  // .error(function(response, status){
                  //     console.log("Error Happened while filtering");
                  // });
          // }

          // code added for getting filtered societies for multiple centers
            promises = [];
            var defer = $q.defer();
            for(var i=0; i<$scope.centers1.length; i++){
              var lat = "?lat=" + $scope.centers1[i].center.latitude ;
              var lng = "&lng=" + $scope.centers1[i].center.longitude;
              var radius = "&r=" + $scope.centers1[i].center.radius;
              var get_url_string = lat + lng + radius;
              get_url_string += makeString($scope.society_inventory_type, "&inv=");
              get_url_string += makeString($scope.society_location, "&loc=");
              get_url_string += makeString($scope.society_quality_type, "&qlt=");
              get_url_string += makeString($scope.society_quantity_type, "&qnt=");
              get_url_string += makeString($scope.society_flat_type, "&flt=");

              promises.push(mapViewService.getFilterSocieties(get_url_string));
              // mapViewService.getFilterSocieties(get_url_string)
              // .success(function(response, status){
              //   console.log(i,response,"i");
              //     $scope.centers[i].center.societies = response.societies;
              //     $scope.centers[i].societies_inventory_count = response.societies_inventory_count;
              //     $scope.centers[i].societies_count = response.societies_count;
              //   //  $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
              //     $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
              // })
              // .error(function(response, status){
              //     console.log("Error Happened while filtering");
              // });
          } //end of for loop

          // promises handled
          $q.all(promises).then(function(response){
            var length = $scope.centers1.length;
            for(var i=0; i<length; i++){
              $scope.centers1[i].societies = promises[i].$$state.value.data.suppliers;
              $scope.centers1[i].societies_inventory_count = promises[i].$$state.value.data.supplier_inventory_count;
              $scope.centers1[i].societies_count = promises[i].$$state.value.data.supplier_count;
              $scope.centers[i] = $scope.centers1[i];
              calculateQualityType($scope.centers1[i].societies);
              //$scope.society_markers = assignMarkersToMap($scope.current_center.societies);
              //$scope.impressions = calculateImpressions($scope.centers1[i].societies_inventory_count);
            } //end of for loop
            $scope.current_center.societies = $scope.centers1[$scope.current_center_index].societies;
            $scope.current_center.societies_inventory_count = $scope.centers1[$scope.current_center_index].societies_inventory_count;
            $scope.current_center.societies_count = $scope.centers1[$scope.current_center_index].societies_count;
            $scope.towers = calculatetowers();
            $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
            $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
            gridView_Summary();

          }) // end of q
      }
// =======
//                 var lat = "?lat=" + $scope.current_center.center.latitude ;
//                 var lng = "&lng=" + $scope.current_center.center.longitude;
//                 var radius = "&r=" + $scope.current_center.center.radius;
//                 var get_url_string = lat + lng + radius;
//                 get_url_string += makeString($scope.society_inventory_type, "&inv=");
//                 get_url_string += makeString($scope.society_location, "&loc=");
//                 get_url_string += makeString($scope.society_quality_type, "&qlt=");
//                 get_url_string += makeString($scope.society_quantity_type, "&qnt=");
//                 get_url_string += makeString($scope.society_flat_type, "&flt=");
//
//                 console.log("get_url_string is : ", get_url_string);
//
//                 mapViewService.getFilterSocieties(get_url_string)
//                 .success(function(response, status){
//                   console.log(response);
//                     $scope.current_center.societies = response.societies;
//                     $scope.current_center.societies_inventory_count = response.societies_inventory_count;
//                     $scope.current_center.societies_count = response.societies_count;
//                     $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
//                     $scope.towers = calculatetowers();
//                     $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
//
//                 })
//                 .error(function(response, status){
//                     console.log("Error Happened while filtering");
//                 });
//             }

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
                if(count==length)
                    my_string = filter_keyword;

                return my_string;
            }
        });
        function calculatetowers (){
          var total_tower_count=0;
          for(var i=0;i<$scope.current_center.societies_count;i++){
            total_tower_count += $scope.current_center.societies[i].tower_count;
          }
          return total_tower_count;
        }

        //Function for calculating total impressions inventory wise
        function calculateImpressions (inventoryCount){
          //var impressions = [];
          $scope.total_flat_count=0, $scope.total_towers = 0;
          for(var i=0;i<$scope.current_center.societies_count;i++){
            $scope.total_flat_count += $scope.current_center.societies[i].flat_count;
            $scope.total_towers += $scope.current_center.societies[i].tower_count;
          }

          // var posterImpression = total_flat_count*4*7*2;
          // var standeeImpression = total_flat_count*4*7*2;
          // var stallImpression = total_flat_count*4*2;
          // var flierImpression = total_flat_count * 4*1;
          //var posterCount = inventoryCount.posters;
          //var standeeCount = inventoryCount.standees;
          //var flierCount = inventoryCount.fliers;
          //var stallCount = inventoryCount.stalls;
          var posterImpression = $scope.total_flat_count*4*7*2;
          var standeeImpression = $scope.total_flat_count*4*7*2;
          var stallImpression = $scope.total_flat_count*4*2;
          var flierImpression = $scope.total_flat_count * 4*1;
          $scope.impressions = {
              posterImpression : posterImpression,
              standeeImpression : standeeImpression,
              stallImpression : stallImpression,
              flierImpression : flierImpression,
          };
          return $scope.impressions;
        }
        function calculateQualityType(filter_array){
          $scope.society_type_High =0;
          for(var i=0;i<filter_array.length;i++){
            if(filter_array[i].society_type_quality == "High")
              $scope.society_type_High++;
            if(filter_array[i].society_type_quality == "Medium High")
                $scope.society_type_Medium++;
            if(filter_array[i].society_type_quality == "Ultra High")
                $scope.society_type_Ultra++;
            if(filter_array[i].society_type_quality == "Standard")
                $scope.society_type_Standard++;
          }
        }
        //End: Function for calculating total impressions inventory wise

      //Start: For sending only shortlisted societies & selected inventory types
      function getShortlistedFilteredSocieties(){
        for(var i=0;i<$scope.centers.length;i++){
          for(var j=0;j<$scope.centers[i].societies.length;j++){
            if($scope.centers[i].societies[j].shortlisted == false){
               $scope.centers[i].societies.splice(j--,1);
               $scope.centers[i].societies_count--;
            }
          }
        }
      //End: For sending only shortlisted society in
      //Start: For sending filtered inventory type
          var society_inventory_type_selected = [];
          for(var i=0;i<$scope.society_inventory_type.length;i++){
            if($scope.society_inventory_type[i].selected == true){
              society_inventory_type_selected.push($scope.society_inventory_type[i].code);
            }
          }
      //End: For sending filtered inventory type
          for(var i=0;i<$scope.centers.length;i++){
            $scope.centers[i].center['society_inventory_type_selected']=society_inventory_type_selected;
          }
        }

        $scope.submitProposal = function(){
          getShortlistedFilteredSocieties();

            console.log("Submitting $scope.centers :", $scope.centers);
        };
        $scope.exportData = function(){
        getShortlistedFilteredSocieties();
        console.log($scope.centers);
        getShortlistedFilteredSocieties();
        console.log($scope.centers);
          mapViewService.exportProposalData($scope.proposal_id_temp, $scope.centers)
          .success(function(response){
              console.log("Successfully Exported");
          })
          .error(function(response){
              console.log("Error response is : ", response);
          });
        }
        $scope.excelFile = [];
        function makeid(){
            var text = "";
            var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            for( var i=0; i < 10; i++ )
                text += possible.charAt(Math.floor(Math.random() * possible.length));
            return text;
        }
        $scope.importData = function(files, errFiles){
                $scope.files = files;
                $scope.errFile = errFiles;
              angular.forEach(files, function(file) {
                console.log(file);
                    var my_filename = "PR_" + $scope.proposal_id_temp + "_" + makeid();
                    files.upload = Upload.upload({
                      url: 'http://mdimages.s3.amazonaws.com/', //S3 upload url including bucket name
                      method: 'POST',
                      data: {
                          key: my_filename, // the key to store the file on S3, could be file name or customized
                          AWSAccessKeyId: 'AKIAI6PVCXJEAXV6UHUQ',
                          acl: 'public-read', // sets the access to the uploaded file in the bucket: private, public-read, ...
                          policy: "eyJleHBpcmF0aW9uIjogIjIwMjAtMDEtMDFUMDA6MDA6MDBaIiwKICAiY29uZGl0aW9ucyI6IFsgCiAgICB7ImJ1Y2tldCI6ICJtZGltYWdlcyJ9LCAKICAgIFsic3RhcnRzLXdpdGgiLCAiJGtleSIsICIiXSwKICAgIHsiYWNsIjogInB1YmxpYy1yZWFkIn0sCiAgICBbInN0YXJ0cy13aXRoIiwgIiRDb250ZW50LVR5cGUiLCAiIl0sCiAgICBbImNvbnRlbnQtbGVuZ3RoLXJhbmdlIiwgMCwgNTI0Mjg4MDAwXQogIF0KfQoK",
                          signature: "GsF32EZ1IFvr2ZDH3ww+tGzFvmw=", // base64-encoded signature based on policy string (see article below)
                          "Content-Type": file.type != '' ? file.type : 'application/octet-stream', // content type of the file (NotEmpty)
                          file: file
                      }
                    });

                    files.upload.then(function (response) {
                      var my_file_url = {"file_details":[{"proposal_id":$scope.proposal_id_temp, "file_url":my_filename, "file_data" : file}]};
                      console.log(my_file_url);
                      $scope.excelFile.push({"proposal_id":$scope.proposal_id_temp, "file_url":my_filename})
                      mapViewService.uploadFile($scope.proposal_id_temp,my_file_url);
                        $timeout(function () {
                            file.result = response.data;
                        });
                    }, function (response) {
                        if (response.status > 0)
                            $scope.errorMsg = response.status + ': ' + response.data;
                    }, function (evt) {
                        files.progress = Math.min(100, parseInt(100.0 *
                                                 evt.loaded / evt.total));
                    });
              });
            }
});
