'use strict';


 angular.module('catalogueApp')
 .factory('createProposalService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base = 'v0/ui/website/';

  	var createProposalService = {};
  	var proposal_id = undefined;

  	createProposalService.setProposalId = function(id){
  		proposal_id = id;
  	}

  	createProposalService.getProposalId = function(id){
  		return proposal_id;
  	}


  	createProposalService.saveInitialProposal = function(account_id, data){
  		var url = url_base + account_id + '/createInitialProposal/';
  		return machadaloHttp.post(url,data);
  	}

  	return createProposalService;
  }]);