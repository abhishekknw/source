angular.module('machadaloPages')
.controller('CreateAccountCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {

      $scope.model = {};
      $scope.model.account = {};
    	$scope.accounts = [];
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

      var contactCopy = angular.copy($scope.contacts);
      $scope.model.account.contacts = [$scope.contacts];

      pagesService.loadBusinessTypes()
      .success(function (response){
          $scope.busTypes = response;
        });

        $scope.getSubTypes = function() {
          var id = $scope.model.business.type;
          pagesService.getSubTypes(id)
          .success(function (response){
              $scope.sub_types = response;
            });
        }

      $scope.addNew = function() {
        $scope.model.account.contacts.push($scope.contacts)
      };

       $scope.remove = function(index) {
        $scope.model.account.contacts.splice(index, 1);
      };

    	$scope.getAllAccounts = function() {
	    	pagesService.getAllAccounts()
	    	.success(function (response, status) {
	    		    console.log(response);
	            $scope.accounts = response;
	       });
	    };

    	$scope.getAccount = function() {
    		pagesService.getAccount($scope.selectAcc)
	    	.success(function (response, status) {
	    		    console.log(response);
	            $scope.account = response.account;
              $scope.business = response.business;
	            $scope.choice = "selected";
	       });
      };

      $scope.readMore = function() {
              $scope.seeMore = "true";
      };

      $scope.editDetails = function() {
              $scope.choice = "select";
      };

      $scope.newAccount = function() {
              $scope.choice = "new";
              $scope.contacts = angular.copy(contactCopy);
              $scope.form.$setPristine();
              $scope.account = {};
              $scope.account.contacts = [$scope.contacts];
      };

    	$scope.create = function() {
        	  console.log($scope.model);
            pagesService.createAccountCampaign($scope.model)
            .success(function (response, status) {
            console.log(response, status);
            console.log(response);
            if (status == '201') {
                 $location.path("/campaign/" + response.id + "/societyList");
            }
            if (status == '200'){
              $scope.choice = "selected";
            }
        }).error(function(response, status){
             $rootScope.errorMsg = response.message ;
             console.log(status);
        })
        };
    }]);
