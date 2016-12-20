angular.module('machadaloPages')
.controller('CreateCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {
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
        if($window.sessionStorage.business != null){
          $scope.model.business = JSON.parse($window.sessionStorage.business);
          if($window.sessionStorage.accounts != null){
            $scope.model.accounts = JSON.parse($window.sessionStorage.accounts);
            if($window.sessionStorage.sel_account_index >= 0){
              $scope.sel_account_id = $scope.model.accounts[$window.sessionStorage.sel_account_index].account_id;
            }
          }
          if($window.sessionStorage.account_proposals != null)
            $scope.account_proposals = JSON.parse($window.sessionStorage.account_proposals);
          $scope.choice = "selected";
        }else {
          $scope.model.business = null;
          $scope.model.accounts = null;
          $scope.account_proposals = null;
        }
      }
      $scope.getStoredData();
      // End: for persisting values after refresh or back from other pages

      pagesService.loadBusinessTypes()
      .success(function (response){
          $scope.busTypes = response;
        });
      $scope.getBusiness = function() {
        pagesService.getBusiness($scope.bsSelect)
        .success(function (response, status) {
              $scope.model.business = response.business;
              $scope.model.accounts = response.accounts;
              $rootScope.business_id = response.business.business_id;
              $window.sessionStorage.business_id = response.business.business_id;
              $rootScope.business_name = response.business.name;
              $window.sessionStorage.business_id = response.business.name;
              $scope.model.business.business_type_id = $scope.model.business.type_name.id.toString();
              $scope.getSubTypes();
              $scope.model.business.sub_type_id = $scope.model.business.sub_type.id.toString();
              $scope.choice = "selected";
              // pagesService.setBusinessObject($scope.model.business);
              //Start: added to persit data after refresh
              $window.sessionStorage.business = JSON.stringify($scope.model.business);
              if($scope.model.accounts.length != 0){
                $window.sessionStorage.accounts = JSON.stringify($scope.model.accounts);
              }else{
                $window.sessionStorage.accounts = null;
              }
              $window.sessionStorage.account_proposals = null;
              $scope.account_proposals = null;
              $window.sessionStorage.sel_account_index = -1;
              $scope.sel_account_id = null;
              $scope.error = false;
              //End: added to persit data after refresh
         });
      };

      var business_id_temp = pagesService.getBusinessId();
      if(business_id_temp){
        $scope.bsSelect = business_id_temp;
        $scope.getBusiness();
      };

      $scope.getSubTypes = function() {
            if($scope.model.business.business_type_id == ''){
                $scope.sub_types = {};
                $scope.model.business.sub_type_id = "";
            }else{
                var id = $scope.model.business.business_type_id;
                pagesService.getSubTypes(id)
                .success(function (response){
                    $scope.sub_types = response;
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
        $window.sessionStorage.account_proposals = null;
        $window.sessionStorage.sel_account_index = null;
        $scope.bsSelect = undefined;
	    	pagesService.getAllBusinesses()
	    	.success(function (response, status) {
	            $scope.businesses = response;
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
            $location.path("/manageCampaign/createAccount");
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
              $location.path("/manageCampaign/createAccount");
      };

      $scope.getProposals = function(sel_account_id,index){
          $scope.error = false;
          // pass account_id of selected account radio button
          $scope.sel_account_id = sel_account_id;
          // $rootScope.account_id = sel_account_id;

          //start : added to persist data after refresh
          $window.sessionStorage.sel_account_index = index;
          $window.sessionStorage.account_id = sel_account_id;

          //start : added to persist data after refresh

          pagesService.getAccountProposal(sel_account_id)
          .success(function(response, status){
              $scope.account_proposals = response.data;
              $window.sessionStorage.account_proposals = JSON.stringify($scope.account_proposals);
          })
          .error(function(response, status){
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
          $window.sessionStorage.proposal_id = 0;
          $location.path('/'+sel_account_id + '/createproposal');
        }
      }

      $scope.showProposalDetails = function(proposal_id){
        $window.sessionStorage.parentProposal = true;
        $window.sessionStorage.proposal_id = proposal_id;
        $location.path('/' + proposal_id + '/showcurrentproposal');
      }

      $scope.showHistory = function(proposalId){$window.sessionStorage.proposal_id = proposalId;
        $window.sessionStorage.proposal_id = proposalId;
        $location.path('/' + proposalId + '/showproposalhistory');
      }
    	$scope.create = function() {
            pagesService.createBusinessCampaign($scope.model)
            .success(function (response, status) {
            var sub_type_id = $scope.model.business.sub_type_id;
            var type_id = $scope.model.business.business_type_id;
            // response = JSON.parse(response);
            $scope.model.business = response.business;
            $scope.model.business.sub_type_id = sub_type_id;
            $scope.model.business.business_type_id = type_id;
            $scope.model.business.contacts = response.contacts;
            if (status == '201') {
                 $location.path("/manageCampaign/createAccount");
            }
            $scope.successMsg = "Successfully Saved"
            $scope.errorMsg = undefined;
            if (status == '200'){
              $scope.choice = "selected";
              pagesService.setBusinessObject($scope.model.business);
              $window.sessionStorage.business = JSON.stringify($scope.model.business);
            }
        }).error(function(response, status){
             if (typeof response != 'number'){
               $scope.successMsg = undefined;
               $scope.errorMsg = response.message;
             // $location.path("");
            }
        })
        };
      // [TODO] implement this
    }]);
