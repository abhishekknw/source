'use strict';


 angular.module('catalogueApp')
 .factory('currentProposalService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';

    var currentProposalService = {};

    currentProposalService.getProposal = function(proposal_id){
    	// will receive proposal_id
        var url = url_base + "proposal/"+ proposal_id + "/";
      	// var url = url_base + proposal_id;
    	return machadaloHttp.get(url);
    }

    currentProposalService.saveProposal = function(proposal_id, data){
    	// will receive proposal_id
    	var url = url_base + proposal_id + '/currentProposal/' ;
    	return machadaloHttp.post(url, data);
    }

    return currentProposalService;

 }]);
