angular.module('machadaloPages')
.factory('userService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base_user = 'v0/';
    var url_base = 'v0/ui/';
    var userService = {};

    userService.createUser = function(data){
      var url = url_base_user + "user/";
      return machadaloHttp.post(url,data);
    }

    userService.createGuestUser = function(data){
      var url = url_base + "guest-user/";
      return machadaloHttp.post(url,data);
    }

    userService.getAllUserPermissions = function(){
      var url = url_base_user + "permission/";
      return machadaloHttp.get(url);
    }

    userService.getAllUserGroups = function(){
      var url = url_base_user + "group/";
      return machadaloHttp.get(url);
    }

    userService.createGroup = function(data){
      var url = url_base_user + "group/";
      return machadaloHttp.post(url,data);
    }


  return userService;
}]);
