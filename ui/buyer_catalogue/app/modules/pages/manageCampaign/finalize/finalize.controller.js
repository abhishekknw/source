angular.module('machadaloPages')
.controller('FinalizeCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {

       
        $scope.model = [{"name":"POwai Poster campaign"}]
    	

    	$scope.viewInventory = function(id) {
            $location.path("/manageCampaign/finalize/" + id + "/finalizeInventory/"); 
	    	
	    };

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
    		console.log($scope.campaign_type);
        $location.path("/manageCampaign/create");    	}
      //[TODO] implement this
    }]);
