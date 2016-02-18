angular.module('machadaloPages')
.controller('FinalizeCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {


    	$scope.viewInventory = function(id) {
            $location.path("/manageCampaign/finalize/" + id + "/finalizeInventory/"); 
	    	
	    };

    	
		pagesService.getCampaigns('Requested')
    	.success(function (response, status) {
    		console.log(response);
            $scope.model = response;
            
       });

    	
    

    	$scope.create = function() {
    		console.log($scope.campaign_type);
        $location.path("/manageCampaign/create");    	}
      //[TODO] implement this
    }]);
