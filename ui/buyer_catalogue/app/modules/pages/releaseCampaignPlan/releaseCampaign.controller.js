angular.module('catalogueApp')
.controller('ReleaseCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location','releaseCampaignService','$stateParams','constants','permissions','mapViewService',
    function ($scope, $rootScope, $window, $location, releaseCampaignService, $stateParams,constants, permissions, mapViewService) {
  $scope.campaign_id = $stateParams.proposal_id;
  $scope.positiveNoError = constants.positive_number_error;
  $scope.campaign_manager = constants.campaign_manager;
  if($rootScope.globals.userInfo.is_superuser == true){
    $scope.backButton = true;
  }
  $scope.supplierSummaryData = {};
  $scope.shortlistedSuppliersIdList = {}
  $scope.permissions = permissions.supplierBookingPage;
  $scope.showSummaryTab = false;
 	$scope.headings = [
        {header : 'Index'},
        {header : 'Supplier Name'},
        {header : 'Area,(Sub Area)'},
        {header : 'Address'},
        {header : 'Flat Count'},
        {header : 'Tower Count'},
        // {header : 'Status'},
        // {header : 'Supplier ID'},
        {header : 'Inventory Type'},
        {header : 'Inventory Count'},
        {header : 'Inventory Supplier Price'},
        {header : 'Total Supplier Price(Per Flat)  '},
        {header : 'Negotiated Price'},
        {header : 'Freebies'},
        {header : 'Booking Status'},
        {header : 'Phase'},
        {header : 'Mode Of Payment'},
        {header : 'Contacts'},
        {header : 'Payment Status'},
      ];
  $scope.booking_status = [
    {name:'Booked', code : 'BK'},
    {name:'Not Booked', code : 'NB'},
  ];
  $scope.contact_headings = [
    {header : 'Salutation'},
    {header : 'Name'},
    {header : 'Designation'},
    {header : 'Email'},
    {header : 'STD Code'},
    {header : 'Landline No'},
    {header : 'Mobile No'},

  ];
  $scope.payment_headings = [
    {header : 'Name On Cheque'},
    {header : 'Bank Name'},
    {header : 'IFSC Code'},
    {header : 'Account Number'},
  ];
  $scope.filters = [
    {name : 'Poster(PO)',  code : 'PO',   selected : false },
    {name : 'Standee(ST)', code : 'ST',   selected : false },
    {name : 'Stall(SL)',   code : 'SL',   selected : false },
    {name : 'Flyer(FL)',   code : 'FL',   selected : false },
    {name : 'Gateway Arch',   code : 'GA',   selected : false },
  ]
  $scope.shortlisted = constants.shortlisted;
  $scope.buffered = constants.buffered;
  $scope.removed = constants.removed;
  $scope.finalized = constants.finalized;

  $scope.statusCode = {
      shortlisted : constants.statusCode_shortlisted,
      buffered : constants.statusCode_buffered,
      removed : constants.statusCode_removed,
      finalized: constants.statusCodeFinalized,
  }
    $scope.clear = function() {
        $scope.dt = null;
      };

      $scope.maxDate = new Date(2020, 5, 22);
      $scope.today = new Date();
      $scope.popup1 = false;
      $scope.popup2 = false;
      $scope.popup3 = false;
      $scope.error = false;

      $scope.setDate = function(year, month, day) {
        $scope.dt = new Date(year, month, day);
      };
      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];

    $scope.saveDetails = function(){
      // alert("vidhi");
    };

    releaseCampaignService.getCampaignReleaseDetails($scope.campaign_id)
    	.then(function onSuccess(response){
        console.log(response);
    		$scope.releaseDetails = response.data.data;
        console.log($scope.releaseDetails);

        angular.forEach($scope.releaseDetails.shortlisted_suppliers, function(supplier){
          $scope.mapViewLat = supplier.latitude;
          $scope.mapViewLong = supplier.longitude;
          // console.log($scope.mapViewLat);
          // console.log($scope.mapViewLong);


        })


        setDataToModel($scope.releaseDetails.shortlisted_suppliers);
        $scope.loading = response;
        angular.forEach($scope.releaseDetails.shortlisted_suppliers, function(supplier){
          $scope.shortlistedSuppliersIdList[supplier.supplier_id] = supplier;
        })
    	})
    	.catch(function onError(response){
        console.log(response);
        commonDataShare.showErrorMessage(response);
    		console.log("error occured", response.status);
    	});

      var setDataToModel = function(suppliers){
        for(var i=0;i<suppliers.length;i++){
          suppliers[i].total_negotiated_price = parseInt(suppliers[i].total_negotiated_price);
          suppliers[i].phase = parseInt(suppliers[i].phase);
        }
      }
    $scope.emptyList = {NA:'NA'};
    $scope.getFilters = function(supplier){
      var keys = Object.keys(supplier.shortlisted_inventories);
      if(keys.length > 0){
        $scope.inventory_type = supplier.shortlisted_inventories
        return supplier.shortlisted_inventories;
      }
      else{
        return $scope.emptyList;
      }
    }
    //Start:To set contacts to show in contactModal
    $scope.setContact = function(supplier){
      if(supplier.contacts.length > 0)
        $scope.contacts = supplier.contacts;
      else
        $scope.contacts = null;
    }
    //End:To set contacts to show in contactModal
    //Start:To set payment details to show in paymentModal
    $scope.setPayment = function(supplier){
        $scope.payment = supplier;
    }
    //End:To set payment details to show in paymentModal
    //Start: TO go to audit release plan pages
    $scope.changeLocation = function(){
      $location.path('/' + $scope.campaign_id + '/auditReleasePlan');
    }
    //To show inventory ids in modal after clicking on inventory type
    $scope.setInventoryIds = function(filter){
      $scope.inventoryIds = [];
      $scope.inventoryIds = filter.detail;
    }
    $scope.updateData = function(){
      releaseCampaignService.updateAuditReleasePlanDetails($scope.campaign_id,$scope.releaseDetails.shortlisted_suppliers)
      .then(function onSuccess(response){
        swal(constants.name,constants.updateData_success,constants.success);
      })
      .catch(function onError(response){
        commonDataShare.showErrorMessage(response);
        // swal(constants.name,constants.updateData_error,constants.error);
        console.log("error occured", response.status);
      });
    }
    $scope.getCampaignState = function(state){
      return constants[state];
    }
    $scope.getInventoryPrice = function(price, inventory){
      if(inventory == 'POSTER')
        price = price * 0.3;
      return price;
    }
    $scope.getTotalSupplierPrice = function(supplier){
      var totalPrice = 0;
      angular.forEach(supplier.shortlisted_inventories, function(value, key){
        if(key == 'POSTER')
          totalPrice = totalPrice + value.actual_supplier_price *0.3;
        else
          totalPrice += value.actual_supplier_price;
      })
      return totalPrice;
    }
    //Start: code added to search & show all suppliers on add societies tab
    $scope.supplier_names = [
      { name: 'Residential',      code:'RS'},
      { name: 'Corporate Parks',  code:'CP'},
      { name: 'Bus Shelter',  code:'BS'},
      { name: 'Gym',  code:'GY'},
      { name: 'Saloon',  code:'SA'},
      { name: 'Retail Store',  code:'RE'},
      ];
    $scope.search;
    $scope.search_status = false;
    $scope.supplier_type_code;
    $scope.center_index = null;
    $scope.searchSuppliers = function(){
     try{
      $scope.search_status = false;
      console.log($scope.supplier_type_code,$scope.search);
      if($scope.supplier_type_code && $scope.search){
        mapViewService.searchSuppliers($scope.supplier_type_code,$scope.search)
          .then(function onSuccess(response, status){
            console.log(response);
              $scope.center_index = null;
            $scope.supplierData = response.data.data;
            if($scope.supplierData.length > 0){
              $scope.search_status = true;
              $scope.errorMsg = undefined;
            }
            else {
              $scope.errorMsg = "No Results Found, Please enter valid Search Text";
              $scope.search_status = false;
            }
          })
          .catch(function onError(response, status){
              console.log("Error Happened while searching");
              commonDataShare.showErrorMessage(response);
              // swal(constants.name,constants.errorMsg,constants.error);
          });
        }
        else {
          $scope.errorMsg = "Please Fill all the details";
          $scope.supplierData = [];
          $scope.search_status = false;
        }
      }catch(error){
        console.log(error.message);
      }
    }
      //End: code added to search & show all suppliers on add societies tab
    $scope.addSuppliersToList = function(supplier){
      if(!(supplier.supplier_id in $scope.shortlistedSuppliersIdList || supplier.supplier_id in $scope.supplierSummaryData))
        $scope.supplierSummaryData[supplier.supplier_id] = supplier;
      else
        alert("supplier Already Present");
      console.log($scope.supplierSummaryData);
    }
    $scope.removeSupplierToList = function(supplier_id){
      delete $scope.supplierSummaryData[supplier_id];
    }
    //Start: function to clear searched supplier data whenever add suppliers button clicked
    $scope.clearSearchData = function(){
      try{
        $scope.supplierData = [];
        $scope.search_status = false;
        $scope.supplier_type_code = null;
        $scope.search = null;
        $scope.errorMsg = undefined;
        $scope.center_index = null;

        $scope.supplierSummaryData = {};
      }catch(error){
        console.log(error.message);
      }
    }
    $scope.addSuppliersToCampaign = function(){
      var supplier_ids = [];
      var filters = [];
      angular.forEach($scope.supplierSummaryData, function(supplier){
        var supplierKeyValueData = {
          id : supplier.supplier_id,
          status : 'F',
        }
        supplier_ids.push(supplierKeyValueData);

      })
      angular.forEach($scope.filters, function(filter){
        if(filter.selected){
          var filterKeyValuData = {
            id : filter.code
          }
          filters.push(filterKeyValuData);
        }
      })
      console.log(filters);
      var data = {
        campaign_id : $scope.releaseDetails.campaign.proposal_id,
        center_data : {
          RS : {
            supplier_data : supplier_ids,
            filter_codes : filters,
          },

        },
      }
      if(filters.length && supplier_ids.length){
        releaseCampaignService.addSuppliersToCampaign(data)
        .then(function onSuccess(response){
          console.log(response);
              $('#addNewSocities').modal('hide');
          swal(constants.name,constants.add_data_success,constants.success);
        }).catch(function onError(response){
          console.log(response);
        })
      }else{
        alert("Atleast One Supplier and One Filter is required to Continue");
      }

    }


$scope.orderProperty = "f";
$scope.setOrderProperty = function(propertyName) {
        if ($scope.orderProperty === propertyName) {
            $scope.orderProperty = '-' + propertyName;
        } else if ($scope.orderProperty === '-' + propertyName) {
            $scope.orderProperty = propertyName;
        } else {
            $scope.orderProperty = propertyName;
        }
    };

$scope.searchSelectAllModel=[];

$scope.multiSelect =
[{
        name: "Whatsapp Group",
        id: "1",

      }, {
        name: "Email Group",
        id: "2",

      }, {
        name: "Building ERP",
        id: "3",

      }, {
        name: "Door To Door",
        id: "4",

      }];
      $scope.selected_baseline_settings = {
       template: '<b>{{option.name}}</b>',
       selectedToTop: true // Doesn't work
     };



      $scope.selected_baselines_customTexts = {buttonDefaultText: 'Select Freebies'};


}]);//Controller function ends here
