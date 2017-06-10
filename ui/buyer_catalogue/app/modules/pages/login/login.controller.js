angular.module('machadaloPages')
.controller('LoginCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'AuthService','$state','userService','constants','AuthService',
    function ($scope, $rootScope, $window, $location, AuthService, $state,userService,constants, AuthService) {
        // reset login status

        AuthService.Clear();

        angular.element("title").text("Login");

        $scope.login = function () {
          $scope.loadingSpinner = true;
            AuthService.Login($scope.username, $scope.password, function(response) {
                if(response.logged_in) {
                  var path = "/";
                  AuthService.getUserData(function(response){
                    angular.forEach(response.data.groups, function(group){
                      if(group.name == constants.campaign_manager){
                          path = "/CampaignList";
                      }
                    })
                    $scope.loadingSpinner = false;
                    $location.path(path);
                  })

                } else {
                  $scope.loadingSpinner = false;
                    $scope.error = response.message;
                }
            });
        };
        $scope.guestPage = function(){
          var userData = {
            first_name : $scope.name,
            email : $scope.email,
            user_code : 99,
            username : $scope.email,
            mobile:$scope.mobile_no,
          }
          //api call to create user
          userService.createGuestUser(userData)
           .then(function onSuccess(response){
             console.log(response);
             var username = response.data.data.username;
             var password = response.data.data.password;
             AuthService.Login(username, password, function(response) {
                 if(response.logged_in) {
                     console.log("hello");
                     $('#guestModal').modal('hide');
                      $('body').removeClass('modal-open');
                      $('.modal-backdrop').remove();
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
