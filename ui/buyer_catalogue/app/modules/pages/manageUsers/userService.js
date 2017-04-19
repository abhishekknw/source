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

    userService.getAllUsers = function(){
      var url = url_base_user + "user/";
      return machadaloHttp.get(url);
    }

    userService.updateUserDetails = function(id,data){
      console.log(data);
      var url = url_base_user + "user/" + id + "/";
      return machadaloHttp.put(url,data);
    }

    userService.deleteUser = function(id){
      var url = url_base_user + "user/" + id + "/";
      return  machadaloHttp.delete(url);
    }

    userService.updateGroupDetails = function(id,data){
      var url = url_base_user + "group/" + id + "/";
      return machadaloHttp.put(url,data)
    }

    userService.deleteGroup = function(id){
      var url = url_base_user + "group/" + id + "/";
      return machadaloHttp.delete(url);
    }

  return userService;
}]);
