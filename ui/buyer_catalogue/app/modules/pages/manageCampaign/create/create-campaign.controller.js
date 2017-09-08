  angular.module('machadaloPages')
.controller('CreateCampaignCtrl',
    function ($scope, $rootScope, $window, $location, pagesService, constants, Upload, commonDataShare, constants, $timeout, AuthService, $state) {

      //start:code added to show or hide details based on user's group permissions
      $scope.bd_manager = constants.bd_manager;
      $scope.campaign_manager = constants.campaign_manager;

      //End:code added to show or hide details based on user permissions
      $scope.uploadfile = true; // added for loading spinner active/deactive
      $scope.account_proposals = [];
      $scope.model = {};
      $scope.model.business = {};
    	$scope.businesses = [];
      $scope.supplier_types = ['Society', 'Corporate', 'Club', 'Mall', 'School/College']
    	$scope.campaign_types = ['Poster', 'Standee', 'Stall', 'CarDisplay', 'Fliers']
    	$scope.campaign_sub_types = {
    		'Poster': ['A4', 'A3'],
    		'Standee': ['Small', 'Medium', 'Large'],
    		'Stall':['Small', 'Medium', 'Large','Canopy'],
    		'CarDisplay':['Normal', 'Premium'],
            'Fliers': ['Normal']
    	}

        $scope.clear = function() {
        $scope.dt = null;
      };
      $scope.proposalRequested = constants.proposalRequested;
      $scope.proposalFinalized = constants.proposalFinalized;
      $scope.proposalConverted = constants.proposalConverted;
      $scope.proposalOnHold = constants.proposalOnHold;
      $scope.proposalDeclined = constants.proposalDeclined;
      $scope.proposalMaking = constants.proposalMaking;
      $scope.maxDate = new Date(2020, 5, 22);
      $scope.today = new Date();
      $scope.popup1 = false;
      $scope.popup2 = false;
      $scope.error = false;

      $scope.setDate = function(year, month, day) {
        $scope.dt = new Date(year, month, day);
      };

      // $scope.sel_account_id = null;
      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];

      //$scope.phoneNumberPattern = /^[1-9]{1}[0-9]{9}$/
    	$scope.campaign_type = {}

      $scope.contact = {
        name: '',
        designation: '',
        department: '',
        email: '',
        phone: '',
        spoc: ''
      };

      $scope.bsSelect = undefined; // initially nothing selected as existing business

      var contactCopy = angular.copy($scope.contact);
      $scope.model.business.contacts = [$scope.contact];

      // Start: for persisting values after refresh or back from other pages
      $scope.getStoredData = function(){
        if($window.localStorage.business != null){
          $scope.model.business = JSON.parse($window.localStorage.business);
          if($window.localStorage.accounts != null){
            $scope.model.accounts = JSON.parse($window.localStorage.accounts);
            if($window.localStorage.sel_account_index >= 0){
              $scope.sel_account_id = $scope.model.accounts[$window.localStorage.sel_account_index].account_id;
              $scope.getProposals($scope.sel_account_id,$window.localStorage.sel_account_index);
            }
          }
          // if($window.localStorage.account_proposals != null)
          //   $scope.account_proposals = JSON.parse($window.localStorage.account_proposals);
          $scope.choice = "selected";
        }else {
          $scope.model.business = null;
          $scope.model.accounts = null;
          $scope.account_proposals = null;
        }
      }
      // End: for persisting values after refresh or back from other pages

      pagesService.loadBusinessTypes()
      .then(function (response){
          $scope.busTypes = response.data;
        })
        .catch(function onError(response){
          commonDataShare.showErrorMessage(response);
          // swal(constants.name,constants.errorMsg,constants.error);
        });
      $scope.getBusiness = function() {
        pagesService.getBusiness($scope.bsSelect)
        .then(function (response) {
          console.log(response);
              $scope.model.business = response.data.business;
              $scope.model.accounts = response.data.accounts;
              $rootScope.business_id = response.data.business.business_id;
              $window.localStorage.business_id = response.data.business.business_id;
              $rootScope.business_name = response.data.business.name;
              $window.localStorage.business_name = response.data.business.name;
              $scope.model.business.business_type_id = $scope.model.business.type_name.id.toString();
              $scope.getSubTypes();
              $scope.model.business.sub_type_id = $scope.model.business.sub_type.id.toString();
              $scope.choice = "selected";
              // pagesService.setBusinessObject($scope.model.business);
              //Start: added to persit data after refresh
              $window.localStorage.business = JSON.stringify($scope.model.business);
              if($scope.model.accounts.length != 0){
                $window.localStorage.accounts = JSON.stringify($scope.model.accounts);
              }else{
                $window.localStorage.accounts = null;
              }
              $window.localStorage.account_proposals = null;
              $scope.account_proposals = null;
              $window.localStorage.sel_account_index = -1;
              $scope.sel_account_id = null;
              $scope.error = false;
              $scope.thenMsg = null;
              //End: added to persit data after refresh
         })
         .catch(function onError(response){
           commonDataShare.showErrorMessage(response);
          //  swal(constants.name,constants.errorMsg,constants.error);
         });
      };

      var business_id_temp = pagesService.getBusinessId();
      if(business_id_temp){
        $scope.bsSelect = business_id_temp;
        $scope.getBusiness();
      };

      $scope.getSubTypes = function() {
            if($scope.model.business.business_type_id == null){
                $scope.sub_types = {};
                $scope.model.business.sub_type_id = "";
            }else{
                var id = $scope.model.business.business_type_id;
                pagesService.getSubTypes(id)
                .then(function (response){
                    $scope.sub_types = response.data;
                  })
                  .catch(function onError(response){
                    commonDataShare.showErrorMessage(response);
                    // swal(constants.name,constants.errorMsg,constants.error);
                  });
            }
        }

        $scope.addNew = function() {
        // object def is directly added to avoid different array elements pointing to same object
            $scope.model.business.contacts.push({
                name: '',     designation: '',    department: '',
                email: '',    phone: '',      spoc: ''
            });
        };

      $scope.remove = function(index) {
        $scope.model.business.contacts.splice(index, 1);
      };

    	$scope.getAllBusinesses = function() {
        $window.localStorage.account_proposals = null;
        $window.localStorage.sel_account_index = null;
        $scope.bsSelect = undefined;
	    	pagesService.getAllBusinesses()
	    	.then(function (response) {
	            $scope.businesses = response.data;
	       })
         .catch(function onError(response){
           commonDataShare.showErrorMessage(response);
          //  swal(constants.name,constants.errorMsg,constants.error);
         });
	    };

      $scope.readMore = function() {
              $scope.seeMore = "true";
      };

      $scope.editDetails = function() {
              $scope.choice = "select";
      };

      $scope.showAccount = function(account) {
             $scope.currentAccount = account;
      };

      $scope.editAccount = function(account) {
            $(".modal-backdrop").hide();
            pagesService.setAccountId(account.account_id);
            $location.path("/manageCampaign/editAccount/" + account.account_id + "/");
      };

      $scope.newBusiness = function() {
              $scope.contact = angular.copy(contactCopy);
              $scope.form.$setPristine();
              $scope.model.business = {};
              $scope.model.accounts = {};
              $scope.model.business.contacts = [$scope.contact];
              $scope.account_proposals = null;
              $scope.sel_account_id = null;
              $scope.choice = "new";
              $scope.bsSelect = undefined;
      };

      $scope.addNewAccount = function() {
              pagesService.setAccountId(undefined);
              $location.path("/manageCampaign/createAccount/");
      };

      $scope.getProposals = function(sel_account_id,index){
          $scope.error = false;
          // pass account_id of selected account radio button
          $scope.sel_account_id = sel_account_id;
          // $rootScope.account_id = sel_account_id;

          //start : added to persist data after refresh
          $window.localStorage.sel_account_index = index;
          $window.localStorage.account_id = sel_account_id;

          //start : added to persist data after refresh

          pagesService.getAccountProposal(sel_account_id)
          .then(function(response){
            console.log("proposal",response);
              $scope.account_proposals = response.data.data;
              $window.localStorage.account_proposals = JSON.stringify($scope.account_proposals);
          })
          .catch(function onError(response){
            commonDataShare.showErrorMessage(response);
            // swal(constants.name,constants.errorMsg,constants.error);
              if(typeof(response) == typeof([]))
                  $scope.proposal_error = response.error;
          });
      }


      $scope.addNewProposal = function(sel_account_id){
        if($scope.sel_account_id==null){
              $scope.error = true;
              return;
        }
        else{
          pagesService.setProposalAccountId(sel_account_id);
          $window.localStorage.proposal_id = 0;
          $window.localStorage.isSavedProposal = false;
          $window.localStorage.isReadOnly = 'false';
          $window.localStorage.proposalState = '';
          $location.path('/'+sel_account_id + '/createproposal');
        }
      }

      $scope.showProposalDetails = function(proposal){
        $window.localStorage.parentProposal = true;
        $window.localStorage.proposalState = constants[proposal.campaign_state];
        $window.localStorage.parent_proposal_id = proposal.proposal_id;
        $location.path('/' + proposal.proposal_id + '/showcurrentproposal');
      }

      $scope.showHistory = function(proposalId){
        $window.localStorage.parent_proposal_id = proposalId;
        $location.path('/' + proposalId + '/showproposalhistory');
      }
    	$scope.create = function() {
        console.log($scope.model);
        pagesService.createBusinessCampaign($scope.model)
          .then(function (response) {
            var sub_type_id = $scope.model.business.sub_type_id;
            var type_id = $scope.model.business.business_type_id;
            // response = JSON.parse(response);
            $scope.model.business = response.data.business;
            $scope.model.business.sub_type_id = sub_type_id;
            $scope.model.business.business_type_id = type_id;
            $scope.model.business.contacts = response.data.contacts;
            if (response.status == '201') {
                 $location.path("/manageCampaign/createAccount");
            }
            // $scope.thenMsg = "Successfully Saved"
            swal(constants.name,constants.business_success,constants.success);
            $scope.errorMsg = undefined;
            if (response.status == '200'){
              $scope.choice = "selected";
              pagesService.setBusinessObject($scope.model.business);
              $window.localStorage.business = JSON.stringify($scope.model.business);
            }
        }).catch(function onError(response){
          commonDataShare.showErrorMessage(response);
            // swal(constants.name,constants.business_error,constants.error);
             if (typeof response != 'number'){
               $scope.thenMsg = undefined;
               $scope.errorMsg = response.message;
             // $location.path("");
            }
        })
        };
        //Start: To upload file when upload button is clicked
        $scope.upload = function (file,proposal_id) {
          $scope.uploadfile = false;
          var uploadUrl = constants.base_url + constants.url_base;
          var token = $rootScope.globals.currentUser.token;
          if(file){
            Upload.upload({
                url: uploadUrl + proposal_id + '/import-supplier-data/',
                data: {file: file, 'username': $scope.username},
                headers: {'Authorization': 'JWT ' + token},
            }).then(function (response) {
              console.log(response);
              $scope.uploadfile = true;
              swal(constants.name,constants.uploadfile_success,constants.success);
              // uploadFileToAmazonServer(response.data.data,file);
            }).catch(function onError(response) {
              console.log(response);
              commonDataShare.showErrorMessage(response);
              // swal(constants.name,constants.errorMsg,constants.error);
              $scope.uploadfile = true;
              // commonDataShare.showMessage(constants.importfile_error);
            });
          }
        };
        //End: To upload file when upload button is clicked
        //Start : function to upload files to amazon server, just provide file name and file
          //  var uploadFileToAmazonServer = function(file_name,file){
          //    Upload.upload({
          //        url: constants.aws_bucket_url,
          //        method : 'POST',
          //        data: {
          //            key: file_name, // the key to store the file on S3, could be file name or customized
          //            AWSAccessKeyId : constants.AWSAccessKeyId,
          //            acl : constants.acl, // sets the access to the uploaded file in the bucket: private, public-read, ...
          //            policy : constants.policy,
          //            signature : constants.signature, // base64-encoded signature based on policy string (see article below)
          //            "Content-Type": constants.content_type,// content type of the file (NotEmpty)
          //            file: file }
          //        }).then(function (response){
          //             $scope.uploadfile = true;
          //             if($window.localStorage.sel_account_index >= 0){
          //               $scope.sel_account_id = $scope.model.accounts[$window.localStorage.sel_account_index].account_id;
          //               $scope.getProposals($scope.sel_account_id,$window.localStorage.sel_account_index);
          //             }
          //             swal(constants.name,constants.uploadfile_success,constants.success);
          //             // commonDataShare.showMessage(constants.uploadfile_success);
          //        }).catch(function onError(response) {
          //             $scope.uploadfile = true;
          //             commonDataShare.showErrorMessage(response);
          //             // swal(constants.name,constants.uploadfile_error,constants.error);
          //             // commonDataShare.showMessage(constants.uploadfile_error);
          //        });
          //  }
        //End : function to upload files to amazon server, just provide file name and file
        $scope.getMenu = function(){
          if($scope.menuItem == true)
            $scope.menuItem = false;
          else
            $scope.menuItem = true;
        }
        $scope.closeMenu = function(){
          $scope.menuItem = undefined;
        }

        //to navigate to mapview pages
        // $scope.showOnMapview = function(proposalId){
        //   $window.localStorage.isReadOnly = 'false';
        //   $window.localStorage.isSavedProposal = 'true';
        //   console.log($window.localStorage.isSavedProposal);
        //   $location.path('/' + proposalId + '/mapview');
        // }
        $scope.goToMapView = function(proposal){
          if(proposal.campaign_state){
            console.log("hello");
            $window.localStorage.isReadOnly = 'true';
            $window.localStorage.isSavedProposal = 'true';
            $window.localStorage.proposalState = constants[proposal.campaign_state];
            $location.path('/' + proposal.proposal_id + '/mapview');
          }
          else {
            console.log("fdsfds");
            $window.localStorage.isSavedProposal = 'true';
            $window.localStorage.isReadOnly = 'false';
            $window.localStorage.proposalState = '';
            $location.path('/' + proposal.proposal_id + '/mapview');
          }
        }

        $scope.getStoredData();
      // [TODO] implement this
    });
