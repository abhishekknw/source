angular.module('machadaloPages')
.controller('CreateCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {

        $scope.model = {};
    	$scope.businesses = [];
    	$scope.campaign_types = ['Poster', 'Standee', 'Stall', 'CarDisplay', 'Fliers']
    	$scope.campaign_sub_types = {
    		'Poster': ['A4', 'A3'],
    		'Standee': ['Small', 'Medium', 'Large'],
    		'Stall':['Small', 'Medium', 'Large','Canopy'],
    		'CarDisplay':['Normal', 'Premium']
    	}
    	$scope.campaign_type = {}

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
	            $scope.choice_new = "selected";
	       });

    	};
    

    	$scope.create = function() {
        	console.log($scope.model);
            pagesService.createBusinessCampaign($scope.model)
            .success(function (response, status) {
            console.log(response, status);
            if (status == '201') {
                 $location.path("/manageCampaign/finalize");  
            }
        }).error(function(response, status){
            
             $rootScope.errorMsg = response.message ;
             console.log(status);           
        })
        }
      //[TODO] implement this
    }]);
