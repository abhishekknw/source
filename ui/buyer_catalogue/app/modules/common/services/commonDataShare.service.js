'use strict';
angular.module('catalogueApp')
.factory('commonDataShare', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

  var commonDataShare = {};
  var url_base = 'v0/ui/website/';

   commonDataShare.showMessage = function(msg){
     alert(msg);
   }

   commonDataShare.getUsersList = function(){
     var url = url_base  + "get-users-list/";
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

   return commonDataShare;
}]);
