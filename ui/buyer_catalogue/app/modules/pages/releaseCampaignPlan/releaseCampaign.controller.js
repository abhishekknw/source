angular.module('catalogueApp')
.controller('ReleaseCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location','releaseCampaignService','$stateParams','permissions','Upload','cfpLoadingBar','constants','mapViewService','$timeout',
    function ($scope, $rootScope, $window, $location, releaseCampaignService, $stateParams, permissions, Upload, cfpLoadingBar,constants, mapViewService, $timeout) {
  $scope.campaign_id = $stateParams.proposal_id;
  $scope.positiveNoError = constants.positive_number_error;
  $scope.campaign_manager = constants.campaign_manager;
  $scope.editPaymentDetails = true;

  $scope.body = {
    message : '',
  };
  $scope.editContactDetails = true;
  $scope.addContactDetails = true;

  if($rootScope.globals.userInfo.is_superuser == true){
    $scope.backButton = true;
  }
  $scope.supplierSummaryData = {};
  $scope.shortlistedSuppliersIdList = {}
  $scope.permissions = permissions.supplierBookingPage;
  $scope.showSummaryTab = false;
  $scope.editPaymentDetails = true;
  $scope.editContactDetails = true;
  $scope.addContactDetails = true;

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
    {name:'Undecided', code : ''},
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
    {header : 'Remove'},

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
      $scope.payment = supplier;
      console.log(supplier);

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
            $scope.editPaymentDetails = true;
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

      $scope.setEditPaymentDetails = function(){
          $scope.editPaymentDetails = false;
          console.log($scope.editPaymentDetails);
        }

        // $scope.saveContactDetails = function(){
        //   console.log($scope.payment);
        //   releaseCampaignService.saveContactDetails($scope.payment,$scope.payment.supplier_id)
        //   .then(function onSuccess(response){
        //     $scope.editContactDetails = true;
        //     console.log($scope.editContactDetails);
        //     console.log(response);
        //   }).catch(function onError(response){
        //     console.log(response);
        //   })
        // }
        var temp_data = [];

        $scope.saveContactDetails = function(){
          var data = {
            supplier_id : $scope.payment.supplier_id,
            contacts : []
          };
          angular.forEach($scope.payment.contacts, function(item){
            console.log(item);
              var temp_data = {
                salutation : item.salutation,
                name : item.name,
                designation: item.designation,
                email:item.email,
                std_code : item.std_code,
                landline: item.landline,
                mobile: item.mobile,
                object_id : item.supplier_id,
              }
              data.contacts.push(temp_data);
          });
          console.log(temp_data);
          console.log(data);
          console.log($scope.payment);
          releaseCampaignService.saveContactDetails($scope.payment,$scope.payment.supplier_id)
          .then(function onSuccess(response){
            console.log(response);
          }).catch(function onError(response){
            console.log(response);
          })
          // console.log($scope.addRow);
        // $scope.addRow.push({});
        }
        $scope.setEditContactDetails = function(){
            $scope.editContactDetails = false;
            console.log($scope.editContactDetails);
          }
          $scope.addRow = ({});
          $scope.addContactDetail = function(){
            $scope.addRow = $scope.payment.contacts;
            $scope.addContactDetails = false;
            console.log($scope.addRow);
          $scope.addRow.push({});
          }

          $scope.removeContact = function(index){
            $scope.payment.contacts.splice(index , 1);
          }
        $scope.IsVisible = false;
       $scope.updateSupplierStatus = function (value) {
      //If DIV is visible it will be hidden and vice versa.
      $scope.IsVisible = value == "Y";
      }

   $scope.uploadImage = function(file,supplier){
     console.log(supplier);

     // cfpLoadingBar.set(0.3)

         var token = $rootScope.globals.currentUser.token;
         if (file) {
            // $("#progressBarModal").modal();
           cfpLoadingBar.start();
           // cfpLoadingBar.inc();
           Upload.upload({
               url: constants.base_url + constants.url_base + constants.upload_image_activity_url,
               data: {
                 file: file,
                 // 'inventory_activity_assignment_id' : inventory.id,
                 // 'supplier_name' : inventory.supplier_name,
                 // 'activity_name' : inventory.act_name,
                 // 'inventory_name' : inventory.inv_type,
                 // 'activity_date' : inventory.act_date,
               },
               headers: {'Authorization': 'JWT ' + token}
           }).then(function onSuccess(response){
                 uploaded_image = {'image_path': response.data.data };
                 supplier.images.push(uploaded_image);
                 cfpLoadingBar.complete();
                 // $("#progressBarModal").modal('hide');
           })
           .catch(function onError(response) {
             cfpLoadingBar.complete();
             console.log(response);
           });
         }
       }
        //to send email
        $scope.loadSpinner = true;
        $scope.sendNotification = function(){
          console.log($scope.body);
          $scope.loadSpinner = false;
          var email_Data = {
            subject:$scope.paymentStatus + " Details For " + $scope.supplierPaymentData.name,
            body:$scope.body.message,
            to:'yogesh.mhetre@machadalo.com',
          };
          releaseCampaignService.sendMail(email_Data)
          .then(function onSuccess(response){
            console.log(response);
            $scope.taskId = response.data.data.task_id;
            sendMailInProgress();
        	})
        	.catch(function onError(response){
            $scope.loadSpinner = true;
            $('#selectedPaymentModal').modal('hide');
            // $('#declineModal').modal('hide');
            commonDataShare.showErrorMessage(response);
            // swal(constants.name,constants.onhold_error,constants.error);
        		console.log("error occured", response);
        	});
          $scope.reason = "";
       }

       var sendMailInProgress = function(){
         releaseCampaignService.sendMailInProgress($scope.taskId)
         .then(function onSuccess(response){
           if(response.data.data.ready != true){
              $timeout(sendMailInProgress,constants.sleepTime); // This will perform async
           }
           else if(response.data.data.status == true){
             $scope.loadSpinner = true;
             $('#selectedPaymentModal').modal('hide');
             // $('#selectedPaymentModal').modal('hide');

             swal(constants.name,constants.email_success,constants.success);
           }
           else {
             $scope.loadSpinner = true;
             swal(constants.name,constants.email_error,constants.error);
           }
         }).catch(function onError(response){
           $scope.loadSpinner = true;
           $('#onHoldModal').modal('hide');
           $('#declineModal').modal('hide');
           commonDataShare.showErrorMessage(response);
           swal(constants.name,constants.email_error,constants.error);
         });
       }

       $scope.getPaymentDetails = function(supplier,status){
         console.log(supplier);
         $scope.body.message = '';
         $scope.supplierPaymentData = supplier;
          $scope.paymentStatus = status;
          if(status == 'NEFT' || status == 'CASH'){
            supplier.payment_status = 'PP';
          }else if(status == 'CHEQUE'){
            supplier.payment_status = 'PCR';
          }

          supplier.booking_status = 'NB';

          $scope.body.message = "Beneficiary Name : " +  $scope.supplierPaymentData.name_for_payment + ",     " +
            "Bank Account Number : " + $scope.supplierPaymentData.account_no + ",     " +
            "IFSC Code : " + $scope.supplierPaymentData.ifsc_code + ",     " +
            "Negotiated Price :" + $scope.supplierPaymentData.total_negotiated_price + ",     " +
            "Message : ";
       }

       $scope.updateSupplierStatus = function(supplier){
         if(supplier.transaction_or_check_number){
           console.log("hello");
           supplier.payment_status = 'PD';
           supplier.booking_status = 'BK';
         }

       }




}]);//Controller function ends here
