angular.module('machadaloPages')


.controller('ShortlistedSocietiesCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {
        pagesService.processParam();

    	$scope.model = {};

    	pagesService.getSocietyInventory($rootScope.campaignId)
            .success(function (response, status) {
                console.log(response);
                $scope.model = response;
            
         })

}]);
