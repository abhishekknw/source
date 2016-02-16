angular.module('machadaloPages')
.controller('SocietyCtrl',
    ['$scope', '$rootScope', '$window', '$location','societyDetailsService',
    function ($scope, $rootScope, $window, $location, societyDetailsService) {
     $scope.society = {};
     societyDetailsService.getSociety('MUMPOHNRSOC2')
      .success(function (response) {
        $scope.society = response;
       console.log(response);
     });
    }]);
