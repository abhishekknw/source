angular.module('machadaloPages')
.controller('LoginCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'AuthService','$state','userService','constants','AuthService',
    function ($scope, $rootScope, $window, $location, AuthService, $state,userService,constants, AuthService) {
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
          console.log($scope.mobile_no);
          var userData = {
            first_name : $scope.name,
            email : $scope.email,
            user_code : 10,
            username : $scope.email,
            password : $scope.mobile_no,
          }
          //api call to create user
          userService.createUser(userData)
           .then(function onSuccess(response){
             var username = $scope.email;
             var password = $scope.mobile_no;
             AuthService.Login(username, password, function(response) {
                 if(response.logged_in) {
                     console.log("hello");
                     $location.path("/guestHomePage");              
                 } else {
                     $scope.error = response.message;
                 }
             });

             // alert("Successfully Created");
             })
             .catch(function onError(response){
                 console.log("error occured");
                 swal(constants.name,constants.errorMsg,constants.error);
                 // alert("Error Occured");
             });
        }
    }]);
