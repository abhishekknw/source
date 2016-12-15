 'use strict';
 angular.module('catalogueApp')
 .factory('opsDashBoardService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
    var opsDashBoard = {};

  	opsDashBoard.getProposalDetails = function(){
      var url = url_base + "proposal/invoice_proposals/";
  		return machadaloHttp.get(url);
  	}
    opsDashBoard.updateProposalDetails = function(proposal_id,data){
      var url = url_base + "proposal/" + proposal_id + "/";
      return machadaloHttp.put(url,data);
    }

    opsDashBoard.sendMail = function(data){
      var url = url_base + "mail/";
      return machadaloHttp.post(url,data);
    }

    return opsDashBoard;
}]);
