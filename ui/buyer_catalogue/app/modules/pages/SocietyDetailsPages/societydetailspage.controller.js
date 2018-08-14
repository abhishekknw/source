angular.module('catalogueApp')
.controller('SocietyDetailsPagesCtrl',
    ['$scope', '$rootScope', '$window', '$location','societyDetailsViewService','$stateParams','commonDataShare','constants','$timeout','Upload','cfpLoadingBar','permissions',
    function ($scope, $rootScope, $window, $location, societyDetailsViewService, $stateParams,commonDataShare,constants,$timeout,Upload,cfpLoadingBar, permissions) {


    console.log("Hellow World");
    var supplierId = $stateParams.supplierId;
    var supplier_type_code = 'RS';
    //start : code added for societyDetails
  $scope.getSocietyDetails = function(){
    // $scope.temp_index = index;
    // $scope.center = center;
    societyDetailsViewService.processParam();
    var supplier_id = supplierId;
    $scope.society = {};
    $scope.disable = false;
    $scope.residentCount = {};
    $scope.inventoryDetails = {};
    $scope.totalInventoryCount = {};
    $scope.supplier_type_code = "RS";
    societyDetailsViewService.getSociety(supplier_id,supplier_type_code)
     .then(function onSuccess(response) {
       console.log(response);
       $scope.loading = response;
       setSocietyLocationOnMap(response.data.data.supplier_data);
        $scope.loading = response.data.data.supplier_data;
       $scope.myInterval=300;
       $scope.society_images = response.data.data.supplier_images;
       console.log($scope.society_images);
       $scope.amenities = response.data.data.amenities;
       $scope.society =  response.data.data.supplier_data;
       console.log($scope.society);
      //  $scope.society = response.data.supplier_data;
       //$rootScope.societyname = response.society_data.society_name;
       $scope.residentCount = estimatedResidents(response.data.data.supplier_data.flat_count);
       $scope.flatcountflier = response.data.data.supplier_data.flat_count;
       var baseUrl = constants.aws_bucket_url;
console.log(baseUrl);
       // Start : Code added to seperate images by their image tag names
       var imageUrl;
       $scope.SocietyImages = [],$scope.FlierImages=[],$scope.PosterImages=[],$scope.StandeeImages=[],$scope.StallImages=[],$scope.CarImages=[];
       for(var i=0;i<$scope.society_images.length;i++){
         if($scope.society_images[i].name == 'Society'){
           imageUrl = baseUrl + $scope.society_images[i].image_url;
           console.log(imageUrl);
           $scope.SocietyImages.push(imageUrl);
         }
         if($scope.society_images[i].name == 'Standee Space'){
           imageUrl = baseUrl + $scope.society_images[i].image_url;
           console.log(imageUrl);
           $scope.StandeeImages.push(imageUrl);
         }
         if($scope.society_images[i].name == 'Stall Space'){
           imageUrl = baseUrl + $scope.society_images[i].image_url;
           console.log(imageUrl);
           $scope.StallImages.push(imageUrl);
         }
         if($scope.society_images[i].name == 'Fliers'){
           imageUrl = baseUrl + $scope.society_images[i].image_url;
           console.log(imageUrl);
           $scope.FlierImages.push(imageUrl);
         }
         if($scope.society_images[i].name == 'Car Display'){
           imageUrl = baseUrl + $scope.society_images[i].image_url;
           console.log(imageUrl);
           $scope.CarImages.push(imageUrl);
         }
         if($scope.society_images[i].name == 'Lift' || $scope.society_images[i].name == 'Notice Board'){
           imageUrl = baseUrl + $scope.society_images[i].image_url;
           $scope.PosterImages.push(imageUrl);
         }
     }
     console.log($scope.StallImages);

     // End : Code added to seperate images by their image tag names
    });

    societyDetailsViewService.get_inventory_summary(supplier_id, supplier_type_code)
    .then(function onSuccess(response){
      console.log(response);
      $scope.societyDetails = true;
      if('inventory' in response.data){
        $scope.inventoryDetails = response.data.inventory;
        console.log(  $scope.inventoryDetails);
         $scope.totalInventoryCount = inventoryCount($scope.inventoryDetails);
         $scope.model = response.data.inventory;
         $scope.inventories_allowed = response.data.inventories_allowed_codes;
         console.log($scope.inventories_allowed);
         $scope.show_inventory = true;
       }
    }).catch(function onError(response){
      console.log("error",response);
      commonDataShare.showErrorMessage(response);
    });
  }//End of function getSocietyDetails

  //start: map start
  var setSocietyLocationOnMap = function(supplier){
    var mapOptions = {
         center:new google.maps.LatLng(0,0),
        //  zoom:13
         mapTypeId: google.maps.MapTypeId.ROADMAP
      }
      var map = new google.maps.Map(document.getElementById("supplierMap"),mapOptions);

      var marker = new google.maps.Marker({
         position: new google.maps.LatLng(supplier.society_latitude, supplier.society_longitude),
         map: map,
         mapTypeId: google.maps.MapTypeId.ROADMAP
      });


      var latlngbounds = new google.maps.LatLngBounds();
      latlngbounds.extend(marker.position);
      // map.setCenter(latlngbounds.getCenter());
      map.fitBounds(latlngbounds);
      //  map.setZoom(15);
      // map.setCenter(marker.getPosition());

      google.maps.event.addListenerOnce(map, 'bounds_changed', function(event) {
        //  map.setCenter(marker.getPosition());
          if (this.getZoom()){
              this.setZoom(16);
          }
        });

        google.maps.event.addListenerOnce(map, 'idle', function() {
          google.maps.event.trigger(map, 'resize');
        });
        // map.panToBounds(latlngbounds);

      // bounds.extend(new google.maps.LatLngBounds(19.088291, 72.442383));
      // map.fitBounds(bounds);

    }
    function inventoryCount (inventoryDetails){
           var totalPoster = inventoryDetails.lift_count + inventoryDetails.nb_count ;
           $scope.totalInventoryCount = {
              totalPoster  : totalPoster,
           };
           return $scope.totalInventoryCount;
    }
    function estimatedResidents (flatcount){
      var residents = flatcount * 4;
      $scope.residentCount = {
         residents  : residents,
      };
      return $scope.residentCount;
    }
    //start: event on close societydetails modal
    $('#societyDetails').on('hidden.bs.modal', function () {
      $scope.inventories_allowed = [];
      $scope.show_inventory = false;
      $scope.societyDetails = true;
    })
    $scope.inventory_codes = {
      poster : 'PO',
      standee : 'ST',
      stall : 'SL',
      flier : 'FL',
      cardisplay : 'CD',
    }

    $scope.isAllowed = function(inventory){
      if($scope.inventories_allowed.indexOf(inventory) >= 0)
        return true;
      else
        return false;
    }

  $scope.getSocietyDetails();
  }]);
