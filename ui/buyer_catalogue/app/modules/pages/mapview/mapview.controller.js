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
          for (var i=0; i <spaces.length; i++) {
            if(spaces[i].society_latitude){
              markers.push({
                  latitude: spaces[i].society_latitude,
                  longitude: spaces[i].society_longitude,
                  id: spaces[i].supplier_id,
                  icon: "img/homeicon1.ico",
                  options : {draggable : false},
                  title : {
                      name : spaces[i].society_name,
                      address1 : spaces[i].society_address1,
                      subarea : spaces[i].society_subarea,
                      location_type : spaces[i].society_location_type,
                  },
              });
            }
          };
          return markers;
      };
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
                $scope.business_name = response.business_name;
                $scope.centers = response.centers;
                $scope.centers1 = response.centers;
                $scope.current_center = $scope.centers[0];
                $scope.current_center_index = 0;
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
  // initial center is to allow user to reset the latitude and longitude to the saved address of the center in the database
                 set_centers();
                  if($scope.current_center.center.space_mappings.society_allowed){
                      // $scope.society_allowed = true;
                      set_space_inventory($scope.current_center.societies_inventory, $scope.space_inventory_type);
                      $scope.society_markers = assignMarkersToMap($scope.current_center.societies);
                  }
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
            $scope.centers1 = [];
            $scope.spaceSociety = function(){
    // this function handles selecting/deselecting society space i.e. society_allowed = true/false
    // code changed after changes done for adding two centers on gridView
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
                    set_space_inventory($scope.centers1[i].societies_inventory, $scope.space_inventory_type);
                }
             }
            }else{
                for(var i=0; i< $scope.centers1.length; i++){
                  $scope.society_markers = [];
                  delete $scope.centers1[i].societies;
                  delete $scope.centers1[i].societies_inventory;
                  delete $scope.centers1[i].societies_count;
                  delete $scope.centers1[i].societies_inventory_count;
                  deselect_space_inventory($scope.space_inventory_type)
                }
            }
        }
    // function to show gridView_Summary on gridView page
         $scope.total_societies, $scope.total_standees, $scope.total_stalls;
         $scope.total_posters, $scope.total_flats;
         function gridView_Summary(){
            $scope.total_societies = 0,$scope.total_standees = 0,$scope.total_stalls = 0;
            $scope.total_posters = 0,$scope.total_flats = 0;
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
      // This function is for showing societies on the map view
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
            for(var i=0; i<$scope.centers1.length; i++){
              var lat = "?lat=" + $scope.centers1[i].center.latitude ;
              var lng = "&lng=" + $scope.centers1[i].center.longitude;
              var radius = "&r=" + $scope.centers1[i].center.radius;
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
            var length = $scope.centers1.length;
            for(var i=0; i<length; i++){
              $scope.centers1[i].societies = promises[i].$$state.value.data.suppliers;
              $scope.centers1[i].societies_inventory_count = promises[i].$$state.value.data.supplier_inventory_count;
              $scope.centers1[i].societies_count = promises[i].$$state.value.data.supplier_count;
              $scope.centers[i] = $scope.centers1[i];
              calculateQualityType($scope.centers1[i].societies);
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
});
