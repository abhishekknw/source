"use strict";
angular.module('catalogueApp')
    .constant('constants',{
      base_url : 'http://localhost:8108/',
      url_base : 'v0/ui/website/',
      AWSAccessKeyId : 'AKIAI6PVCXJEAXV6UHUQ',
      policy : "eyJleHBpcmF0aW9uIjogIjIwMjAtMDEtMDFUMDA6MDA6MDBaIiwKICAiY29uZGl0aW9ucyI6IFsgCiAgICB7ImJ1Y2tldCI6ICJtZGltYWdlcyJ9LCAKICAgIFsic3RhcnRzLXdpdGgiLCAiJGtleSIsICIiXSwKICAgIHsiYWNsIjogInB1YmxpYy1yZWFkIn0sCiAgICBbInN0YXJ0cy13aXRoIiwgIiRDb250ZW50LVR5cGUiLCAiIl0sCiAgICBbImNvbnRlbnQtbGVuZ3RoLXJhbmdlIiwgMCwgNTI0Mjg4MDAwXQogIF0KfQoK",
      acl : 'public-read',
      signature : "GsF32EZ1IFvr2ZDH3ww+tGzFvmw=",
      content_type : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    })
    .controller('MapCtrl', function(constants, $scope, $rootScope, $stateParams,  $window, $location, createProposalService, mapViewService ,$http, uiGmapGoogleMapApi,uiGmapIsReady,$q, Upload, $timeout) {
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
      // TO show different colors for suppliers based on status
      $scope.status_color;
      function getIcon(supplier,key){
        if(supplier.status == 'X')
          $scope.status_color = "0000FF";//blue color for new suppliers
        if(supplier.status == 'S')
          $scope.status_color = "00FF00";//green color for shortlisted suppliers
        if(supplier.status == 'R')
          $scope.status_color = "FF0000";//red color for removed suppliers
        if(supplier.status == 'B')
          $scope.status_color = "A52A2A";//black color for buffered suppliers
        var icon;
        icon = icons[key] + $scope.status_color +'/000000/FF0000/';
        return icon;
      }
      var icons = {
        // http://www.googlemapsmarkers.com/v1/LABEL/FILL COLOR/LABEL COLOR/STROKE COLOR/
        'RS':'http://www.googlemapsmarkers.com/v1/'+'S/',
        'CP':'http://www.googlemapsmarkers.com/v1/'+'C/',
      };
      function assignMarkersToMap(spaces) {
          // assigns spaces(society, corporate) markers on the map
          // ADDNEW --> this function needs to have "if" condition for society as its variables have society_ in every variable while other doesn't
          var markers = [];
          var icon;
          angular.forEach(spaces, function(suppliers,key){

            for (var i=0; i <suppliers.length; i++) {
                markers.push({
                    latitude: suppliers[i].latitude,
                    longitude: suppliers[i].longitude,
                    id: suppliers[i].supplier_id,
                    icon:getIcon(suppliers[i],key),
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

            if($scope.current_center.suppliers_meta != null){
              checkSavedFilters();
              toggleInventoryFilters($scope.current_center,'true','RS');
              mapViewBasicSummary();
              suppliersData();
              gridViewBasicSummary();
            }
            $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
            $scope.center_marker =assignCenterMarkerToMap($scope.current_center.center);
            suppliersData();
            mapViewBasicSummary();
            mapViewFiltersSummary();
            mapViewImpressions();
            gridViewBasicSummary();
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
                  $scope.center_changed = false;
              }
              if(change_center == false){
                $scope.current_center.center.latitude = $scope.old_data[$scope.current_center_index].center.latitude;
                $scope.current_center.center.longitude = $scope.old_data[$scope.current_center_index].center.longitude;
                $scope.current_center.center.radius = $scope.old_data[$scope.current_center_index].center.radius;
              }
              $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);

              $scope.circle.center.latitude = $scope.current_center.center.latitude;
              $scope.circle.center.longitude = $scope.current_center.center.longitude;
              $scope.circle.radius = $scope.current_center.center.radius * 1000;

              // this service will return above deleted variables if checked in the filter
              $scope.current_center.center.center_id = $scope.current_center.center.id;
              mapViewService.getChangedCenterSpaces($scope.proposal_id_temp, $scope.current_center.center)
              .success(function(response, status){
                // Start : Code changes to add response of suppliers
                $scope.current_center.suppliers = response.data.suppliers[0].suppliers;
                // $scope.current_center = response;
                $scope.center_data[$scope.current_center_index].suppliers = response.data.suppliers[0].suppliers;
                // to copy extra suppliers searched in add more suppliers
                // needs to add every time whenever new response come from backend
                // current_center_keys gets all keys in current_center so that we can copy
                var current_center_keys = Object.keys($scope.center_data[$scope.current_center_index].suppliers);
                for (var i = 0; i < current_center_keys.length; i++) {
                  var code = current_center_keys[i];
                  $scope.center_data[$scope.current_center_index].suppliers[code].push.apply($scope.center_data[$scope.current_center_index].suppliers[code],$scope.extraSuppliersData[$scope.current_center_index][code]);
                }
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
            $scope.corporates_count = $scope.current_center.suppliers['CP'].length;
          }
      }
    //End: mapview basic summary
    //Start: mapview filter summary required after applying filters
     var mapViewFiltersSummary = function(){
       $scope.stall_count = 0, $scope.standee_count = 0;
       if($scope.current_center.suppliers_meta != null){
         if($scope.current_center.suppliers_meta['RS'] != undefined){
           if($scope.current_center.suppliers_meta['RS'].inventory_count != null){
             $scope.stall_count += $scope.current_center.suppliers_meta['RS'].inventory_count.stalls;
             $scope.standee_count += $scope.current_center.suppliers_meta['RS'].inventory_count.standees;
           }
         }
         if($scope.current_center.suppliers_meta['CP'] != undefined){
           if($scope.current_center.suppliers_meta['CP'].inventory_count != null){
             $scope.stall_count += $scope.current_center.suppliers_meta['CP'].inventory_count.stalls;
             $scope.standee_count += $scope.current_center.suppliers_meta['CP'].inventory_count.standees;
           }
         }
       }
     }
    //End: mapview filter summary required after applying filters
    //Start: impressions on mapview
      var mapViewImpressions = function(){
        $scope.posterMapImpressions = $scope.flat_count*4*7*2;
        $scope.standeeMapImpression = $scope.flat_count*4*7*2;
        $scope.stallMapImpression = $scope.flat_count*4*2;
        $scope.flierMapImpressions = $scope.flat_count * 4*1;

      }
    //End: impressions on mapview
    //Start: collectng all centers suppliers data in one varible for RS,CP..etc
      var suppliersData = function(){
        $scope.total_societies = [], $scope.total_corporates = [];
        for (var index=0;index<$scope.center_data.length;index++){
          if($scope.center_data[index].suppliers['RS']!=undefined){
            $scope.total_societies = $scope.total_societies.concat($scope.center_data[index].suppliers['RS']);
          }
          if($scope.center_data[index].suppliers['CP']!=undefined){
            $scope.total_corporates = $scope.total_corporates.concat($scope.center_data[index].suppliers['CP']);
          }
        }
      }
      //End: collectng all centers suppliers data in one varible like for RS,CP..etc
        //Start: gridView basic summary
      var gridViewBasicSummary = function(){
        $scope.total_flat_count = 0, $scope.total_tower_count = 0;
        $scope.total_societies_count = $scope.total_societies.length;
        $scope.total_corporates_count = $scope.total_corporates.length;
          for(var temp=0; temp<$scope.total_societies_count; temp++){
            $scope.total_flat_count += $scope.total_societies[temp].flat_count;
            $scope.total_tower_count += $scope.total_societies[temp].tower_count;
          }
      }
    //End: gridView basic summary
    //Start: summary on gridview for total stalls & standees after applying filters
    var gridViewFilterSummary = function(){
      $scope.total_stalls = 0, $scope.total_standees = 0;
      for(var center = 0; center < $scope.center_data.length; center++){
        if($scope.center_data[center].suppliers_meta != null){
          if($scope.center_data[center].suppliers_meta['RS'] != null){
            if($scope.center_data[center].suppliers_meta['RS'].inventory_count != null){
              $scope.total_stalls += $scope.center_data[center].suppliers_meta['RS'].inventory_count.stalls;
              $scope.total_standees += $scope.center_data[center].suppliers_meta['RS'].inventory_count.standees;
            }
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
            $scope.employee_count = [
              {name:'0-1000',     code : {min:'0',      max:'1000'},   selected:false},
              {name:'1000-3000',  code : {min:'1000',   max:'3000'},   selected:false},
              {name:'3000-6000',  code : {min:'3000',   max:'6000'},   selected:false},
              {name:'6000-10000', code : {min:'6000',   max:'10000'},  selected:false},

            ];
            $scope.inventory_filters = {
              inv_poster : 0,
              inv_standee : 0,
              inv_stall : 0,
              inv_flier : 0,
            };
        //Start: filters for suppliers
            $scope.RS_filters = {
              inventory : $scope.space_inventory_type,
              locality_rating : $scope.space_location,
              quality_type : $scope.space_quality_type,
              quantity_type : $scope.space_quantity_type,
              flat_type : $scope.society_flat_type,
            };
            $scope.CP_filters = {
              inventory : $scope.space_inventory_type,
              locality_rating : $scope.space_location,
              quality_type : $scope.space_quality_type,
              quantity_type : $scope.space_quantity_type,
              employee_count : $scope.employee_count,
            };
        //End: filters for suppliers
        //Start: add filter varible for each supplier in each center
        //set created to maintain unique_suppliers in all centers
    $scope.society_show = false,$scope.corporate_show = false;
    $scope.supplier_centers_list = {
      RS:[],
      CP:[],
    };
    //created set of suppliers to collect unique suppliers in multiple centers
    //this is used to show all suppliers uniquely on gridview
    //i.e no duplication if the supplier is repeated in multiple centers
    $scope.unique_suppliers = new Set();
    $scope.extraSuppliersData = [];
    var center_id=0;
    //function basically adds required keys to handle supplier allowed checkbox
    //function called from getSpaces after loading the page
    $scope.addSupplierFilters = function(centers){
      angular.forEach(centers, function(center){

        center.suppliers_allowed = {};
        center.filters_meta = {};
        $scope.extraSuppliersData[center_id] = {};
       if(center.suppliers['RS'] != undefined){
         $scope.extraSuppliersData[center_id]['RS'] = [];
         center.suppliers_allowed.society_allowed = true;
         $scope.unique_suppliers.add('RS');
         center.suppliers_allowed['society_show'] = true;
         center.RS_filters = angular.copy($scope.RS_filters);
        //  center.suppliers_meta = {};
         $scope.supplier_centers_list.RS.push(center_id);
         //added to show selected filter on mapview summary
         center.filters_meta['RS'] = {};
         center.filters_meta['RS'] = angular.copy($scope.inventory_filters);
       }
       if(center.suppliers['CP'] != undefined){
         $scope.extraSuppliersData[center_id]['CP'] = [];
        center.suppliers_allowed['corporate_allowed'] =  true;
        $scope.unique_suppliers.add('CP');
        center.suppliers_allowed['corporate_show'] =  true;
         center.CP_filters =  angular.copy($scope.CP_filters);
        //  center.suppliers_meta = {};
         $scope.supplier_centers_list.CP.push(center_id);
       }
       center_id++;
     });
     //Start : code added to display filter panel for all centers on gridview
     if($scope.unique_suppliers.has('RS')){
        $scope.gridView_RS_filters = angular.copy($scope.RS_filters);
        $scope.society_show = true;
        $scope.society_allowed_gridview = true;
      }
     if($scope.unique_suppliers.has('CP')){
        $scope.gridView_CP_filters = angular.copy($scope.CP_filters);
        $scope.corporate_show = true;
        $scope.corporate_allowed_gridview = true;
      }
      //End : code added to display filter panel for all centers on gridview
    }
    //End: add filter varible for each supplier in each center
      //Start: reset all filters
    // $scope.clearAllFilters = function(){
    //     // addSupplierFilters($scope.center_data);
    //     var defer = $q.defer();
    //     console.log($scope.center_data);
    //     for(var i=0;i<$scope.center_data.length;i++){
    //       $scope.center_data[i].RS_filters = angular.copy($scope.RS_filters);
    //       $scope.center_data[i].CP_filters =  angular.copy($scope.CP_filters);
    //     }
    //     var func = function(){$scope.societyFilters();}
    //     setTimeout(func, 1000);
    //     $scope.corporateFilters();
    // }
      //End: reset all filters
// This service gets all the spaces according to center specification like society_allowed
          //Start: adding code to call shortlisted_spaces api if the proposal data is already saved
          $scope.proposal_id_temp = $stateParams.proposal_id;
          if($window.sessionStorage.isSavedProposal == 'true'){
            mapViewService.getShortlistedSuppliers($scope.proposal_id_temp)
              .success(function(response, status){
                //TO convert dict to array as response coming in dict form and very difficult to use
                $scope.center_data = $.map(response.data, function(value, index){
                  return [value];
                });
                $scope.current_center = $scope.center_data[0];
                $scope.addSupplierFilters($scope.center_data);
                var flag;
                for(var i=0;i<$scope.center_data.length;i++){
                  if($scope.center_data[i].suppliers_meta != null){
                    flag = true;
                  }
                }
                if(flag == true){
                  checkSavedFilters();
                }
                $scope.current_center_index = 0;
                $scope.current_center_id = $scope.current_center.center.id;
                $scope.old_data = angular.copy($scope.center_data);
                toggleInventoryFilters($scope.current_center,'true','RS');
                mapViewBasicSummary();
                suppliersData();
                gridViewBasicSummary();
                gridViewFilterSummary();


                for(var i=0;i<$scope.center_data.length; i++)
                  $scope.initial_center_changed.push(false);
                $scope.current_center_id = $scope.current_center.center.id
                $scope.map = { zoom: 13, bounds: {},
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
                  $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
                  $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
                //loading icon
                $scope.loadIcon1 = response;
            })
              .error(function(response, status){
                alert("Error Occured");
              });
          }
          //Start: adding code to call shortlisted_spaces api if the proposal data is already saved
          else{
          mapViewService.getSpaces($scope.proposal_id_temp)
            .success(function(response, status){
                $scope.business_name = response.data.business_name;
                $scope.center_data = response.data.suppliers;

                $scope.current_center = response.data.suppliers[0];
                $scope.current_center_index = 0;
                $scope.current_center_id = $scope.current_center.center.id;
                $scope.old_data = angular.copy($scope.center_data);

                //loading icon
                $scope.loadIcon2 = response;
                //Start: code added if proposal is already created or exported, and user wants to edit that proposal
                var flag;
                // for(var i=0;i<$scope.center_data.length;i++){
                //   if($scope.center_data[i].suppliers_meta != null){
                //     flag = true;
                //   }
                // }
                // if(flag == true){
                //   checkSavedFilters();
                // }
                //End: code added if proposal is already created or exported and user wants to edit that proposal
                $scope.addSupplierFilters($scope.center_data);

                mapViewBasicSummary();
                suppliersData();
                gridViewBasicSummary();
                // gridView_Summary();
                for(var i=0;i<$scope.center_data.length; i++){
                  $scope.initial_center_changed.push(false);
                }
                $scope.current_center_id = $scope.current_center.center.id
                $scope.map = { zoom: 13, bounds: {},
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
                $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
                $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
              })
            .error(function(response, status){
                $scope.get_spaces_error = response.message;
                console.log("Error response : ",response);
            });
          }
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

// Start: supplier filters select deselecting functionality
    $scope.checkSuppliers = function(code){
      if(code == 'RS'){
        if($scope.society_allowed_gridview == true)
          $scope.society_allowed_gridview = false;
        else
          $scope.society_allowed_gridview = true;
        }
        if(code == 'CP'){
          if($scope.corporate_allowed_gridview == true)
            $scope.corporate_allowed_gridview = false;
          else
            $scope.corporate_allowed_gridview = true;
          }
    }
    // Start : check saved filter
    var checkSavedFilters = function (){
      console.log($scope.current_center);
        if($scope.current_center.suppliers_meta['RS'] != null){
          var filter_types = Object.keys($scope.current_center.suppliers_meta['RS']);
          for(var j=0;j<filter_types.length;j++){
            if(filter_types[j]=='inventory_type_selected'){
              selectFilters($scope.current_center.suppliers_meta['RS'][filter_types[j]],$scope.current_center.RS_filters['inventory']);
            }else
              selectFilters($scope.current_center.suppliers_meta['RS'][filter_types[j]],$scope.current_center.RS_filters[filter_types[j]]);
          }
        }
        if($scope.current_center.suppliers_meta['RS'] != null || $scope.current_center.suppliers['RS'] != null){
            $scope.societyFilters();
          }
        if($scope.current_center.suppliers_meta['CP'] != null){
          var filter_types = Object.keys($scope.current_center.suppliers_meta['CP']);
          for(var j=0;j<filter_types.length;j++){
            if(filter_types[j]=='inventory_type_selected'){
              selectFilters($scope.current_center.suppliers_meta['CP'][filter_types[j]],$scope.CP_filters['inventory']);
            }else
              selectFilters($scope.current_center.suppliers_meta['CP'][filter_types[j]],$scope.CP_filters[filter_types[j]]);
          }
        }
        if($scope.current_center.suppliers_meta['CP'] != null || $scope.current_center.suppliers['CP'] != null){
          $scope.corporateFilters();
        }

    }
    var selectFilters = function(saved_filter_type,current_filter_type){
      for(var i=0;i<saved_filter_type.length;i++){
        for(var j=0;j<current_filter_type.length;j++){
          if(saved_filter_type[i]==current_filter_type[j].code)
            current_filter_type[j].selected=true;
        }
      }
    }
    // End : check saved filter
    $scope.spaceSupplier = function(code,supplier){
    // this function handles selecting/deselecting society space i.e. society_allowed = true/false
    // code changed after changes done for adding two centers on gridView
        if(code == 'RS'){
          if(supplier == false){
            supplier = true;
            delete $scope.current_center.suppliers['RS'];
          }
          else{
            supplier = false;
            $scope.societyFilters();
          }
        }
        if(code == 'CP'){
          if(supplier == false){
            supplier = true;
            delete $scope.current_center.suppliers['CP'];
          }
          else{
            supplier = false;
            $scope.corporateFilters();
          }
        }
        $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
      }
     // This function is for showing societies on the map view
       $scope.showSocieties = function(){
              $scope.show_societies = !$scope.show_societies
       }
      var toggleInventoryFilters = function(center,value,code){
        if(value){
          center.filters_meta[code] = angular.copy($scope.inventory_filters);
          for(var i=0;i<center.RS_filters.inventory.length;i++){
            if(center.RS_filters.inventory[i].code.indexOf('PO') > -1 && center.RS_filters.inventory[i].selected == true){
              center.filters_meta[code].inv_poster++;
            }
            if(center.RS_filters.inventory[i].code.indexOf('ST') > -1 && center.RS_filters.inventory[i].selected == true){
              center.filters_meta[code].inv_standee++;
            }
            if(center.RS_filters.inventory[i].code.indexOf('SL') > -1 && center.RS_filters.inventory[i].selected == true){
              center.filters_meta[code].inv_stall++;
            }
            if(center.RS_filters.inventory[i].code.indexOf('FL') > -1 && center.RS_filters.inventory[i].selected == true){
              center.filters_meta[code].inv_flier++;
            }
          }
      }
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
  //Start:code for society filters
  $scope.societyFilters = function(value){
    //Start : Code added to filter multiple centers on gridview
    promises = [];
    var defer = $q.defer();
    if($scope.show_societies){
      for(var i=0;i<$scope.center_data.length;i++){
        if($scope.center_data[i].suppliers['RS'] != null){
          $scope.center_data[i].RS_filters = angular.copy($scope.gridView_RS_filters);
          toggleInventoryFilters($scope.center_data[i],value,'RS');
        }
      }
      for(var i=0;i<$scope.center_data.length;i++){
        if($scope.center_data[i].suppliers['RS'] != null){
          var filters = {
            'supplier_type_code' : 'RS',
            proposal_id : $scope.proposal_id_temp,
            center_id : $scope.center_data[i].center.id,
            common_filters : {
            latitude : $scope.center_data[i].center.latitude,
            longitude : $scope.center_data[i].center.longitude,
            radius : $scope.center_data[i].center.radius,
            quality : [],
            locality : [],
            quantity : [],
          },
          inventory_filters : [],
          specific_filters : {
            flat_type : [],
          },
        };
        makeFilters($scope.center_data[i].RS_filters.inventory,filters.inventory_filters);
        makeFilters($scope.center_data[i].RS_filters.flat_type,filters.specific_filters.flat_type);
        makeFilters($scope.center_data[i].RS_filters.quality_type,filters.common_filters.quality);
        makeFilters($scope.center_data[i].RS_filters.locality_rating,filters.common_filters.locality);
        makeFilters($scope.center_data[i].RS_filters.quantity_type,filters.common_filters.quantity);
        $scope.checkFilters = true;
        promises.push(mapViewService.getFilterSuppliers(filters));

      }
    }
    var data = [];
    $q.all(promises).then(function(response){
      data = angular.copy(promises);
      handleSupplierPromise(data,"RS");
      $scope.checkFilters = false;
    },function (error) {
    //This will be called if $q.all finds any of the requests erroring.
      handleErrors();
      $scope.checkFilters = false;
  });
  }
    //End : Code added to filter multiple centers on gridview
  else{
    $scope.gridView_RS_filters = angular.copy($scope.current_center.RS_filters);
    toggleInventoryFilters($scope.current_center,value,'RS');
      var filters = {
        'supplier_type_code' : 'RS',
        proposal_id : $scope.proposal_id_temp,
        center_id : $scope.current_center.center.id,
          common_filters : {
          latitude : $scope.current_center.center.latitude,
          longitude : $scope.current_center.center.longitude,
          radius : $scope.current_center.center.radius,
          quality : [],
          locality : [],
          quantity : [],
        },
        inventory_filters : [],
        specific_filters : {
          flat_type : [],
        },
      };
      makeFilters($scope.current_center.RS_filters.inventory,filters.inventory_filters);
      makeFilters($scope.current_center.RS_filters.flat_type,filters.specific_filters.flat_type);
      makeFilters($scope.current_center.RS_filters.quality_type,filters.common_filters.quality);
      makeFilters($scope.current_center.RS_filters.locality_rating,filters.common_filters.locality);
      makeFilters($scope.current_center.RS_filters.quantity_type,filters.common_filters.quantity);
      filterSupplierData(filters.supplier_type_code,filters);
      }
  }
  //End: code for society filters
  //Start: code for corporate filters
      $scope.real_estate_allowed = false;

      $scope.corporateFilters = function(value){
        //Start : Code added to filter multiple centers on gridview
        $scope.real_estate_allowed = value;
        promises = [];
        var defer = $q.defer();
        if($scope.show_societies){
          for(var i=0;i<$scope.center_data.length;i++){
            if($scope.center_data[i].suppliers['CP'] != null)
              $scope.center_data[i].CP_filters = angular.copy($scope.gridView_CP_filters);
          }
          for(var i=0;i<$scope.center_data.length;i++){
            if($scope.center_data[i].suppliers['CP'] != null){
              var filters = {
                'supplier_type_code' : 'CP',
                proposal_id : $scope.proposal_id_temp,
                center_id : $scope.center_data[i].center.id,
                common_filters : {
                latitude : $scope.center_data[i].center.latitude,
                longitude : $scope.center_data[i].center.longitude,
                radius : $scope.center_data[i].center.radius,
                quality : [],
                locality : [],
                quantity : [],
              },
              inventory_filters : [],
              specific_filters : {
                // real_estate_allowed : $scope.real_estate_allowed,
                employees_count : [],
              },
            };
            makeFilters($scope.center_data[i].CP_filters.inventory,filters.inventory_filters);
            makeFilters($scope.center_data[i].CP_filters.employee_count,filters.specific_filters.employees_count);
            makeFilters($scope.center_data[i].CP_filters.quality_type,filters.common_filters.quality);
            makeFilters($scope.center_data[i].CP_filters.locality_rating,filters.common_filters.locality);
            makeFilters($scope.center_data[i].CP_filters.quantity_type,filters.common_filters.quantity);
            if($scope.real_estate_allowed == true)
              filters.specific_filters.real_estate_allowed = true;
            $scope.checkFilters = true;
            promises.push(mapViewService.getFilterSuppliers(filters));

          }
        }
        var data = [];
        $q.all(promises).then(function(response){
          data = angular.copy(promises);
          handleSupplierPromise(data,"CP");
          $scope.checkFilters = false;
        },function (error) {
        //This will be called if $q.all finds any of the requests erroring.
          handleErrors();
          $scope.checkFilters = false;
      });
      }
        //End : Code added to filter multiple centers on gridview
    else{
      $scope.gridView_CP_filters = angular.copy($scope.current_center.CP_filters);
        var filters = {
          'supplier_type_code' : 'CP',
          proposal_id : $scope.proposal_id_temp,
          center_id : $scope.current_center.center.id,
            common_filters : {
            latitude : $scope.current_center.center.latitude,
            longitude : $scope.current_center.center.longitude,
            radius : $scope.current_center.center.radius,
            quality : [],
            locality : [],
            quantity : [],
          },
          inventory_filters : [],
          specific_filters : {
            // real_estate_allowed : $scope.real_estate_allowed,
            employees_count : [],
          },
        };
        makeFilters($scope.current_center.CP_filters.inventory,filters.inventory_filters);
        makeFilters($scope.current_center.CP_filters.employee_count,filters.specific_filters.employees_count);
        makeFilters($scope.current_center.CP_filters.quality_type,filters.common_filters.quality);
        makeFilters($scope.current_center.CP_filters.locality_rating,filters.common_filters.locality);
        makeFilters($scope.current_center.CP_filters.quantity_type,filters.common_filters.quantity);
        if($scope.real_estate_allowed == true)
          filters.specific_filters.real_estate_allowed = true;
        filterSupplierData(filters.supplier_type_code,filters);
      }
    }
//End: code for corporate filters
//Start: for handling multiplse center response in promises for all suppliers
      var handleSupplierPromise = function(responseData,code){
          for(var index=0;index<$scope.supplier_centers_list[code].length;index++){
            $scope.center_data[$scope.supplier_centers_list[code][index]].suppliers[code] = responseData[index].$$state.value.data.data.suppliers[code];
            if($scope.center_data[$scope.supplier_centers_list[code][index]].suppliers_meta){
              $scope.center_data[$scope.supplier_centers_list[code][index]].suppliers_meta[code] = responseData[index].$$state.value.data.data.suppliers_meta[code];
            }else {
              $scope.center_data[$scope.supplier_centers_list[code][index]].suppliers_meta = responseData[index].$$state.value.data.data.suppliers_meta;
            }
            //$scope.center_data[$scope.supplier_centers_list[code][index]].suppliers[code].push.apply($scope.center_data[$scope.supplier_centers_list[code][index]].suppliers[code],$scope.extraSuppliersData[index][code]);
          }
        $scope.current_center = $scope.center_data[$scope.current_center_index];
        suppliersData();
        mapViewBasicSummary();
        mapViewFiltersSummary();
        mapViewImpressions();
        gridViewBasicSummary();
        gridViewFilterSummary();
        gridViewImpressions();
        $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
        $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
      }
//End: for handling multiplse center response in promises for all suppliers
//Start: function for adding filters code to provided filter type list
              var makeFilters = function(filter_array,filter_list){
                for(var i=0; i<filter_array.length; i++){
                  if(filter_array[i].selected == true)
                    filter_list.push(filter_array[i].code);
                }
              }
//End: function for adding filters code to provided filter type list
//start: generic function for fetching all supplier filters
        var filterSupplierData = function (code,supplier_filters){
          $scope.checkFilters = true;
          mapViewService.getFilterSuppliers(supplier_filters)
                .success(function(response, status){
                    response.data.center = $scope.current_center.center;
                    $scope.center_data[$scope.current_center_index].suppliers[code] = response.data.suppliers[code];
                    if($scope.center_data[$scope.current_center_index].suppliers_meta){
                      $scope.center_data[$scope.current_center_index].suppliers_meta[code] = response.data.suppliers_meta[code];
                    }else {
                      $scope.center_data[$scope.current_center_index].suppliers_meta = response.data.suppliers_meta;
                    }
                    $scope.center_data[$scope.current_center_index].suppliers[code].push.apply($scope.center_data[$scope.current_center_index].suppliers[code],$scope.extraSuppliersData[$scope.current_center_index][code]);
                    $scope.current_center = $scope.center_data[$scope.current_center_index];

                    suppliersData();
                    mapViewBasicSummary();
                    mapViewFiltersSummary();
                    mapViewImpressions();
                    gridViewBasicSummary();
                    gridViewFilterSummary();
                    gridViewImpressions();
                    $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
                    $scope.center_marker = assignCenterMarkerToMap($scope.current_center.center);
                    $scope.checkFilters = false;
                })
                .error(function(response, status){
                    console.log("Error Happened while filtering");
                    $scope.checkFilters = false;
                });
        }
  //End: generic function for fetching all supplier filters
  //Start : function to handle all errors on mapview and gridview, call this function when error comes in response
    var handleErrors = function(){
      alert("Error Occured");
    }
  //End : function to handle all errors on mapview and gridview, call this function when error comes in response
            var promises = [];
      //       $scope.getFilteredSocieties = function(){
      //       promises = [];
      //       var defer = $q.defer();
      //       // start: for mapview only
      //       if(!$scope.show_societies){
      //       // for(var i=0; i<$scope.centers1.length; i++){
      //         var lat = "?lat=" + $scope.current_center.center.latitude ;
      //         var lng = "&lng=" + $scope.current_center.center.longitude;
      //         var radius = "&r=" + $scope.current_center.center.radius;
      //         var get_url_string = lat + lng + radius;
      //         get_url_string += makeString($scope.space_inventory_type, "&inv=");
      //         get_url_string += makeString($scope.space_location, "&loc=");
      //         get_url_string += makeString($scope.space_quality_type, "&qlt=");
      //         get_url_string += makeString($scope.space_quantity_type, "&qnt=");
      //         get_url_string += makeString($scope.society_flat_type, "&flt=");
      //
      //         // promises.push(mapViewService.getFilterSocieties(get_url_string));
      //     // } //end of for loop
      //
      //     // promises handled
      //
      //     mapViewService.getFilterSocieties(get_url_string)
      //           .success(function(response, status){
      //             //console.log(response);
      //             response.data.center = $scope.current_center.center;
      //               $scope.current_center = response.data;
      //               $scope.center_data[$scope.current_center_index] = response.data;
      //               //console.log($scope.center_data);
      //               // $scope.current_center.societies_inventory_count = response.societies_inventory_count;
      //               // $scope.current_center.societies_count = response.societies_count;
      //               // console.log("\n\n$scope.centers : ", $scope.centers);
      //               $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
      //               mapViewBasicSummary();
      //               mapViewFiltersSummary();
      //               mapViewImpressions();
      //               suppliersData();
      //               gridViewBasicSummary();
      //               gridViewFilterSummary();
      //               gridViewImpressions();
      //           })
      //           .error(function(response, status){
      //               console.log("Error Happened while filtering");
      //           });// end of q
      //         }
      //     // End: for mapview only
      //     //start: for gridview filters
      //     else{
      //       for(var i=0; i<$scope.center_data.length; i++){
      //         var lat = "?lat=" + $scope.center_data[i].center.latitude;
      //         var lng = "&lng=" + $scope.center_data[i].center.longitude;
      //         var radius = "&r=" + $scope.center_data[i].center.radius;
      //         var get_url_string = lat + lng + radius;
      //         get_url_string += makeString($scope.space_inventory_type, "&inv=");
      //         get_url_string += makeString($scope.space_location, "&loc=");
      //         get_url_string += makeString($scope.space_quality_type, "&qlt=");
      //         get_url_string += makeString($scope.space_quantity_type, "&qnt=");
      //         get_url_string += makeString($scope.society_flat_type, "&flt=");
      //
      //         promises.push(mapViewService.getFilterSocieties(get_url_string));
      //       } //end of for loop
      //
      //         // promises handled
      //       $q.all(promises).then(function(response){
      //         var length = $scope.center_data.length;
      //         for(var i=0; i<length; i++){
      //           response[i].data.data.center = $scope.center_data[i].center;
      //           $scope.center_data[i] = response[i].data.data;
      //
      //         } //end of for loop
      //         $scope.current_center = $scope.center_data[$scope.current_center_index];
      //         $scope.society_markers = assignMarkersToMap($scope.current_center.suppliers);
      //         mapViewBasicSummary();
      //         mapViewFiltersSummary();
      //         mapViewImpressions();
      //         suppliersData();
      //         gridViewBasicSummary();
      //         gridViewFilterSummary();
      //         gridViewImpressions();
      //       }) // end of q
      //     }
      //     //End: for gridview filters
      // }

      //End: angular-google-maps is loaded properly only then proces code inside then
    // var makeString = function(filter_array, filter_keyword){
    //           var my_string = filter_keyword;
    //           var length = filter_array.length;
    //           var count = 0;
    //           for(var i=0;i<length;i++)
    //               if(filter_array[i].selected){
    //                   my_string += filter_array[i].code + " ";
    //                   count += 1;
    //               }
    //           // Uncomment for better performance but this will also include null values for that filter
    //           // What this does is basically dont apply the filter if all values are selected
    //           if(count==length)
    //               my_string = filter_keyword;
    //           return my_string;
    //     }

  //Start: code added to search & show all suppliers on add societies tab
  $scope.supplier_names = [
    { name: 'Residential',      code:'RS'},
    { name: 'Corporate Parks',  code:'CP'},
    ];
  $scope.search;
  $scope.search_status = false;
  $scope.supplier_type_code;
  $scope.center_index = null;
  $scope.searchSuppliers = function(){
    $scope.search_status = false;
    if($scope.supplier_type_code && $scope.search){
      mapViewService.searchSuppliers($scope.supplier_type_code,$scope.search)
        .success(function(response, status){
            $scope.center_index = null;
          $scope.supplierData = response.data;
          if($scope.supplierData.length > 0){
            $scope.search_status = true;
            $scope.errorMsg = undefined;
          }
          else {
            $scope.errorMsg = "No Results Found, Please enter valid Search Text";
            $scope.search_status = false;
          }
        })
        .error(function(response, status){
            console.log("Error Happened while searching");
        });
      }
      else {
        $scope.errorMsg = "Please Fill all the details";
        $scope.supplierData = [];
        $scope.search_status = false;
      }
    }
    //End: code added to search & show all suppliers on add societies tab
    //Start: function to clear searched supplier data whenever add suppliers button clicked
    $scope.clearSearchData = function(){
    $scope.supplierData = [];
    $scope.search_status = false;
    $scope.supplier_type_code = null;
    $scope.search = null;
    $scope.errorMsg = undefined;
    $scope.center_index = null;

    $scope.createSupplierList();
    }
    //Start: To add searched societies in given center
      $scope.addMoreSuppliers = function(supplier,id){
        if($scope.center_data[$scope.current_center_index].suppliers[$scope.supplier_type_code] != undefined && $scope.center_index != null && checkDuplicateSupplier(supplier)){
          // supplier.status = 'S';
          // $scope.extraSuppliersData[$scope.current_center_index][$scope.supplier_type_code].push(supplier);
          $scope.center_data[$scope.current_center_index].suppliers[$scope.supplier_type_code].push(supplier);
          $scope.supplierData.splice(id,1);
          // $scope.changeCurrentCenter($scope.center_index);
          var center = $scope.center_data[$scope.current_center_index];
          $scope.updateSupplierStatus(supplier,center,$scope.supplier_type_code);
          mapViewBasicSummary();
          suppliersData();
          gridViewBasicSummary();
          $scope.errorMsg = "Supplier Added Successfully";
          if($scope.supplierData.length <=0){
            $scope.search_status = false;
            $scope.supplier_type_code = null;
            $scope.search = null;
          }
        }
        else if($scope.center_index == null){
          supplier.status = null;
          $scope.errorMsg = "Please select center first to add new suppliers";
        }
        else if($scope.center_index == null){
          $scope.errorMsg = "Selected supplier not allowedadd in this center";
        }
      }
    //End: To add searched societies in given center
    //Start: function to select center at add more suplliers
    $scope.selectCenter = function(center_index){
      $scope.center_index = center_index;
      if(center_index != null){
        for(var i=0;i<$scope.center_data.length; i++){
          if($scope.center_data[i].center.id == center_index){
              $scope.current_center_index = i;
          }
        }
      }
    }
    //End: function to select center at add more suplliers
//Start: upload and import functionality
//Start: For sending only shortlisted societies & selected inventory types
     function saveSelectedFilters(){
     //Start: For sending filtered inventory type

         var society_inventory_type_selected = [];
         for(var center = 0; center<$scope.center_data.length; center++){
           if($scope.center_data[center].suppliers_meta){
             if($scope.center_data[center].suppliers_meta['RS']){
               $scope.center_data[center].suppliers_meta['RS'].inventory_type_selected = [];
               $scope.center_data[center].suppliers_meta['RS'].quality_type = [];
               $scope.center_data[center].suppliers_meta['RS'].quantity_type = [];
               $scope.center_data[center].suppliers_meta['RS'].flat_type = [];
               $scope.center_data[center].suppliers_meta['RS'].locality_rating = [];
               makeFilters($scope.center_data[center].RS_filters.inventory,$scope.center_data[center].suppliers_meta['RS'].inventory_type_selected);
               makeFilters($scope.center_data[center].RS_filters.quality_type,$scope.center_data[center].suppliers_meta['RS'].quality_type);
               makeFilters($scope.center_data[center].RS_filters.quantity_type,$scope.center_data[center].suppliers_meta['RS'].quantity_type);
               makeFilters($scope.center_data[center].RS_filters.flat_type,$scope.center_data[center].suppliers_meta['RS'].flat_type);
               makeFilters($scope.center_data[center].RS_filters.locality_rating,$scope.center_data[center].suppliers_meta['RS'].locality_rating);
             }
             if($scope.center_data[center].suppliers_meta['CP']){
               $scope.center_data[center].suppliers_meta['CP'].inventory_type_selected = [];
               $scope.center_data[center].suppliers_meta['CP'].quality_type = [];
               $scope.center_data[center].suppliers_meta['CP'].quantity_type = [];
               $scope.center_data[center].suppliers_meta['CP'].employee_count = [];
               $scope.center_data[center].suppliers_meta['CP'].locality_rating = [];

               makeFilters($scope.center_data[center].CP_filters.inventory,$scope.center_data[center].suppliers_meta['CP'].inventory_type_selected);
               makeFilters($scope.center_data[center].CP_filters.quality_type,$scope.center_data[center].suppliers_meta['CP'].quality_type);
               makeFilters($scope.center_data[center].CP_filters.quantity_type,$scope.center_data[center].suppliers_meta['CP'].quantity_type);
               makeFilters($scope.center_data[center].CP_filters.employee_count,$scope.center_data[center].suppliers_meta['CP'].employee_count);
               makeFilters($scope.center_data[center].CP_filters.locality_rating,$scope.center_data[center].suppliers_meta['CP'].locality_rating);
             }
           }
         }
       }
       //End: For sending filtered inventory type

       //Start: setting status of suppliers like shortlisted, removed or buffer
       $scope.setSupplierStatus = function (supplier,value){
          if(supplier.buffer_status == false && value == 'B')
              supplier.status = 'S';
          else if(supplier.buffer_status == true && value != 'R')
            supplier.status = 'B';
          else
            supplier.status = value;
          if(value != 'B')
            supplier.shortlisted = !supplier.shortlisted;
       };
       //End: setting status of suppliers like shortlisted, removed or buffer
       $scope.submitProposal = function(){
         saveSelectedFilters();
       };
     $scope.exportData = function(){
         $scope.checkFileExport = true;
         var parent_proposal_id = $window.sessionStorage.parent_proposal_id;
         saveSelectedFilters();
         var proposal_data = {
           centers:$scope.center_data,
           is_proposal_version_created:$window.sessionStorage.isSavedProposal,
         };
         //console.log(data);
         $http({
              url: constants.base_url + constants.url_base + parent_proposal_id + '/proposal-version/',
              method: 'POST',
              //responseType: 'arraybuffer',
              data: proposal_data, //this is your json data string
              headers: {
                  'Content-type': 'application/json',
                  // 'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                  'Authorization' : 'JWT ' + $rootScope.globals.currentUser.token
              }
         }).success(function(response){
           console.log(response);
              // convert it onto Blob object because it's a binary file.
              // var blob = new Blob([data], {
              //     type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
              // });
              // fetch the content_type and file name from headers
              // $scope.content_type = headers('content-type');
              // $scope.file_name = headers('file_name');
              // set the file to blob
              // $scope.file_data = blob
              // var uploadUrl = 'http://mdimages.s3.amazonaws.com/';
              //upload file to amazon server
              //uploadFileToAmazonServer($scope.file_name,$scope.file_data);
              // download it immediately
              //saveAs(blob, $scope.file_name);
              $scope.checkFileExport = false;

         }).error(function(response){
              //Some error log
              $scope.checkFileExport = false;
              alert('Error in exporting the file');
         });
     }

//Start : function to upload files to amazon server, just provide file name and file
   var uploadFileToAmazonServer = function(file_name,file){
     // upload it to S3 Bucket
     Upload.upload({
         url: 'http://mdimages.s3.amazonaws.com/',
         method : 'POST',
         data: {
             key: file_name, // the key to store the file on S3, could be file name or customized
             AWSAccessKeyId : constants.AWSAccessKeyId,
             acl : constants.acl, // sets the access to the uploaded file in the bucket: private, public-read, ...
             policy : constants.policy,
             signature : constants.signature, // base64-encoded signature based on policy string (see article below)
             "Content-Type": constants.content_type,// content type of the file (NotEmpty)
             file: file }
         }).success(function (response){
              alert("Upload to Server Successful");
         }).error(function(response) {
             alert("Upload to server Unsuccessful");
         });
   }
//End : function to upload files to amazon server, just provide file name and file
    $scope.upload = function (file) {
      var uploadUrl = 'http://localhost:8108/v0/ui/website/';
      var token = $rootScope.globals.currentUser.token ;
      Upload.upload({
          url: uploadUrl + $scope.proposal_id_temp + '/import-supplier-data/',
          data: {file: file, 'username': $scope.username},
          headers: {'Authorization': 'JWT ' + token},
      }).success(function (response) {
        uploadFileToAmazonServer(response.data,file);
          //console.log('Success ' + resp.config.data.file.name + 'uploaded. Response: ' + resp.data);
      }).error(function (response) {
          console.log('Error status: ' + response.status);
          alert("Data not Imported");
      });
    };
    //End: upload and import functionality
    //Start:save suppliers and filters to save the current state
    $scope.saveData = function(){
       saveSelectedFilters();
      mapViewService.saveData($scope.proposal_id_temp,$scope.center_data)
        .success(function(response, status){
          alert("Saved Successfully");
        }).error(function(response, status){
          alert("Error Occured");
      });//
    }
    //End:save suppliers and filters to save the current state
    // Start: function to update status of supplier and save in db
    $scope.updateSupplierStatus = function(supplier,center,code){
      var data = {
        'center_id':center.center.id,
        'supplier_id':supplier.supplier_id,
        'status':supplier.status,
        'supplier_type_code':code,
      };
      mapViewService.updateSupplierStatus($scope.proposal_id_temp,data)
        .success(function(response, status){
          alert("Saved Successfully");
        }).error(function(response, status){
          alert("Error Occured");
      });
    }
    // End: function to update status of supplier and save in db
    //Start:create dict of supplier_ids
    $scope.createSupplierList = function(){
      $scope.supplier_id_list = [];

      for(var i=0;i<$scope.center_data.length;i++){
        $scope.supplier_id_list[i] = {};

        var supplier_keys = Object.keys($scope.center_data[i].suppliers);
        angular.forEach(supplier_keys,function(key){
          $scope.supplier_id_list[i][key] = {};
          for(var j=0;j<$scope.center_data[i].suppliers[key].length; j++){
            $scope.supplier_id_list[i][key][$scope.center_data[i].suppliers[key][j].supplier_id] = j;
          }
        });
      }
    }
    //Start: check duplicate suppliers if adding more suppliers
    var checkDuplicateSupplier = function(supplier){
        if($scope.supplier_id_list[$scope.current_center_index][$scope.supplier_type_code][supplier.supplier_id] !=null){
          // var index = $scope.supplier_id_list[$scope.current_center_index][$scope.supplier_type_code][supplier.supplier_id]
          // var center = $scope.center_data[$scope.current_center_index];
          // $scope.updateSupplierStatus(supplier,center,$scope.supplier_type_code);
          // center.suppliers[$scope.supplier_type_code][index].status = supplier.status;
          // alert("Supplier already Exist and You changed Supplier status");
          supplier.status = null;
          $scope.errorMsg = "Supplier already Exist";
          return false;
        }
        else{
          return true;
        }
    }
  });
  //start : code added for societyDetails
$scope.getSocietyDetails = function(supplier,center,index){
  $scope.temp_index = index;
  $scope.center = center;
  mapViewService.processParam();
  var supplier_id = supplier.supplier_id;
  $scope.society = {};
  $scope.disable = false;
  $scope.residentCount = {};
  $scope.inventoryDetails = {};
  $scope.totalInventoryCount = {};
  $scope.supplier_type_code = "RS";
  mapViewService.getSociety(supplier_id,$scope.supplier_type_code)
   .success(function (response) {
     $scope.myInterval=300;
     $scope.society_images = response.data.supplier_images;
     $scope.society = supplier;
    //  $scope.society = response.data.supplier_data;
     //$rootScope.societyname = response.society_data.society_name;
     $scope.residentCount = estimatedResidents(response.data.supplier_data.flat_count);
     $scope.flatcountflier = response.data.supplier_data.flat_count;
     var baseUrl = 'http://mdimages.s3.amazonaws.com/';
     // Start : Code added to seperate images by their image tag names
     var imageUrl;
     $scope.SocietyImages = [],$scope.FlierImages=[],$scope.PosterImages=[],$scope.StandeeImages=[],$scope.StallImages=[],$scope.CarImages=[];
     for(var i=0;i<$scope.society_images.length;i++){
       if($scope.society_images[i].name == 'Society'){
         imageUrl = baseUrl + $scope.society_images[i].image_url;
         $scope.SocietyImages.push(imageUrl);
       }
       if($scope.society_images[i].name == 'Standee Space'){
         imageUrl = baseUrl + $scope.society_images[i].image_url;
         $scope.StandeeImages.push(imageUrl);
       }
       if($scope.society_images[i].name == 'Stall Space'){
         imageUrl = baseUrl + $scope.society_images[i].image_url;
         $scope.StallImages.push(imageUrl);
       }
       if($scope.society_images[i].name == 'Fliers'){
         imageUrl = baseUrl + $scope.society_images[i].image_url;
         $scope.FlierImages.push(imageUrl);
       }
       if($scope.society_images[i].name == 'Car Display'){
         imageUrl = baseUrl + $scope.society_images[i].image_url;
         $scope.CarImages.push(imageUrl);
       }
       if($scope.society_images[i].name == 'Lift' || $scope.society_images[i].name == 'Notice Board'){
         imageUrl = baseUrl + $scope.society_images[i].image_url;
         $scope.PosterImages.push(imageUrl);
       }
   }
   // End : Code added to seperate images by their image tag names
  });

  mapViewService.get_inventory_summary(supplier_id, $scope.supplier_type_code)
  .success(function (response){
    $scope.inventoryDetails = response;
     $scope.totalInventoryCount = inventoryCount($scope.inventoryDetails);
     $scope.model = response;
  });
}//End of function getSocietyDetails
  function estimatedResidents (flatcount){
    var residents = flatcount * 4;
    $scope.residentCount = {
       residents  : residents,
    };
    return $scope.residentCount;
  }
  function inventoryCount (inventoryDetails){
         var totalPoster = inventoryDetails.lift_count + inventoryDetails.nb_count ;
         $scope.totalInventoryCount = {
            totalPoster  : totalPoster,
         };
         return $scope.totalInventoryCount;
  }

 if($rootScope.campaignId){
     mapViewService.getShortlistedSocietyCount($rootScope.campaignId)
     .success(function(response,status){
         $scope.societies_count = response.count;

     }).error(function(response,status){
         console.log("error ",response.error);
     });
 }

 $scope.society_ids = {}
 mapViewService.getSocietyIds()
 .success(function(response,status){
     $scope.society_ids = response.society_ids;
     $scope.minlength = 0;
     $scope.maxlength = $scope.society_ids.length-1;
     for(var i=0;i<= $scope.maxlength; i++){
         if($rootScope.societyId == $scope.society_ids[i]){
             $scope.index = i;
             break;
         }
     }
 });

     $scope.nextSociety = function(){
     $scope.index = $scope.index + 1;
     if($scope.index <= $scope.maxlength){
         // getsocietyfunc($scope.model[$scope.index].supplier_id)
         var current_path = $location.path()
         var pos = current_path.lastIndexOf("/");
         var required_path = current_path.slice(0,pos+1) + $scope.society_ids[$scope.index] ;
         $location.path(required_path);
         // history.pushState({bar : "foo"}, "page 3", required_path);
         // setCurrentPage(required_path);
     }else{
         $scope.index = $scope.index - 1;
     }
 }

 $scope.previousSociety = function(){
    $scope.index = $scope.index - 1;
     if($scope.index >= $scope.minlength){
         var current_path = $location.path()
         var pos = current_path.lastIndexOf("/");
         var required_path = current_path.slice(0,pos+1) + $scope.society_ids[$scope.index] ;
         $location.path(required_path);
         // history.pushState({bar : "foo"}, "page 3", required_path);
         // setCurrentPage(required_path);
     }
     else{
        $scope.index = $scope.index + 1;
     }
 }

 $scope.societyByIndex = function(index){
     $scope.numberError = false;
     if(index <= $scope.maxlength && index >= $scope.minlength){
         $scope.index = index;
         var current_path = $location.path()
         var pos = current_path.lastIndexOf("/");
         var required_path = current_path.slice(0,pos+1) + $scope.society_ids[$scope.index] ;
         $location.path(required_path);
     }
     else{
         $scope.numberError = true;
          // $scope.startFade = true;
          //  $timeout(function(){
          //    $scope.numberError = true;
          //  }, 2000);
     }
     $scope.societyIndex = undefined;
 }
 $scope.getSecondIndex = function(Images,index)
 {
   if(index-Images.length>=0)
     return null;
   else
     return index;
 }
  $scope.societyList = function() {
    $location.path("manageCampaign/shortlisted/" + $rootScope.campaignId + "/societies");
  };
  //Start:code added for shortlist societies
  $scope.shortlistThis = function(status){
    var code = 'RS';
    $scope.society.status = status;
    $scope.updateSupplierStatus($scope.society,$scope.center,code);
  }
  //End:code added for shortlist societies
  //Start:For adding shortlisted society
  // if($rootScope.campaignId){
  //   $scope.shortlistThis = function(id) {
  //   mapViewService.addShortlistedSociety($rootScope.campaignId, id)
  //    .success(function (response){
  //        // $scope.model = response;
  //          // $location.path("manageCampaign/shortlisted/" + $rootScope.campaignId + "/societies");
  //          $scope.disable = true;
  //          $scope.societies_count = response.count;
  //
  //          // var temp = "#alert_placeholder" + index;
  //          var temp = "#alert_placeholder";
  //        var style1 = 'style="position:absolute;z-index:1000;margin-left:-321px;margin-top:-100px;background-color:gold;font-size:18px;"'
  //        $(temp).html('<div ' + style1 + 'class="alert alert-warning alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>'+response.message +'</span></div>')
  //        setTimeout(function() {
  //            $("div.alert").remove();
  //        }, 3000);
  //   });
  // }}//End: For adding shortlisted society
//End: code added for societydetails
$(".modal-fullscreen").on('show.bs.modal', function () {
  setTimeout( function() {
    $(".modal-backdrop").addClass("modal-backdrop-fullscreen");
  }, 0);
});
$(".modal-fullscreen").on('hidden.bs.modal', function () {
  $(".modal-backdrop").addClass("modal-backdrop-fullscreen");
});

});
