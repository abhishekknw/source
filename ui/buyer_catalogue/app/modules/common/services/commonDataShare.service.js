'use strict';
angular.module('catalogueApp')
.factory('commonDataShare', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

  var commonDataShare = {};

   commonDataShare.showMessage = function(msg){
     alert(msg);
   }

   return commonDataShare;
}]);
