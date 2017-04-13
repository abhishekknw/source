'use strict';
angular.module('catalogueApp')
.factory('commonDataShare', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

  var commonDataShare = {};
  var url_base = 'v0/ui/website/';
  var url_base1 = 'v0/ui/'
  var url_base_user = 'v0/'

   commonDataShare.showMessage = function(msg){
     alert(msg);
   }

   commonDataShare.getUsersList = function(){
     var url = url_base_user  + "get-users-list/";
     return machadaloHttp.get(url);
   }

   commonDataShare.formatDate = function(date){
     var d = new Date(date),
         month = '' + (d.getMonth() + 1),
         day = '' + d.getDate(),
         year = d.getFullYear();
     if (month.length < 2) month = '0' + month;
     if (day.length < 2) day = '0' + day;

     return [year, month, day].join('-');
   }

   commonDataShare.getUserDetails = function(userId){
     var url = url_base1 + "user/" + userId + "/";
     return machadaloHttp.get(url);
   }

   return commonDataShare;
}]);
