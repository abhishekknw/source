angular.module('machadaloPages')
.controller('SocietyCtrl',
    ['$scope', '$rootScope', '$window', '$location','societyDetailsService',
    function ($scope, $rootScope, $window, $location, societyDetailsService) {
	    getSociety();
      function getSociety(id) {
       societyDetailsService.getSocietyData()
         .success(function (response) {
           $scope.society = response;
           console.log($scope.society)

         });
     }
    }]);
