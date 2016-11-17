'use strict';


 angular.module('catalogueApp')
 .factory('createProposalService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base = 'v0/ui/website/';
    var url_base1 = 'v0/ui/';

  	var createProposalService = {};
  	var proposal_id = undefined;

  	createProposalService.loadInitialData = function () {
       var url = url_base1 + "create_supplier/load_initial_data/";
       return machadaloHttp.get(url);
    }

    createProposalService.getLocations = function (type, id) {
       var url = url_base1 + "locations/" + id + "/?type=" + type;
       return machadaloHttp.get(url);
   }

    createProposalService.setProposalId = function(id){
  		proposal_id = id;
  	}

  	createProposalService.getProposalId = function(id){
  		return proposal_id;
  	}


  	createProposalService.saveInitialProposal = function(account_id, data){
  		var url = url_base + account_id + '/create-initial-proposal/';
  		return machadaloHttp.post(url,data);
  	}

  	return createProposalService;
  }]);
