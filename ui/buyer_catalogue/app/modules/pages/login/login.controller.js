angular.module('machadaloPages')
.controller('LoginCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'AuthService','$state','userService','constants','AuthService','vcRecaptchaService',
    function ($scope, $rootScope, $window, $location, AuthService, $state,userService,constants, AuthService, vcRecaptchaService) {
        // reset login status

        AuthService.Clear();

        angular.element("title").text("Login");

        $scope.login = function () {
          if(vcRecaptchaService.getResponse() === ""){ //if string is empty
                swal(constants.name,constants.captcha_error,constants.error);
            }
            else {
              $scope.loadingSpinner = true;
                AuthService.Login($scope.username, $scope.password, function(response) {
                    if(response.logged_in) {
                      var path = "/";
                      AuthService.getUserData(function(response){
                        if(!response.data.profile){
                          swal(constants.name, constants.profile_error, constants.error);
                          $location.path("/logout");
                        }else {
                          $location.path(path);
                        }
                      })
                    } else {
                      $scope.loadingSpinner = false;
                        $scope.error = response.message;
                        swal(constants.name,constants.login_error,constants.error);
                    }
                });
            }

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
                 commonDataShare.showErrorMessage(response);
                //  swal(constants.name,constants.errorMsg,constants.error);
                 // alert("Error Occured");
             });
        }
    }]);
