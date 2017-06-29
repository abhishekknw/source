'use strict';
angular.module('catalogueApp')
.factory('commonDataShare', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http','constants',
 function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http, constants) {

  var commonDataShare = {};
  var url_base = 'v0/ui/website/';
  var url_base1 = 'v0/ui/'
  var url_base_user = 'v0/'
  var defaultError = "No data key in response of this API. Cannot render the exact error. For your reference here is the response: ";


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

   commonDataShare.getUserDetails = function(userId){
     var url = url_base_user + "user/" + userId + "/";
     return machadaloHttp.get(url);
   }

   commonDataShare.showErrorMessage = function(response){

     console.log(response.data);

     if(constants.show_system && constants.show_general) {
          if ( response.data.data ) {
            swal(constants.name, response.data.data.system_error+ " " + response.data.data.general_error, constants.error);
          }
          else {
            swal(constants.name, defaultError + JSON.stringify(response.data, null, 4) , constants.error);

          }

        }
     else if(constants.show_general) {

          if ( response.data.data  ) {
            swal(constants.name,response.data.data.general_error, constants.error);
          }
          else  {
            swal(constants.name, defaultError + JSON.stringify(response.data, null, 4), constants.error);
          }

        }
     else if(constants.show_system) {

          if (response.data.data  ) {
            swal(constants.name, response.data.data.system_error, constants.error);
          }
          else {
             swal(constants.name, defaultError + JSON.stringify(response.data, null, 4), constants.error);
          }

        }

     else
        swal(constants.name, constants.errorMsg, constants.error);
   }

   return commonDataShare;
}]);
