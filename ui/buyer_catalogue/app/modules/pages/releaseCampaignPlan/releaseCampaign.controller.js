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
  $scope.editPaymentDetails = true;
 	$scope.headings = [
        {header : 'Index'},
        {header : 'Supplier Name'},
        {header : 'Area,(Sub Area)'},
        {header : 'Address'},
        {header : 'RelationShip Data'},
        {header : 'Flat Count'},
        {header : 'Tower Count'},
        // {header : 'Status'},
        // {header : 'Supplier ID'},
        {header : 'Inventory Type'},
        // {header : 'Stall Location'},
        {header : 'Inventory Count'},
        {header : 'Inventory Supplier Price'},
        {header : 'Total Supplier Price   (Per Flat)  '},
        {header : 'Negotiated Price'},
        {header : 'Freebies'},
        {header : 'Booking Status'},
        {header : 'Phase'},
        {header : 'Mode Of Payment'},
        {header : 'Contacts'},
        {header : 'Payment Status'},
      ];
  $scope.booking_status = [
    {name:'Decision Pending', code : 'DP'},
    {name:'Confirmed Booking', code : 'BK'},
    {name:'Tentative Booking', code : 'NB'},
    {name:'Phone Booked' , code : 'PB'},
    {name:'Visit Booked', code : 'VB'},
    {name:'Rejected', code : 'SR'},
    {name:'Send Email', code : 'SE'},
    {name:'Visit Required', code : 'VR'},
    {name:'Call Required', code : 'CR'},
  ];

  $scope.payment_status = [
    {name:'Not Initiated', code : 'PNI'},
    {name:'Pending', code : 'PP'},
    {name:'Cheque Released' , code : 'PCR'},
    {name:'Paid', code : 'PD'},
    {name:'Rejected', code : 'PR'},

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
      $scope.Data = [];
    releaseCampaignService.getCampaignReleaseDetails($scope.campaign_id)
    	.then(function onSuccess(response){
        console.log(response);

    		$scope.releaseDetails = response.data.data;
        $scope.Data = $scope.releaseDetails.shortlisted_suppliers;
        console.log($scope.Data);
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
    $scope.search = {};
    $scope.search_status = false;
    $scope.supplier_type_code = {};
    $scope.center_index = null;
    $scope.searchSuppliers = function(){
     try{
      $scope.search_status = false;
      console.log($scope.supplier_type_code.code,$scope.search.query);
      if($scope.supplier_type_code.code && $scope.search.query){
        mapViewService.searchSuppliers($scope.supplier_type_code.code,$scope.search.query)
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
      if(!(supplier.supplier_id in $scope.shortlistedSuppliersIdList || supplier.supplier_id in $scope.supplierSummaryData)){
        $scope.supplierSummaryData[supplier.supplier_id] = supplier;
        $scope.showAddSupplierMsg = 'Added Successfully';
        alert($scope.showAddSupplierMsg);
      }
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
        $scope.supplier_type_code = {};
        $scope.search = {};
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

    $scope.selectAllLocation=[];

    $scope.stallLoc =
    [{
            name: "Near Entry Gate",
            id: "1",

          }, {
            name: "Near Exit Gate",
            id: "2",

          }, {
            name: "In Front of Tower",
            id: "3",

          }, {
            name: "Near Garden",
            id: "4",

          },
          {
            name: "Near Play Area",
            id: "5",

          },
          {
            name: "Near Club House",
            id: "6",

          },
          {
            name: "Near Swimming Pool",
            id: "7",

          },{
            name: "Near Parking Area",
            id: "8",

          },
          {
            name: "Near Shopping Area",
            id: "9",

          }];
          $scope.selected_baseline = {
           template: '<b>{{option.name}}</b>',
           selectedToTop: true // Doesn't work
         };

        $scope.selected_customTexts = {buttonDefaultText: 'Stall Location'};
        $scope.getRelationShipData = function(supplier){
          $scope.relationshipData = {};
          var supplierCode = 'RS';
          var campaignId = $scope.releaseDetails.campaign.proposal_id;
          $scope.supplierFlatCount = supplier.flat_count;
          releaseCampaignService.getRelationShipData(supplier.supplier_id,supplierCode,campaignId)
          .then(function onSuccess(response){
            $scope.relationshipData = response.data.data;
            console.log(response);
          }).catch(function onError(response){
            console.log(response);
          })
        }

        $scope.savePaymentDetails = function(){
          console.log($scope.payment);
          releaseCampaignService.savePaymentDetails($scope.payment,$scope.payment.supplier_id)
          .then(function onSuccess(response){
            $scope.editPaymentDetails = !$scope.editPaymentDetails;
            console.log($scope.editPaymentDetails);
            // $scope.payment.name_for_payment = response.data.name_for_payment;
            // $scope.payment.bank_name = response.data.bank_name;
            // $scope.payment.ifsc_code = response.data.ifsc_code;
            // $scope.payment.ifsc_code = response.data.account_no;
            console.log(response);
          }).catch(function onError(response){
            console.log(response);
          })
        }


}]);//Controller function ends here
