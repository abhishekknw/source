angular.module('machadaloPages')
.factory('userService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/';
    var userService = {};

    userService.createUser = function(data){
      var url = url_base + "user/";
      return machadaloHttp.post(url,data);
    }
 
   
  return userService;
}]);

