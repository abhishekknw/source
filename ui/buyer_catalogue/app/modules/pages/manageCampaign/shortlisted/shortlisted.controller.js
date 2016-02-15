angular.module('machadaloPages')
.controller('ShortlistedCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {

    	$scope.businesses = [];

    	pagesService.getShortlistedCampaigns()
    	.success(function (response, status) {
    		console.log(response);
            $scope.model = response;
            
       });

    	$scope.getBusiness = function() {
    		pagesService.getBusiness($scope.bsSelect)
	    	.success(function (response, status) {
	    		    console.log(response);
	            $scope.business = response;
	            $scope.contact = response.business_contact[0]
	            $scope.choice_new = "selected";
	       });

    	};

    	$scope.create = function() {
        $location.path("/society/inventory");    	}
      //[TODO] implement this
    }]);
