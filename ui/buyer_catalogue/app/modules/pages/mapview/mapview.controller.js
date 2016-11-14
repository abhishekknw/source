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
          console.log(spaces);
          var markers = [];
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
            // $scope.selectSuppliers($scope.current_center.suppliers);
            suppliersData();
            mapViewBasicSummary();
            // mapViewFiltersSummary();
            // mapViewImpressions();
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
                $scope.current_center.suppliers = response.data.suppliers[0].suppliers;
                // $scope.current_center = response;
                $scope.center_data[$scope.current_center_index].suppliers = response.data.suppliers[0].suppliers;
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
            $scope.corporates_count = $scope.current_center.suppliers['CP'].length;
          }
      }
    //End: mapview basic summary
    //Start: mapview filter summary required after applying filters
     var mapViewFiltersSummary = function(){
       $scope.stall_count = 0, $scope.standee_count = 0;
       if($scope.current_center.suppliers_meta['RS'] != undefined){
         $scope.stall_count += $scope.current_center.suppliers_meta['RS'].inventory_count.stalls;
         $scope.standee_count += $scope.current_center.suppliers_meta['RS'].inventory_count.standees;
       }
       if($scope.current_center.suppliers_meta['CP'] != undefined){
         console.log($scope.current_center);
         $scope.stall_count += $scope.current_center.suppliers_meta['CP'].inventory_count.stalls;
         $scope.standee_count += $scope.current_center.suppliers_meta['CP'].inventory_count.standees;
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
        if($scope.center_data[center].suppliers_meta !=undefined){
          if($scope.center_data[center].suppliers_meta['RS'] != undefined){
            $scope.total_stalls += $scope.center_data[center].suppliers_meta['RS'].inventory_count.stalls;
            $scope.total_standees += $scope.center_data[center].suppliers_meta['RS'].inventory_count.standees;
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
    $scope.unique_suppliers = new Set();
    var center_id=0;
    $scope.addSupplierFilters = function(centers){
      angular.forEach(centers, function(center){

        center.suppliers_allowed = {};
       if(center.suppliers['RS'] != undefined){
         center.suppliers_allowed.society_allowed = true;
         $scope.unique_suppliers.add('RS');
         center.suppliers_allowed['society_show'] = true;
         center.RS_filters = angular.copy($scope.RS_filters);
         center.suppliers_meta = {};
         $scope.supplier_centers_list.RS.push(center_id);
       }
       if(center.suppliers['CP'] != undefined){
        center.suppliers_allowed['corporate_allowed'] =  true;
        $scope.unique_suppliers.add('CP');
        center.suppliers_allowed['corporate_show'] =  true;
         center.CP_filters =  angular.copy($scope.CP_filters);
         center.suppliers_meta = {};
         $scope.supplier_centers_list.CP.push(center_id);
       }
       center_id++;
     });
     console.log($scope.supplier_centers_list);
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
          $scope.proposal_id_temp = $stateParams.proposal_id;
          mapViewService.getSpaces($scope.proposal_id_temp)
            .success(function(response, status){
              console.log("center",response);
                $scope.business_name = response.data.business_name;
                $scope.center_data = response.data.suppliers;
                $scope.addSupplierFilters($scope.center_data);
                console.log("printing center_data", $scope.center_data);
                $scope.current_center = response.data.suppliers[0];
                // console.log($scope.current_center);
                console.log("printing current_center", $scope.current_center);
                $scope.current_center_index = 0;
                $scope.old_data = angular.copy($scope.center_data);
                // $scope.selectSuppliers($scope.center_data[0].suppliers);
                // $scope.checkSuppliers();

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

    // $scope.society_allowed = false, $scope.corporate_allowed = false;
    // $scope.selectSuppliers = function(suppliers){
    //     if(suppliers['RS'] != undefined){
    //       $scope.society = true;
    //     }
    //     else{
    //       $scope.society = false;
    //     }
    //     if(suppliers['CP'] != undefined){
    //       $scope.corporate =true;
    //     }
    //     else {
    //       $scope.corporate = false;
    //     }
    // }

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
            console.log(value);
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
          $scope.societyFilters();
              // $scope.getFilteredSocieties();
        }
      //Start: remove selected supplier filters
      // var deselectFilters = function(code){
      //   if(code == 'RS'){
      //     console.log($scope.current_center);
      //     // $scope.current_center.RS_filters = angular.copy($scope.RS_filters);
      //     $scope.inv_poster=false,$scope.inv_flier=false,$scope.inv_stall=false,$scope.inv_standee=false;
      //     pcount=0,stcount=0,slcount=0,flcount=0;
      //   }
      //   if(code == 'CP'){
      //     $scope.current_center.CP_filters =  angular.copy($scope.CP_filters);
      //   }
      //   mapViewBasicSummary();
      //   gridViewBasicSummary();
      // }
      //End:  remove selected supplier filters
      // Just deselects all the checkboxes of filter_array passed.Added reset function to deselct all inventoriesclearAllFilters

            // $scope.clearAllFilters = function(){
            //     reset($scope.space_quality_type);
            //     reset($scope.space_location);
            //     reset($scope.space_quality_type);
            //     reset($scope.space_quantity_type);
            //     reset($scope.society_flat_type);
            //     $scope.getFilteredSocieties();
            // }
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
        if($scope.center_data[i].suppliers['RS'] != null)
          $scope.center_data[i].RS_filters = angular.copy($scope.gridView_RS_filters);
      }
      for(var i=0;i<$scope.center_data.length;i++){
        if($scope.center_data[i].suppliers['RS'] != null){
          var filters = {
            'supplier_type_code' : 'RS',
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

        promises.push(mapViewService.getFilterSuppliers(filters));

      }
    }
    var data = [];
    $q.all(promises).then(function(response){
      data = angular.copy(promises);
      handleSupplierPromise(data,"RS");
    })
  }
    //End : Code added to filter multiple centers on gridview
  else{
    $scope.gridView_RS_filters = angular.copy($scope.current_center.RS_filters);
      var filters = {
        'supplier_type_code' : 'RS',
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
            console.log($scope.real_estate_allowed);
            if($scope.real_estate_allowed == true)
              filters.specific_filters.real_estate_allowed = true;
            promises.push(mapViewService.getFilterSuppliers(filters));

          }
        }
        var data = [];
        $q.all(promises).then(function(response){
          data = angular.copy(promises);
          handleSupplierPromise(data,"CP");
        })
      }
        //End : Code added to filter multiple centers on gridview
    else{
      $scope.gridView_CP_filters = angular.copy($scope.current_center.CP_filters);
        var filters = {
          'supplier_type_code' : 'CP',
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
        console.log(responseData);
          for(var index=0;index<$scope.supplier_centers_list[code].length;index++){
            $scope.center_data[$scope.supplier_centers_list[code][index]].suppliers[code] = responseData[index].$$state.value.data.data.suppliers[code];
            $scope.center_data[$scope.supplier_centers_list[code][index]].suppliers_meta[code] = responseData[index].$$state.value.data.data.suppliers_meta[code];
            console.log($scope.center_data);
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
          mapViewService.getFilterSuppliers(supplier_filters)
                .success(function(response, status){
                  // console.log($scope.current_center);
                  console.log("response of filters",response);
                    response.data.center = $scope.current_center.center;
                    $scope.center_data[$scope.current_center_index].suppliers[code] = response.data.suppliers[code];
                    $scope.center_data[$scope.current_center_index].suppliers_meta[code] = response.data.suppliers_meta[code];
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
                })
                .error(function(response, status){
                    console.log("Error Happened while filtering");
                });
        }
  //End: generic function for fetching all supplier filters
  //
  var filterAllCenterSupplierData = function (code,supplier_filters){
    mapViewService.getFilterSuppliers(supplier_filters)
          .success(function(response, status){
            console.log(response);
          })
          .error(function(response, status){
              console.log("Error Happened while filtering");
          });
        }
  //

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
              var lat = "?lat=" + $scope.center_data[i].center.latitude;
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
  $scope.supplier_names = [
    { name: 'Residential',      code:'RS'},
    { name: 'Corporate Parks',  code:'CP'},
    ];
  $scope.search;
  $scope.supplier_type_code;
  $scope.searchSuppliers = function(){
    mapViewService.searchSuppliers($scope.supplier_type_code,$scope.search)
      .success(function(response, status){
        console.log(response);
        $scope.search_SupplierData = response.data;
        console.log($scope.search_SupplierData);
      })
      .error(function(response, status){
          console.log("Error Happened while searching");
      });
  }
//End: Function added to show all suppliers on gridView

//Start: upload and import functionality
//Start: For sending only shortlisted societies & selected inventory types
     function getShortlistedFilteredSocieties(){
      //  for(var i=0;i<$scope.center_data.length;i++){
      //    for(var j=0;j<$scope.center_data[i].societies.length;j++){
      //      if($scope.center_data[i].societies[j].shortlisted == false){
      //         $scope.center_data[i].societies.splice(j--,1);
      //         $scope.center_data[i].societies_count--;
      //      }
      //    }
      //  }
     //End: For sending only shortlisted society in
     //Start: For sending filtered inventory type

         var society_inventory_type_selected = [];
         for(var center = 0; center<$scope.center_data.length; center++){
           if($scope.center_data[center].suppliers_meta['RS']){
             $scope.center_data[center].suppliers_meta['RS'].inventory_type_selected = [];
             for(var filter = 0; filter<$scope.center_data[0].RS_filters.inventory.length; filter++){
               if($scope.center_data[center].RS_filters.inventory[filter].selected == true){
                 $scope.center_data[center].suppliers_meta['RS'].inventory_type_selected.push($scope.center_data[center].RS_filters.inventory[filter].code);
               }
             }
           }
           if($scope.center_data[center].suppliers_meta['CP']){
             $scope.center_data[center].suppliers_meta['CP'].inventory_type_selected = [];
             for(var filter = 0; filter<$scope.center_data[0].CP_filters.inventory.length; filter++){
               if($scope.center_data[center].CP_filters.inventory[filter].selected == true){
                 $scope.center_data[center].suppliers_meta['CP'].inventory_type_selected.push($scope.center_data[center].RS_filters.inventory[filter].code);
               }
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
         getShortlistedFilteredSocieties();
           console.log("Submitting $scope.centers :", $scope.centers);
       };
       $scope.exportData = function(){
           $scope.download = false;
         getShortlistedFilteredSocieties();
         console.log($scope.center_data);
           mapViewService.exportProposalData($scope.proposal_id_temp, $scope.center_data)
           .success(function(data, status, headers, config){
               console.log("Successfully Exported");
               $scope.file_name = headers('file_name');
               console.log($scope.file_name);
               console.log(headers());
              //  window.open($scope.file_name);
              var file = data;
              var file_type = headers('content-type');
              console.log(file_type);
              // saveAs(file,$scope.file_name);
              var uploadUrl = 'http://mdimages.s3.amazonaws.com/';
              console.log(uploadUrl+$scope.file_name);
              Upload.upload({
                  url: uploadUrl + $scope.file_name,
                  method : 'PUT',
                  data: {
                    key: $scope.file_name, // the key to store the file on S3, could be file name or customized
                    AWSAccessKeyId: 'AKIAI6PVCXJEAXV6UHUQ',
                    acl: 'public-read', // sets the access to the uploaded file in the bucket: private, public-read, ...
                    policy: "eyJleHBpcmF0aW9uIjogIjIwMjAtMDEtMDFUMDA6MDA6MDBaIiwKICAiY29uZGl0aW9ucyI6IFsgCiAgICB7ImJ1Y2tldCI6ICJtZGltYWdlcyJ9LCAKICAgIFsic3RhcnRzLXdpdGgiLCAiJGtleSIsICIiXSwKICAgIHsiYWNsIjogInB1YmxpYy1yZWFkIn0sCiAgICBbInN0YXJ0cy13aXRoIiwgIiRDb250ZW50LVR5cGUiLCAiIl0sCiAgICBbImNvbnRlbnQtbGVuZ3RoLXJhbmdlIiwgMCwgNTI0Mjg4MDAwXQogIF0KfQoK",
                    signature: "GsF32EZ1IFvr2ZDH3ww+tGzFvmw=", // base64-encoded signature based on policy string (see article below)
                    "Content-Type": file_type, // content type of the file (NotEmpty)
                    file: file}
              });
              $scope.download_url = uploadUrl + $scope.file_name;
              $scope.download = true;
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

    $scope.upload = function (file) {
      var uploadUrl = 'http://localhost:8108/v0/ui/website/';
      Upload.upload({
          url: uploadUrl + $scope.proposal_id_temp + '/import-supplier-data/',
          data: {file: file, 'username': $scope.username}
      }).then(function (resp) {
        console.log(resp);
          console.log('Success ' + resp.config.data.file.name + 'uploaded. Response: ' + resp.data);
      }, function (resp) {
          console.log('Error status: ' + resp.status);
      });
    };
    //End: upload and import functionality

});
