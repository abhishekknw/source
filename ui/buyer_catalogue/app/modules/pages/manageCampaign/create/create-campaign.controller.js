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


      $scope.setDate = function(year, month, day) {
        $scope.dt = new Date(year, month, day);
      };

      $scope.sel_account_id = null;
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

      pagesService.loadBusinessTypes()
      .success(function (response){
          $scope.busTypes = response;
          console.log("BusTypes : ");
          console.log($scope.busTypes);
        });


      $scope.getBusiness = function() {
        pagesService.getBusiness($scope.bsSelect)
        .success(function (response, status) {
              console.log("model.business :  ")
              console.log(response);
              $scope.model.business = response.business;
              $scope.model.accounts = response.accounts;
              $scope.model.business.business_type_id = $scope.model.business.type_name.id.toString();
              $scope.getSubTypes();
              $scope.model.business.sub_type_id = $scope.model.business.sub_type.id.toString();
              $scope.choice = "selected";
              pagesService.setBusinessObject($scope.model.business);
         });
      };

      var business_id_temp = pagesService.getBusinessId();
      if(business_id_temp){
        console.log("business_id_temp received", business_id_temp);
        $scope.bsSelect = business_id_temp;
        $scope.getBusiness();
      };
      

        $scope.getSubTypes = function() {
          // debugger;
            console.log($scope.model.business.business_type_id);
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
            console.log($scope.model.business.contacts);
        };

      
      $scope.remove = function(index) {
        $scope.model.business.contacts.splice(index, 1);
        console.log($scope.model.business.contacts);
      };

    	$scope.getAllBusinesses = function() {
        $scope.bsSelect = undefined;
	    	pagesService.getAllBusinesses()
	    	.success(function (response, status) {
	    		    console.log(response);
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
              $scope.choice = "new";
              $scope.bsSelect = undefined;
              $scope.contact = angular.copy(contactCopy);
              $scope.form.$setPristine();
              $scope.model.business = {};
              $scope.model.business.contacts = [$scope.contact];
      };

      $scope.addNewAccount = function() {
              pagesService.setAccountId(undefined);
              $location.path("/manageCampaign/createAccount");
      };

      $scope.getProposals = function(sel_account_id){
          // pass account_id of selected account radio button
          console.log("Get Proosals\t account_id received  : ", sel_account_id);
          $scope.sel_account_id = sel_account_id;
          pagesService.getAccountProposal(sel_account_id)
          .success(function(response, status){
              $scope.account_proposals = response;
              alert($scope.account_proposals);
          })
          .error(function(response, status){
              if(typeof(response) == typeof([]))
                  $scope.proposal_error = response.error;
          });
      }


      $scope.addNewProposal = function(sel_account_id){
        console.log("hi");
        console.log("$scope.sel_account_id : ", $scope.sel_account_id);
        pagesService.setProposalAccountId(sel_account_id);
        $location.path('/'+sel_account_id + '/createproposal');
      }

    	$scope.create = function() {
        	  console.log($scope.model);
            pagesService.createBusinessCampaign($scope.model)
            .success(function (response, status) {
    
            console.log("\n\nresponse is : ");
            console.log(response);
            var sub_type_id = $scope.model.business.sub_type_id;
            var type_id = $scope.model.business.business_type_id;

            console.log(sub_type_id, type_id);
            console.log('response is : ',response);
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
            }
        }).error(function(response, status){
             console.log("response is : ", response);
             console.log("status is  : " ,status);
             if (typeof response != 'number'){
               $scope.successMsg = undefined;
               $scope.errorMsg = response.message;
               console.log($scope.errorMsg);
             // $location.path("");
            }

        })
        };
      //[TODO] implement this
    }]);
