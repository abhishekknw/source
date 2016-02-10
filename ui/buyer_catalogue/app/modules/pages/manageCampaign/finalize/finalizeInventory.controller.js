angular.module('machadaloPages')
.controller('FinalizeInventoryCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {
        pagesService.processParam();

       
    	$scope.create = function() {
    		console.log($scope.campaign_type);
        $location.path("/manageCampaign/create");    	}
      //[TODO] implement this
    }]);
