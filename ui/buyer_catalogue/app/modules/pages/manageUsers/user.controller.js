angular.module('machadaloPages')
.controller('userCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'userService','constants',
    function ($scope, $rootScope, $window, $location, userService, constants) {
        // reset login status
     $scope.model = {};
     $scope.options = [
        {usercode : 'BD', id : '01'},
        {usercode : 'Ops', id: '02'},
        {usercode : 'Agency', id: '03'}
      ];

     $scope.register = function(){
     userService.createUser($scope.model)
      .then(function onSuccess(response){
        console.log("Successful");
        swal(constants.name,constants.createUser,constants.success);
        // alert("Successfully Created");
        })
        .catch(function onError(response){
            console.log("error occured");
            swal(constants.name,constants.errorMsg,constants.error);
            // alert("Error Occured");
        });
     }

    }]);
