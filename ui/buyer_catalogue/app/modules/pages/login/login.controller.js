angular.module('machadaloPages')
.controller('LoginCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'AuthService','$state',
    function ($scope, $rootScope, $window, $location, AuthService, $state) {
        // reset login status

        AuthService.Clear();

        angular.element("title").text("Login");

        $scope.login = function () {

            AuthService.Login($scope.username, $scope.password, function(response) {
                if(response.logged_in) {
                    $location.path("/");
                } else {
                    $scope.error = response.message;
                }
            });
        };
        $scope.guestPage = function(){
          $location.path("/guestHomePage");
        }
    }]);
