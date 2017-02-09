'use strict';
angular.module('catalogueApp')
.factory('opsExecutionPlanService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

   var url_base = 'v0/ui/website/';
   var opsExecutionPlanService = {};

   opsExecutionPlanService.getOpsExecutionImageDetails = function(proposal_id){
        var url = url_base + "inventory-activity-image/" + "?proposal_id=" + proposal_id;
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.getSuppierDetails = function(supplier_id,content_type){
     var url = url_base + "supplier-details/" + "?supplier_id=" + supplier_id  + "&content_type=" + content_type;
     return machadaloHttp.get(url);
   }


   return opsExecutionPlanService;
}]);
