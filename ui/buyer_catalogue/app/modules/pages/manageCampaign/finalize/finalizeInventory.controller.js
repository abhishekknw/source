angular.module('machadaloPages')
.controller('FinalizeInventoryCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {
        pagesService.processParam();

        $scope.model = {};
        if($rootScope.campaignId){
           pagesService.getRequestedInventory($rootScope.campaignId)
            .success(function (response, status) {
                console.log(response);
                $scope.model = response;
            });
        }
            
       
    	$scope.create = function() {
    		console.log($scope.campaign_type);
            $location.path("/manageCampaign/create");  
        }
      //[TODO] implement this
    }]);
