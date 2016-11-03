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

// after angular-google-maps is loaded properly only then proces code inside then
  uiGmapGoogleMapApi.then(function(maps) {
      function assignCenterMarkerToMap(center){
        // This is to assign marker for the current center on the map could have used single marker (ui-gmap-marker) but wasn't working hence used ui-gmap-markers
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
      function assignMarkersToMap(spaces) {
          // assigns spaces(society, corporate) markers on the map
          // ADDNEW --> this function needs to have "if" condition for society as its variables have society_ in every variable while other doesn't
          var markers = [];
          //console.log("printing spaces", spaces);
          angular.forEach(spaces, function(suppliers) {
            for (var i=0; i <suppliers.length; i++) {
                markers.push({
                    latitude: suppliers[i].latitude,
                    longitude: suppliers[i].longitude,
                    id: suppliers[i].supplier_id,
                    icon: "img/homeicon1.ico",
                    options : {draggable : false},
                    title : {
                        name : suppliers[i].name,
                        address1 : suppliers[i].address1,
                        subarea : suppliers[i].subarea,
                        location_type : suppliers[i].location_type,
                    },
                });
            };
          });
          return markers;
      };
      $scope.changeCurrentCenter = function(center_id){
            // changes the center currently shown on the map
            // only front end work
            for(var i=0;i<$scope.center_data.length; i++)
                if($scope.center_data[i].center.id == center_id){
                    $scope.current_center = $scope.center_data[i]
                    $scope.current_center_index = i;
                }
            // make the current center of map equal to center of the map
            $scope.map.center.latitude = $scope.current_center.center.latitude;
            $scope.map.center.longitude = $scope.current_center.center.longitude;
            $scope.circle.center.latitude = $scope.current_center.center.latitude;
            $scope.circle.center.longitude = $scope.current_center.center.longitude;
            $scope.circle.radius = $scope.current_center.center.radius * 1000;
            // set_centers();
            // deselect_all_society_filters();
            // show the societies only if selected in this center
            // if($scope.current_center.center.space_mappings.society_allowed){
                $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
            // }else{
            //     $scope.society_markers = [];
            //     deselect_space_inventory($scope.space_inventory_type);
            // }
            //ADDNEW -->  do the same for corporate and gym and salonS
            // do the same for corporate and gym and salons
            // reassing the center_marker acc. to the selected center
            $scope.center_marker =assignCenterMarkerToMap($scope.current_center.center);
        }
        //Start:reset center to original center
        //End: reset center to original center
        // Start: Change center,change radius functionality
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
              // delete $scope.current_center.society_inventory;
              // delete $scope.current_center.societies;
              // delete $scope.current_center.corporate_inventory;
              // delete $scope.current_center.corporates;
              // this service will return above deleted variables if checked in the filter
              $scope.current_center.center.center_id = $scope.current_center.center.id;
              mapViewService.getChangedCenterSpaces($scope.proposal_id_temp, $scope.current_center.center)
              .success(function(response, status){
                console.log("change center",response);
                // Start : Code changes to add response of suppliers
                $scope.current_center.suppliers = response.data[0].suppliers;
                // $scope.current_center = response;
                $scope.center_data[$scope.current_center_index].suppliers = response.data[0].suppliers;
                // $scope.centers1[$scope.current_center_index].societies_count = response.supplier_count;
                // $scope.centers1[$scope.current_center_index].societies_inventory_count = response.supplier_inventory_count;
                // $scope.centers = $scope.centers1;
                // End : Code changes to add response of suppliers
                  // gridView_Summary();
                  $scope.center_data[$scope.current_center_index] = $scope.current_center;
                  suppliersData();
                  mapViewBasicSummary();
                  // mapViewFiltersSummary();
                  // mapViewImpressions();
                  gridViewBasicSummary();
                  // $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);
                  if($scope.current_center.suppliers != undefined){
                      $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
                      // $scope.society_markers1 = assignMarkersToMap($scope.area_societies);
                  }else
                      $scope.society_markers = [];
              })
              .error(function(response, status){
                  if (typeof(response) == typeof([]))
                      console.log("Error fetching : ", response.message);
              });
          }
        //End: Change center,change radius and reset center functionality
    //start: mapview basic summary required when load a page
      var mapViewBasicSummary = function(){
          $scope.flat_count = 0, $scope.tower_count = 0;
          if($scope.current_center.suppliers['RS'] != undefined){
              $scope.societies_count = $scope.current_center.suppliers['RS'].length;
              for(var temp=0;temp<$scope.societies_count;temp++){
                $scope.flat_count += $scope.current_center.suppliers['RS'][temp].flat_count;
                $scope.tower_count += $scope.current_center.suppliers['RS'][temp].tower_count;
              }
            }
          if($scope.current_center.suppliers['CP'] != undefined){
          }
      }
    //End: mapview basic summary
    //Start: mapview filter summary required after applying filters
     var mapViewFiltersSummary = function(){
       $scope.stall_count = 0, $scope.standee_count = 0;
       if($scope.current_center.suppliers['RS'] != undefined){
         $scope.stall_count += $scope.current_center.suppliers_meta['RS'].inventory_count.stalls;
         $scope.standee_count += $scope.current_center.suppliers_meta['RS'].inventory_count.standees;
       }
       if($scope.current_center.suppliers['CP'] != undefined){
         $scope.stall_count += $scope.current_center.suppliers_meta['CP'].inventory_count.stalls;
         $scope.standee_count += $scope.current_center.suppliers_meta['CP'].inventory_count.standees;
       }
     }
    //End: mapview filter summary required after applying filters
    //Start: impressions
      var mapViewImpressions = function(){
        $scope.posterMapImpressions = $scope.flat_count*4*7*2;
        $scope.standeeMapImpression = $scope.flat_count*4*7*2;
        $scope.stallMapImpression = $scope.flat_count*4*2;
        $scope.flierMapImpressions = $scope.flat_count * 4*1;

      }
    //End: impressions
    //Start: collectng all centers suppliers data in one varible for RS,CP..etc
      var suppliersData = function(){
        $scope.total_societies = [];
        for (var temp=0;temp<$scope.center_data.length;temp++){
          if($scope.center_data[temp].suppliers['RS']!=undefined){
            $scope.total_societies = $scope.total_societies.concat($scope.center_data[temp].suppliers['RS']);
          }
        }
      }
      //End: collectng all centers suppliers data in one varible like for RS,CP..etc
        //Start: gridView basic summary
      var gridViewBasicSummary = function(){
        $scope.total_flat_count = 0, $scope.total_tower_count = 0;
        $scope.total_societies_count = $scope.total_societies.length;
          for(var temp=0; temp<$scope.total_societies_count; temp++){
            $scope.total_flat_count += $scope.total_societies[temp].flat_count;
            $scope.total_tower_count += $scope.total_societies[temp].tower_count;
          }
      }
    //End: gridView basic summary
    //Start: summary on gridview for total stalls & standees after applying filters
    var gridViewFilterSummary = function(){
      for(var center = 0; center < $scope.center_data.length; center++){
        if($scope.total_stalls = $scope.center_data[center].suppliers_meta !=undefined){
          if($scope.center_data[center].suppliers_meta['RS'] != undefined){
            $scope.total_stalls = $scope.center_data[center].suppliers_meta['RS'].inventory_count.stalls;
            $scope.total_standees = $scope.center_data[center].suppliers_meta['RS'].inventory_count.standees;
          }
        }
      }
    }
    //End: summary on gridview for total stalls & standees after applying filters
      //Start: gridview impressions : multiply with total flat count for societies
    var gridViewImpressions = function(){
      $scope.flierGridImpressions = 0, $scope.posterGridImpressions = 0;
      $scope.standeeGridImpression = 0,$scope.stallGridImpression = 0;

      $scope.flierGridImpressions = $scope.total_flat_count *4*1;
      $scope.posterGridImpressions = $scope.total_flat_count *4*7*2;
      $scope.standeeGridImpression = $scope.total_flat_count *4*7*2;
      $scope.stallGridImpression = $scope.total_flat_count *4*2;
    }
      //End: gridview impressions : multiply with total flat count for societies

// Execute code inside them only when uiGMapIsReady is done --> map is loaded properly
      uiGmapIsReady.promise()
        .then(function(instances) {
            // initiated here as this is used in the service below
            // similarly initiate for other spacecs as well
          $scope.space_inventory_type = [
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
          ];
// This service gets all the spaces according to center specification like society_allowed
          $scope.proposal_id_temp = $stateParams.proposal_id;
          mapViewService.getSpaces($scope.proposal_id_temp)
            .success(function(response, status){
              console.log("center",response);
                $scope.business_name = response.business_name;
                $scope.center_data = response.data;
                console.log("printing center_data", $scope.center_data);
                $scope.current_center = response.data[0];
                console.log("printing current_center", $scope.current_center);

                $scope.current_center_index = 0;
                mapViewBasicSummary();
                suppliersData();
                gridViewBasicSummary();
                // gridView_Summary();
                for(var i=0;i<$scope.center_data.length; i++)
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
  // initial center is to allow user to reset the latitude and longitude to the saved address of the center in the database
                //  set_centers();
                  // if($scope.current_center.center.space_mappings.society_allowed){
                      // $scope.society_allowed = true;
                      // set_space_inventory($scope.current_center.societies_inventory, $scope.space_inventory_type);
                      $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
                  // }
                  $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
                })
            .error(function(response, status){
                $scope.get_spaces_error = response.message;
                console.log("Error response : ",response);
            });
        });
          $scope.windowCoords = {}; // at windowCoords the window will show up
          $scope.space = {}
          //onClick function is called when a marker is clicked
          $scope.onClick = function(marker, eventName, model) {
            $scope.space = {};
              if(model.id == 0){
                $scope.space = {
                    name : "Center Chosen By You",
                    address1 : "Center Address",
                    location_type : "Posh",
                  }
              }else{
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
            $scope.space_location = [
                {name : 'Ultra High',   code : 'UH',    selected : false},
                {name : 'High',         code : 'HH',    selected : false},
                {name : 'Medium High',  code : 'MH',    selected : false},
                {name : 'Standard',     code : 'ST',    selected : false},
            ];
            $scope.space_quality_type = [
                {name : 'Ultra High',   code : 'UH',    selected : false},
                {name : 'High',         code : 'HH',    selected : false},
                {name : 'Medium High',  code : 'MH',    selected : false},
                {name : 'Standard',     code : 'ST',    selected : false},
            ];
            $scope.space_quantity_type = [
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
// Start: supplier filters select deselecting functionality
    $scope.society_checked = false;
    $scope.selectSuppliers = function(spaces){
      angular.forEach(spaces, function(supplier){
        if(spaces == 'RS'){
          $scope.society_checked =true;
        }
        if(spaces == 'CP'){
          $scope.corporate_checked =true;
        }
      });
    }

    $scope.spaceSupplier = function(supplier){
    // this function handles selecting/deselecting society space i.e. society_allowed = true/false
    // code changed after changes done for adding two centers on gridView
        if($scope.supplier == true)
          $scope.supplier = false;
        else
          $scope.supplier = true;
      }
// End: supplier filters select deselecting functionality
    // function to show gridView_Summary on gridView page
      //    $scope.total_societies, $scope.total_standees, $scope.total_stalls;
      //    $scope.total_posters, $scope.total_flats;
      //    function gridView_Summary(){
      //       $scope.total_societies = 0,$scope.total_standees = 0,$scope.total_stalls = 0;
      //       $scope.total_posters = 0,$scope.total_flats = 0;
      //       var merge_societies = [];
      //       for(var i=0;i<$scope.centers1.length;i++){
      //         $scope.total_societies+= $scope.centers1[i].societies_count;
      //         $scope.total_standees+= $scope.centers1[i].societies_inventory_count.standees;
      //         $scope.total_stalls+= $scope.centers1[i].societies_inventory_count.stalls;
      //         merge_societies = merge_societies.concat($scope.centers1[i].societies);
      //       }
      //       for(var i=0; i<merge_societies.length; i++){
      //         $scope.total_posters +=merge_societies[i].tower_count;
      //         $scope.total_flats +=merge_societies[i].flat_count;
      //       }
      //       // impressions for gridView
      //       $scope.total_posterImpressions = $scope.total_flats*4*7*2;
      //       $scope.total_flierImpressions = $scope.total_flats*4*1;
      //       $scope.total_standeeImpressions = $scope.total_flats*4*7*2;
      //       $scope.total_stallImpressions = $scope.total_flats*4*2;
      //    }
      // // This function is for showing societies on the map view
         $scope.showSocieties = function(){
                $scope.show_societies = !$scope.show_societies
         }
         var pcount=0,stcount=0,slcount=0,flcount=0;// This count variables are to display count tab in gridView
         // society filter is called when some checkbox in society filters is changed value is just for inventories , inventories changed will be changed in
         // $scope.current_center.societies_inventory as well (this is present only if society_allowed is true)
         // change from inventory_name to inventory_code
          $scope.societyFilter = function(value){
            if(value){
              var inventory_name = value.name.toLowerCase();
              var inventory_code = value.code;
              // $scope.current_center.societies_inventory[inventory_name + '_allowed'] = value.selected;
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
      // Just deselects all the checkboxes of filter_array passed.Added reset function to deselct all inventoriesclearAllFilters
            $scope.clearAllFilters = function(){
                reset($scope.space_quality_type);
                reset($scope.space_location);
                reset($scope.space_quality_type);
                reset($scope.space_quantity_type);
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
            promises = [];
            var defer = $q.defer();
            // start: for mapview only
            if(!$scope.show_societies){
            // for(var i=0; i<$scope.centers1.length; i++){
              var lat = "?lat=" + $scope.current_center.center.latitude ;
              var lng = "&lng=" + $scope.current_center.center.longitude;
              var radius = "&r=" + $scope.current_center.center.radius;
              var get_url_string = lat + lng + radius;
              get_url_string += makeString($scope.space_inventory_type, "&inv=");
              get_url_string += makeString($scope.space_location, "&loc=");
              get_url_string += makeString($scope.space_quality_type, "&qlt=");
              get_url_string += makeString($scope.space_quantity_type, "&qnt=");
              get_url_string += makeString($scope.society_flat_type, "&flt=");

              // promises.push(mapViewService.getFilterSocieties(get_url_string));
          // } //end of for loop

          // promises handled

          mapViewService.getFilterSocieties(get_url_string)
                .success(function(response, status){
                  console.log(response);
                  response.data.center = $scope.current_center.center;
                    $scope.current_center = response.data;
                    $scope.center_data[$scope.current_center_index] = response.data;
                    console.log($scope.center_data);
                    // $scope.current_center.societies_inventory_count = response.societies_inventory_count;
                    // $scope.current_center.societies_count = response.societies_count;
                    // console.log("\n\n$scope.centers : ", $scope.centers);
                    $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
                    mapViewBasicSummary();
                    mapViewFiltersSummary();
                    mapViewImpressions();
                    suppliersData();
                    gridViewBasicSummary();
                    gridViewFilterSummary();
                    gridViewImpressions();
                })
                .error(function(response, status){
                    console.log("Error Happened while filtering");
                });// end of q
              }
          // End: for mapview only
          //start: for gridview filters
          else{
            console.log($scope.center_data);
            for(var i=0; i<$scope.center_data.length; i++){
              var lat = "?lat=" + $scope.center_data[i].center.latitude ;
              var lng = "&lng=" + $scope.center_data[i].center.longitude;
              var radius = "&r=" + $scope.center_data[i].center.radius;
              var get_url_string = lat + lng + radius;
              get_url_string += makeString($scope.space_inventory_type, "&inv=");
              get_url_string += makeString($scope.space_location, "&loc=");
              get_url_string += makeString($scope.space_quality_type, "&qlt=");
              get_url_string += makeString($scope.space_quantity_type, "&qnt=");
              get_url_string += makeString($scope.society_flat_type, "&flt=");

              promises.push(mapViewService.getFilterSocieties(get_url_string));
            } //end of for loop

              // promises handled
            $q.all(promises).then(function(response){
              var length = $scope.center_data.length;
              for(var i=0; i<length; i++){
                response[i].data.data.center = $scope.center_data[i].center;
                $scope.center_data[i] = response[i].data.data;
                // $scope.centers1[i].societies = promises[i].$$state.value.data.suppliers;
                // $scope.centers1[i].societies_inventory_count = promises[i].$$state.value.data.supplier_inventory_count;
                // $scope.centers1[i].societies_count = promises[i].$$state.value.data.supplier_count;
                // $scope.centers[i] = $scope.centers1[i];
                // calculateQualityType($scope.centers1[i].societies);
                //$scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                //$scope.impressions = calculateImpressions($scope.centers1[i].societies_inventory_count);
              } //end of for loop
              console.log($scope.current_center);
              $scope.current_center = $scope.center_data[$scope.current_center_index];
              console.log($scope.current_center);
              // $scope.current_center.societies = $scope.centers1[$scope.current_center_index].societies;
              // $scope.current_center.societies_inventory_count = $scope.centers1[$scope.current_center_index].societies_inventory_count;
              // $scope.current_center.societies_count = $scope.centers1[$scope.current_center_index].societies_count;
              // $scope.towers = calculatetowers();
              $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
              suppliersData();
              mapViewBasicSummary();
              mapViewFiltersSummary();
              mapViewImpressions();
              suppliersData();
              gridViewBasicSummary();
              gridViewFilterSummary();
              gridViewImpressions();
              // $scope.impressions = calculateImpressions($scope.current_center.societies_inventory_count);

              }) // end of q
          }
          //End: for gridview filters
      }

      //End: angular-google-maps is loaded properly only then proces code inside then
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
//Start: Function added to show all suppliers on gridView
  $scope.supplier_codes =['RS','CP','GY'];
  $scope.getSuppliers = function(suppl){
      // angular.forEach(supplier, function(suppliers) {
      //   console.log("hi",index,suppliers);
      // });

    return suppl;
  }
//End: Function added to show all suppliers on gridView

});
