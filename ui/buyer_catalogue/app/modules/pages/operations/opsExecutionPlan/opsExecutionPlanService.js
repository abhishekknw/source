'use strict';
angular.module('catalogueApp')
.factory('opsExecutionPlanService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

   var url_base = 'v0/ui/website/';
   var opsExecutionPlanService = {};


  
   return opsExecutionPlanService;
}]);
