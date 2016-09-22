"use strict";
angular.module('catalogueApp')
    .controller('MapCtrl', function($scope, $rootScope, $stateParams,  $window, $location, createProposalService, mapViewService ,$http, uiGmapGoogleMapApi,uiGmapIsReady,$q) {
        // You have to initailise some value for the map center beforehand
        // $scope.map is just for that purpose --> Set it according to your needs.
        // One good way is to set it at center of India when covering multiple cities otherwise middle of mumbai
        $scope.map = {
          zoom: 9,
          bounds: {},
          center: {
            latitude: 19.119,
            longitude: 73.48,
          }
        };
        $scope.options = {
          scrollwheel: false,
          mapTypeControl: true,
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
        console.log("Inside map view with proposal_id : ", $stateParams.proposal_id);

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
                    console.log("response is : ", response);
                    $scope.current_center = response.centers[0];
                    $scope.centers1[$scope.current_center_index] = $scope.current_center;
                    $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
                    gridView_Summary();
                     console.log("$scope.current_center = ", $scope.current_center);
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
                console.log($scope.current_center_index);
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
                console.log("$scope.circle  : ", $scope.circle);
                // saves bandwidth
                // ADDNEW --> add new spaces variables as well
                delete $scope.current_center.society_inventory;
                delete $scope.current_center.societies;
                delete $scope.current_center.corporate_inventory;
                delete $scope.current_center.corporates;
                // this service will return above deleted variables if checked in the filter
                mapViewService.getChangedCenterSpaces($scope.proposal_id_temp, $scope.current_center)
                .success(function(response, status){
                    console.log("Changing Center \nResponse is : ", response);
                    $scope.current_center = response;
                    $scope.centers1[$scope.current_center_index] = response;
                    gridView_Summary();
                    console.log("\nAfter request $scope.current_center : ", $scope.current_center);

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
                console.log("$scope.current_center", $scope.current_center);
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
                            console.log("new Latitude : ", $scope.new_center.latitude);
                            if($scope.old_center.latitude != $scope.new_center.latitude || $scope.old_center.longitude != $scope.new_center.longitude){
                                $scope.center_changed = true;
                            }else
                                $scope.center_changed = false;
                        }
                    }
                });
                return center_marker;
            }

            function assignMarkersToMap(spaces) {
                // assigns spaces(society, corporate) markers on the map
                // ADDNEW --> this function needs to have "if" condition for society as its variables have society_ in every variable while other doesn't
                var markers = [];
                for (var i=0; i <spaces.length; i++) {
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
                    console.log("\n\nResponse is : ", response);
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
                        $scope.map = {
                          zoom: 12,
                          bounds: {},
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
                    console.log("calling set_centers ");
                    set_centers();
                    console.log("$scope.old_center : ", $scope.old_center);
                    console.log("$scope.new_center : ", $scope.new_center);
                    if($scope.current_center.center.space_mappings.society_allowed){
                        // $scope.society_allowed = true;
                        set_space_inventory($scope.current_center.societies_inventory, $scope.society_inventory_type);
                        $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
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
                    console.log("hello");
                    for(var i=0;i<$scope.centers1.length;i++){
                      console.log($scope.centers1[1]);
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
                      $scope.societyFilter($scope.centers1[i].societies_inventory);
                      delete $scope.centers1[i].societies;
                      delete $scope.centers1[i].societies_inventory;
                      delete $scope.centers1[i].societies_count;
                      delete $scope.centers1[i].societies_inventory_count;
                      deselect_space_inventory($scope.society_inventory_type)
                      console.log($scope.centers1);
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

              console.log("get_url_string is : ", get_url_string,i);
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
              console.log(promises[i].$$state.value);
              $scope.centers1[i].societies = promises[i].$$state.value.data.societies;
              $scope.centers1[i].societies_inventory_count = promises[i].$$state.value.data.societies_inventory_count;
              $scope.centers1[i].societies_count = promises[i].$$state.value.data.societies_count;
              calculateQualityType($scope.centers1[i].societies);
              //$scope.society_markers = assignMarkersToMap($scope.current_center.societies);
              //$scope.impressions = calculateImpressions($scope.centers1[i].societies_inventory_count);
            } //end of for loop
            console.log($scope.centers1);
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
          console.log(total_tower_count);
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
          console.log($scope.total_flat_count);
          //var posterCount = inventoryCount.posters;
          var standeeCount = inventoryCount.standees;
          //var flierCount = inventoryCount.fliers;
          var stallCount = inventoryCount.stalls;
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
        // code added to send selected society inventory types while submitting the proposal & sending only shortlisted societies
        $scope.submitProposal = function(){
          for(var i=0;i<$scope.centers.length;i++){
            for(var j=0;j<$scope.centers[i].societies.length;j++){
              if($scope.centers[i].societies[j].shortlisted == false){
                 $scope.centers[i].societies.splice(j--,1);
                 $scope.centers[i].societies_count--;
              }
            }
          }
            var society_inventory_type_selected = [];
            for(var i=0;i<$scope.society_inventory_type.length;i++){
              if($scope.society_inventory_type[i].selected == true){
                society_inventory_type_selected.push($scope.society_inventory_type[i].code);
              }
            }
            for(var i=0;i<$scope.centers.length;i++){
              $scope.centers[i].center['society_inventory_type_selected']=society_inventory_type_selected;
            }
            console.log("Submitting $scope.centers :", $scope.centers);
            mapViewService.createFinalProposal($scope.proposal_id_temp, $scope.centers)
            .success(function(response, status){
                console.log("Successfully Saved");
                $location.path('/' + $scope.proposal_id_temp + '/showcurrentproposal');
            })
            .error(function(response, status){
                console.log("Error response is : ", response);
            });
        }



    // grid view starts

    // $scope.showDetails = function(){
    //     $scope.new_centers = new Array();
    //     console.log("\n$scope.centers : ", $scope.centers, "\n\n");

    //     // converting the data in the required and a suitable form for the backend
    //     // fomat is center = [
    //     //     space_mappings : [
    //     //         inventory_type : [],
    //     //         spaces : []
    //     //     ]
    //     // ]

    //     for(var i=0;i<$scope.centers.length;i++){
    //         $scope.new_centers.push({
    //             center : $scope.centers[i].center
    //         });

    //         console.log("$scope.centers[i].center  : ", $scope.centers[i].center);

    //         var center_var = $scope.centers[i]

    //         console.log("center_var.center.space_mappings : ", center_var.center.space_mappings);
    //         // only iterate over space_mappings if it is an object/array
    //         if(typeof(center_var.center.space_mappings) == typeof([])){
    //             for(var j=0;j<center_var.center.space_mappings.length;j++){
    //                 center_var.center.space_mappings[j].spaces = new Array();
    //                 console.log("Inside if")
    //                 if(center_var.center.space_mappings[j].space_name == 'Society'){
    //                     for(var k=0;k<center_var.societies.length; k++){
    //                         if(center_var.societies[k].shortlisted){
    //                             center_var.center.space_mappings[j].spaces.push({
    //                                 object_id : center_var.societies[i].supplier_id,
    //                             })
    //                         }
    //                     }
    //                 }

    //                 else if (center_var.center.space_mappings[j].space_name == 'Corporate'){
    //                     for(var k=0;k<center_var.corporates.length; k++){
    //                         if(center_var.corporates[k].shortlisted){
    //                             center_var.center.space_mappings[j].spaces.push({
    //                                 object_id : center_var.corporates[i].supplier_id
    //                             });
    //                         }
    //                     }
    //                 }

    //     //                // here goes the code for salon and gyms and other spaces
    //             }
    //         }
    //     }
    //     console.log("\n\n$scope.new_centers", $scope.new_centers, "\n\n");
    // }

});
