angular.module('machadaloPages')
.controller('CreateCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {

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


      $scope.model.business.contacts = [$scope.contact];

      $scope.addNew = function() {
        $scope.model.business.contacts.push($scope.contact)
      };

       $scope.remove = function(index) {
        $scope.model.business.contacts.splice(index, 1);
      };

    	$scope.getAllBusinesses = function() {
	    	pagesService.getAllBusinesses()
	    	.success(function (response, status) {
	    		    console.log(response);
	            $scope.businesses = response;
	       });
	    };

    	$scope.getBusiness = function() {
    		pagesService.getBusiness($scope.bsSelect)
	    	.success(function (response, status) {
	    		    console.log(response);
	            $scope.model.business = response;
	            $scope.choice = "selected";
	       });
      };

      $scope.readMore = function() {
              $scope.seeMore = "true";
      };

      $scope.readLess = function() {
              $scope.seeMore = "false";
      };

    	$scope.create = function() {
        	  console.log($scope.model);
            pagesService.createBusinessCampaign($scope.model)
            .success(function (response, status) {
            console.log(response, status);
            console.log(response);
            if (status == '201') {
                 $location.path("/campaign/" + response.id + "/societyList");
            }
        }).error(function(response, status){
             $rootScope.errorMsg = response.message ;
             console.log(status);
        })
        };
      //[TODO] implement this
    }]);
