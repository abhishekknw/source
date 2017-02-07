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
    opsDashBoard.getCampaignDetails = function(userId){
      var url = url_base + "campaign-assignment/?include_assigned_by=0&to="+userId;
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
    // this endpoint converts proposal to campaign
    opsDashBoard.convertProposalToCampaign = function(proposal_id, data){
      var url = url_base  + proposal_id + "/convert-to-campaign/";
      return machadaloHttp.post(url,data);
    }
    // this endpoint converts a campaign to proposal
    opsDashBoard.convertCampaignToProposal = function(proposal_id, data){
      var url = url_base + proposal_id + "/convert-to-proposal/";
      return machadaloHttp.post(url,data);
    }



    return opsDashBoard;
}]);
