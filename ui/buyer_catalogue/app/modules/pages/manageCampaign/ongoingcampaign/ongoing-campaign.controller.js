angular.module('machadaloPages')
.controller('OngoingCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {

        $scope.model = {};

        $scope.viewDetails = function() {
                $scope.show = "details";
        };
  }]);
