'use strict';


 angular.module('catalogueApp')
 .factory('createProposalService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base = 'v0/ui/website/';

  	var createProposalService = {};

  	createProposalService.saveInitialProposal = function(data){
  		var url = url_base + 'createInitialProposal/';
  		return machadaloHttp.post(url,data);
  	}

  	return createProposalService;
  }]);