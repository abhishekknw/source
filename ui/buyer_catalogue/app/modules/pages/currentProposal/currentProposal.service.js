'use strict';


 angular.module('catalogueApp')
 .factory('currentProposalService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';

    var currentProposalService = {};

    currentProposalService.getProposal = function(){
    	// will receive proposal_id
    	var url = url_base + 'currentProposal/' ;
    	return machadaloHttp.get(url);
    }

    currentProposalService.saveProposal = function(data){
    	// will receive proposal_id
    	var url = url_base + 'currentProposal/' ;
    	return machadaloHttp.post(url, data);
    }

    return currentProposalService;

 }]);