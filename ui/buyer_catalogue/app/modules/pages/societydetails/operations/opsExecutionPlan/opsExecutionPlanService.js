'use strict';
angular.module('catalogueApp')
.factory('opsExecutionPlanService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

   var url_base = 'v0/ui/website/';
   var opsExecutionPlanService = {};

   opsExecutionPlanService.getOpsExecutionImageDetails = function(proposal_id){
        var url = url_base + "campaigns-suppliers-inventory-list/" + "?proposal_id=" + proposal_id +  "&do_not_query_by_date=" + 1;
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.getSuppierDetails = function(supplier_id,supplier_type_code){
     var url = url_base + "supplier-details/" + "?supplier_id=" + supplier_id  + "&supplier_type_code=" + supplier_type_code;
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.getSummaryDetails = function(proposal_id){
        var url = url_base + "generate-inventory-activity-summary/" + "?proposal_id=" + proposal_id;
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.saveReAssignedActivities = function(data){
     var url = url_base + "inventory-activity-date-user-reassignment/";
     return machadaloHttp.post(url,data);
   }

   opsExecutionPlanService.downloadImages = function(proposal_id){
     var url = url_base + "bulk-download-images-amazon/?proposal_id=" + proposal_id;
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.downloadInProgress = function(taskId){
     var url = url_base + "task/is-group-task-successfull/" + taskId + "/";
     return machadaloHttp.get(url);
   }

   opsExecutionPlanService.finishDownload = function(taskId,proposal_id){
     var url = url_base + "proposal-images-path/?task_id=" + taskId + "&proposal_id=" + proposal_id;
     return machadaloHttp.get(url);
   }

   return opsExecutionPlanService;
}]);
