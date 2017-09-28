angular.module('machadaloPages')
.factory('userService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base_user = 'v0/';
    var url_base = 'v0/ui/';
    var url_base_website = 'v0/ui/website/';
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
      return machadaloHttp.put(url,data);
    }

    userService.deleteGroup = function(id){
      var url = url_base_user + "group/" + id + "/";
      return machadaloHttp.delete(url);
    }
    userService.changePassword = function(id,data){
      var url = url_base_user + "user/" + id + "/change_password/";
      return machadaloHttp.post(url,data);
    }

    userService.createProfile = function(data){
      var url = url_base_website + "profile/";
      return machadaloHttp.post(url,data);
    }

    userService.createOrganisation = function(data){
      var url = url_base_website + "organisation/";
      return machadaloHttp.post(url,data);
    }

    userService.getOrganisations = function(){
      var url = url_base_website + "organisation/";
      return machadaloHttp.get(url);
    }

    userService.updateOrganisationDetails = function(data){
      var url = url_base_website + "organisation/" + data.organisation_id + "/";
      return machadaloHttp.put(url,data);
    }

    userService.getProfiles = function(id){
      if(id)
        var url = url_base_website + "profile/?organisation_id=" + id;
      else
        var url = url_base_website + "profile/";
      return machadaloHttp.get(url);
    }

    userService.updateProfile = function(data){
      var url = url_base_website + "profile/" + data.id + "/";
      return machadaloHttp.put(url,data);
    }

    userService.getObjectLevelPermissions = function(){
      var url = url_base_website + "object-level-permission/";
      return machadaloHttp.get(url);
    }

    userService.createObjectLevelPermission = function(data){
      var url = url_base_website + "object-level-permission/";
      return machadaloHttp.post(url,data);
    }

    userService.updateObjectLevelPermission = function(data){
      var url = url_base_website + "object-level-permission/";
      return machadaloHttp.put(url,data);
    }

    userService.getContentTypes = function(){
      var url = url_base_website + "content-type/";
      return machadaloHttp.get(url);
    }

    userService.getGeneralUserLevelPermissions = function(){
      var url = url_base_website + "general-user-permission/";
      return machadaloHttp.get(url);
    }

    userService.createGeneralUserLevelPermission = function(data){
      var url = url_base_website + "general-user-permission/";
      return machadaloHttp.post(url,data);
    }

    userService.updateObjectLevelPermission = function(data){
      var url = url_base_website + "object-level-permission/" + data.id + "/";
      return machadaloHttp.put(url,data);
    }

    userService.updateGeneralUserPermission = function(data){
      var url = url_base_website + "general-user-permission/" + data.id + "/";
      return machadaloHttp.put(url,data);
    }

    userService.getStandardProfileToClone = function(){
      var url = url_base_website + "profile/standard_profiles/";
      return machadaloHttp.get(url);
    }

  return userService;
}]);
